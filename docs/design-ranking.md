# Ranking v1
Bounded corpus: seed plus at most 50 hydrated candidates; normalized lowercase Unicode letters/numbers,
stopwords, title repeated twice, tags once, description capped at 2000 characters.
TF=count/total; IDF=log((N+1)/(df+1))+1. Cosine zero for empty vectors.
Score=.55 cosine+.20 tag Jaccard+.10 known category agreement+.10 min/max positive duration
+ .05 known language agreement. Empty tags/category/language do not count as matches.
Stable sorting: descending score then ID. Exclude seed, unavailable candidates and duplicates.
Channel ranking uses title/description cosine and stable ID ties. Subscriber counts are not quality.
Personal profile combines normalized source text vectors, weights .45 likes/.30 subscriptions/.25
playlist items, renormalizing available sources with coverage warnings. Exclude known videos.

## Evaluation

RankingEvaluationTest supplies four synthetic labeled educational seeds, two relevant candidates and two unrelated distractors for each. Acceptance precision@2 is at least .75; the test requires 1.0 for these intentionally clear cases. It also times 100 ranking/selector workflows at the 50-candidate bound with a 10-second ceiling. Machine-readable results: target/evidence/ranking-evaluation.json. These are author-labeled cases, not a user study; Day 7 of the shared plan requires independent human label review, channel/personal cases and noisy metadata evaluation before declaring relevance accepted.
