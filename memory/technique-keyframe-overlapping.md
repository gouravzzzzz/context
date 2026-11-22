---
name: technique-keyframe-overlapping
description: Keyframe overlapping (MahdiEdits AE tutorial): start the next move ~50% into the previous eased move via a parented null so there is never a pause; how it maps to the reel engine
metadata:
  type: reference
---

Source: MahdiEdits, "Overlapping Keyframes: Biggest Trick to Smooth Animation" (youtube.com/watch?v=jp-XjJGxXHg, 2:39), studied 2026-11-17 at the user's request.

- Problem: A→B then B→C as back-to-back keyframes leaves a few-frame pause at B ("our eyes can feel it", looks stiff/robotic).
- Fix: keep A→B on the object; parent the object to a null; animate B→C on the null, starting BEFORE A→B ends, "around the middle". Measured from the timeline in the video: the null's first key sits ~49% into the object's move, and the null's move is ~1.1x as long. Both pairs are Easy Ease. Repeat with more nulls for more moves.
- Result: when the object reaches B it is already moving toward C; everything flows.

**How to apply in our engine:** reel_rl/work/photocam.py cam_at already sums moves as deltas (= stacked nulls). Rule: each next move starts at 40-60% of the previous move's duration (not 80-90%), both eased; last move of a shot still eases to ~0 before the cut. Check with the per-frame speed print. Related: [[feedback-documentry-v4-review]], [[ease-graph-user-smooth]], [[edit-rule-smooth-motion]].
