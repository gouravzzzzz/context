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

**Build folder (durable, since 2026-11-14 evening):** ~/chase-009-build/. v3 renderer = v2/reel3.py, venv at ~/chase-009-build/venv. Test frames: `cd ~/chase-009-build/v2 && ../venv/bin/python -I reel3.py test <secs...>`. Full render: `~/chase-009-build/tools/render_full.sh ~/Downloads/CHASE_009_Reel_vN.mp4`. See RECOVERY.md. v3 = ~/Downloads/CHASE_009_Reel_v3.mp4 (notes 13-18 applied). Never build in the scratchpad again; it gets wiped.

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

**Round 3 notes on v3 (2026-11-14 night). v4 = v3 + these. Low-quality preview FIRST, final HQ render only after the user reviews:**
19. REVERSE notes 14/15/16: remove ALL the camera movement and zooms added in v3 ("really bad and not at all what i showed you"). Everything else in v3 stays exactly as is.
20. Opening scene + the ~28 s scene: photo+text style from IG reel DdcWLwATu68 (study EVERY frame): how photos are used/animated with text, camera graphs + photo movement graphs (copy), typography on photos. Smooth like the reel. Photos = real Chase MacLeod photos from his socials (IG, LinkedIn, X, YouTube).
21. ~6 s and ~17 s animations: look like Dropbox Ray_TalkingHeads_002.mp4 (Dime Motion Ray episode 1); copy its glow and colours.
22. ~12 s document scene: animate like Pinterest pin pin.it/2QhQyDvsT.
23. ~21 s scene: inspired by ~/Downloads/_.jpeg (flat halftone sticker illustration, two people at a table, cream grid paper, orange square). The document appears from behind the table; whole scene feels 3D, with text animation.
24. Phone scene: keep the 3D phone, but the camera must be much smoother/slower. Phone UI no longer gold/blue: use the UI style of pin.it/2Zk4F9ndH.
25. Scene after the phone: a 3D animation like the 21 s scene.
26. Backgrounds of every NON-3D graphic scene: warm beige/cream/taupe soft gradients with fine grain, like ~/Downloads/ -271.jpg, -272.jpg, -273.jpg, -274.jpg.
27. (answered) The 27.1–30.9 s room scene is SPLIT: "and in rooms" (27.1–28.2) = 3D like the table scene; "working together… engaged" (28.2–30.9) = IG photo style with real Chase photos.
28. (answered) Chase shots: KEEP the head tracking; remove the unnecessary v3 camera movement; keep zoom in/out ONLY at transitions.
**v4 build (2026-11-14 night):** renderer ~/chase-009-build/v2/reel4.py = reel3.py + v4_parts.py (merge recipe in session; edit BOTH or regenerate). Refs + every-frame studies in ~/chase-009-build/refs4/ (FINDINGS.md). Chase photos ~/chase-009-build/chase_photos/ (24, SOURCES.md). Preview: `PREVIEW=1 ../venv/bin/python -I reel4.py` -> out4p (540x960) -> ~/Downloads/CHASE_009_Reel_v4_preview.mp4. Final HQ only after user OKs the preview.
**Round 4 notes on v4 preview (2026-11-14 ~22:15):**
29. Chase photos (opening + 28 s): his FACE centred in frame; no bounce/slide/stack moves; the only camera move is a zoom INTO his face as each photo appears.
30. Photo-scene type much bigger, white with glow + soft shadow, like the user's refs (Pam_TH small line over a big bold line with a white halo; "$3-5M+" bold white with a gold box). Type refs apply to the photo scenes only.
31. Remove every quick flash (white/bloom), including the one at 8 s.
32. Every time Chase's clip comes in: a smooth zoom-out transition.
33. 12 s document: the look is good but the motion was bad. Smooth rise from the bottom and a smooth page turn, using [[ease-graph-user-smooth]].
34. 21-24 s 3D table: keep it, add a bit more subtle movement, CENTRED (it was drifting right), and a subtle spotlight on the document that grows as the camera zooms in.
35. Phone: the phone moves toward camera on "calls" and back on "texts", 3D and centred, using the user's graph. Bigger type. White bg with a gentle gradient.
36. 27 s rooms 3D: zoom OUT from centre, with the text moving with the zoom. Bigger text.
37. 28 s photos: same as 29/30.

## Round 5 notes (on v4 preview2, 2026-11-14)
38. Never any text/graphic on Chase (face, head, body), anywhere. (global rule now)
39. All zooms last 2-3 s on the user graph.
40. Replace the 2nd opening photo (sofa, 14): too similar to the next one (24).
41. 13 s: put back the transition from v4 preview1 (reel4_preview1.py), not the smooth push.
42. "deal" pills (gold/white) -> dark brown glossy rounded boxes with light rim and cream text (ref screenshot "4% rule").
43. Last photo scene: pan slowly (sideways, from the bottom) on the graph instead of zooming.
44. Text everywhere comes on earlier and stays readable longer.
45. Vignette whenever photos are on screen.
Round 5 build: ~/chase-009-build/v2/reel5.py = reel4.py + v5_parts.py (inserted before "NO_CAP.append((27.12, 28.18))") + small seds (rooms 2.2 s, pill sizes, FAST, PMASK/person check). Person masks: v4/assets/masks/NN.png (rembg u2net_human_seg). Test: `reel5.py test <secs>` -> v2/test5, fails on text touching a person. Preview3 -> ~/Downloads/CHASE_009_Reel_v4_preview3.mp4. User OK'd TH captions staying on chest (rule 38 is photos/graphics only).

## Round 6 notes (on v4 preview3, 2026-11-14): "everything looks good"
46. Motion blur on every movement, graphic and transition (stronger than before).
47. Vignette + radial fast blur (CC Radial Fast Blur look) as an overlay on photo and graphic scenes.
48. Textures as overlays, texture only (no colour): Texturelabs_Paper_316L on all photo and graphic scenes; Texturelabs_Paper_317L (crease) on the document and table scenes only. Copies in ~/chase-009-build/v4/assets/tex/ (originals ~/textures/).

## Round 7 notes (on preview4, 2026-11-14)
49. "partner." photo 24 was low-res and over-zoomed -> replaced with 02 (5504x8256 studio portrait). Root cause fixed: photo_src now loads each photo at the resolution its zoom needs (NEED_H), not 1.45x frame.
50. Table figures (21 s table + rooms): subtle head sway/nod and small hand moves via a local warp of table_clean.png (sticker_anim in v7_parts.py). Keep it subtle, slow (2-4 s periods).
Build now: v2/reel7.py = reel6 (v6 finish pass) + v7_parts.py. Preview5 -> ~/Downloads/CHASE_009_Reel_v4_preview5.mp4.
51. PRICE/TERMS/TIMING chips (s4 tag_chip) blue -> GOLD with NAVY text. User: "this will be the final revision". Final 1080p render of reel7.py -> ~/Downloads/CHASE_009_Reel_v4.mp4 (out4, SUB 10 / FAST 16, shutter 270, render_full.sh encode settings).

## Round 8 (2026-11-15): redo the 12 s document scene after RAY_TH_APRIL_005 (Dropbox, scene 1.67-4.25 s)
Ref (all 62 frames read, ~/chase-009-build/refs5/ray005): top-down warm wood desk + blind light, black clipboard + pen, top page peels and flies up-left curled, sheet writes on line by line, fast pull-back with defocus revealing props, offset khaki tag boxes ("Community Call").
Built: v2/v8_parts.py -> reel8.py (sc_paper5 replaces sc_paper4; wood = ~/textures/Texturelabs_Wood_266L.jpg graded dark; labels gold boxes navy type replace captions 11.30-14.05; pull-back 2.1 s USER with defocus). Scene-only preview: FRANGE=264,344 OUTD=... -> ~/Downloads/CHASE_009_document_scene_preview.mp4. User asked for scene-only preview first.
Round 8b (user liked the doc scene): labels now ride the camera (world space), clipboard + pen float in slow 3D tilt with moving shadows, wood desaturated (0.62). Build: v9_parts.py -> reel9.py (sc_paper6). Scene preview2 -> ~/Downloads/CHASE_009_document_scene_preview2.mp4. Next after approval: full final render from reel9.py.

## Round 9 (2026-11-15): intro redone after pin.it/3tCnanAx5 (first second)
Doc scene approved ("yes thats good"). Intro ref (refs5/pin_intro, frames 0-47 read): starts on paper grain blurred, slides onto a printed photo, one long smooth pull-back with dutch tilt revealing a grey newspaper page (line-screen photo, columns, window shadow, vignette), serif headline types on, red marker circle + underline.
Built v10_parts.py -> reel10.py (sc_hook10): newspaper page with photos 02 / 19 / 13 printed, kicker "AT SOME POINT," + Playfair headline typed on in navy, gold marker loop around "competition" and swash under "partner." (marker never on Chase). Intro-only preview -> ~/Downloads/CHASE_009_intro_preview.mp4.
Intro approved with one change: marker loop around "competition" -> red (196,22,38), thicker (12), like the ref (user exception to the 2-colour rule; "partner." swash stays gold). Intro done. User: don't render, include in final, wait for next revisions. Current build = reel10.py.

## Round 10 (2026-11-15): club (4.8 s), rivals (16 s), career (19 s) redone from style refs
Refs studied (every frame): pin.it/1wNrZYmUe (sty1: cutouts in solid circles, connector lines + travelling dots, label wipes, frame draw + pull-back), pin.it/1fNEe5PXB (sty2: B&W cutouts on mint grid paper, 3D grid wall, translucent circle+bar shape, bold words assembling, slow push), pin.it/74tYGXxjE (sty3: dot grows to disc, window-light shadows, grid paper, ellipse marker); images: Valere brain graph (halftone engraved cutout + HUD callouts), Tredence (concentric circles, UI pills with chevrons, grain), Brain drain (pixel squares), Extensoes (centre circles + curved connectors to dark tiles). Saved in ~/chase-009-build/refs5/sty1..3.
"Dossier" style built in v11_parts.py -> reel11.py: grid paper + window light, real people from Chase's photos as halftone cutouts (masks in v4/assets/masks16), gold discs, navy/gold/blue palette, sty2 word assembly, img23 HUD. Club = 12 broker faces on a ring -> 4 gold stay; rivals = Chase (02) vs broker (24 left, mirrored) on ground line, deal tiles; career = Chase profile (03) with years dial + callout 1 -> 20+ YEARS. Preview (scenes only) -> ~/Downloads/CHASE_009_new_scenes_preview.mp4.
Round 10b: Chase cutout slides in from the left into the career scene; designed transitions (v12_parts.py -> reel12.py): 4.80 iris from centre, 8.02 iris out of the client's gold disc, 16.07 paper push up, 18.95 pan push left->right with Chase parallax, 20.92 iris out of the years dial (gold ring edge). Push-ins stronger (club 0.18, rivals 0.15, career 0.15), same speed. Preview -> ~/Downloads/CHASE_009_new_scenes_preview2.mp4.
Round 10c: club -> Chase iris now waits for the club animation (club extends to 8.30), fast 0.34 s iris (v13_parts.py -> reel13.py). User approved everything else; final 1080p render -> ~/Downloads/CHASE_009_Reel_v5.mp4 (out13).
Bug found during final: v8 doc scene redefined global PW/PH (phone size) -> phone crashed. Renamed doc vars to DPW/DPH in reel13.py, v8_parts.py, v9_parts.py. Lesson: prefix new globals per scene.
