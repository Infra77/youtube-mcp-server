# Local rehearsal and live demonstration

1. Run local-check and inspect its JSON result. Explain that this is a stdio Java MCP service.
2. In an existing MCP client discover ten tools, five resources and one workflow prompt.
3. Read limitations; call get_video_overview(FIXTURE0001), then find_similar_videos with limit=4.
4. Call find_similar_channels(@ExampleMath,3), recommend_for_me(3), and analyze_my_engagement
   comparing 2026-01-01/2026-02-01 to 2026-02-01/2026-03-01. Explain coverage and timestamp meaning.
5. Plan a 1800-second English Fourier playlist with maxVideoSeconds=1200 and maxVideos=3.
6. Commit without approval and show APPROVAL_REQUIRED. Display the full saved draft.
7. The human runs admin.ps1 -Mode fixture approve UUID in a terminal and types the digest.
8. Commit through the host; show CREATED with fixture=true and no real playlist URL. Repeat to
   demonstrate no duplicate write. Explain that the test-only grant simulation is not real consent.
9. Walk through video-to-playlist skill and brief output analysis, then use brain-query to explain
   quota reservation from its note, ADR-0007, QuotaService and DatabaseIT test.
10. For the actual live gate, first complete google-cloud-setup.md and switch to live mode. Use small
    approved constraints and check remaining quota before any operation. Record only nonprivate evidence.

The scripted SDK test performs the fixture sequence automatically. It does not impersonate human
consent to a live account, nor substitute for a human evaluator reviewing the real CLI preview.
