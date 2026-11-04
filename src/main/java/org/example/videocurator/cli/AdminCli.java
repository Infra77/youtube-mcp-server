package org.example.videocurator.cli;

import java.nio.file.Path;
import org.example.videocurator.application.CuratorService;
import org.example.videocurator.domain.CuratorException;
import org.example.videocurator.oauth.WindowsTokenVault;
import org.example.videocurator.persistence.DraftStore;
import org.example.videocurator.provider.YouTubeProvider;
import org.example.videocurator.quota.CostCatalog;
import org.example.videocurator.quota.QuotaService;
import org.springframework.context.ConfigurableApplicationContext;

public final class AdminCli {
  private AdminCli() {}

  public static int run(ConfigurableApplicationContext ctx, String[] args) {
    try {
      var vault = ctx.getBean(WindowsTokenVault.class);
      var store = ctx.getBean(DraftStore.class);
      var quota = ctx.getBean(QuotaService.class);
      if (args.length == 2 && args[0].equals("auth") && args[1].equals("status")) {
        System.out.println(vault.status());
        return 0;
      }
      if (args.length == 2 && args[0].equals("auth") && args[1].equals("login")) {
        requireConsole();
        String path = System.getenv("GOOGLE_CLIENT_FILE");
        if (path == null)
          throw new CuratorException(
              "OAUTH_CONFIG_REQUIRED",
              "Set GOOGLE_CLIENT_FILE to the local Desktop client JSON, outside the project.");
        try (var budget = quota.reserve(CostCatalog.read(), 0)) {
          vault.login(Path.of(path));
          String account = vault.verifyAndSave(budget);
          System.out.println(
              "Authorized YouTube channel: " + account + ". Credential stored with Windows DPAPI.");
        }
        return 0;
      }
      if (args.length == 2 && args[0].equals("auth") && args[1].equals("logout")) {
        requireConsole();
        String account = null;
        try {
          account = vault.account();
        } catch (CuratorException ignored) {
        }
        if (!"LOGOUT"
            .equals(
                System.console()
                    .readLine("Type LOGOUT to revoke authorization and delete local drafts: ")))
          return 1;
        var outcome = vault.logout();
        if (account != null) store.deleteAccount(account);
        System.out.println(outcome);
        System.out.println(
            account == null
                ? "Account unavailable: use delete-account-data <channelId> to remove orphan local drafts."
                : "Local account drafts removed. Restart any running MCP server.");
        return 0;
      }
      if (args.length == 2 && args[0].equals("approve")) {
        requireConsole();
        var provider = ctx.getBean(YouTubeProvider.class);
        String account = provider.account();
        var id = CuratorService.uuid(args[1]);
        var d = store.get(id, account);
        var p = d.proposal();
        System.out.printf(
            "Mode: %s%nAccount/channel: %s%nTitle: %s%nPrivacy: %s%nTotal: %d seconds; upper bound: %d; shortfall: %d%nMax per video: %d; language metadata: %s%nExpires: %s%n",
            provider.fixture() ? "SYNTHETIC FIXTURE" : "LIVE YOUTUBE",
            account,
            p.title(),
            p.privacy(),
            p.totalSeconds(),
            p.constraints().targetSeconds(),
            p.shortfallSeconds(),
            p.constraints().maxVideoSeconds(),
            p.constraints().language(),
            p.expiresAt());
        int i = 0;
        for (var v : p.videos())
          System.out.printf(
              "%d. %s | %s | %d seconds | language=%s%n",
              ++i, safe(v.title()), v.url(), v.seconds(), v.language());
        System.out.println("SHA-256: " + d.fingerprint());
        String phrase =
            System.console()
                .readLine(
                    "Type APPROVE followed by the full SHA-256 to approve this exact draft: ");
        store.approve(id, account, phrase);
        System.out.println("Approval stored. No YouTube write was performed.");
        return 0;
      }
      if (args.length == 1 && args[0].equals("cleanup")) {
        System.out.println("Expired uncommitted drafts removed: " + store.cleanupExpired());
        return 0;
      }
      if (args.length == 2 && (args[0].equals("repair") || args[0].equals("resolve"))) {
        requireConsole();
        var service = ctx.getBean(CuratorService.class);
        var d = service.draft(args[1]);
        System.out.println(
            "Stop every other MCP/CLI writer before recovery. Inspect the remote playlist yourself. Never infer a missing create outcome.");
        System.out.println(
            "Account: "
                + d.proposal().account()
                + "; remote playlist: "
                + d.remoteId()
                + "; state: "
                + d.state());
        for (var video : d.proposal().videos())
          System.out.println(safe(video.title()) + " | " + video.url() + " | " + video.seconds());
        System.out.println("Exact fingerprint: " + d.fingerprint());
        String phrase =
            System.console()
                .readLine(
                    "Type "
                        + args[0].toUpperCase(java.util.Locale.ROOT)
                        + " followed by the full fingerprint: ");
        if (args[0].equals("repair")) System.out.println(service.repair(args[1], phrase));
        else {
          store.resolve(d.id(), d.proposal().account(), phrase);
          System.out.println(
              "Marked manually resolved. No YouTube write performed; this does not claim complete creation.");
        }
        return 0;
      }
      if (args.length == 2 && args[0].equals("delete-account-data")) {
        requireConsole();
        String account = args[1];
        if (!account.matches("UC[A-Za-z0-9_-]{22}"))
          throw new CuratorException("INVALID_INPUT", "Expected exact YouTube channel ID.");
        if (!("DELETE " + account)
            .equals(
                System.console()
                    .readLine(
                        "Type DELETE followed by the channel ID to remove orphan local records: ")))
          return 1;
        System.out.println("Removed local drafts: " + store.deleteAccount(account));
        return 0;
      }
      if (args.length == 1 && args[0].equals("delete-data")) {
        requireConsole();
        String account = ctx.getBean(YouTubeProvider.class).account();
        if (!"DELETE LOCAL DATA"
            .equals(
                System.console()
                    .readLine(
                        "Type DELETE LOCAL DATA to remove local drafts and journals (YouTube playlists remain): ")))
          return 1;
        System.out.println("Removed drafts: " + store.deleteAccount(account));
        return 0;
      }
      System.err.println(
          "Commands: mcp | auth login|status|logout | approve <draftId> | repair <draftId> | resolve <draftId> | cleanup | delete-data | delete-account-data <channelId>");
      return 2;
    } catch (CuratorException e) {
      System.err.println(e.code() + ": " + e.getMessage());
      return 1;
    }
  }

  private static void requireConsole() {
    if (System.console() == null)
      throw new CuratorException(
          "INTERACTIVE_CONSOLE_REQUIRED",
          "Run this command yourself in a local terminal; piped input cannot authorize it.");
  }

  private static String safe(String text) {
    return text.replaceAll("[\\p{Cntrl}\\p{Cf}]", " ");
  }
}
