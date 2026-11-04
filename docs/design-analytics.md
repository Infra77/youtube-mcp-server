# Analytics semantics
All outputs identify sampled counts, missing timestamps and collection bounds.
Top channel/category counts use deduplicated liked and playlist videos; subscriptions have a separate
channel count. Durations: positive known seconds, median, short <=600, medium <=1200, long >1200.
Trends count playlist-item additions and subscription additions by month. Compare half-open UTC
date intervals [start,end). No valid event evidence means unavailable, not invented history.
Liked-video publication timestamps never enter engagement trends. No watch-time metric exists.
