---
name: edit-rule-smooth-motion
description: "Every animation, camera move and transition must be smooth — no choppy/stepped motion; use eased curves, slower travel and real motion blur"
metadata:
  type: feedback
---

Every animation, graph, transition and camera move must look smooth. Nothing choppy, stepped or jumpy.

**Why:** The user found the 3D phone entrance in CHASE_009 v2 choppy on 2026-11-14. It travelled about 1,600 px in 0.9 s at 24 fps with no motion blur, so each frame jumped about 100 px. The user said: "I want every animation, every graph, and every transition to be smooth."

**How to apply:**
- Use eased curves only. The camera uses cubic-bezier(0.60, 0, 0.15, 1), from [[zoom-reference-chase-th-008]]. Never use linear starts or stops.
- Keep travel distances short and entrances about 1.2–1.5 s long.
- Never use 1-frame jumps. Snap punch-ins become a fast ease over about 5 frames, then ease back.
- Don't stop and start the camera between closely spaced targets; glide through them in one move.
- Render real motion blur with a 180° shutter by averaging sub-frames: 4 normally, about 12 during fast moves. With too few sub-frames, fast objects show ghost copies.
- Before delivering, run a frame-difference spike check: flag any frame whose change is more than about 2.2× the median of its neighbours.

Related: [[edit-rule-camera-movement]].
