---
name: edit-rule-reels-safe-zone
description: "Mandatory Instagram Reels safe zone (1080x1920) — every caption and graphic must sit inside it, on every reel"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 9802d9e8-f883-4a2c-9d65-9a2816a4ab5d
  modified: 2026-11-13T22:31:19.455Z
---

All captions, text and graphics on every vertical reel stay inside this safe zone (from the user's reference image, saved at ~/Downloads/"Find high-quality images, photos, and animated GIFS with Bing Images.jpeg"). The zone is L-shaped:
- **Upper block:** x 70–1025, y 250–1110 (top margin 250, left 70, right 55).
- **Lower block:** x 70–887, y 1110–1500 (right margin 193 for the like/comment/share icons, bottom margin 420 for the username and caption).
- Nothing goes above y 250 or below y 1500. Nothing goes left of x 70 or right of x 1025, and nothing goes right of x 887 below y 1110.

**Why:** In CHASE_009_Reel_v1 (2026-11-14), captions and graphics ran to the very top, bottom, left and right edges of the frame, under Instagram's UI. The user said to keep everything in the safe zone.
**How to apply:** Check a text or graphic's full bounding box against both blocks, including its glow, overshoot and animation start and end positions. **Alignment fix (user, 2026-11-14: "why tf is this misaligned"):** never centre text on the lower block's own centre (about x 478). That shifts it off the frame's axis and it looks misaligned, the way "SAFE ZONE" sits in the reference image. Centred text always sits on the frame centre, x = 540, all reel long. Below y 1110 it is capped at 694 px wide (x 193–887). Above y 1110 it can be up to 940 px wide (x 70–1010). Left-aligned text all shares one left margin. Text never jumps between axes. Before delivering, overlay the zone on test frames to verify. Background art and full-frame B-roll can fill the frame. Related: [[edit-rule-cut-silence-and-fillers]], [[flourish-edit-sop]].
