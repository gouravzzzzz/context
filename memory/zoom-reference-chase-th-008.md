---
name: zoom-reference-chase-th-008
description: "Measured zoom language from ~/Krish works/Chase_TH_008.mp4 — the user's reference for how zoom-ins/outs should move in reels (curves, amounts, timing, snap punch-ins)"
metadata:
  node_type: memory
  type: reference
  originSessionId: 9802d9e8-f883-4a2c-9d65-9a2816a4ab5d
  modified: 2026-11-14T00:24:35.199Z
---

The user pointed to ~/"Krish works"/Chase_TH_008.mp4 (31.5 s, 1080×1920, 29.97 fps) on 2026-11-14 and asked for its zoom-ins and zoom-outs to be applied throughout reels. I measured them frame by frame, using the stripe spacing on the wall behind Chase as the zoom gauge. The values below are relative to the widest framing (1.00).

**The camera is always alternating in and out.** Over the whole clip it goes IN, OUT, IN, OUT… The total range is 1.00 to about 1.52. Between moves there are holds of about 0.4–2.5 s, and only one long hold of 5.6 s, while a graphic plays.

**Smooth push-ins and pull-outs** (the most common move):
- **Push-in:** ×1.11–1.27, lasting 1.1–2.0 s.
- **Pull-out:** ×0.78–0.90, lasting 1.1–1.7 s.
- **Curve:** best fit is cubic-bezier(0.60, 0.00, 0.15, 1.00), with an error of about 0.03. It starts gently, peaks in speed at about 38% of the move, is 50% done at about 39% and 90% done at about 65%, then settles slowly.

**Snap punch-in, then ease back** (used for impact beats):
- In a single frame the shot jumps in by about +18%: 1.138 → 1.345 at 10.44 s, and 1.284 → 1.517 at 25.86 s.
- It then eases back out over about 1.5–1.7 s on a decelerating curve that is fast at first and slows into the settle.

**Opening:** a long push-in from wide over 3.0 s, ×1.43 (0.945 → 1.356), front-loaded (50% done by 14% of the time), with a long settle.

**Motion blur:** sharpness drops about 10–35% during fast moves, so there's a slight zoom blur while the camera moves quickly.

**How to apply:** Use this as the zoom language on talking heads, and adapt it for graphics scenes:
- alternate in and out on every beat
- snap punch-ins with an ease back on impact words
- add mild zoom blur proportional to zoom speed

Combine it with head tracking ([[edit-rule-talking-head-framing]]) and [[edit-rule-camera-movement]].
