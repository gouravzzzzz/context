---
name: feedback-jl-trailer-scene-review
description: "Krish's hard rules from the Justin Levine trailer scene reviews (2026-11-22) — no zoom-through ever, copy ref transitions exactly, big captions near the subject, subject centred, no laggy footage, ref-speed camera"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 38bd0f11-486d-4e3a-b942-c55a0475a391
  modified: 2026-11-21T20:47:13.939Z
---

Rules from Krish's angry review of the trailer v1 and the redone scenes (2026-11-22). They apply to every scene of every trailer/reel.

1. **No zoom-in / zoom-out "zoom-through" transitions, ever.** ("why the fucking hell are we always doing a zoom in and out transition … stop using this zoom in transition its ridiculous"). Copy the exact transition the given reference uses, e.g.:
   - Dime S2→S3: the outgoing shot whips LEFT (ease-in, heavy horizontal blur); the speaker cut-out rises from below while scaling 1.2→1.0 (cubic ease-out, about 0.83 s); the card does a left-anchored wipe; hard cut out.
   - Pinterest openings: a hard cut onto the ref's opening animation.
2. **Captions big, readable and close to the subject.** Never small text in a corner. Caption animation in every scene follows the references:
   - Per word: fade over 2–4 frames with a 10–16 px rise and blur clearing.
   - Hero word types on letter by letter.
   - Laid out in place, never re-centred.
   - The trailer v1's caption animation was called "shitty".
3. **Subject/main image centred in the frame,** not high up or off to one side, unless the ref or Krish says otherwise (e.g. Autodesk photo on the right, captions on the left).
4. **No laggy footage.**
   - Screen-recorded web captures (MediaRecorder at 30 fps) can be half duplicate frames, which plays as lag. Check the duplicate-frame ratio before using any capture.
   - Prefer the ORIGINAL file. Vimeo: open player.vimeo.com/video/<id> in neo; `window.playerConfig.request.files.hls.cdns[...]` gives the m3u8 URL; download it with ffmpeg `-c copy`.
   - Map native 23.98/24 fps frames 1:1 onto the 24 fps timeline. Never resample, slow down or optical-flow it ([[feedback-footage-normal-speed]]).
5. **Camera moves as slow and smooth as the reference's.** Measure the ref's move durations in seconds and keep them; never compress them to fit. Use fewer moves instead. Moves between elements must read as 3D (dolly plus orbit, parallax), not a flat pan/zoom. Match the reference's element density (more satellites/elements).

6. **Never invent element motion.** Check the ref frame by frame and give each element only the moves it has there. The v2 card whip-out wasn't in the ref, and Krish said "this is not the way everything moves in the reference check it frame by frame". Write the per-element timeline (refs/dime_s3/study.md style) BEFORE building.
7. **Don't swap a camera he accepted.** When he flags only one element, fix that element and keep the camera he didn't complain about. v3 replaced v2's smooth 3D camera with the ref's fast 0.7 s truck profile, and he said "why the fuck the camera movement in this got bad again". Camera smoothness (his graphs, overlap) beats copying a ref's whip-speed move.
8. **Photo card behind the speaker** (Dime S3, 10–14 s): the card sits on his right (screen left) and ends halfway through him. It's revealed by a FEATHERED wipe travelling RIGHT→LEFT out from behind him, using the ref's measured edge profile (f101–f112, 0.37 s). The caption on the card is revealed by the same wipe. It's a still photo, and it leaves with its caption on the truck.
9. **Overlap scene hand-offs; keep the background.** Never wait for the outgoing element to finish closing before the next scene animates. The next captions and the carried-over element (e.g. the 'to' becoming the star) start AS the exit starts. Keep the previous scene's background running underneath (no ground swap, no cut) so it reads as one continuous shot (Krish, Autodesk v4).

**Why:** these are Krish's direct, repeated complaints. Ignoring them costs his trust.
**How to apply:** check every scene against all of these rules before stills and before rendering. Related: [[feedback-copy-reference-exactly]], [[feedback-trailer-v1-rules]], [[edit-rule-zoom-direction-continuity]] (now superseded for transitions: no zoom-throughs at all).
