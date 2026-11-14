---
name: edit-rule-talking-head-framing
description: "Talking-head framing rule: show the raw full-frame (never shrunk/cropped/offset), speaker centred; zooms only push in, anchored on the face"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 9802d9e8-f883-4a2c-9d65-9a2816a4ab5d
  modified: 2026-11-13T22:55:23.093Z
---

Talking-head footage is always shown as the **full raw frame**, scaled exactly to fill 1080×1920. It is never shrunk with black edges, never cropped off one side and never shifted off-centre. The speaker stays in the middle the whole time.

Zooms only **push in from full frame**, anchored on the speaker's face. The face stays where it is while the frame tightens around it. There's no sideways travel, no starting him on one side and sliding him to centre, and no zoom-out below full frame.

**Why:** In CHASE_009_Reel_v1 the "83–96 %" zoom values were actually *below* full frame. The raw shrank to about 900×1600 and pinned top-left, so there were black strips on the right and bottom and Chase sat left. The "push" then slid him toward centre. Shots 3, 5, 7b and 13 were all affected. The user flagged it on 2026-11-14: "I don't want him cropped… Keep him in the center… When you zoom in, focus on his face."

**Head tracking (user, 2026-11-14):** whenever Chase or the speaker is on screen, the frame is **head-tracked**, the way it's done in ~/"Krish works"/CHASE_004.mp4 from 8 to 10 s. There's a slight punch-in, and the crop window follows his head so it stays locked near the centre while the background drifts behind him. Measured in that clip: the background shifts about 260–340 px horizontally while his face moves only about ±70 px on screen. So it's a smoothed follow, not a rigid lock, with no jitter.
Implementation:
- Track the face every frame. Smooth it only enough to remove jitter, not so much that the follow disappears.
- Punch in clearly: about 1.35–1.45× of full frame, so the head is big and the follow can be seen. v2 used 1.15× with heavy smoothing, and the user said it 'was not done enough'.
- Follow with light smoothing so the camera reads as following his head, not sitting still.
- Centre the crop on the smoothed head and clamp it so it never leaves the raw.
- Eased zooms on his face layer on top of the tracking.

**How to apply:**
- Base scale = output width ÷ raw width. For a 9:16 raw that is an exact fit with nothing cut off.
- Zoom factor is always ≥ 1.0 on top of that, with the anchor at the face. For CHASE_009 (raw 1296×2304) the face is at about x 0.56, y 0.365, close to centre. Up to about 1.2× is still native resolution.
- Check: every frame edge must be raw picture, never black or reflected padding.
- Combine with [[edit-rule-reels-safe-zone]].
