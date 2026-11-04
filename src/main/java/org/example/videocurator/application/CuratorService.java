package org.example.videocurator.application;

import static org.example.videocurator.domain.Models.*;

import java.time.*;
import java.util.*;
import org.example.videocurator.domain.*;
import org.example.videocurator.persistence.DraftStore;
import org.example.videocurator.provider.*;
import org.example.videocurator.quota.CostCatalog;
import org.example.videocurator.quota.QuotaService;

public final class CuratorService {
  private final YouTubeProvider provider;
  private final QuotaService quota;
  private final DraftStore drafts;
  private final Clock clock;

  public CuratorService(
      YouTubeProvider provider, QuotaService quota, DraftStore drafts, Clock clock) {
    this.provider = provider;
    this.quota = quota;
    this.drafts = drafts;
    this.clock = clock;
  }

  public Map<String, Object> overview(String input) {
    String id = Input.video(input);
    try (var r = quota.reserve(CostCatalog.read(), 0)) {
      Video v = provider.video(id, r);
      return Map.of(
          "video",
          v,
          "url",
          v.url(),
          "source",
          "video_metadata",
          "overview",
          v.title() + " — " + v.description(),
          "warnings",
          List.of("Metadata-derived overview; no transcript downloaded or video watched."));
    }
  }

  public Object similar(String input, int limit) {
    String id = Input.video(input);
    Input.limit(limit);
    try (var r = quota.reserve(2 * CostCatalog.read(), CostCatalog.search())) {
      Video seed = provider.video(id, r);
      var candidates = provider.searchVideos(seed.title(), r);
      return Map.of(
          "rankingVersion",
          "tfidf-v1",
          "candidates",
          Ranking.videos(seed, candidates, limit),
          "warnings",
          List.of("Metadata similarity is computed locally; not YouTube's internal ranking."));
    }
  }

  public Object channels(String input, int limit) {
    String selector = Input.channel(input);
    Input.limit(limit);
    try (var r = quota.reserve(2 * CostCatalog.read(), CostCatalog.search())) {
      Channel seed = provider.channel(selector, r);
      var candidates =
          provider.searchChannels(seed.title(), r).stream()
              .filter(c -> !c.id().equals(seed.id()))
              .distinct()
              .toList();
      var texts = new ArrayList<String>();
      texts.add(seed.text());
      candidates.forEach(c -> texts.add(c.text()));
      var vectors = Ranking.vectors(texts);
      var scores = new ArrayList<Map<String, Object>>();
      for (int i = 0; i < candidates.size(); i++)
        scores.add(
            Map.of(
                "channel",
                candidates.get(i),
                "score",
                Ranking.cosine(vectors.getFirst(), vectors.get(i + 1)),
                "reason",
                "title/description TF-IDF cosine"));
      scores.sort(
          Comparator.<Map<String, Object>>comparingDouble(
                  m -> ((Number) m.get("score")).doubleValue())
              .reversed()
              .thenComparing(m -> ((Channel) m.get("channel")).id()));
      return Map.of("channels", scores.stream().limit(limit).toList());
    }
  }

  public Object recommend(int limit) {
    Input.limit(limit);
    try (var r = quota.reserve(22 * CostCatalog.read(), CostCatalog.search())) {
      PersonalData p = provider.personal(r);
      var sourceText =
          List.of(
              p.likes().stream().map(Video::text).reduce("", (a, b) -> a + " " + b),
              p.subscriptions().stream().map(Channel::text).reduce("", (a, b) -> a + " " + b),
              p.playlistVideos().stream().map(Video::text).reduce("", (a, b) -> a + " " + b));
      var profile = new TreeMap<String, Double>();
      double[] weights = {.45, .30, .25};
      for (int i = 0; i < 3; i++) {
        double w = weights[i];
        Ranking.terms(sourceText.get(i)).forEach((k, v) -> profile.merge(k, w * v, Double::sum));
      }
      if (profile.isEmpty())
        throw new CuratorException(
            "INSUFFICIENT_PROFILE",
            "No usable authorized signals; request an explicit topic instead.");
      String query =
          profile.entrySet().stream()
              .sorted(
                  Map.Entry.<String, Double>comparingByValue()
                      .reversed()
                      .thenComparing(Map.Entry.comparingByKey()))
              .limit(6)
              .map(Map.Entry::getKey)
              .reduce((a, b) -> a + " " + b)
              .orElseThrow();
      var known = new HashSet<String>();
      p.likes().forEach(v -> known.add(v.id()));
      p.playlistVideos().forEach(v -> known.add(v.id()));
      var result =
          provider.searchVideos(query, r).stream()
              .filter(v -> !known.contains(v.id()))
              .map(
                  v ->
                      new RankedVideo(
                          v,
                          Ranking.cosine(profile, Ranking.terms(v.text())),
                          Map.of(
                              "weightedProfileCosine",
                              Ranking.cosine(profile, Ranking.terms(v.text())))))
              .sorted(
                  Comparator.comparingDouble(RankedVideo::score)
                      .reversed()
                      .thenComparing(v -> v.video().id()))
              .limit(limit)
              .toList();
      return Map.of(
          "recommendations",
          result,
          "coverage",
          p.coverage(),
          "sources",
          List.of("likes", "subscriptions", "playlists"),
          "warnings",
          List.of(
              "Sampled metadata interests; no watch history. Empty source weights contribute no evidence."));
    }
  }

  public Object analyze(String a, String b, String c, String d) {
    long supplied =
        java.util.stream.Stream.of(a, b, c, d).filter(v -> v != null && !v.isBlank()).count();
    Input.require(
        supplied == 0 || supplied == 4, "Supply all four period dates, or omit all four.");
    if (a != null && !a.isBlank()) {
      Input.require(
          Analytics.day(a).isBefore(Analytics.day(b))
              && Analytics.day(c).isBefore(Analytics.day(d)),
          "Invalid period order.");
    }
    try (var r = quota.reserve(21 * CostCatalog.read(), 0)) {
      return Analytics.analyze(provider.personal(r), a, b, c, d);
    }
  }

  public DraftStore.Draft plan(Constraints c, String request) {
    try (var r = quota.reserve(CostCatalog.read(), CostCatalog.search())) {
      var candidates = provider.searchVideos(c.topic(), r);
      var selection =
          PlaylistSelector.select(
              Ranking.topic(c.topic(), candidates).stream().filter(v -> v.score() > 0).toList(), c);
      return drafts.save(
          new Proposal(
              2,
              provider.account(),
              c.topic(),
              "private",
              c,
              selection.videos(),
              selection.totalSeconds(),
              selection.shortfallSeconds(),
              clock.instant().plusSeconds(1800),
              "greedy-local-swap-v1; strict declared audio-language metadata; total is upper bound",
              request,
              selection.exclusions()));
    }
  }

  public DraftStore.Draft draft(String id) {
    return drafts.get(uuid(id), provider.account());
  }

  public Object commit(String input) {
    UUID id = uuid(input);
    String account = provider.account();
    var before = drafts.get(id, account);
    if (before.state().equals("CREATED")) return commitResult(before);
    // Reserve before claiming approval: quota failure leaves the human grant usable.
    try (var r =
        quota.reserve(
            CostCatalog.write() * (before.proposal().videos().size() + 1) + 2 * CostCatalog.read(),
            0)) {
      if (!before.state().equals("APPROVED"))
        throw new CuratorException(
            before.state().equals("PROPOSED") ? "APPROVAL_REQUIRED" : "WRITE_REVIEW_REQUIRED",
            "Approve the exact draft locally; ambiguous prior writes require manual review.");
      if (provider instanceof OfficialYouTubeProvider official) official.verifyAccount(r);
      if (!drafts.claim(id, account)) return commitResult(drafts.get(id, account));
      String playlist = null;
      boolean attempted = false;
      try {
        drafts.journal(id, "000-create", "ATTEMPTED", null, null);
        attempted = true;
        playlist =
            provider.insertPlaylist(before.proposal().title(), before.proposal().privacy(), r);
        drafts.journal(id, "000-create", "CONFIRMED", playlist, null);
        drafts.state(id, "CREATING", playlist, null);
        int position = 0;
        for (Video video : before.proposal().videos()) {
          String step = String.format(Locale.ROOT, "%03d-item", position + 1);
          drafts.journal(id, step, "ATTEMPTED", null, null);
          String item = provider.insertItem(playlist, video.id(), position++, r);
          drafts.journal(id, step, "CONFIRMED", item, null);
        }
        var actual = provider.playlistVideoIds(playlist, r);
        var expected = before.proposal().videos().stream().map(Video::id).toList();
        if (!actual.equals(expected))
          throw new CuratorException(
              "READBACK_MISMATCH",
              "Playlist readback does not match approved order; manual review required.");
        drafts.state(id, "CREATED", playlist, null);
      } catch (Exception e) {
        String code = e instanceof CuratorException ce ? ce.code() : "LOCAL_PERSISTENCE_FAILURE";
        String state =
            !attempted
                ? "FAILED_BEFORE_WRITE"
                : playlist == null ? "NEEDS_MANUAL_REVIEW" : "PARTIAL";
        drafts.state(id, state, playlist, code);
        drafts.journal(id, "999-failure", state, null, code);
      }
      return commitResult(drafts.get(id, account));
    }
  }

  private Map<String, Object> commitResult(DraftStore.Draft d) {
    var result = new LinkedHashMap<String, Object>();
    result.put("state", d.state());
    result.put("draftId", d.id());
    result.put("journal", d.journal());
    result.put("fixture", provider.fixture());
    result.put("playlistId", Objects.toString(d.remoteId(), ""));
    result.put(
        "playlistUrl",
        provider.fixture() || d.remoteId() == null
            ? ""
            : "https://www.youtube.com/playlist?list=" + d.remoteId());
    result.put("proposedTotalSeconds", d.proposal().totalSeconds());
    result.put("proposedItemCount", d.proposal().videos().size());
    var items = new ArrayList<Map<String, Object>>();
    long confirmedSeconds = 0;
    int confirmed = 0;
    for (int i = 0; i < d.proposal().videos().size(); i++) {
      var video = d.proposal().videos().get(i);
      String step = String.format(Locale.ROOT, "%03d-item", i + 1);
      String status =
          d.journal().stream()
              .filter(j -> step.equals(j.get("step")))
              .map(j -> Objects.toString(j.get("status")))
              .findFirst()
              .orElse("NOT_ATTEMPTED");
      if (status.equals("CONFIRMED")) {
        confirmed++;
        confirmedSeconds += video.seconds();
      }
      items.add(Map.of("videoId", video.id(), "url", video.url(), "position", i, "status", status));
    }
    result.put("confirmedItemCount", confirmed);
    result.put("confirmedTotalSeconds", confirmedSeconds);
    result.put("items", items);
    result.put(
        "warning",
        provider.fixture()
            ? "Synthetic fixture result; no YouTube playlist was created."
            : "Inspect state and journal before claiming success. Partial/ambiguous attempts are never automatically replayed.");
    return result;
  }

  /** CLI only. Reconcile an existing private playlist before appending any missing suffix. */
  public Object repair(String input, String phrase) {
    UUID id = uuid(input);
    String account = provider.account();
    var d = drafts.get(id, account);
    try (var r =
        quota.reserve(
            CostCatalog.write() * d.proposal().videos().size() + 3 * CostCatalog.read(), 0)) {
      if (provider instanceof OfficialYouTubeProvider official) official.verifyAccount(r);
      drafts.claimRepair(id, account, phrase);
      try {
        var expected = d.proposal().videos().stream().map(Video::id).toList();
        var actual = provider.playlistVideoIds(d.remoteId(), r);
        if (actual.size() > expected.size() || !expected.subList(0, actual.size()).equals(actual))
          throw new CuratorException(
              "READBACK_MISMATCH",
              "Remote playlist is not an exact prefix; no repair writes attempted.");
        for (int i = 0; i < actual.size(); i++)
          drafts.journal(
              id, String.format(Locale.ROOT, "%03d-item", i + 1), "CONFIRMED", null, null);
        for (int i = actual.size(); i < expected.size(); i++) {
          String step = String.format(Locale.ROOT, "%03d-item", i + 1);
          drafts.journal(id, step, "ATTEMPTED", null, null);
          String item = provider.insertItem(d.remoteId(), expected.get(i), i, r);
          drafts.journal(id, step, "CONFIRMED", item, null);
        }
        if (!provider.playlistVideoIds(d.remoteId(), r).equals(expected))
          throw new CuratorException(
              "READBACK_MISMATCH", "Repair readback differs; inspect remote account.");
        drafts.state(id, "CREATED", d.remoteId(), null);
      } catch (Exception e) {
        String code = e instanceof CuratorException ce ? ce.code() : "LOCAL_PERSISTENCE_FAILURE";
        drafts.state(id, "PARTIAL", d.remoteId(), code);
        drafts.journal(id, "999-failure", "PARTIAL", null, code);
      }
      return commitResult(drafts.get(id, account));
    }
  }

  public Object quota() {
    return Map.of(
        "buckets",
        quota.status(),
        "date",
        QuotaService.quotaDate(clock),
        "timezone",
        "America/Los_Angeles");
  }

  public boolean fixture() {
    return provider.fixture();
  }

  public static UUID uuid(String id) {
    try {
      return UUID.fromString(id);
    } catch (Exception e) {
      throw new CuratorException("INVALID_INPUT", "draftId must be a UUID.");
    }
  }
}
