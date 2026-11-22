---
name: feedback-documentry-v4-review
description: User's v4 review rules for documentry-style reels: outpaint horizontals to vertical, slow moves, pure transitions, left/right/centre alignment, leaks into talking head, captions move with graphics
metadata:
  type: feedback
---

The rules from the user's review of Ron documentry v4 (2026-11-17), all applied in v5:
- Always outpaint a horizontal photo to 9:16 first (Gemini via neo), never blurred bands.
- Slow moves by default. Fast moves only at cuts where needed. One person = one move.
- A slide transition is only a slide and a zoom is only a zoom. A zoom-in transition stays a zoom IN on the next photo.
- Zoom into faces or the centre, never the back of a head or a corner. "this is the last time im tolerating such stupid and silly mistakes".
- Text on the left is left aligned, on the right is right aligned, otherwise centred (pills/marks too). Every text gets a visible shadow + glow.
- A light leak on every cut back to the talking head. A caption above a graphic moves with it.

**Why:** the user had to spell out each of these in their v4 notes and said "what i just told you to do is what you should do on your own".
**How to apply:** check every shot against this list before rendering. Added to the SOP on 2026-11-17 (artifact v3) at the user's request. See [[skill-documentry-style]], [[edit-rule-no-text-on-person]], [[feedback-open-reel-after-render]].

**v5 review (2026-11-17), user very angry about repeats:**
- Never place text on/near existing lettering in a photo ("never make this mistake again").
- Slide transitions must land on a smooth eased curve, never an abrupt stop.
- Always remove every third-person voice in the reel ("i thought i had already told you once"). Check word ends aren't clipped by cuts ("Canada").
- Always add vignette + radial fast blur + subtle chromatic aberration + Texturelabs_Grunge_356M texture on all graphics/photo animations.

**v6 review (2026-11-17):**
- Every move's graph must slow down at the END of its shot: end moves before the cut (never let an ease run past the cut and get chopped mid-speed), except a deliberate slide/zoom-through transition.
- Never a stop in the middle of one sentence's movement. When a zoom reverses, keep a slow pan running under it. Join consecutive moves so velocity never hits zero; check with a per-frame speed print (dips < 35 % of neighbours = fail).
- Light leak on EVERY scene change that has no slide/zoom transition (photo→photo, speaker→photo, photo→speaker, speaker→graphic).
- Moves slow but clearly visible (≈ 1.5+ px/frame). Vignette strength 0.525 (user +25 %).
- (2026-11-17, v7 family shot) The camera must always move TOWARD the person being named (Steve stands left of Marie → pan left on "Steve"). A "keep-it-moving" pan must never point away from the subject. Check direction with a per-frame print of each named face's screen x. User: "are you fucking dumb?"
- (2026-11-17) Never start a render (full or partial) unless the user asks for one in that message. After making changes, report and wait. User: "i didnt ask you to render it".
