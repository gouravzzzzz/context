---
name: ease-graph-opening-move
description: "Krish's graph for a scene's STARTING camera move = cubic-bezier(0,1,1,1), starting on the scene's first frame so the fast part shows"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 38bd0f11-486d-4e3a-b942-c55a0475a391
  modified: 2026-11-21T21:40:15.883Z
---

For the opening camera move of a scene, Krish's graph is cubic-bezier(0, 1, 1, 1) (`J3.bez(0, 1, 1, 1)`): it is steepest at the very start, reaches y≈0.875 at x=0.5, then settles slowly into the end. Start that move exactly on the scene's first frame, so its fastest part is seen as the scene opens. Never start it before the cut, where the fast part would be hidden. He gave this on JL trailer 15–19 v2 (2026-11-22). In v2 the opening move started before the cut on EASE_USER, so the scene opened on a near-still camera.

**Why:** a scene should open with the camera already moving fast and then decelerating. A slow ease-in at the start reads as dead.

**How to apply:**
- Use it for the first move only. Later moves stay on [[ease-graph-user-smooth]] with keyframe overlap.
- Because the curve's slope at x=0 is infinite, a ~1.45 s move covers ~28 % of its travel in the first frame. Size the move so that first step stays around the scene's peak speed (≈85–90 px/f). The first frame to second frame speed drop (~57 px/f) is inherent to the graph and is not a spike.
- Make the opening travel in the same direction as the next move, so the hand-off doesn't park the camera.
- If the first move is a long travel away from something the speaker is captioning, add a separate opening move on the current subject instead. Don't whip the captioned card off-screen.

Related: [[edit-rule-transition-ease-pair]], [[technique-keyframe-overlapping]].
