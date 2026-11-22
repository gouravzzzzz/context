---
name: edit-rule-camera-movement
description: "Camera movement must be calm and purposeful: v3 constant pushes/tilts were rejected; zooms only at transitions/entries, centred, using the user ease graph"
metadata:
  type: feedback
---

The user wants plenty of camera movement in every reel. A frame that sits still reads as dead. Every shot should have a purposeful move that **focuses on what is happening right now**:
- push in on the word, number or object being talked about
- tilt or pan to the next element as it appears
- punch closer when a highlight or stamp lands

Moves stay smooth (eased bezier curves, one clear direction at a time, no shake or rotation jitter). They chain into each other so the camera is almost always travelling.

**Why:** User feedback on CHASE_009 v2 (2026-11-14): "not enough zooms and camera movement, overall it was looking very still, needed more camera movement to focus on things happening".
**How to apply:**
- Plan a camera keyframe for every beat (each spoken key word or graphic event), not one slow drift per scene.
- On graphics, move the camera to frame each new element as it appears.
- On talking heads, combine strong head tracking ([[edit-rule-talking-head-framing]]) with pushes on key words.
- Captions stay fixed and unzoomed, in [[edit-rule-reels-safe-zone]].

**SUPERSEDED IN PART (2026-11-14 night, rounds 3 and 4 on CHASE_009):** the user said the v3 camera movement and zooms were "really bad and not at all what i showed you" and had them removed. What they want now:
- On Chase: head tracking, plus a smooth zoom-out each time his clip comes in. Nothing else.
- On photos: one zoom into his face as the photo appears, with the face centred. No bounce, slide or slam.
- In 3D scenes: subtle, centred moves only, never drifting to one side, on [[ease-graph-user-smooth]].
- No flash transitions.
