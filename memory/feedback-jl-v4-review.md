---
name: feedback-jl-v4-review
description: Krish's JL trailer v4 notes — talking heads dead stable (no face-follow/drift), ONLY his 3 graphs for every move/transition, no music, voice must have no chopped words or dropouts
metadata:
  type: feedback
---
From Krish's review of JL trailer v4 (2026-11-22):
- **Talking heads stay completely stable.** No face-tracked anchor (it wiggles), no slow pan or push drift. The camera moves only during an animation or a transition.
- **Only three graphs, for every movement, fade and transition:**
  - EU, cubic-bezier(0.68,0,0.03,1)
  - G1, (0,0,0,1)
  - G2, (1,0,1,1)
  - Never bez(0,1,1,1), cubic/quadratic ease-outs, smoothstep timing, linear drifts or ref-measured curves. This supersedes [[ease-graph-opening-move]].
- **No music bed** when he says remove music. Keep only tiny SFX he hasn't rejected.
- **Voice quality:**
  - Never splice with fades to digital zero.
  - Never cut on a coarticulated word boundary with a moved joint.
  - Adobe Enhance: SUPERSEDED on 2026-11-22 (v6 review). Krish now wants the whole voice cleaned in Adobe Podcast Enhance v2 with Speech 100 %, Music 0 % and Background 0 %, so there's no background noise. Set the sliders with keyboard arrows (the slider value is 100 minus the displayed %). Check the words afterwards with Whisper on short clips; the full-file Whisper is flaky.
  - Check every render for dropouts (<-75 dBFS holes), clicks and leaked filler fragments with Whisper (word probability + diff against the script).
**Why:** he heard the wiggle at 0–8 s and "weird"/mispronounced words in v4.
**How to apply:** every trailer and reel. Related: [[project-justin-levine-trailer]], [[edit-rule-talking-head-framing]], [[edit-rule-transition-ease-pair]].
**v5 review (2026-11-22), same project:**
- **No abrupt mutes anywhere.** Room tone must sit at the speaker's REAL background level, not the quietest 2 %. Pauses must never fall to digital silence. Source dropouts get faded and filled.
- **Breaking news:** when he says something repeated, make the speaker full screen and cut + zoom in on EVERY repeat.
- **Never an empty black screen** between the last shot and the end title.
- **Dull webcam footage:** grade it (contrast, saturation, warm skin, tamed white wall).
- **Text exits:** text leaves on G2 into the cut, and the next element enters on G1 in the same direction.
**v6 review (2026-11-22):**
- **Text near a face:** a caption box that overlaps the speaker goes BEHIND him, using a rembg person matte and Item.behind. Its position stays the same.
- **Background noise:** clean the entire voice in Adobe Podcast (background 0). The room-tone bed only exists to stop abrupt mutes when Adobe is NOT used.
