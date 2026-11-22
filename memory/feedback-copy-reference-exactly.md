---
name: feedback-copy-reference-exactly
description: "When copying a reference style, never invent deviations (tilt, transparency, sizes, positions); check every element against the ref frame by frame before showing stills"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 03a641b8-0192-4c30-bc2c-eb940a542004
  modified: 2026-11-18T18:52:50.763Z
---

When Krish gives a reference reel, every element must match what the reference actually does: end pose, opacity, size relative to other elements, centring, timing. Do not add "creative" tweaks the reference doesn't have.

**Why:** On Ron short 02 v2 (2026-11-19) I left a code card tilted after its spin, made it see-through, made it bigger than the word behind it, and put a "500" at a 3D angle off-centre — none of that was in the reference. Krish: "i wont tolerate these silly fucking mistakes from now on."

**How to apply:** Before showing stills, for each animated element: pull the reference moment frame by frame (`refs_jen2/tools/sheet.py`), write down start pose → end pose, opacity, size ratio, alignment, then render the same frames of ours side by side and compare. Fix every mismatch first. If I'm unsure what the ref does, look again instead of guessing. Never change something Krish said to keep (e.g. the halftone transition). Related: [[project-jennifer-musselman-style]], [[feedback-documentry-v4-review]].

**Text is always straight (2026-11-20, Kristina trailer):** I put the scene-09 text and neon box at a 3D yaw/pitch angle and the user asked: "why is the text at an angle here make it all straight". Even when they ask for text that "moves with the camera in a 3D way", the 3D is only in the motion (parallax, push, swing-in). Every caption, word and box settles flat, straight and level, and stills show it straight.
