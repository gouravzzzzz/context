---
name: chase-009-v2-revisions
description: "Running list of the user's revision notes for CHASE_009 reel v2 (Chase talking-head motion-graphics reel) — read before building v2"
metadata:
  node_type: memory
  type: project
  originSessionId: 9802d9e8-f883-4a2c-9d65-9a2816a4ab5d
  modified: 2026-11-13T22:55:24.448Z
---

**v1:** ~/Downloads/CHASE_009_Reel_v1.mp4. It was built by reel.py in the previous session's scratchpad (/private/tmp/claude-501/-Users-gourav/9f217e95-…/scratchpad/reel/), which also holds src frames, chase.wav and fonts. That's temp storage and may be wiped. The raw is ~/Downloads/CHASE_009.mp4 (1296×2304). v2 output goes to ~/Downloads/CHASE_009_Reel_v2.mp4.

Revision notes, received 2026-11-14 one at a time with "wait for next":
1. Tight cut: remove pauses, repeats, stutters and fillers → [[edit-rule-cut-silence-and-fillers]].
2. All text and graphics inside the IG safe zone → [[edit-rule-reels-safe-zone]].
3. Typography learned from the user's Pinterest Typography board → [[typography-board-reference]].
4. No big bold text; use only Helvetica Regular/Bold + Playfair Display Regular → [[edit-rule-fonts-no-big-bold]].
5. Blue + golden only → [[edit-rule-two-color-palette]].
6. Centred text stays on frame centre x=540, not shifted to the lower block's centre.
7. Fix the wavy baseline ("ends up being").
8. Chase always full-frame and centred, with zooms pushing in on his face → [[edit-rule-talking-head-framing]].
9. Remove the abrupt cut after "…refuse to entertain." Replace the stroked box on REFUSE with a solid highlight rect that wipes left→right.
10. Replace the circles with good-looking person icons/PNGs, and the fake document with real paper, both from Pinterest → [[edit-rule-real-assets-over-shapes]].
11. Calls/texts shot (raw ~31.8–35.0 s): a 3D iPhone pops up from below. Its screen shows the real iOS call UI during "on calls together". The SAME phone then shows an iMessage conversation during "on text together". This replaces the 2D waveform and the bubbles. Keep the phone in the palette: iMessage blue = you, gold-tinted bubbles = them, and the call buttons recoloured to blue/gold.

12. Head tracking on every Chase shot, matching CHASE_004 8–10 s → [[edit-rule-talking-head-framing]].

**How to apply:** Implement all of these in v2 and check each one against test frames before rendering. More notes may follow.

**Round 2 notes on v2 (2026-11-14, after v2 was sent to Krish on WhatsApp):**
13. The user didn't like the duotone photo people. Replace them with **flat solid silhouette person icons** like the user's pins 685250899581888637, 1077275173336113062, 567383253070205213 and 677580706478353643: a round head and a rounded shoulder/body shape, one variant a businessman silhouette with a tie, filled in a single solid colour (you = blue, them = gold). The downloads are in the session scratchpad at refpins/r1–r4.
14. Too still overall. Add far more camera movement that pushes, tilts and pans to **focus on whatever is happening**: the highlighted row, the number counting, the bubble arriving, the word being said.
15. Head tracking on Chase wasn't strong enough. Punch in tighter so his head fills more of the frame, and follow it more closely with less smoothing, so the follow is clearly visible like CHASE_004 at 8–10 s.
16. Zoom style: apply the zoom language measured from Chase_TH_008 throughout → [[zoom-reference-chase-th-008]].
17. Money/number counters (e.g. $10M → $1B+) in Helvetica Bold, BIG, gold, emphasised → [[edit-rule-fonts-no-big-bold]] (exception).
18. Term-sheet document (~12–13 s in v2) looked flat 2D. Make it a real 3D sheet of paper: it rises from below lying back in perspective, then swings up to vertical. It needs real paper bend/curl, per-fold lighting, a shadow that tracks its height, and a springy settle with a slight flutter, then keeps gently floating/rotating ("more animation, more life"). The camera follows the highlight rows. Reuse the same 3D sheet in the table/CLOSED shot.
