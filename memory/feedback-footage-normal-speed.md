---
name: feedback-footage-normal-speed
description: Play footage at its normal speed; never slow-mo or optical-flow it to fill time. Only camera moves get smoothed
metadata:
  node_type: memory
  type: feedback
  originSessionId: 38bd0f11-486d-4e3a-b942-c55a0475a391
  modified: 2026-11-21T20:31:09.398Z
---

Footage (B-roll, speaker film) plays at its normal speed. Don't slow it down, minterpolate it, or add optical-flow in-betweens to stretch a clip across a shot. Smoothing applies to the camera moves only: Krish's ease graphs, overlapping keyframes and motion blur.

**Why:** Krish, 2026-11-22, on the 10–14 s 3D section of the Justin Levine trailer: "play the video normally no need to smoothen the footage only smoothen the camera movements".

**How to apply:**
- If a clip is too short, use more real frames: other takes, or the same clip's later frames past an internal cut. Line up the face across the cut and hide it under the camera move or defocus. Don't stretch time.
- Before using frames, check where cuts fall inside the clip (diff the frames).
- Related: [[edit-rule-smooth-motion]], [[technique-keyframe-overlapping]].
