---
name: edit-rule-cut-silence-and-fillers
description: "Mandatory first step on every video/reel edit: cut all dead air, pauses, repeats, stutters and filler words from the speaker's audio"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 9802d9e8-f883-4a2c-9d65-9a2816a4ab5d
  modified: 2026-11-13T22:45:08.110Z
---

On every video built from a raw file (Chase, Flourish, any client), the first pass on the raw is a tight cut:
- Find every pause or empty gap where nobody is speaking and cut it out, including pauses *inside* a sentence, not only between shots.
- Cut repeated words or phrases (said twice), stutters and false starts.
- Cut filler words: "you know", "right", "like", "um", "uh", "so" used as filler, and similar.

- **No abrupt jump cuts.** Every cut inside talking-head footage must be hidden. Keep the framing continuous across the cut, with the same zoom and face anchor on both sides and any zoom carrying on smoothly. Bridge it with a short soft blend of about 4–6 frames. Never pair a cut with a sudden change of scale. v1's cut from "…refuse to entertain." to "So to get a deal done" jumped from a 100% punch-in to a shrunken frame, and the user said it "looks odd" on 2026-11-14.

**Why:** User flagged leftover pauses in CHASE_009_Reel_v1 (2026-11-14) as a cutting mistake and said to do this for every video they create.
**How to apply:** Before designing any animation, run word-level transcription plus silence detection on the raw. Build the cut list from that (keep a few frames of breath so words aren't clipped), then time all animation to the tightened edit. Re-check the final audio for gaps over ~0.25 s. This complies with [[flourish-edit-sop]]: if a filler sits inside a black script line, flag it with a comment instead of silently removing it. Pacing reference: [[flourish-reference-reel-arnold]].
