---
name: ease-graph-user-smooth
description: The user's smooth S-curve speed graph (cubic-bezier 0.68,0,0.03,1) to use for every smooth move (documents, phones, camera, page turns)
metadata:
  type: feedback
---

The user gave this value graph on 2026-11-14 and said "save this graph for future use": a steep S-curve. It starts very slow, has a fast middle, and has a long soft landing. The handles were read off the screenshot as **cubic-bezier(0.68, 0.0, 0.03, 1.0)**: the out handle sits flat at x≈0.68, and the in handle sits flat at the top at x≈0.03. The screenshot is copied to ~/chase-009-build/refs4/img/user_ease_graph.png.

**Why:** v4's document and phone moves (springs, sine wobbles, eased whips) read as "really bad". This curve is what they want smooth motion to feel like.
**How to apply:** use it for objects rising in or entering, page turns, phone moves toward and away from camera, camera pushes, and Chase zoom-out entries. Never add springs, bounces or sine wobble on top unless asked. Related: [[edit-rule-smooth-motion]], [[edit-rule-camera-movement]].
