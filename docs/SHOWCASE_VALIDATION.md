# Visual showcase validation

The site is buildless HTML/CSS/JS, deployed from`site/` by GitHub Pages. It does not call a model/API or load third-party fonts, scripts or analytics.

## Verified before deployment

-Local HTTP200 for the page, CSS, JS, evidence JSON and media.
-33 HTML resource/anchor references checked; source-video checksum identities verified.
-All three compressed MP4s decoded locally:400/557/267 frames at20fps, durations20.0/27.85/13.35s. The full source timeline is retained at4×; not end-to-end policy latency.
-Data-equality checks against the released450-episode task table and G1/G2 summaries.
-Actual app JavaScript executed in a deterministic DOM-logic unit harness:15/7/8 task filtering,4/8 method-stage switching, case switching, image-dialog open/close and stage-scope copy. This is **not a browser rendering test**.
-Existing7 numerical/contract regression tests pass; publication source/asset manifest and leak checks are regenerated for this release.

## Verification limit

The available CUA browser inventory exposed only MCP Apps; an in-app browser was unavailable. A local preview was offered in Codex, but no successful browser screenshot/desktop-mobile visual QA or browser video-playback test is claimed. CSS includes responsive layouts and reduced-motion handling; their real rendering needs independent browser confirmation. Source video frames were visually inspected with contact sheets. No substituted or generated action imagery is used.

The repository README includes ordinary image previews and MP4 links because GitHub Markdown does not reliably render custom interactive pages or video tags. The separate Pages site provides playable video and chart interactions.
