# Dime Motion trailer (Jenny Nguyen / The Sports Bra): frame study, part A
Frames 0-935 (0.00-31.17 s), 30 fps. The source is 960x540. **Every position and size below is converted to a 1920x1080 frame** (960 measurements x2) unless marked "(960)".
Measurements come from per-frame pixel analysis (bbox / ORB+SIFT camera solves / row profiles) of a full-res 960x540 re-extraction, plus visual checks of all 26 contact sheets (00-25) and zoom crops.
Reference stills: `refs/zoom_dmA/fNNNN.jpg` (full 960x540 frames). Analysis crops: `refs/zoom_dmA/ana_*.jpg` (legend at the end).

Transcript note: `dime_words.json` **misses "Tell me about that night"** (29.92-30.74 s) and mis-times "I remember". A re-run of Whisper medium.en on 28.3-31.3 s gives: You're 28.30, watching 28.90, that 29.20, game 29.50, **Tell 29.92 (f898), me 30.02 (f901), about 30.18 (f905), that 30.36 (f911), night 30.54 (f916)**, I 30.86 (f926), remember 30.90 (f927).

---------------------------------------------------------------------------------------------------

## 0. Global look (applies to the whole part)

| Item | Value |
|---|---|
| Speaker footage | Blue studio set: saturated blue seamless backdrop (RGB ≈ 29,72,140 in CUs; brighter 40,110,220 at the frame sides of wides), a grey acoustic-foam wall panel with rounded corners behind the two chairs, two hanging mics, white plinth tables. Interviewer wears a navy blazer and white shirt; Jenny wears a mustard "Sports Bra" sweatshirt. |
| Graphic ground | Pure white (255,255,255, clipped), with a ghost texture under 2 % luminance (only visible when contrast-boosted, see ana_ghost.jpg) plus sparse white/dark dust specks. |
| Type families | (1) **Heavy grotesk**: Bold/Black, tight negative tracking, single-storey "g", double-storey "a". Used for hero words and numbers. (2) The **same grotesk in Regular/Light** for connector words. (3) **Editorial serif italic** (SemiBold, ball terminals) for one emphasis word per phrase. (4) **Condensed all-caps** (Bebas-style) for the name title only. (5) **Thin handwriting** for the graph axis labels only. |
| Type colours | White 255; brand blue 50,107,185 (#326BB9) for "founder"/"Insane"; deeper blue 29,92,178 (#1D5CB2) for the "3000" core; bar blue 14,126,215 (#0E7ED7); dark grey 89,89,92 (#59595C) for dark-on-white words ("Revenue", "Sports Bra", "that's"). |
| Mixed-type rule | Almost every phrase is **heavy sans + regular sans + one italic serif word**. Examples: "it *was* like the", "graph / went from / *this*", "you / *brought* / in like", "I / had / no / *Idea*", "I'm *talking* to", "*the* / founder", "A *sports* / Bar", "that only / *plays*", "You / *are* / watching", "tell *me* / about", "*that* / night", "I *remember*". |
| Word build | Words appear one at a time, close to the voice (0-10 f late; sometimes 3-5 f early). Each word fades 0→100 % in 2-4 f, with a slight upward settle (≈10-16 px) and a little blur. Long hero words type on **letter by letter** at about one letter per 1-3 f ("Revenue", "million", "founder", "people", "Sports Bra", "that's Insane"). Words reveal **in place**: the whole phrase is laid out first and never re-centres. |
| Finish | Light grain (high-pass std ≈ 0.5-0.7 on flat areas); a dust/speck overlay (white specks) on graphic scenes; natural studio falloff with corners 30-45 % darker than centre; heavy motion blur on every whip; lens blur used as a design tool (defocus behind text, foreground layer defocus). Film-gate/VHS overlays only on the archival-style B-roll. |
| Camera language | Nearly every speaker shot **enters with a fast zoom-OUT on a strong ease-out**: 40-60 % of the move happens in the first 4-6 frames and it settles in 15-35 f. One shot ("I had no idea") is a fast push-IN instead. Text layers are parented to the footage and shrink with the zoom. |
| Transitions | Hard cuts on the speaker shots. Graphic scenes use: white band matte wipe; whip-left (ease-in exit / ease-out entry) with a blue "speed-tail" bar; a 2.5D parallax truck; card-shrink; light-leak burn to white; VHS glitch. |

---------------------------------------------------------------------------------------------------

## 1. SHOT LOG

### S1 · f0-42 (0.00-1.40 s) · Wide two-shot + "Our Grand / opening" behind the heads
- **Words**: "Our (f0) grand (f7) opening (f16), we (f25) saw (f31) about (f37)".
- **Footage**: frontal wide of the blue studio. Interviewer on the left chair, Jenny on the right; foam wall; mics. Backdrop sample at TL = 40,83,150.
- **Camera**: zoom-OUT from 125 % to 100 %, anchored at frame centre (centre drift < 1 px). f0 and f1 are identical; the move runs f1-f34. Fraction of the move complete: f2 15 %, f4 41 %, f6 58 %, f8 70 %, f10 77 %, f12 82 %, f16 90 %, f20 96 %, f24 98.5 %, f34 100 %. That is a strong expo ease-out with no overshoot. Motion blur shows on f2-f6.
- **Text 1, "Our Grand"**: heavy grotesk, white, Title case, one line, centred. Settled at x 430-1506, y 398-526 (cap height ≈ 128 px, font ≈ 175 px). **Entry f3-f14 is a pixelate + blur + fade reveal** (ana_o7): at f5 the letters are made of ~12-16 px square blocks at ~30 % opacity; at f8 they are still blocky and blurred; f11 is nearly sharp; f13-14 is sharp. The text is parented to the zoom: it shrinks 3 % from f13 (x 412-1522) to f24 (x 430-1506).
- **Text sits BEHIND both people** (roto cut-outs): the interviewer's head covers the "O" and Jenny's head covers the "n" of "Grand", so it reads "Cur Grar d" (ana_o1).
- **Text 2, "opening"**: same grotesk in Regular, white, lowercase, x 812-1342, y 606-716 (x-height ≈ 70 px). It is offset right of the "Our Grand" centre (its centre x = 1077 vs 968). It fades/blur-rises in f15-f22 and sits **in front of** Jenny's arm and torso.
- **Transition out: "white line → band matte" wipe (f25-f43)**
  - f25-26: a 2-4 px white horizontal line draws across the full width at y 538-540, exactly on the "Our Grand" baseline (the line is invisible over the white letters).
  - f28-f43: the line thickens symmetrically around y 540 with an accelerating (ease-in/expo) curve. Band height in px: f28 4, f29 8, f30 16, f31 24, f32 32, f33 44, f34 60, f35 80, f36 102, f37 130, f39 176, f40 308, f41 528, f42 1012, f43 1080 (full).
  - **The band is a matte window onto the next scene** (white ground + blue number), not a flat white shape. Inside it the blue "3" is visible from f35, "30" from f38, and "30" fills the band by f41.
  - The old shot and its text stay untouched outside the band until they are covered. 15 frames from line to full frame.

### S2 · f43-~100 (1.43-3.33 s) · White ground, "3000" counter, the door opens, "people"
- **Words**: "3 (f43) ,000 (f51) people (f61) come (f69) through (f77) the (f83) door (f86)".
- **Ground**: white (255) with a faint ghost texture (ana_ghost).
- **Number**: heavy grotesk digits, slightly extended, blue (core 29,92,178; lit 52,107,184). Cap height 250 px (y 424-674).
  - Digits are added as the voice says them: "3" (inside the band, f35) → "30" (f38) → "300" (f43-50, x 518-1148) → "3000" (f51, x 510-1378).
  - The number does not count up through values; zeros are appended. It is left-anchored at x ≈ 512, so each digit is appended to the right.
  - A **glossy specular sweep** (a lighter diagonal streak) crosses the digits on f45-f55 (visible on the last "0" at f50 and f53).
- **Door build (f52-f82)**:
  - f52-f58: a thin (2-3 px) grey-blue vertical line draws **top→bottom** at x 1394, the door's free edge (y 0→370 at f53, →734 at f56, full height at f58).
  - f58-f60: the door becomes a full-height white panel x 514-1384 with "3000" printed on it.
  - f60-f82: the leaf **swings open in 3D (Y-rotation)**, hinged on its left edge at x 576. The opening frame is x 576-1310, y 34-1044 (734x1010). Free-edge x at y=800: f58 1362, f60 1328, f62 1254, f64 1198, f66 1140, f68 1088, f70 1048, f72 1018, f74 996, f76 980, f78 970, f80 962, f82 960. That is an ease-out over 24 f to ≈ 60°.
  - "3000" stays printed on the leaf and foreshortens with it: the last digit squeezes and the right edge goes 1378 → 1244.
  - Behind the door is a pale blue-grey gradient room (top ≈ 225,230,240 to bottom ≈ 150,160,185) with **grey-gradient silhouettes of 4 men in suits** walking toward camera. They are darker at the top and fade to light at the feet.
- **"people"**: the grotesk in Light, white, sitting on the dark silhouettes right of "3000" (x ≈ 972-1248, y ≈ 500-590, x-height ≈ 50 px). It types on letter by letter, each letter fading in: p f72, pe f74, peo f76, peop f78, peopl f82, people f88 (≈ 2.7 f per letter).
- **Exit (f88-f103), whip LEFT with ease-in and heavy horizontal motion blur**: the door graphic's left edge goes 572 (f88) → 562 → 542 → 508 → 454 → 360 (f98) → 170 (f100) → 0 (f102), and it is gone by f104. Motion blur is about 40-80 px on f96-f103.

### S3 · f100-160 (3.33-5.33 s) · Jenny cut-out + restaurant photo card → parallax truck to "that's Insane"
- **Words**: "for (f92) a (f98) 40 (f101) -seat (f109) restaurant (f116) that's (f130) insane (f142)".
- **Layers, back to front**: white ground → restaurant photo card (left) → caption "For 40 Seats / Restaurant" → **Jenny roto cut-out** with a sticker outline.
- **Jenny cut-out**: interview footage of Jenny (mustard sweatshirt, chair) cut out with an **≈20 px light ice-blue outline stroke (≈218,230,245)** with a soft edge. Entry f100-f125 is a **rise from below plus scale-down, ease-out**: hair-top y goes 1074 (f100) → 940 → 726 → 528 (f106) → 396 → 310 (f110) → ~260 → ~190 → ~140 → ~84 (f125). Scale goes ≈1.20 → 1.00 (camera solve: 1 → 0.836 over f104-f128) with a 62 px leftward drift. Motion blur shows on f100-f108.
- **Restaurant card** (real photo of the bar interior, packed tables, framed jerseys and flags; literal for "40-seat restaurant"):
  - Size: x 92 to a right edge hidden behind Jenny's head (≈ 1200-1280), y 80-982. Square corners, no shadow.
  - Entry f103-f112 is a **left-anchored horizontal wipe/expand**: the right edge grows from x 0 to ≈ 600 with heavy motion blur on the leading edge, ease-out.
  - Slow leftward drift after landing (left edge 92 → 20 by f140).
- **Caption**, bottom-left inside the card, left-aligned at x 84-86:
  - "For 40 Seats": Regular, white, y 712-782 (cap ≈ 70 px). Words appear For (f110-112), 40 (f118-120), Seats (f125). Each fades in over 2-3 f.
  - "Restaurant": Bold/Black, white, y 810-944 (cap ≈ 110 px). It appears at f130-132 (1-2 f pop-fade). Its tail "nt" overlaps Jenny's outline and sits in front of it (ana_o2).
- **Transition (f133-f155): 2.5D parallax truck right + defocus on the foreground**
  - Whole-frame solve: content moves left 546 px total. Per-frame speed (px/f, 1920): 2, 3, 4, 5, 6, 8, 10, 12, 15, 19, 26, 37, 49, **80, 90** (f146-147 peak), 46, 28, 18, 11, 8, 4, 1 (f154). That is a slow 13-frame ease-in and a fast 7-frame ease-out.
  - Parallax differs per layer between f143 and f149 (960 measures ×2): card and "Restaurant" move ≈ 540 px, **Jenny moves ≈ 500 px but scales up ×1.4 and goes out of focus** (lens blur ≈ 10-15 px), and the headline moves ≈ 280 px. The camera trucks right and pushes forward past Jenny, who becomes a blurred foreground layer.
  - Heavy motion blur on f144-f149 (ana_o6).
- **Landing (f150-160)**: Jenny is a soft, blurred foreground on the left (sweater fills x 0-1100).
  - **"that's"**: dark grey 89,89,94, heavy grotesk, lowercase, x 1316-1564, y 344-410.
  - **"Insane"**: blue 52,107,184, heavy grotesk, Title case, x 932-1762, y 378-584 (cap ≈ 200 px). Its left edge **sits behind Jenny's blurred shoulder** (the "I" is cut by her, ana_o5).
  - Both words were already typing on at the right edge during the truck: "tha" at f140, "Ins"/"that" f143, "Insa"/"that'" f149, "Insane"/"that's" f155.
  - Hold f155-160 (static).
- **Out**: hard cut at f161.

### S4 · f161-185 (5.37-6.17 s) · Interviewer MCU + "overwhelming"
- **Words**: "Overwhelming." (f167-179).
- **Footage**: interviewer MCU, blue backdrop on the left, foam wall on the right.
- **Camera**: zoom-OUT from 146 % to 100 % on a hard ease-out. Per-frame scale change: −7.8 %, −4.6 % (f164), −3.2 %, −1.7 % (f168), −1.35 %, −0.54 % (f172), then about −0.3 %/f to f184. Overall 1 → 0.683, with motion blur on f161-166.
- **Text**: "overwhelming", heavy grotesk, white, lowercase, one line, x 216-1756, y 516-726 (x-height ≈ 140 px, ascender-to-descender 210 px). It crosses the interviewer's chest **in front of him**.
  - Entry f164-f172 is a **blur-in**: f164 ≈ 30 % opacity with ~20 px blur, f166 ~50 %, f168 ~70 % with ~12 px blur, f172 sharp.
  - It keeps shrinking with the zoom (x 210-1766 at f172 → 238-1730 at f184).
- **Out**: hard cut at f186.

### S5 · f186-260 (6.20-8.67 s) · Jenny CU, "it was like the" over defocus → graph drawn on her hand gesture
- **Words**: "It (f188) was (f189) like (f192) the (f197) graph (f202) went (f208) from (f214) this (f221) to (f230) this (f244)."
- **Footage**: Jenny CU, blue seamless backdrop. Her hand makes a flat horizontal gesture ("this"), then a vertical one ("to this").
- **Defocus for readability**:
  - f186-f200: the footage is **heavily lens-blurred** (face Laplacian variance 0.2-0.4 vs 4.0 when sharp) while "it was like the" is on screen.
  - f200-f212: it **racks to sharp** (0.4 → 0.8 → 2.0 → 3.3 → 4.0) exactly as the sentence fades and the graph starts (ana_c23).
- **Sentence 1, "it *was* like the"**: one centred line, x 532-1384, y 472-584. "it", "like", "the" are grotesk Medium, white; "*was*" is the serif italic SemiBold.
  - Words appear in place: it (f187-189), was (f191-193), like (f195-197), the (f199-201). Each fades in over 2-3 f with a slight rise and blur.
  - It sits over her chin/mouth, which is blurred at this point. Exit f209-f211 is a fade plus slight blur, in place.
- **Blueprint grid overlay**: a square grid of thin light lines at low opacity (≈10-15 %), 144 px spacing. It fades in over f209-f213 and covers the full frame (ana_hp).
  - It is parented to the footage: spacing shrinks 144 → 138 px as the shot drifts out f212-245.
- **Camera**: punch-IN of +10.4 % in 5 f at f211-f216 (+1.7, +2.8, +2.5, +1.3, +1.7 %/f), then a slow drift back to about +6 % by f240 (−0.1 to −0.2 %/f), with a 40 px upward tilt over f216-226.
- **Line graph drawn over the gesture**:
  - A **white, ≈16 px, round-capped stroke** draws on from the bottom-left corner, starting at f209 and following under her flat hand: a gently rising, slightly wobbly line ending near x 980, y 760 at f230.
  - At f246-f252, when her hand turns vertical, the line continues and **shoots straight up** to the top edge at x ≈ 1300.
  - Measured f252 path (1920): (60,1080) → (420,880) → (720,780) → (980,710) → (1080,760) dip → (1180,680) → (1300,0).
  - Axes are drawn as thin 2-3 px white lines:
    - **Vertical axis** at x ≈ 190, y 330-980, drawing down over f228-240.
    - **"Growth" label**: thin white handwriting, top-left at x 70-350, y 200-290. It types on letter by letter f228-243: "Gro" at f230, "Growth" at f243.
    - **Horizontal-axis tick** at x ≈ 1350-1490, y 980, plus a **"Time"** label (handwriting) at x 1530-1710, y 930-1000. Both appear f236-244.
- **Sentence 2, right-aligned stack on the right side** (its right edge ≈ 1720-1750):
  - "graph": heavy grotesk, lowercase, white, x 1052-1720, y 398-618 (x-height ≈ 150 px). It enters f212-215 with a fade from ~40 % and a slight slide.
  - "went from": Regular, white, x 1230-1750, y 630-720, appearing word by word f212-218.
  - "*this*": serif italic, white, under it at x 1580-1750, y 720-800, appearing f218-222.
  - Exit ≈ f245-246 (cut-out with a quick fade).
- **Sentence 3, "to *this.*"**: right side at x 1260-1710, y 510-650. "to" is Regular sans and "*this.*" is serif italic Bold. It enters f246-250 as the line spikes.
- **Out**: hard cut at f261.

### S6 · f261-329 (8.70-10.97 s) · High-angle wide + vertical word stack + "8 Months" behind the mic + "you brought in like"
- **Words**: "I (f263) think (f266) in (f269) the (f272) first (f277) eight (f285) months (f296), you (f309) brought (f314) in (f322) like (f328)".
- **Footage**: high angle looking down on the set. Interviewer on the left, Jenny on the right with her back partly to camera, and the foam wall filling the right half.
- **Camera**: zoom-OUT from 142 % to 100 % (overall 1 → 0.705), ease-out with a long tail. Per-frame scale change: −2.8 %/f at f262-266, −1.6 % at f269, −0.8 % at f275, −0.4 % at f281, −0.2 % at f290, then about −0.1 %/f to the end. 50 % of the move is done by ≈ f268.
- **Stack 1**: five lines, left-aligned at x 194-202, white, ~14 px line gaps. Words appear one per line, each fading in over 3-4 f:
  - "I" y 216-330, at f282
  - "think" y 346-460, w 378, at f275-277
  - "in" y 474-586, at f278-280
  - "the" y 604-720, at f282-284
  - "**first**" y 732-904, heavy grotesk, at f288-290
  - Regular weight for every line except "first" (Black, about 1.5× the size).
  - The stack spans y 216-904 on the left third, beside the interviewer and not over him. It cuts out at f295-296 (1-2 f fade).
- **"8 Months"** (f298-f313):
  - **"8"**: heavy grotesk, white, x 754-1026, y 260-588 (328 px tall). It pops in over f298-f302 (4 f fade/scale).
  - It sits **BEHIND the hanging microphone**: the mic head and cable are rotoscoped in front of the top of the "8" (ana_c7, f0305.jpg).
  - **"Months"**: Regular, light grey/white ≈ 85 % opacity, x 1000-1574, y 280-394, top-aligned with the "8". It is revealed by a **left→right wipe** over f300-f308.
  - Both shrink with the zoom-out. They cut out at f313-314.
- **Stack 2, "you / *brought* / in like"**: centred-left over the interviewer, in front of him, spanning x 164-774, y 388-726.
  - "you": Regular, y 388-480. "*brought*": serif italic, larger, y 490-610. "in like": Regular, y 620-726.
  - Timing: you f315-318, brought f317-318, in f319-322, like f324-326.
- **Out**: hard cut at f330.

### S7 · f330-383 (11.00-12.77 s) · Frontal wide → **card-shrink** with zoom-in inside → "million / *dollars*" → whip-left with blue speed-tail → "Revenue" + money photo card
- **Words**: "a (f334) million (f341) dollars (f352) in (f363) revenue (f370)".
- **Zoom-out entry** (f330-337): 117 % → 100 % (−4.7, −3.8, −2.4, −1.9, −1.4, −1.0, −0.3 %/f).
- **Card shrink** (f340-f354): the footage frame shrinks from full frame to a **1520x750 card** with square corners, no border and no shadow, on the white ground. Ease-out:
  - f342 x 0-1918, y 0-1070
  - f344 x 30-1888, y 62-1018
  - f346 x 112-1820, y 98-962
  - f348 x 148-1774, y 128-938
  - f350 x 178-1746, y 144-926
  - f352 x 192-1726, y 154-916
  - f354 x 202-1722, y 160-910 (≈14 f)
- Meanwhile the footage **inside the card zooms IN** (camera solve f337→f353: ×1.307, plus 126 px of upward reframing). The people stay roughly the same size while the frame closes around them.
- **"million"**: heavy grotesk, white, lowercase, x ≈ 430-1380, y ≈ 570-780. It types on **letter by letter**: "mil" f344, "millio" f353, "million" f358. It sits over the two people, in front of them.
- **"*dollars*"**: serif italic, white. It starts semi-transparent (f344 ≈ 50 %) and becomes opaque. It sits at x ≈ 820-1380, y ≈ 780-900 and is **clipped by the card's bottom edge** (the text is masked inside the card).
- **Whip exit LEFT** (f354-f368): the card accelerates out to the left with ease-in (expo). Per-frame dx (px, 1920): 1, 5, 8, 12, 18, 24, 31, 41, 53, 71, 97, 139, 222, 374. Motion blur appears from f360.
- **Blue speed-tail bar A**: a 66 px tall blue bar (14,126,215) grows out of the card's **right edge** at y 742-812 as it accelerates.
  - Length grows with speed: 16 px (f360) → 266 (f363) → 538 (f366) → 638 (f368) → 680 (f369).
  - After the card exits, it retracts to a stub at the left edge: x 0-416 (f372) → 0-256 (f376) → 0-200 (f380) → 0-196 (f383). It ends tucked behind the money card.
- **Landing layout (f369-f383)**: the whole layout slides in from the right with ease-out, continuing the whip's momentum. "Revenue" left edge: 690 (f369), 380 (f372), 242 (f376), 210 (f378), 198 (f380), 196 (f383).
  - **"Revenue"**: dark grey 89,89,92, heavy grotesk, Title case, x 196-~956, y 274-412 (cap ≈ 138 px). It types on letter by letter, left-anchored: R f369, Re f370, Reve f372, Revenu f374, Revenue f378.
  - **Blue bar B**: 38 px tall at y 374-412, baseline-aligned with "Revenue". It enters from the right edge (x 1760-1920 at f372 → 1226-1780 at f376 → 1050-1736 at f383) and ends with its right edge aligned to the money card's right edge.
  - **Money photo card**: real photo of scattered $100/$500 bills, desaturated with a dark vignette inside the photo. Final position x 200-1728 (1528 wide), top edge y 430, running off the bottom of frame; square corners, no shadow.
  - It rises from below with ease-out (top edge y: 970 f371, 764 f372, 660, 594, 548, 512, 488, 470, 456, 448, 440, 438, 436 f383) and drifts left at the same time (left edge 550 → 200).
  - The card's left edge is aligned with the "Revenue" left edge (one left column at x ≈ 196-200).
- **Out**: hard cut at f384.

### S8 · f384-412 (12.80-13.73 s) · Jenny CU push-in + "I / had / no / *Idea*"
- **Words**: "I (f385) had (f388) no (f393) idea (f400)".
- **Footage**: Jenny CU on the blue backdrop (29,72,140; the left edge is brighter at 76 luminance and the bottom-left darker at 59).
- **Camera**: the only push-IN entry in this part. Scale 1.000 (f384-385) → 1.055 (f387) → 1.155 (f389) → 1.205 (f391) → 1.222 (f393) → 1.229 (f395), then a second small push to 1.274 (f401) and a hold. Net about +27 %, ease-in-out with a quick middle, and about +40 px rightward re-centring.
- **Text**: left-aligned at x 284 on the left third; Jenny's face is at about x 900-1400.
  - "I" y 254-390, appears f396
  - "had" y 414-554 (w 320), appears f398-400
  - "no" y 586-692, appears f402-404
  - These three are the grotesk Regular, white, with a slight transparency on entry.
  - "*Idea*": serif italic, white, larger, x 298-764, y 700-882 (≈ 180 px). It appears f406-408 and overlaps her shoulder, in front.
- **Out**: hard cut at f413.

### S9 · f413-450 (13.77-15.00 s) · Dark BTS silhouettes + "Today" → "I'm *talking* to"
- **Words**: "Today (f423), I'm (f431) talking (f437) to (f446)".
- **Footage**: behind-the-scenes of the studio, nearly black. Crew silhouettes (camera operator on a tripod, a man in a suit) against the lit blue set, mean RGB ≈ 25,33,55.
- **Camera**: zoom-OUT from 140 % to 100 %, ease-out (−11.2 %/f on the first frame, then −3.9, −2.2, −1.4, −0.7, −0.2), settling by f424. After that there is a slight drift.
- **"Today"**: grotesk Medium/SemiBold, white, centred, x 760-1154, y 474-606 when settled (f422).
  - Entry f414-f417: from about 25 px lower, about 10 % larger and vertically motion-blurred → settles sharp (ease-out, 3-4 f). Exit is a **hard 1-frame cut-out at f425**.
- **"I'm *talking* to"**: one centred line, x 568-1352, y 472-616. "I'm" and "to" are grotesk Medium; "*talking*" is serif italic SemiBold.
  - Words appear in place: I'm f426-430, talking f434-437, to f441-444. Each fades in over 3-4 f with a slight blur and a 10-15 px rise.
- **Out**: hard cut at f451 (f451 alone carries a cool/desaturated one-frame blend).

### S10 · f451-478 (15.03-15.93 s) · Jenny in her bar + glitch-on name "JENNY NGUYEN"
- **Words**: "Jenny (f456) Nguyen (f463)".
- **Footage**: locked-off wide of Jenny seated on a stool inside The Sports Bra (bar shelving, bar stools, warm wood floor), warm grade. **VHS scan-line texture** over the image, and the highlights shift magenta/pink on f456-f464.
- **Camera**: slow push-IN of 100 → 107 % over 27 f (≈ +0.25 %/f, near-linear).
- **Title**: "JENNY NGUYEN", **condensed all-caps** (Bebas-like), white, one line, centred over Jenny's torso and in front of her: x 290-1610, y 428-648 (cap 220 px).
  - Letters **flicker on in random order** (ana_c25): f451 "G"; f452 "J"; f454 "J G"; f455 "GU"; f456 "J NG N"; f457 "J N NGU N"; f458 "J NN NGU EN"; f459 "JENN NGU EN"; f460 "JENN NGUYEN"; f462 "J ENNY NGUYEN"; f464 complete.
  - During the flicker the letters carry a **pink/magenta glow + RGB split** (glow ≈ 246,178,250), which settles to clean white with a faint pink edge by f470.
- **Out**: hard cut at f479.

### S11 · f479-516 (15.97-17.20 s) · Portrait photo card (card shrink) + "*the* / founder" + period that becomes the bar
- **Words**: "the (f481) founder (f481-490) of (f490) the (f503) sports (f509)".
- **Asset**: professional studio portraits of Jenny (mustard sweatshirt, light-blue gradient backdrop), on white ground.
- **Card shrink** (f479-f492), ease-out, full height to inset:
  - f479 x 392-1530, full height
  - f481 x 408-1514
  - f483 x 494-1428, y 24-1044
  - f485 x 542-1380, y 46-1024
  - f487 x 566-1356, y 56-1014
  - f489 x 580-1342, y 62-1008
  - f492 x 590-1332, y 66-1004
  - Final ≈ 740x936, square corners, no border, no shadow.
- **Photo swap inside the card**: f479-f488 is a tight face crop (chin to forehead); **f489 cuts to a wider photo from the same shoot** (head to waist, hands clasped). The card stays put across the swap.
- **"founder"**: brand blue 50,107,185, heavy grotesk, lowercase, x 342-1564 at f500, y 530-776 (x-height ≈ 150 px), across the lower half of the card and spilling well beyond it on both sides onto white.
  - Types on letter by letter: fou f479, foun f481, found f484, founde f487, founder f492.
  - A **specular gloss sweep** runs across "un/de" on f487-f492 (ana_o4).
  - It is opaque over the photo; on f505-513 the necklace dog-tag shows over the "n".
- **"*the*"**: serif italic, white, about 1/2 the size of "founder", over the sweater above the "n-d" (x ≈ 900-1142, y ≈ 434-584). It fades in f483-487.
- **Period → bar**: a blue square "." (x 1554-1616, y 704-770, 62x66) appears at f505-509 after the "r".
- **Exit (f505-f516), whip LEFT with ease-in**: card left edge 578 (f505) → 492 (f509) → 452 → 400 → 328 → 232 → 92 (f514) → gone (f515).
  - The **period stretches into a horizontal bar** as it moves: x 1460-1578 at f511, 1294-1484 at f513, 554-900 at f516, 182-590 at f517. It hits the left edge at f518.

### S12 · f516-548 (17.20-18.27 s) · "Sports / Bra" + storefront photo (stacked photos) → light-leak burn to white
- **Words**: "sports (f509) bra (f521)." then "A (f540) Portland (f546)".
- **Blue bar (carried over)**: 66 px tall at y 704-770. It first retracts into the left edge (right end 440 at f518, 378 at f519, 366 at f520), then **extends right** with ease-out to underline the title (430 f522 → 562 f524 → 706 f526 → 770 f528). It ends at x 0-764, right edge aligned with the text.
- **Photo**: portrait-orientation photo of Jenny on a green picnic table in front of "The Sports Bra" storefront window. This is literal: the business's own sign.
  - Entry from the right with ease-out. Left edge: 1594 (f517), 1372 (f518), 1228 (f519), 1136 (f520), 1010 (f522), 886 (f524), 844 (f526), 824 (f528), 818-834 (f530).
  - Size 642 x 942 (x 834-1476, y 84-1026).
  - A **second photo from the same shoot is stacked behind it**, offset ≈ +84 px right and −30 px up (stack extends to x 1560, y 54). The pair reads as a small photo pile. Square corners, no shadow.
- **"Sports / Bra"**: dark grey 89,89,92, heavy grotesk, two lines, **right-aligned at x ≈ 772**, about 50 px left of the photo edge.
  - "Sports" spans x 176-772, y 266-400; "Bra" spans x 454-772, y 400-568.
  - Types on letter by letter: S f517, Spo f519, Sport f521, Sports Br f524, Sports Bra f526. During the type-on the block slides left with the photo (ease-out). It ends at f528.
- **Light-leak burn to white (f540-f548)**:
  - f540: frame +3 % brighter.
  - f541: the text turns a peach→salmon gradient, the bar fades from its left end (left transparent, right blue), and the photo picks up a magenta cast.
  - f542-543: the text goes peach/yellow, the bar shrinks to a fading right-end stub, and the photo becomes warm magenta.
  - f544-546: the text becomes yellow-white and nearly invisible, and the photo blows out yellow-white from the bottom-left.
  - **f547-548: pure white (255).** f549: hard cut.
  - Mean luminance per frame: 193 (f539), 196, 205, 211, 217, 223, 227, 232 (f546), 254, 255.

### S13 · f549-584 (18.30-19.47 s) · Archival film-gate footage 1: Jenny at the Sports Bra window
- **Words**: "Portland (f546), Oregon (f560) establishment (f568)". **No on-screen text.**
- **Footage**: Jenny walks past and then stands in front of the "The Sports Bra" window, giving a double thumbs-up; green picnic tables.
- **Film-gate treatment**: Super-8 look. A black frame border on the left (x 0-230) and right (x 1690-1920) with gate weave; heavy grain, dust, scratches and hair specks; lifted, warm, faded colour with exposure flicker (f553 warm orange flash on the edges). Full height.

### S14 · f585-619 (19.50-20.63 s) · Archival film-gate footage 2: bar interior → orange leak → white
- **Words**: "that's (f589) the (f609) first (f613)". **No text.**
- **Footage**: the bar interior at night (counter, staff, customers), and two women talking (f604+). The camera drifts in.
- **Film-gate treatment**: the image sits in a rounded-corner film frame (x ≈ 330-1750) with dark borders. A **white-outlined sprocket hole** (rounded rectangle, ≈ 2-3 px line) sits at x 96-330, y 364-656. Heavy grain and dust.
- **Transition**: an orange light leak burns in from the left from f611 (mean RGB 87,61,67 → 154,100,95 at f612 → 226,152,144 at f615 → 225,172,142 at f617). **f618-619 pure white.** Hard cut at f620 to the white-ground collage.

### S15 · f620-666 (20.67-22.20 s) · Photo-tile mosaic building around "first of its kind."
- **Words**: "of (f628) its (f638) kind (f643)."
- **Ground**: white.
- **Tiles**: real interior and exterior photos of The Sports Bra: flags and banners, the bar wall, the counter with a blue-haired bartender, a booth with a customer, and the **storefront exterior** last. All are rectangular, square-cornered, with no border, no shadow and hard edges overlapping each other.
- **Build**: each tile **pops in on a single frame** (no slide). Pop frames show as diff spikes at f625, f631, f637, f642, f648.
  - T1 (landscape) is present at f620: x 532-1380, y 268-824 (848x556). It still carries the warm leak tint on f620-624.
  - T2 (portrait) at f625: x 642-1266, y 164-924, on top.
  - T3 (wide) at f631: x 382-1504, y 384-724.
  - T4 (tall) at f637: x ≈ 718-1218, y ≈ 100-988.
  - T5 at f642: x ≈ 300-1590, y ≈ 360-750.
  - T6 (storefront) at f648: x ≈ 270-1640, y ≈ 326-870.
  - The tiles form a **stepped, symmetric "plus/diamond" silhouette** centred near (960, 545). Total bbox grows 868x556 → 1378x1008 (x 270-1648, y 40-1048).
- **Continuous slow scale-up of the collage between pops**: +1.2 % over f631-636, +4 % over f637-641, +2.5 % over f643-647, +1.2 % over f648-666.
- **Text "first of its kind."**: heavy grotesk, white, lowercase, one line across the collage (in front), centred: x ≈ 367-1552, y ≈ 464-614 (x-height ≈ 100 px). It starts left-aligned from x ≈ 367 as it types ("firs" at f631 already starts at the final left edge).
  - Builds word by word, with the newest word typing on: "firs" f631, "first of" f633, "first of its" f637, "first of its k" f638, "first of its kind" f643, "first of its kind." f648.
  - New words land in step with the tile pops.
- **Out**: hard cut at f667.

### S16-S23 · f667-797 (22.23-26.57 s) · Fast full-frame B-roll montage with a sentence that builds across cuts
- **Words**: "A (f670) sports (f674) bar (f685) that (f696) only (f712) plays (f728) women's (f748) sports (f775)."
- **All clips are full frame**: no cards and no frames. Warm, saturated grade with grain and dust specks. The footage moves on its own (handheld, slow pans).
- **The caption persists across cuts**, and each phrase gets a new position:
  - **"A *sports* / Bar"**: lower-left, left-aligned at x 160. "A" (heavy) at x 162-298, y 660-794 appears on S16 (f670-672). "*sports*" (serif italic) is added on the same line on S17 (f685-690). "Bar" (heavy) is line 2 at y ≈ 820-960. The block spans x 160-932, y 654-960.
  - **"that only / *plays*"**: upper-left, left-aligned at x 154-160. "that" (heavy, white) at x 160-518, y 192-326 appears at f712-715. "only" is added at f720-727. "*plays*" (serif italic, white) is line 2 at y ≈ 350-520 and fades in over f727-732. The block spans x 154-920, y 190-524.
  - **"Women's Sports"**: one line, **centred**, x 330-1606, y 472-622, heavy grotesk, white.
    - "Women's" fades in on f748-753 (blurred and transparent at first) at its final left-hand position, x 330-1048.
    - "Sports" fades in on f762-766 (greyish → white, at about 60 % on f763).
- **Clip list**:

| Clip | Frames | Length | Footage | Text on screen |
|---|---|---|---|---|
| S16 | f667-676 | 10 f | burgers and fries on plates at the counter (shallow DOF) | "A" |
| S17 | f677-707 | 31 f | bartender pulling beer from a row of wooden tap handles | "A sports Bar"; footage pans, solve scale 0.91, tx +260 px |
| S18 | f708-726 | 19 f | hand lifting a pint off a wooden table | "that" → "that only" |
| S19 | f727-747 | 21 f | beers on the wood table, top-down angle | "that only plays" |
| S20 | f748-753 | 6 f | server carrying a tray of beers past a window with fairy lights | "Women's" fading in |
| S21 | f754-762 | 9 f | framed photo of a tennis player on the bar's pink wall with plants | "Women's" |
| S22 | f763-770 | 8 f | hand holding a drink in front of a TV showing soccer | "Women's Sports" ("Sports" lands) |
| S23 | f771-797 | 27 f | close-up of a **TV screen** (women's game), soft, with moiré/scan-lines and a grey wash | "Women's Sports" held |

- **Transition out of S23 (f798-f811), light-leak transition**:
  - f798-799, over the old TV shot: cyan/teal vertical light streaks left of centre, white bokeh blobs at the left edge, and a **red circular ring flare** at the right edge.
  - **f800 hard cut** to the two-shot under the leak: cyan-white on the left, magenta-pink on the right.
  - f801-807: the leak spreads pink/orange, white vertical film scratches appear, and the ND card fades in faintly underneath (f804+).
  - **f808-809 pure white.**
  - f810: a white haze clears from the left, with the ND card visible. f811: a slight pink residue at the right. f812: clean.

### S24 · f800-854 (26.67-28.47 s) · Two-shot with team-logo cards BEHIND the cut-out people: "Notre Dame VS Mississippi State"
- **Words**: "Notre (f802) Dame (f808) versus (f819) Mississippi (f829) State (f844)."
- **Footage**: frontal wide two-shot (same set as S1).
- **Camera**: slow continuous zoom-OUT, 1 → 0.908 over f812-f854. The rate decays from −0.5 %/f to −0.15 %/f, so it reads as a slow drift. **The cards are parented to the footage** (ND card 534 → 484 px wide, matching ×0.906).
- **Card 1, Notre Dame**:
  - **White rounded card**: x 300-784, y 106-694 at f845 (484x588), corner radius ≈ 50 px, no visible shadow.
  - Carries the **gold "ND" monogram** (197,160,9) at x 380-718, y 270-574.
  - It sits on the left over the foam wall and is present from f804, fading up through the leak.
- **"VS"**: heavy grotesk caps, white, x 856-1118, y 380-518 (centred between the cards).
  - Entry f812-f820 is a fade from 0 → 100 % plus a **scale-down of ≈ 10 %** (it starts larger and blurred), ease-out (ana_c17).
- **Card 2, Mississippi State**:
  - **Maroon rounded card** (148,41,97) with a **≈ 4-6 px white stroke** and corner radius ≈ 50 px, x ≈ 1122-1598, y ≈ 112-694, carrying the white/maroon "M STATE" logo.
  - Entry f821-f829: a ghost outline at about 20 % opacity with a blue tint (f821-823), then a magenta fill (f824-826), then full maroon (f828).
  - A **diagonal gloss sweep** crosses it on f829-833.
- **Layering**: **both people are rotoscoped IN FRONT of the cards**.
  - The interviewer's head and shoulders cover the bottom of the ND card.
  - Jenny's head, shoulder and arm cover the bottom-left of the State card (ana_c16 / f0845.jpg).
  - The cards cover the foam wall and backdrop.
- **Out**: hard cut at f855.

### S25 · f855-874 (28.50-29.13 s) · Interviewer CU + right-aligned "You / *are* / watching"
- **Words**: "You're (f858) watching (f866) that (f876)".
- **Footage**: interviewer CU on the left half, gesturing with his right hand; blue backdrop (23,63,135) and the foam wall on the right.
- **Camera**: almost static (−1 % over 18 f).
- **Text**: a right-aligned stack on the right half.
  - "You": grotesk Medium, white, x 1316-1594, y 282-372. It appears f860-866 as a fade plus de-blur, in place.
  - "*are*": serif italic, white ≈ 85 %, smaller, x 1340-1590, y 340-400. It appears f864-868.
  - "watching": heavy grotesk, white ≈ 80-90 % opacity, x 1124-1558, y 438-528. It appears f867-872, and its left part ("wa") crosses the interviewer's shoulder, in front of him.
- **Transition out: VHS glitch (f873-f886, 14 f)**
  - f873: two horizontal white-blue tracking bars (≈ 40-60 px tall) cross the frame at y ≈ 440 and y ≈ 140.
  - f874: the bars move, with slight noise.
  - f875: the frame floods white (≈ 80 %), the image ghosted.
  - f876-877: the white flood covers the top 5/6; the original shows only at the bottom (y > 920).
  - f878-879: white top band, then purple/pink chroma-smeared VHS bands.
  - f880: white and blue-grey bands with a dark noise strip.
  - f881: a dark blue noise band plus a light band.
  - f882: a grey static (snow) slab on a diagonal, with crowd footage peeking at the top-left.
  - f883: the crowd footage with heavy **zig-zag horizontal displacement**, a magenta/blue chroma band and a diagonal static stripe.
  - f884-885: the crowd with a strong sine-wave horizontal displacement (≈ 40 px amplitude).
  - f886: residual displacement. f887: clean.

### S26 · f887-913 (29.57-30.43 s) · Crowd footage + "tell *me* / about" (left) + "*that* / night" (right)
- **Words**: "game (f884)… Tell (f898) me (f901) about (f905) that (f911) night (f916)".
- **Footage**: archival stadium crowd (red/white fans), slightly soft, with residual scan-lines. The footage pans: content moves left about 154 px over 26 f.
- **Left block**, right-aligned at x ≈ 770-784 on the left half:
  - "tell *me*": "tell" is grotesk Medium and "*me*" is serif italic, white, x 318-760, y 542-662. Words appear f894-899.
  - "about": heavy grotesk, white, x 198-784, y 664-802. It appears f901-906.
- **Right block**, left-aligned at x 1188 on the upper right:
  - "*that*": serif italic, white, x 1188-1462, y 176-284. It appears f906-912.
  - "night": heavy grotesk, white, x 1188-1710, y 310-478. It appears f909-914.
- The two blocks form a **diagonal composition** (lower-left vs upper-right).

### S27 · f914-919 (30.47-30.63 s) · 6-frame insert: basketball collision
- Close, low-res broadcast footage (blue and white uniforms, blonde player), with scan-lines and soft focus. Both text blocks stay on screen across this cut.

### S28 · f920-935+ (30.67-31.17 s, continues into part B) · Indiana-Fever-style player dribbling on a pink court + "I *remember*"
- **Words**: "I (f926) remember (f927)".
- **Footage**: low-res broadcast of a player in a red uniform dribbling on a pink/magenta court, heavy grain and scan-lines; footage camera moves (solve tx +116 px, ty +100 px over f920-935).
- **Text exit**: "tell me about" fades and blurs out on f920-923; "that night" on f922-923.
- **"I *remember*"**: one line, left-aligned at x 334, y 532-664.
  - "I" is grotesk Regular (a plain bar shape). It appears alone at f928.
  - "*remember*" is serif italic, white. It fades in f931-935 (≈ 30 % → 90 %).

---------------------------------------------------------------------------------------------------

## 2. B-ROLL INTEGRATION (every asset in f0-935)

| # | Frames | Asset (what it shows) | Relation to the line | Integration, size, edge, entry and exit |
|---|---|---|---|---|
| 1 | f0-42 | Interview wide (main footage) | n/a | Full frame, zoom-out 125→100 %; text behind both heads (roto) |
| 2 | f43-103 | **Illustrated door + 4 grey-gradient suit silhouettes** (graphic, no photo) | **Literal**: "3,000 people come through the door" | On a white ground. Frame 734x1010 at x 576-1310; the leaf swings open in 3D (hinge left, ease-out 24 f). Exit: whip-left with ease-in and motion blur |
| 3 | f100-150 | **Jenny interview footage as a roto cut-out** with a ≈20 px ice-blue sticker outline | Speaker | Over white. Rises from below with scale 1.2→1.0, ease-out ~25 f. Becomes a blurred ×1.4 foreground during the truck |
| 4 | f103-150 | **Photo of the busy bar interior** | **Literal**: "40-seat restaurant" | Card behind the cut-out, x 92-~1260, y 80-982, square, no shadow. Entry: left-anchored wipe-expand with a blurred leading edge, ~9 f. Exit: parallax pan left |
| 5 | f161-185 | Interviewer MCU | Reaction | Full frame, zoom-out 146→100 %, text in front |
| 6 | f186-260 | Jenny CU + **hand-drawn line graph + blueprint grid** | **Literal + gesture**: "the graph went from this to this". The line follows her flat hand, then spikes when her hand goes vertical | Full frame. Defocus behind the first sentence, then rack to sharp. Grid 144 px at ~12 % opacity. A 16 px white round-cap stroke draws on. Axes 2-3 px with handwritten "Growth"/"Time" |
| 7 | f261-329 | High-angle wide | n/a | Full frame zoom-out. "8" sits **behind the hanging mic** (roto) |
| 8 | f330-368 | Frontal wide as a **card** | "a million dollars" | Full frame shrinks to a 1520x750 card in 14 f while the footage inside zooms in ×1.3. Text clipped by the card. Exit: whip-left ease-in with a blue speed-tail |
| 9 | f371-383 | **Photo of piles of $100/$500 bills** (desaturated, vignetted) | **Literal**: "revenue" | Card x 200-1728, top y 430, bleeding off the bottom. Rises from below with ease-out in ~12 f. Left edge aligned with the "Revenue" title; blue bar above right |
| 10 | f384-412 | Jenny CU | Speaker | Full frame push-in +27 %, text left of the face |
| 11 | f413-450 | **BTS silhouettes of the crew** (camera on tripod) in the dark studio | **Metaphor/intro**: "Today, I'm talking to", the host introducing the show | Full frame, zoom-out 140→100 %, centred text |
| 12 | f451-478 | **Jenny seated inside her bar** (wide) | **Literal**: name intro | Full frame with a VHS scan-line overlay and a pink highlight shift; slow push-in; name glitches on in front of her |
| 13 | f479-516 | **Studio portrait photos of Jenny** (2 framings) | **Literal**: "the founder" | Card shrink from full height to 740x936 (ease-out 13 f) with a photo swap inside at f489. Text spills beyond the card. Exit: whip-left ease-in; the period becomes a bar |
| 14 | f517-548 | **2 stacked photos: Jenny on a green picnic table at the Sports Bra window** | **Literal**: "the Sports Bra" (the sign is visible) | Photo 642x942 at x 834-1476, with a second photo offset +84/−30 behind. Slides in from the right with ease-out in 13 f. Title right-aligned beside it with a blue underline bar. Exit: light-leak burn to white |
| 15 | f549-584 | **Archival-look film footage**: Jenny in front of the Sports Bra window | "Portland, Oregon establishment" (literal place) | Full frame with a Super-8 gate (black side borders), grain, dust, flicker. No text |
| 16 | f585-619 | **Film footage of the bar interior at night** | "that's the first…" | Full frame with a rounded film gate and a white sprocket-hole outline. Exit: orange leak to white |
| 17 | f620-666 | **6 photos of the bar** (flags wall, booth, counter, bartender, storefront) | **Literal + build**: "first of its kind". The place assembles itself | Mosaic of hard-edged rectangular tiles popping in 1 frame each, overlapping into a symmetric plus/diamond silhouette, with a slow scale-up of 1-4 % between pops. Text in front |
| 18-25 | f667-797 | Burgers; tap pour; pint lift; beers on table; server tray; **framed tennis photo on the wall**; drink in front of a soccer TV; **TV screen showing a women's game** | **Literal/mood**: "a sports bar that only plays women's sports". Food/beer = "bar"; TVs and sports photos = "women's sports" | **All full frame**, hard cuts every 6-31 f. One caption sentence builds across the cuts; each phrase in a new place (lower-left, upper-left, centre) |
| 26 | f800-854 | Interview wide + **Notre Dame and Mississippi State logos as badge cards** | **Literal**: "Notre Dame versus Mississippi State" | Two 484x588 rounded cards (r ≈ 50) **behind the roto'd people**, parented to the zoom. ND card white; State card maroon with a white stroke. "VS" between them. Entry via light leak, fades and gloss sweeps |
| 27 | f855-874 | Interviewer CU | Question | Full frame, right-aligned text stack. Exit: VHS glitch |
| 28 | f887-913 | **Archival stadium crowd** | "that game / tell me about that night" | Full frame with residual scan-lines; diagonal two-block caption |
| 29 | f914-919 | **Archival basketball collision** (6 f) | "that night" | Full frame insert, captions carried over |
| 30 | f920-935 | **Archival WNBA broadcast** (player in red on a pink court) | "I remember" | Full frame, grain and scan-lines |

---------------------------------------------------------------------------------------------------

## 3. TECHNIQUES (rebuildable recipes)

1. **Text behind people (roto sandwich)**: footage plate, then title, then a roto matte of the people on top.
   - S1 "Our Grand": heads cover "O" and "n".
   - S6 "8": the hanging mic is in front.
   - S24 logo cards: both people in front.
   - S3 "Insane": the blurred Jenny in front of the "I".
   - Secondary words stay IN FRONT ("opening", "Restaurant", "you brought…"), so only one hero element per shot goes behind.

2. **Zoom-out entry on every speaker cut**:
   - Start scale ~117-146 % (S1 125, S4 146, S6 142, S7 117, S9 140) and land at 100 %, anchored at centre.
   - Expo ease-out: 15 % done by frame 1, 40 % by frame 3, 60 % by frame 5, 80 % by frame 10, 95 % by frame ~18.
   - Real motion blur on the first 3-6 f.
   - Text layers are parented to the footage, so they shrink 2-4 % along with it.

3. **Push-in variant**: S8 goes 100 → 122 % in 9 f (peak +4 %/f at frame 3-5), then a second +4 % nudge 6 f later. S5 punch-in: +10.4 % in 5 f, then a slow −4 % drift over 25 f.

4. **Pixelate-blur reveal for the opening title** (S1): a mosaic block size of ~16 px down to 1 px, plus a Gaussian blur of ~12 px down to 0, plus opacity 0 → 100 %, over 10-11 f (f3-f14), ease-out.

5. **Blur-in for a single hero word** (S4 "overwhelming"): blur ~20 px → 0 and opacity 30 → 100 % over 8 f (f164-172), no position change, while the shot zooms out under it.

6. **Word-by-word phrase build**:
   - Lay out the full line or stack first, then reveal each word in place on its syllable.
   - Each word: opacity 0 → 100 % in 2-4 f, a 10-16 px rise, and 2-6 px blur → 0.
   - Exits: either a 1-2 f cut-out ("Today", "8 Months", the vertical stack) or a 3 f fade+blur ("it was like the", "tell me about").

7. **Letter-by-letter type-on for hero words**: about one letter per 1-3 f, with each letter fading in over 1-2 f. Used for "people", "million", "Revenue", "founder", "Sports Bra", "that's Insane", and "Growth" (handwriting). Left-anchored, except "Sports Bra", which is right-aligned to the photo.

8. **Type pairing**: heavy grotesk for the hero/noun, Regular grotesk for connectors, and one serif-italic word per phrase for voice/emphasis. Scale ratios measured:
   - "*Idea*" ≈ 1.3× "had"
   - "first" ≈ 1.5× the other stack words
   - "graph" ≈ 1.9× "went from"
   - "8" ≈ 2.9× "Months"
   - "*the*" ≈ 0.5× "founder"

9. **Stack layouts and alignment** (all on the side opposite the face, except hero words that cross bodies):
   - Left-aligned stacks at x ≈ 160-300: "I/think/in/the/first", "I/had/no/Idea", "A sports/Bar", "that only/plays", "I remember".
   - Right-aligned stacks at a right edge of ≈ 1560-1750: "graph/went from/this", "You/are/watching".
   - Centred single lines: "Our Grand", "overwhelming", "it was like the", "Today", "I'm talking to", "JENNY NGUYEN", "first of its kind.", "Women's Sports", "VS".
   - Diagonal two-block layout: "tell me about" (lower-left, right-aligned at 780) vs "that night" (upper-right, left-aligned at 1188).

10. **White-line → band matte wipe** (S1→S2):
    - A 4 px full-width white line on the title baseline (y 540), drawn in 1-2 f.
    - It expands vertically, symmetric about y 540, on an exponential curve. Height (px): 4, 8, 16, 24, 32, 44, 60, 80, 102, 130, 156, 176, 308, 528, 1012, 1080 over f28-f43.
    - The band is a **track matte revealing the next scene**, so the next scene's number is already visible inside the band.

11. **Number built by appending digits on the voice**: 3 → 30 → 300 → 3000, left-anchored, with a glossy specular sweep across the digits (a lighter diagonal band moving left → right over ~10 f).

12. **3D door reveal** (literal "through the door"):
    - The door edge line draws top→bottom in 6 f.
    - The panel holds the number; the leaf rotates on its left hinge to ≈ 60° with ease-out over 24 f.
    - Grey-gradient silhouettes stand behind it, and the label "people" types on over the silhouettes.

13. **Roto cut-out speaker with sticker outline**: a ≈ 20 px outline (RGB ≈ 218,230,245) with a soft edge, placed over white with a photo card behind. Entry from below the frame with scale 1.2 → 1.0, ease-out over ~25 f, with motion blur early.

14. **Card wipe-expand**: a photo card grows from its left edge, its right edge moving with a 40-80 px motion-blurred leading edge, ease-out over ~9 f.

15. **2.5D parallax truck with foreground defocus** (S3→"Insane"):
    - The camera moves right over 21 f: slow 13 f ease-in, peak 90 px/f, fast 7 f ease-out.
    - The nearest layer (cut-out person) scales ×1.4 and blurs ~10-15 px while moving ≈ 500 px.
    - The mid layer (card and caption) moves ≈ 540 px; the far headline moves ≈ 280 px and keeps typing on during the move.
    - It lands with the person as a soft foreground partly covering the headline.

16. **Defocus-under-text, then rack focus** (S5): lens-blur the speaker plate heavily (Laplacian 0.3 vs 4.0 sharp) while a full-sentence caption sits over the face. Rack to sharp over ~10 f as the sentence fades and the graphic begins.

17. **Gesture-locked line graph** (S5):
    - Fade in a 144 px blueprint grid at ~12 % opacity, parented to the footage.
    - Draw a 16 px white round-capped stroke from bottom-left along the speaker's flat hand ("from this").
    - On "to this" the stroke turns vertical and shoots to the top edge in ~6 f, matching the hand going vertical.
    - Add thin axes plus handwritten "Growth" (top-left) and "Time" (bottom-right) labels.

18. **Card shrink + inner push-in** (S7, S11): the full-frame plate shrinks to a card (S7: 1520x750 centred; S11: 740x936 centred) over 13-14 f with ease-out, while the plate inside scales up (×1.3 in S7), so the subject stays about the same size. Square corners, no border, no shadow, on white. In S11 the photo inside the card hard-cuts to a wider frame mid-hold.

19. **Text clipped by the card**: "*dollars*" sits half outside the card's bottom edge and is masked by the card.

20. **Whip-left transition pair with a blue speed-tail**:
    - The outgoing card accelerates left on an expo ease-in over 14 f: dx 1, 5, 8, 12, 18, 24, 31, 41, 53, 71, 97, 139, 222, 374 px.
    - A 66 px blue bar trails from its right edge, its length tied to speed (16 → 680 px).
    - The incoming layout slides in from the right on an ease-out over ~12 f (left edge 690, 380, 242, 210, 198, 196).
    - The tail retracts to a left-edge stub behind the new card.
    - S11→S12 variant: the **period of "founder." is the bar**. It stretches as it whips left, exits, then re-enters from the left edge as the underline of "Sports Bra" (ease-out over 8 f to a right edge of 764).

21. **Dark-on-white editorial layout** (S7 end, S12):
    - Dark grey 89,89,92 heavy-grotesk title.
    - A blue 14,126,215 bar baseline-aligned with it: 38 px tall beside "Revenue", 66 px tall under "Sports Bra".
    - A photo card sharing the title's left or right edge: money card left edge = title left edge; storefront photo 50 px right of the right-aligned title.
    - Photos rise or slide in with ease-out over 12-13 f.

22. **Stacked-photo pile**: a second photo from the same shoot sits behind the main photo, offset about +84 px x and −30 px y, with no rotation and no shadow.

23. **Light-leak burn to white**:
    - Version A (S12, 9 f): text recolours peach → yellow → white, bars fade from one end, and the photo turns magenta then washes white. 2 pure-white frames, then a hard cut.
    - Version B (S14, 8 f): an orange leak from the left, 2 white frames, then a cut to a white-ground scene.
    - Version C (S23→S24, 14 f): cyan/white streaks, a red ring flare, a pink/orange wash and white scratches, with the cut hidden under the leak at f800. 2 pure-white frames (f808-809), then it clears from the left while the new graphic (ND card) fades up underneath.

24. **Archival film-gate treatment for "place/history" B-roll**: Super-8 gate borders (black sides x 0-230 and 1690-1920, or a rounded gate with a white 2-3 px sprocket-hole outline at x 96-330, y 364-656), heavy grain, dust and scratches, warm faded colour, flicker. Used without captions.

25. **Photo-tile mosaic** (S15):
    - Hard-edged rectangular photos pop in on single frames (every 5-6 f), overlapping into a centred, symmetric stepped plus/diamond shape on white.
    - The collage scales up 1-4 % between pops.
    - A one-line headline sits across it, with words landing on the pop frames.

26. **Caption that survives B-roll cuts**: a sentence keeps building while the footage cuts every 6-31 f underneath. Each new phrase takes a new anchor (lower-left → upper-left → centre); within a phrase the anchor never moves.

27. **Logo badge cards behind people** (S24):
    - Two portrait rounded cards, 484x588 with radius ≈ 50 px. One is white with the gold logo; the other is a solid team colour with a ≈ 5 px white stroke.
    - "VS" between them in white heavy caps (262x138), entering with a −10 % scale-down and fade over 8 f.
    - The second card enters as a ghost outline, then a colour fill, then a gloss sweep (≈ 12 f).
    - The cards are parented to the shot's slow zoom-out (−9 % over 42 f), with roto'd people in front.

28. **Glitch-on name title** (S10): condensed caps letters flicker on in random order over 13 f, with a pink glow (246,178,250) and RGB split. The footage gets scan-lines and a pink highlight shift during the flicker; it settles to clean white.

29. **VHS glitch transition** (S25→S26, 14 f): tracking bars (2 f) → white overexposure flood from the top (3 f) → chroma-smeared horizontal bands (2 f) → noise and static slabs, including a diagonal static band (3 f) → sine-wave horizontal displacement of the incoming clip (≈ 40 px amplitude, 3 f) → clean.

30. **Gloss / specular sweep on graphic type and cards**: a lighter diagonal streak crosses blue letters ("3000" f45-55, "founder" f487-492) and the maroon logo card (f829-833), ~5-10 f per pass.

31. **Timing rhythm** (part A): 28 shots/beats in 31.2 s.
    - Speaker shots: 20-75 f.
    - Graphic beats: 30-60 f.
    - B-roll montage cuts: 6-31 f.
    - White flash frames: exactly 2 f at the peak of every leak transition (f547-548, f618-619, f808-809).

---------------------------------------------------------------------------------------------------

### Legend of analysis images in `refs/zoom_dmA/`

| File | Shows |
|---|---|
| `fNNNN.jpg` | Full 960x540 frame NNNN (≈150 frames: every shot, plus frame-by-frame runs through the band wipe, whips, leaks, VHS glitch and type-ons) |
| `ana_o7_ourgrand_pixel_reveal.jpg` | Pixelate reveal f5/f8/f11 |
| `ana_o1.jpg` | "Our" behind the interviewer's head |
| `ana_c1.jpg` | "Our Grand" reveal f3-f24 |
| `ana_c3.jpg` | Band wipe f23-f41 |
| `ana_c4.jpg` / `ana_g2.jpg` / `ana_ghost.jpg` | 3000 + door build, ghost texture |
| `ana_c24.jpg` | "people" type-on |
| `ana_c5.jpg` / `ana_c28.jpg` | Door exit, Jenny cut-out rise, card wipe |
| `ana_o6.jpg` / `ana_o5.jpg` | Parallax truck; "Insane" behind the blurred Jenny |
| `ana_c6.jpg` / `ana_c26.jpg` / `ana_c23.jpg` / `ana_hp.jpg` | Graph shot: word build, defocus rack, grid/graph high-pass |
| `ana_g7.jpg` / `ana_c9.jpg` / `ana_ghost2.jpg` / `ana_o3.jpg` | Card shrink, "million dollars", whip, speed-tail, Revenue |
| `ana_c10.jpg` / `ana_c27.jpg` | "Today" / "I'm talking to" entries |
| `ana_c25.jpg` | "JENNY NGUYEN" flicker |
| `ana_c11.jpg` / `ana_o4.jpg` | "the founder" card shrink, gloss |
| `ana_c12.jpg` | Period→bar, "Sports Bra" layout |
| `ana_c29.jpg` | Leak burns f536-549, f610-617 |
| `ana_c13.jpg` | Mosaic tiles |
| `ana_c15.jpg` | "Women's Sports" montage + cyan/red leak |
| `ana_g12.jpg` / `ana_c16.jpg` / `ana_c17.jpg` | VS logo cards behind people, VS entry |
| `ana_c19.jpg` / `ana_c18.jpg` | "You are watching", VHS glitch |
| `ana_g13.jpg` / `ana_c21.jpg` | Crowd captions, "I remember" |
