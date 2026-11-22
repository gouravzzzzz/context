# TWIML AI podcast trailer: study part B (frames 1044-2083, 43.50-86.79 s)

Source: `refs/dl/twiml_trailer.mp4`, 1920x1080, 24 fps. All positions are in px on the 1920x1080 frame. "f1234" means frame 1234, and t = f/24.
Method: I read every contact sheet 29-57 (all 1040 frames). I read full-res frames from the mp4 and measured them with OpenCV: bounding boxes, colour samples, Laplacian sharpness for blur, ORB similarity transforms for camera zoom and pan, and per-word opacity curves. Evidence crops and grids are in `refs/zoom_twB/`.
Audio check: I compared the per-frame RMS of `twiml.wav` with the frame each word appears on screen. Words appear **0-8 frames (typically 3-6, about 0.15 s) before they are spoken**. A few early lines appear complete well ahead of the voice; these are noted per shot.

Global look facts (measured):
- **Grain: none.** Flat white grounds are #fdfdfd and flat black grounds are #0a0a0a / #131313, with a std-dev of 0.0 across 400x200 px patches. No noise or texture overlay.
- **Vignette: none on graphic scenes.** All four corners equal the centre (253,253,253) on white scenes.
- **No light leaks, no glow on type, no drop shadows on cards or text.** Card edges go from ground to image in 1-2 px (anti-aliasing only). No border, no corner radius.
- **Motion blur: yes.** It appears on every fast move (measured sharpness dips at f1122-1123, 1380, 1524, 1586-1588, 1617-1621, 1693, 1872-1874).
- **Gaussian blur** is used only as a transition device (see the TRANSITIONS list).
- **Letterbox** appears only on the final shot.
- Type system (3 voices):
  1. **Neo-grotesk sans** (Helvetica / Helvetica Neue look), Regular for running words, Bold for the hologram line and the "properties of the" line.
  2. **Narrow, high-contrast text serif**: double-storey g, ball terminals, very tight default spacing ("entireworld" nearly touches). Closest free match: Instrument Serif Regular; a Times-style condensed serif is also close. It is used for the emphasised or "meaning" word.
  3. **Colour emphasis** with mint #8efde8 (measured medians #8efde8, #86fee9, #8afbe4, #8afbe4). Mint is used **only over speaker footage**.
- Text colours: white #fcfcfc-#fefeff on dark or footage, pure black #000 on white grounds. A word that is still fading in reads grey (#acacac mid-fade).
- Mixed-voice rule: a caption is normally **line 1 = small sans setup words (often with very wide word spacing) + line 2 = big serif (or bold) payoff words**. The serif line is 1.5-2.5x the sans x-height.

---

## 1. SHOT LOG

### S1 - Blue hologram man (stock), f1044-1118 (43.50-46.58 s)
- **Words:** "...so we can analyze weights of neural networks / and we can generate weights of neural networks."
- **Footage:** the same stock set-up in 3 hard-cut angles; the overlay text stays locked on screen across the cuts.
  - **S1a** (to f1045): man from behind, facing a glowing blue data-hologram band (y~240-660).
  - **S1b** (f1046-1075): 3/4 front.
  - **S1c** (f1076-1118): frontal, standing behind a glass table; the hologram band crosses his chest.
  - The ground is the footage itself: near-black navy with the hologram cyan/blue (#3aa0c8-ish glow).
- **Camera:** only the stock clip's own movement. No added zoom could be measured (ORB tracking fails on the hologram noise).
- **Caption set 1** (already up at f1044): "so we can analyze" / "**weights of neural networks**". Positions at f1060:
  - Line 1: Helvetica Regular white, bbox x1151-1608, y437-482 (ascender-to-descender 46 px, about 50 px font). Very wide word spacing: 40-42 px gaps (about 0.8 em, roughly 3x normal).
  - Line 2: Helvetica **Bold** white, bbox x953-1818, y507-573. x-height 38 px ('w' 521-558), about 73 px font. Normal tight spacing (22-27 px gaps).
  - The block is **centred on x≈1382** (L1 centre 1379.5, L2 centre 1385.5), the right-of-centre half. Baselines ~473 and ~558.
  - Text sits **over the hologram light band**, beside the man's head (never on the face). In S1c line 2 crosses his shirt and the hologram.
- **Word reveal (set 1, L2):** in-place opacity fade, no movement. "neural" goes 0% (f1045) → 23% (1046) → 59% (1047) → 65/70/75/81% (1048-1051) → about 100% by f1056. "networks" goes 30% (1049) → 53% (1050) → 70% (1051) → 89% (1055). That is a **jump to 25-55% on frame 1, then ease-out to full over about 8-10 frames**. This line led the voice by about 20 frames ("neural" is spoken at f1066).
- **Set 1 exit:** a hard 1-frame off. Last visible frame is f1078, gone at f1079 (a blank frame), even though the shot cut was at f1076.
- **Caption set 2:** "And we can *generate*" / "**weights of neural networks**".
  - Line 1: "And we can" in Helvetica Regular white, cap 'A' 45 px (y447-491), about 63 px font, gaps about 50 px. "**generate**" is in the **serif**, white, x1498-1670, sharing the sans baseline (y~491); the serif x-height is about 30 px vs 33 px for the sans.
  - Line 2: Helvetica Bold, x892-1878, y512-588, x-height 43 px (about 82 px font, 1.13x set 1).
  - Again centred on x≈1382 (L1 1089-1670 → 1379.5; L2 892-1878 → 1385).
- **Reveal timing (set 2):** same fade curve, about 35% on the first frame, then ease-out to 100% in about 10 frames.

| Word | Starts showing (frame) | Spoken (frame) |
|---|---|---|
| And | 1080 | 1075 |
| we | 1083 | 1080 |
| can | 1086 | 1081 |
| generate | 1090 | 1084 |
| weights | 1092 | 1091 |
| of | 1095 | 1101 |
| neural | 1098 | 1104 |
| networks | 1102 (91% at 1107) | 1108 |

- Set 2 holds complete until the shot cut (f1118 last).
- **Transitions:**
  - IN: caption carried over the hard cuts at 1046 and 1076.
  - OUT: hard cut at 1119 to the white page.

### S2 - White page, footage card with scattered words, f1119-1165 (46.63-48.54 s)
- **Words:** "This isn't just about improving models,"
- **Ground:** pure white #fdfdfd.
- **Footage card:** woman with an AR headset manipulating a holographic turbine; a shutterstock watermark is visible. The card is 16:9 with hard edges: no border, radius or shadow. At rest it is 602x340 (x675-1276, y372-711), centre (975, 541), i.e. dead centre.
- **Words:** Helvetica Regular **black**, cap height 32 px (about 44 px font). They are scattered in a ring **outside the card, never over it**.
  - Top row (y≈229-264), 4 words spread across the full width: "This" x223-297, "isn't" x665-730, "just" x1169-1231 (sits 9 px higher, y220-259), "about" x1637-1736. Word centres ≈260 / 697 / 1200 / 1686.
  - Bottom row (y≈831-871): "improving" x567-737, "models" x1225-1378.
- **Word entry:** **pop-on at full opacity in 1 frame** (no fade, no move); verified in `strip_white_top_*` and `strip_white_bot_*`.

| Word | Pops on (frame) | Spoken (frame) |
|---|---|---|
| This | 1119 | 1122 |
| isn't | 1125 | 1125 |
| just | 1130 | 1132 |
| about | 1136 | 1138 |
| improving | 1142 | 1144 |
| models | 1151 | 1154 |

- **Camera (whole 2D layout scaled about the frame centre; card and words move together)** as % of rest size:

| Frame | 1119 | 1120 | 1121 | 1122 | 1123 | 1124 | 1125 | 1126 | 1128 | 1130 | 1134 | 1138 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Scale % | 112.5 | 112.0 | 111.5 | 109.5 | 106.0 | 104.2 | 103.2 | 102.2 | 101.7 | 101.0 | 100.3 | 100.0 |

  - Zoom-OUT entry: S-curve with its fastest step at f1122-1123 (3.5%/frame, motion-blurred; sharpness 216 → 116), 19 frames long.
  - Hold f1138-1147.
  - Push-IN exit, ease-in, 18 frames: 100.2 (1148) → 100.3 (1150) → 100.7 (1154) → 101.3 (1158) → 101.8 (1160) → 103.0 (1163) → 104.2 (1165), still accelerating at the hard cut.
- **Transitions:** IN is a hard cut from S1; OUT is a hard cut at f1166 while moving.

### S3 - Rotating 3D stack of 4 portrait clips on near-black, f1166-1263 (48.58-52.63 s)
- **Words:** "it's about unlocking an entirely new dimension of AI research."
- **Ground:** flat #0a0a0a-#0c0c0c.
- **4 portrait (about 9:16) video cards** in a 3D Z-stack, all dreamlike: a figure floating/skydiving in a dark starfield; a man lying on a green grass spiral; a man lying in a meadow; a tiny figure running on a mirror-like salt flat under clouds. The card in front is brighter (sky card mean RGB 154,187,233 in front vs 66,139,217 when at the back), so there is a depth fade.
- **Cards:** hard edges (242→43 in 1-2 px), no border, radius or shadow.
- **At rest, f1236** (back → front, each successive card larger, so the stack is in perspective):

| Card | x | y | Size |
|---|---|---|---|
| Skydiver (back) | 880-1062 | 319-643 | 183x324 |
| Grass spiral | 900-1088 | 383-716 | 189x333 |
| Meadow | 923-1118 | 449-796 | 196x347 |
| Salt-flat sky (front) | 980-1183 | 482-841 | 204x360 |

  The cascade runs top-left → bottom-right, stepping +20 to +57 px in x and +33 to +66 px in y per card. The stack is centred on about x1030, y580.
- **Stack motion, frame by frame** (see `grid_stack_1176_1199_every1.jpg` and `grid_stack_1166_1263_every3.jpg`):
  - f1166-1175: fanned diagonal, slow start of a Y-axis orbit. The stack narrows and rises (bbox 802-1247 → 807-1251, top y359 → 334).
  - f1176-1184: orbit accelerates. The cards go edge-on into a single vertical column (f1182-1184 bbox x902-1139 wide, y232-906 tall) with motion blur.
  - f1185-1187: pass-through; the order flips and the skydiver card is now in front, top-right.
  - f1188-1197: the stack fans out in the mirrored direction (back = sky card bottom-left, front = skydiver right) and drops. Fully fanned at f1196 (bbox 768-1285 x 358-779).
  - f1198-1222: second swing. The sky card jumps to the front-left and the others rotate behind it until almost hidden (f1214-1223 only slivers show).
  - f1223-1236: re-fan into the original diagonal (front = sky card bottom-right) and grow. Settled about f1236.
  - f1236-1262: slow drift/grow (stack top y318 → 305).
  - The orbit is about **70 frames of continuous 3D rotation**, eased in and out at each "fan" pose, and the words play over it.
- **Text** (both lines share a baseline ≈546, block vertically centred about y530):
  - **Left block** "it's about unlocking an entirely": Helvetica Regular white #fcfcfc, about 47 px font (ascender-descender 44 px, y511-555). **Left-aligned**; its left edge slides 186 → 138 between f1170 and f1226 (48 px, ease-out). At rest x138-710.
  - **Right block** "new dimension of *AI research.*": "new dimension of" in sans x1303-1640, "AI research." in the **serif** (cap 'A' about 44 px tall, larger than the sans), white. Block x1303-1892, so the right margin is only 28 px.
  - The stack sits **between** the two text blocks; text is never over the cards while at rest.
- **Word reveal:** grey → white opacity fade, about 8-10 frames, ease-out, no position change apart from the block drift.

| Word | On screen (frame) | Spoken (frame) |
|---|---|---|
| it's | 1170 | 1171 |
| about | 1178 | 1175 |
| unlocking | 1186 | 1181 |
| an | 1192 | 1195 |
| entirely | ~1198 | 1202 |
| new | 1206 | 1212 |
| dimension | 1214 | 1221 |
| of | 1222 | 1233 |
| AI | 1228 | 1238 |
| research. | 1236 (still #acacac grey at 1236) | 1248 |

  The right block leads the voice by 6-12 frames.
- **Exit f1240-1263 ("collapse to centre" + blur):**
  - Left block: left edge pinned at x138, right edge 709 → 701 (1250) → 687 (1256) → 668 (1260). The text compresses (scales down, anchored left).
  - Right block: slides left and compresses, left edge 1303 → 1285 (1250) → 1257 (1256) → <1250 (1260), right edge 1891 → 1765 (1260) → 1687 (1262). It ends overlapping the stack.
  - Horizontal motion blur builds over f1259-1262 (sharpness 357 → 163).
  - f1263 is one fully Gaussian-blurred frame (sharpness 0.6, blur radius about 25 px).
  - Hard cut at f1264.

### S4 - Speaker "You have this new / entire world", f1264-1318 (52.67-54.92 s)
- **Words:** "You know, you have this new entire world,"
- **Footage:** webcam talking head, full frame. Speaker at right-centre (face about x920-1350), office bookshelf and blinds, natural soft background.
- **Entry:** the frame arrives Gaussian-blurred (sharpness 4 at f1264) and sharpens over 6 frames (f1270 sharpness 119) **while zooming out**: about 105% (f1264), 101.9% (1266), 101.2% (1268), 100.3% (1270), 100% (1272).
- **Camera:**
  - Hold f1272-1277.
  - **Punch-in** f1277-1303 from 100 → 110.4%, fixed point about (-250, 539) (far left), so the content also drifts right. Curve: 100.3 (1277), 101.2 (1278), 102.1, 103.2, 104.5, 106.0 (1282), 106.6, 107.1, 107.4, 108.0 (1286), 108.5 (1288), 109.0 (1290), 109.7 (1294), 110.1 (1298), 110.4 (1303). That is about 6% in the first 5 frames, then a long ease-out tail (26 frames, 1.1 s).
  - Then a slow zoom back out, accelerating: 110.4 (1306) → 110.0 (1313) → 109.2 (1317) → 108.2 (1318), going into the cut.
- **Caption** (left third, over the bookshelf, beside the face):
  - Line 1 "You have this new": Helvetica Regular white #fefefe, cap 'Y' 45 px (y500-545), about 63 px font, x221-694.
  - Line 2 "**entire world**": serif, mint #8efde8, x-height 61-62 px ('e' y586-647), ascender 'd' to baseline 92 px, about 135 px font, x208-711. The two words nearly touch (tight serif spacing; the space has been killed).
  - **Centred block** on x≈458 (L1 centre 457.5, L2 459.5), block y500-647, so its centre is about 35 px above frame centre.
  - Text is inside the camera comp (it scales with the punch-in, then a bit more: 'You' grows 81 → 94 px wide while the camera does 1.10x).
- **Build:**
  - "You" is visible blurred at f1264 (the blur transition covers the text too); "have" 1268; "this" 1272; "new" 1276.
  - Spacing settles: the words land spaced out and the gaps contract. Gaps were 17/51/62 px at f1276 and are 24/19/21 px at rest from f1292. This is about 15 frames of ease-out "tracking tighten".
  - "entire" appears at f1280 (mint, at x149, slides right to 208 by 1300); "world" at f1284 with a visible gap that closes by f1292.
  - Spoken: entire 1288, world 1301. Line 2 leads the voice by 8-17 frames.
- **Exit:** f1318 the caption ghosts (about 50% opacity plus zoom-out), then hard cut at 1319 into S5, which is also zooming out (zoom-direction match).

### S5 - White 3x3 grid, footage in the centre cell, "empty | space", f1319-1353 (54.96-56.38 s)
- **Words:** "empty space"
- **Ground:** #ffffff.
- **Grid:** 2 horizontal and 2 vertical hairlines running the full frame, about 1.5 px, dark grey (profile 194/141/206 across the line, i.e. a 1 px black line at about 50% after anti-aliasing).
  - At rest (f1333) the vertical lines are at x767 and x1171, the horizontal lines at y322 and y756. The centre cell is 404x434 (almost square) and centred.
- **Footage** fills the centre cell exactly, edge to edge with the lines: an iridescent glass hand pinching a crystal in a dark nebula (CG), #1a1418-ish dark.
- **Words:** serif, black, small: x-height about 19 px, about 42 px font, on one baseline y≈552 (row centre). Both sit in the cells **flanking** the footage:
  - "empty" x582-662 in the left cell, **right-aligned toward the footage** (105 px gap to the line at 767).
  - "space" x1307-1376 in the right cell, left-aligned toward the footage (135 px gap from the line at 1172).
- **Word entry:** fade plus a small slide left, ease-out.
  - "empty": darkest pixel 114 (f1323) → 83 → 57 → 29 → 23 → 17 → 10 → 0 (f1330), about 7 frames; x 593 → 582 (11 px).
  - "space": 96 (f1330) → 70 → 48 → 36 → 17 → 14 → 6 → 0 (f1338); x 1307 → 1304 → 1306.
  - Spoken: empty 1319, space 1328.
- **Camera:** grid and card move as one layer.
  - f1319-1333: zoom out about 1.6% (cell 409x441 → 404x434) and pan left 20 px (left line x787 → 767), ease-out.
  - f1333-1349: reverse, zoom in and pan right 11 px (line → 778).
- **Exit:** f1350-1353 is a full-frame Gaussian blur (sharpness 0.9-1.5) with a small push-in (card x784 → 792 and growing). Hard cut at 1354 to blurred S6, which is also zooming in.

### S6 - Speaker "things you can / do with weights", f1354-1380 (56.42-57.54 s)
- **Footage:** same webcam.
- **Entry:** blurred (sharpness 8 → 289 by f1358, 4 frames) and **zooming in**: 96.0% (1354) → 98.0 (1356) → 99.2 (1358) → 100 (1362), fixed point at the left side (x≈-74 to -476).
- **Camera:**
  - Hold f1362-1370.
  - **Zoom-out exit, ease-in**: 99.6 (1370) → 99.4 (1372) → 98.8 (1374) → 98.0 (1376) → 96.3 (1378) → 95.5 (1379) → 94.0 (1380), fixed point about (20, 541) (left edge). Motion-blurred at 1380 (sharpness 150).
- **Caption** (left, over the bookshelf, beside the face at x1000-1450):
  - Line 1 "things  you  can": Helvetica Regular white, x-height about 30 px (about 58 px font), very wide gaps (about 45-50 px). At f1376: things x357-495, you x545-626, can x668-752; y504-557.
  - Line 2 "**do with weights**": serif, mint, 'do' ascender-baseline 81 px (about 115 px font), x293-858, y556-669.
  - Block centre x≈575.
- **Per-word entry, each word from its own direction with an ease-out settle:**
  - "things": appears (blurred) f1354 and drifts right 345 → 367 (with the camera).
  - "you": drops in from above, top y482 (f1358) → 489 → 494 → 498 → 505 (1362) → 507 → 509 → 511 → 513 → 514 → 515 (f1369). That is 33 px in 11 frames, ease-out.
  - "can": slides in from the right, x755 (f1360) → 736 → 719 → 713 → 709 → 705 → 699 → 696 → 694 → 692 → 687 → 685 (f1371). That is 70 px in 11 frames.
  - "do": slides in from the left, x250 (f1363) → 260 → 269 → 281 → 286 → 289 → 291 → 295 → 296 (1371).
  - "with": **rises from below**, top y628 (f1367) → 607 → 596 → 581 → 576 → 571 → 568 → 562 → 560 → 559 (f1376). That is 70+ px, ease-out.
  - "weights": rises from below, top y622 (f1370) → 607 → 596 → 588 → 576 → 571 → 568 → 565 (f1377).
  - Spoken: things 1353, you 1360, can 1364, do 1368, with 1371, weights 1376.
- **Exit:** f1378-1380 the caption fades to about 40% and blurs with the zoom-out. Hard cut 1381.

### S7 - Speaker "weights are *exciting*", bottom-centre caption, f1381-1407 (57.54-58.67 s)
- **Entry:** **continues the zoom-out** from S6: 105.3% (1381) → 102.8 (1382) → 102.2 → 101.7 → 101.3 → 100.7 (1386) → 100.5 → 100.4 (1388) → 100. This is a zoom-out match cut; S6 leaves zooming out and S7 enters zooming out.
- **Camera:**
  - Slow pan f1388-1401: content shifts 15 px left.
  - **Push-in exit, ease-in**: 100.4 (1401) → 101.3 (1404) → 102.8 (1406) → 103.7 (1407), fixed point right of centre (x1326-1881, y536).
- **Caption:** one line, **bottom centre**, over the speaker's shirt (body, not face).
  - "weights are": Helvetica Regular white, x697-1058, y977-1049.
  - "**exciting**": serif, mint, x1080-1293, y980-1052. Baseline ≈1033, i.e. 47 px from the bottom edge.
  - About 79 px sans font (x-height 'are' 41 px).
  - Line centre x≈995 (slightly right of the frame centre).
- **Entry:** "weights" slides in from the right, x796 (f1384) → 734 → 726 → 723 → 720 → 717 → 713 (1390), then keeps drifting with the camera to 697 (1398). "are" at f1389; "exciting" at f1393, settling 1090 → 1080. Each word has a 3-6 frame fade (max value 230 → 255).
- Spoken: weights 1390, are 1393, exciting 1396-1407.
- **Exit:** hard cut 1408 into the strobe transition.

### S8 - Strobe-invert transition then white "UI flow" scene, f1408-1495 (58.67-62.29 s)
- **Words:** "not only as the output of learning, but as the input for learning."
- **Transition f1408-1418** (11 frames):
  - f1408: **inverted (negative) frame** of the new scene; black ground, the green task card appears purple.
  - f1409-1410: positive, sharp.
  - f1411: negative, heavily blurred.
  - f1412-1418: positive, Gaussian-blurred, sharpening (sharpness 0.3 → 4.6).
  - f1419 sharp (38).
  - Audio: a beat drop under "exciting,".
- **Ground:** white #fdfdfd.
- **Footage:** borrowed SaaS-promo motion graphic, full frame, no card. App icons (Gmail, App Store, YouTube, X) and grey UI chips ("Need an option to export data", "Too slow on mobile") stream from left into a central **OpenAI logo tile** (x912-1045, y495-610), which feeds a peach task card on the right ("Change bedding for all cows ...", x1050-1410, y438-640).
  - Depth of field: far-left icons are blurred and faded.
  - The whole scene slowly pushes in: the top caption line grows from 883 px wide (f1449) → 905 (1471) → 956 (1475) → 984 (1495), i.e. 111% overall, with a quick +5.6% step at f1471-1475.
- **Text:**
  - Two lines **framing the footage band**: one above, one below.
  - Helvetica Regular black, x-height 24 px (about 46 px font). **Extreme word spacing: a constant 77-80 px gap between every word** (about 1.7 em).
  - Top "not  only  as  the  output  of  learning": x479-1459, y274-315 (baseline ≈306).
  - Bottom "but  as  the  input  for  learning": x551-1387, y794-836 (baseline ≈827).
  - Both centred on x≈969.
- **Word reveal:** slow opacity fade, about 20 frames to full black. For "as" (darkest pixel): 201 (f1419) → 122 → 81 → 63 → 47 → 35 → 26 → 22 → 13 → 9 → 0 (f1441). That is ease-out: about 20% on frame 1, 60% by frame 4.

| Word | First frame | Spoken | Word | First frame | Spoken |
|---|---|---|---|---|---|
| not | 1409 | 1416 | but | 1453 | 1464 |
| only | 1415 | 1421 | as | 1459 | 1469 |
| as | 1419 | 1428 | the | 1465 | 1475 |
| the | 1427 | 1431 | input | 1473 | 1478 |
| output | 1431 | 1434 | for | 1479 | 1485 |
| of | 1437 | 1442 | learning | 1485 | 1489 |
| learning | 1443 | 1450 | | | |

  Words lead the voice by 3-11 frames.
- **Exit:** hard cut at 1496.

### S9 - Dark gradient title card "Discover the challenges / And the immense potential", f1496-1550 (62.33-64.58 s)
- **Ground:** #131313 top 55%. The lower 45% has two cyan "stage light" glows rising from the bottom-left and bottom-right corners, with a dark V gap in the middle:
  - bottom edge #11aec8 (x300) and #10b1cd (x1400)
  - #118a9d at (1700, 950); #134249 at (100, 800)
  - dark centre #123f46 at (800, 1050) and #131a1a at (960, 800)
- No footage.
- **Entry f1496-1504 (focus pull):** the frame starts fully defocused (sharpness 0-27) with the text invisible, then grey. Text brightness max 125 (1500) → 157 → 205 → 223 → 235 (1504); sharp at f1505.
- **Line A** "Discover the challenges": Helvetica Regular white, cap 'D' 72 px (y484-555), about 100 px font. At f1515 x513-1510 (centre about 1011), baseline about 557.
  - "Discover the" is up first (blurred). "challenges" enters at f1509 from x1132 and slides left 1132 → 1097 → 1089 → 1082 → 1077 → 1068 → 1064 (1515) → 1057 → 1049 → 1044 → 1039 (1520), with a fade 145 → 255 over 8 frames.
  - The whole line drifts left and very slightly shrinks (Discover x539 → 482, width 360 → 343 by f1523).
- **Line swap f1523 → 1524 (1 frame):** line A disappears and **line B** "And the immense potential" appears. It is smaller: cap about 57 px (y498-555), about 80 px font.
  - "And the" slams in from the right: 'And' left edge x755 (f1524) → 611 → 577 → 567 → 561 (1528), i.e. 194 px in 4 frames with motion blur (sharpness 279), then creeps to 536 (1536) and 521 (1548).
  - "immense" arrives at f1528 faint (min 117), slides 984 → 874 → 849 → 841 → 835 → 829 → 822 (1534).
  - "potential" arrives at f1534 at x1165 → 1124 (1545).
  - Spoken: discover 1507, the 1507, challenges 1513, and 1522, the 1533, immense 1536, potential 1542.
- **Exit f1549-1550:** text Gaussian-blurred (sharpness 2-3), then cut on f1551 to S10 on the **same gradient ground**.

### S10 - 3D CNN block diagram + scrambled title "weight space learning", f1551-1588 (64.63-66.17 s)
- **Ground:** same as S9 (continuity across the cut).
- **3D blocks:** flat-shaded isometric cuboids in blue #176898-#1a7ea9 (light face #267eab), a classic CNN layer diagram (tall slab → shrinking cubes → thin bar).
  - f1551-1553: about 8 blocks fly in from scattered positions with motion blur.
  - f1554: snapped into the assembled row, bbox x650-1330, y396-705.
  - f1554-1588: slow push/grow (bbox x648-1435 by 1584).
- **Title** "weight space learning": Helvetica Regular white, x-height 57 px ('w' y545-602), about 110 px font. Left edge x511, y524-626, overlapping the blocks (text over the diagram).
  - **Decoder/scramble reveal**, f1565-1577: random glyphs resolve into the letters, roughly left → right, while opacity rises from about 40% to 100%.
    - f1565 "veyst hpqce leGIHnw" (faint)
    - f1567 "yeimgt apace leRINn l"
    - f1570 "weie `t space le Qnin"
    - f1572 "weigat space leWnin"
    - f1574 "weight space leafning"
    - f1577 "weight space learning"
  - 12 frames to resolve. Spoken: weight 1563, space 1568, learning 1574.
- **Exit f1576-1588:** the title scales up anchored on its left edge x511 (glyph 'w' 69 → 78 px wide, last glyph right edge 1441 → 1550). It accelerates with motion blur at f1586-1588 (sharpness 52 at 1588). Hard cut at 1589.

### S11 - White page, op-art card + "Can we truly / manipulate", then card drops into a 3x3 grid, f1589-1694 (66.21-70.58 s)
- **Words:** "Can we truly manipulate and edit the behavior of neural networks at their core?"
- **Ground:** #fdfdfd.
- **Part 1, f1589-1621:**
  - **Card:** psychedelic op-art tunnel (rainbow concentric rings), 16:9.
  - It enters already moving (from the hard cut): bbox 750-1559 x 314-766 (810 wide) at f1589 → 769-1633 (865) → 775-1659 → 780-1683 → 784-1695 → 786-1707 (922) at f1599 → 786-1713 x 279-800 (928) at f1601.
  - So it scales up 1.146x and drifts right 95 px, ease-out, 12 frames.
  - At rest about 784-1708 x 280-800 (925x521), centre (1246, 540): **the card sits right of centre and the text sits left of it**.
- **Text** (from f1603):
  - Line 1 "Can we truly": Helvetica Regular black, cap 52 px (y493-545), about 72 px font, x345-708.
  - Line 2 "**manipulate**": serif black, x-height 59 px (y585-644), about 130 px font, x289-759 (descender to 672).
  - **Centred block** on x≈525. Line 2's right edge is 24 px from the card's left edge.
  - Spoken: can 1594, we 1595, truly 1598, manipulate 1605.
- **Card into grid, f1613-1622:**
  - The card shrinks and moves left: width 1069 incl. text (1613) → card 902 (1615) → 890 (1617) → 872 (1618) → 860 → 844 → 818 (1621), centre 1224 → 1144. It is motion-blurred.
  - The text is gone at f1621 (cut off in 1 frame).
  - **f1622: a black 3x3 grid snaps on in 1 frame**, with its centre-cell lines landing exactly on the card's edges (card 684-1366 x 348-733). Lines are about 2-3 px pure black.
  - The card and cell then keep shrinking together, ease-out: 683 (1622) → 672 → 663 → 658 → 649 (1626) → 642 (1628) → 632 (1631) → 624 (1635) → 616 (1641) → 611 (1647) → 608 (1655) → 605 (1663) → 601 (1671).
  - Centre cell at rest about x656-1263, y373-712 (607x339 = 16:9), centred at (960, 542).
- **Footage inside the cell:** op-art tunnel f1622-1627, **hard cut inside the cell at f1628** to a businessman's hands manipulating a green particle neural-network hologram (dark teal #14302c). There is a second cut inside the clip at about f1682.
- **Grid text "and edit | the behavior of neural networks | at their core?":** one line **sitting on the top grid line** (baseline y≈346, the line is at y374), Helvetica Regular black, x-height 25 px (about 48 px font). Each phrase occupies a column:
  - "and edit" x490-667, **right-aligned** to the left grid line (16 px gap).
  - "the behavior of neural networks" x688-1238, **fills the centre column exactly** (5 px from each line).
  - "at their core?" from x1249, **left-aligned** just right of the right grid line.
  - Words fade in grey → black. Approximate first frames: and 1625, edit about 1630, the/behavior/of about 1640-1650, neural about 1655 (grey at 1660), networks about 1668, at their about 1675, core? about 1686 (still grey at 1690).
  - Spoken: and 1620, edit 1626, the 1633, behavior 1637, of 1647, neural 1655, networks 1662, at 1674, their 1681, core 1687.
- **Exit f1675-1694:** the grid and card shrink again, accelerating: 597 (1675) → 590 (1681) → 583 (1685) → 570 (1689) → 556 (1691) → 505 (1693).
  - f1693 is a frame-blend: ghosted double grid lines and text (motion echo, sharpness 181).
  - f1694 a single crisper frame, then hard cut at f1695.

### S12 - Speaker, right-side caption "Can we learn some / representation", f1695-1748 (70.63-72.83 s)
- **Entry:** zoom-out continues from the S11 exit: 103.8% (1695) → 102.1 (1697) → 100.4 (1699) → 99.0 (1702) → 98.5 → 97.9 (1706) → 97.6 (1708), fixed point about (1000, 540) (centre).
- **Camera, big push-in f1710-1746**, fixed point drifting from about (2700, 1013) to (1631, 801), i.e. pushing toward the lower right where the caption is:

| Frame | 1712 | 1714 | 1716 | 1718 | 1720 | 1724 | 1728 | 1732 | 1736 | 1740 | 1745 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Scale % | 98.5 | 101.1 | 104.5 | 109.2 | 111.5 | 115.1 | 117.4 | 118.8 | 119.8 | 120.5 | 120.9 |

  That is +23.6% in 1.4 s, ease-out (peak about 2.3%/frame at f1714-1718).
- **Caption** (right side, over the window and frame background, beside the face; face at x560-1010 after the push):
  - Line 1 "Can we learn some": Helvetica Regular white.
  - Line 2 "**representation**": serif, mint.
  - At f1730: L1 about x1190-1832, y483-545; L2 about x1150-1858, y560-667.
  - Block centred on x≈1505. Text scales with the push.
- **Build:**
  - "Can" grey at f1699, "we" 1700, "learn" 1702, "some" 1704 (fade about 4-6 frames each).
  - "representation" fades in at f1707, overlapping L1 slightly, and settles by 1712.
  - Spoken: can 1700, we 1703, learn 1705, some 1712, representation 1719.
- **Exit (blur dissolve, f1747-1753):**
  - f1747-1748: S12 Gaussian-blurred, caption included.
  - f1749: 1-frame crossfade blend of blurred S12 and blurred S13.
  - f1750-1753: S13 blurred, sharpening; sharp at f1754 (sharpness 74 → 187 at 1755).

### S13 - Speaker, left caption, 3 lines "use it to predict / properties of the / neural network", f1749-1827 (72.88-76.13 s)
- **Camera:** lateral slide-in. Content offset relative to rest (positive = content shifted right of rest): -122 px (1751) → -100 (1753) → -76 (1755) → -66 (1757) → -49 (1760) → -21 (1764) → -20 (1772) → -13 (1776) → -7 (1780) → -3 (1784) → 0 (1788). That is a 122 px pan over 37 frames, ease-out, no zoom. Static f1788-1827.
- **Caption** (left side over the bookshelf; face at x830-1300):
  - L1 "use  it  to  predict": Helvetica Regular white, x-height 40 px (about 77 px font), x165-732, y447-516, wide gaps.
  - L2 "**properties of the**": **Helvetica Bold, mint #86fee9**, x88-817, y524-615 (about 95 px).
  - L3 "neural   network": **serif, white**, x185-745, y616-685.
  - Lines centred on x≈450-465. Leading is tight: L2 top 524 vs L1 bottom 516; L3 top 616 vs L2 bottom 615.
- **Build (each word its own move):**
  - "use" at f1752 (inside the blur); "it" 1752 from above; "to" 1755 from above, dropping to the baseline by about 1760; "predict" 1758.
  - "**properties**" slides in from the **left** edge: x0 (f1781, clipped) → 7 → 19 → 29 → 38 → 52 → 58 → 63 → 67 → 74 (1790) → 77 → 80 → 82 → 85 → 86 → 87 → 88 (1798). That is 88 px, 17 frames, ease-out.
  - "of" from the left: x507 (1784) → 560 (1798).
  - "the" from the **right**: x732 (1787) → 723 → 716 → 705 → 701 → 697 → 694 → 689 → 687 → 683 → 681 → 679 (1799). It converges on "of".
  - "neural" and "network" **rise from below**: tops y≈715 (f1801, clipped) → 659 → 652 → 636 (1805) → 632 → 626 → 621 (1810) → 617 → 616 (1812); "network" 1804 → 1812.
  - Spoken: use 1749, it 1758, to 1764, predict 1769, properties 1777, of 1793, the 1807, neural 1813, network 1816.
- **Exit:** hard cut at 1828.

### S14 - White page, growing card with typewriter serif caption below, f1828-1876 (76.17-78.21 s)
- **Words:** "or to manipulate and edit the behavior,"
- **Ground:** #fdfdfd.
- **Card:** 16:9, no border.
  - Content: op-art tunnel f1828-1852, **hard cut inside the card at f1853** to the green-hologram hands clip (same clip family as S11).
  - **Constant-speed push**: width 531 (1828, x716-1246, y378-676) → 540 → 548 → 560 → 568 → 579 → 587 → 597 → 604 → 615 → 623 → 633 (1850) → 642 → 650 → 657 → 667 → 674 (1860) → 683 → 688 → 698 → 703 → 709 (1870) → 712 → 714 (1874). That is about 4.5 px/frame (0.8%/frame), linear with a slight ease at the end; 1.345x in 46 frames.
  - Centre drifts left: x981 (1828) → 954 (1870) → 935 (1874).
- **Caption:** one line **below the card**, serif black, x-height about 26 px (about 55 px font), wide word gaps about 49 px. Baseline y≈809 at f1866, i.e. 83 px below the card's bottom edge (726).
  - **Typewriter reveal, letter by letter, re-centred on the card each frame**: f1831 "to" (centre about x850), f1837 "to mani", f1840 "to manipu", f1843 "to manipulate", f1849 "...and", f1855 "...and e", f1858 "...edit", f1864 "...the", f1870 "...beh", f1873 "...behavi".
  - About 1 character per 1-1.5 frames, synced to speech (manipulate 1836-1847, and 1847, edit 1854, the 1860, behavior 1870).
  - Line centre stays at the card centre (at f1866 x651-1232, centre 941).
  - **Periodic echo frames** (double image of text and card) at f1843, 1858, 1873: a 1-frame frame-blend every 15 frames.
- **Exit:**
  - f1872-1874: card accelerates left (x-centre 954 → 935) with horizontal motion blur on the text.
  - f1875-1876: Gaussian blur.
  - Hard cut at 1877 to blurred S15.

### S15 - Speaker, bottom-right caption "change and *modify?*", f1877-1903 (78.25-79.33 s)
- **Entry:** blurred (sharpness 6 → 378 by f1883, 6 frames) plus zoom-out 103.9% (1877) → 102.7 → 102.0 → 101.4 → 100.8 (1885) → 100.
- **Camera:** then a slight further zoom-out to 99.2% (1901).
- **Caption** (bottom-right, over the desk area to the right of the speaker):
  - "change and": Helvetica Regular white, about 90 px font, x1072-1515, y889-974.
  - "**modify?**": serif, mint, x1536-1809, y876-978.
  - Baseline ≈955 (125 px from the bottom). Right margin 111 px.
- **Build:**
  - "change" at f1881 (inside the blur; spoken 1882).
  - "and" at f1890 from the right: x1426 → 1410 → 1400 → 1393 → 1390 → 1388 → 1386 → 1382 → 1381 → 1379 → 1378 → 1376 → 1375 (1903). That is 51 px, 13 frames, ease-out (spoken 1888).
  - "modify?" at f1893 from the right: 1594 → 1576 → 1568 → 1562 → 1552 → 1548 → 1546 → 1544 → 1540 → 1537 → 1536 (1903). That is 58 px, 10 frames (spoken 1894).
- **Exit:** hard cut at 1904.

### S16 - Hooded hacker in a control room: full frame, then shrinks into a card on white, f1904-1959 (79.33-81.63 s)
- **Words:** "The future of AI is being written,"
- **Footage:** hooded figure from behind at monitors with green world maps; dark teal, soft focus; "PFX" watermark bottom-right.
- **f1904-1919:** full frame, almost static (scale 100.5 → 100%).
- **Caption:** serif white "The future of AI is being written", **inside the footage layer** (it shrinks with it).
  - Full-frame size at f1915: cap 'T' 55 px (y492-547), about 80 px font, starting x481.
  - "The future" visible at f1915; the remaining words follow (spoken the 1907, future 1911, of 1918, AI 1924, is 1934, being 1942, written 1946).
  - At the card size (f1940): x706-1163, cap 29 px, centred on the card (centre about 935; "written" was still fading).
- **Full frame → card shrink**, scale about the frame centre (959, 539), white #fdfdfd revealed around it. Scale % (16:9 kept):

| Frame | 1920 | 1921 | 1922 | 1923 | 1924 | 1925 | 1926 | 1927 | 1928 | 1929 | 1930 | 1931 | 1932 | 1933 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Scale % | 99.6 | 98.4 | 97.8 | 97.0 | 96.2 | 94.3 | 93.2 | 92.1 | 90.8 | 87.8 | 85.9 | 84.0 | 81.7 | 76.1 |

| Frame | 1934 | 1935 | 1936 | 1937 | 1938 | 1939 | 1940 | 1941 | 1942 | 1943 | 1944 | 1945 | 1947 | 1949 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Scale % | 72.6 | 68.7 | 64.8 | 58.9 | 56.9 | 55.5 | 54.2 | 52.4 | 51.7 | 51.0 | 50.5 | 49.6 | 48.8 | 47.9 |

  It continues 47.2 (1952) → 46.6 (1954) → 46.0 (1957) → **45.8 at f1961 (card 879x495, x520-1398, y292-786)**.
  - Shape: ease-in-out, peak speed about 5.6-5.9%/frame at f1933 and f1937, then a long ease-out tail. 41 frames total (1.7 s).
- **Exit:** **hard cut inside the card** at f1960. The caption "The future of AI is being written" carries over onto the new clip for 2 frames (visible at 1960-1961, gone by 1962).

### S17 - Same card: purple CG figure with flying CRT monitors, "one weight at a time", f1960-1992 (81.67-83.00 s)
- **Card:** hold at 45.8% (f1961-1972), then a slow linear grow begins (see S18).
- **Footage:** a 3D hooded mannequin standing still while retro CRT monitors and laptops fly and tumble around it. It starts grey and becomes purple-lit, then cyan-lit at f1987-1992 (the clip's own light change, with glitch-like colour flashes on the monitors).
- **Caption:** serif white "one weight at a time", centred on the card (at f1975 x786-1026 so far, x-height 25 px at card scale).
  - Words fade in word by word, roughly in sync with the voice: "one weight at" is on screen at f1975 and the line is complete by about f1985.
  - Spoken: one 1963, weight 1968, at 1974, a 1977, time 1981.
- **Exit:** hard cut inside the card at f1993. The caption **carries over onto the street clip for 4 frames** (f1993-1996), then fades.

### S18 - Same card: Paris street walkers, "Don't miss this insightful conversation.", f1993-2037 (83.04-84.88 s)
- **Footage:** two people walking away down a Paris street, Eiffel Tower in the distance; natural daylight, slightly desaturated.
- **Card:** keeps growing slowly and linearly: 47.2% (1992) → 47.7 (1998) → 48.2 (2004) → 48.7 (2010) → 49.2 (2016) → 49.7 (2022) → 50.3 (2028) → 50.8 (2034) → 51.2% (f2037; x464-1446, y263-815). That is about 0.09%/frame, constant. The content inside does not move relative to the card.
- **Caption:** serif white "Don't miss this insightful conversation.", centred on the card, cap 'D' 29 px at card scale. At f2025: x669-1265, y511-554 (centre 967).
  - Word-by-word fade-in: "Don't" about f1998, "miss" 2003, "this" 2006, "insightful" 2009, "conversation." about 2013.
  - Spoken: don't 1987, miss 1998, this 2002, insightful 2008, conversation 2020.
- **Exit:** f2038 is one blurred mixed frame (Gaussian-blurred speaker, desaturated, with a ghosted rectangle of the blurred card at about x660-1310, y340-740). Hard cut, cuts list 2038/2039.

### S19 - Final speaker, letterboxed, right-side 3-line caption, f2038-2083 (84.92-86.79 s, end)
- **Words:** "Let's see where we will be in three years."
- **Entry:**
  - f2038 blend frame; f2039 blurred (sharpness 5); f2040 sharp-ish (264); f2041-2043 soft (85-90) while the bars move; f2044 sharp.
  - Zoom-in: about 97.8% (2045) → 98.4 (2047) → 99.0 (2050) → 99.6 (2055) → 100 (2060) → 100.3 (2066) → 100.5 (2078). The fixed point is on the right side (x≈1850, y≈556), i.e. the push goes toward the caption.
  - Earlier frames estimate about 92% with low confidence.
- **Letterbox:** pure black bars slide in from the top and bottom edges together. Bar height:

| Frame | 2040 | 2041 | 2042 | 2043 | 2044 | 2045 | 2046 | 2047 | 2048 | 2049 | 2050 | 2051 | 2052 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Bar px | 1 | 12 | 46 | 87 | 109 | 123 | 132 | 138 | 143 | 145 | 147 | 149 | 150 |

  - Ease-out over 12 frames; final bars 0-150 and 930-1079. The visible picture is 1920x779, about 2.46:1.
- **Caption** (right side, over the desk and cabinets beside the face, starting about 25 px right of the shoulder):
  - L1 "Let's see": Helvetica Regular white, cap 'L' 61 px (y679-740), about 85 px font, x1316-1629.
  - L2 "where we will be": same style, x1325-1911 (**right edge 9 px from the frame edge**), y737-807.
  - L3 "in **three years.**": "in" in sans white x1339-1391; "three years." in **serif, mint #8afbe4**, x1420-1852, y790-907.
  - **Negative leading:** L2 top 737 is above L1 bottom 744; line pitch is about 62-70 px for an 85 px font, so leading is about 0.78.
  - Left edges are ragged-left aligned at x≈1316-1339.
- **Build** (words land spaced, then the gaps contract, like S4):
  - "Let's" visible at f2044 (faint from 2041 inside the blur).
  - "see" at f2045 at x1662 → 1606 (2047) → 1500 (2049) → stays about 1500-1513.
  - "where" about f2048, "we" 2050, "will" about 2054, "be" about 2058, "in" about 2060, "three" 2064, "years." 2067.
  - Spoken: let's 2044, see 2050, where 2053, we 2058, will 2060, be 2063, in 2067, three 2072, years 2078-2082.
- **End:** the caption is complete from f2069. The video ends at f2083, one frame after the voice ends. There is no fade-out and no end card in this part.

---

## 2. B-ROLL INTEGRATION

| # | Frames | Footage (what it shows) | Line | Relation | Integration |
|---|---|---|---|---|---|
| 1 | 1044-1118 | Man at a blue holographic data wall (stock), 3 angles | "analyze / generate weights of neural networks" | Near-literal (AI data hologram) | **Full frame.** Caption overlaid on the empty half, laid over the hologram light band so the type reads as part of the hologram. Caption stays on screen across the 2 angle cuts. |
| 2 | 1119-1165 | Woman in an AR headset shaping a holographic turbine (shutterstock wm) | "This isn't just about improving models" | Metaphor (engineering, improving) | **16:9 card on white**, 602x340, centred, no border, shadow or radius. Words scattered around it in a ring (4 on top, 2 below). The whole page zooms 112.5 → 100% in and 100 → 104% out. |
| 3 | 1166-1263 | 4 surreal portrait clips: floating in space, lying on a grass spiral, lying in a meadow, running on a mirror salt flat | "unlocking an entirely new dimension of AI research" | Metaphor (other worlds / dimensions) | **4 portrait cards (about 183-204 x 324-360) in a 3D Z-stack on #0a0a0a**, diagonal cascade +20-57 px x, +33-66 px y per card, perspective-scaled. The stack orbits about 70 frames on Y (fan → edge-on → mirrored fan → back). Back cards are dimmer. Text blocks sit left and right of the stack and collapse into it at the exit. |
| 4 | 1319-1353 | Iridescent glass hand pinching a crystal in a dark nebula (CG) | "empty space" | Metaphor (void / space) | **Inside the centre cell of a full-frame 3x3 hairline grid** on white; the cell is exactly the footage size (404x434, about square). The words sit in the flanking cells on the row centre line. |
| 5 | 1408-1495 | SaaS motion graphic: app icons and feedback chips flowing into an OpenAI logo, out to a task card | "not only as the output... but as the input for learning" | Metaphor (input → model → output) | **Full frame on white**, borrowed footage used as a band in y≈440-780. Text lines placed above (baseline 306) and below (baseline 827), framing the band. |
| 6 | 1551-1588 | 3D blue CNN layer diagram (cuboids) | "weight space learning" | Literal (network architecture) | **Full-frame CG on the same gradient ground** as the previous title card (seamless). Blocks fly in and assemble in 3 frames. Title overlaps the blocks. |
| 7 | 1589-1627 | Op-art rainbow tunnel | "Can we truly manipulate" | Metaphor (mind-bending, manipulation) | **Large 16:9 card right of centre** (925x521, centre x1246) with a 2-line text block left of it. Then the card **shrinks and slides into the centre cell of a black 3x3 grid** that snaps on aligned to the card's edges. |
| 8 | 1628-1694 and 1853-1876 | Businessman's hands manipulating a green particle neural-net hologram | "edit the behavior of neural networks" | Literal | (a) **In the grid's centre cell** (607x339) with text set into the columns above. (b) **Card on white growing at a constant 0.8%/frame** (531 → 714 px) with a typewriter caption centred below. Both swaps into this clip happen by a **hard cut inside the card/cell** while the frame keeps moving. |
| 9 | 1904-1959 | Hooded hacker at world-map monitors (PFX wm) | "The future of AI is being written" | Metaphor | **Starts full frame, then scales down to a 45.8% card (879x495) on white** over 41 frames (ease-in-out). Caption lives inside the footage layer and shrinks with it. |
| 10 | 1960-1992 | CG hooded mannequin with flying CRT monitors | "one weight at a time" | Metaphor (building piece by piece) | **Same card** (persistent frame, new clip by a hard cut inside it). Card holds, then grows slowly. |
| 11 | 1993-2037 | Two people walking down a Paris street | "Don't miss this insightful conversation" | Metaphor (a conversation / journey) | **Same card**, hard cut inside. Card grows linearly 47.2 → 51.2%; caption centred on the footage. |
| 12 | speaker shots | Guest on webcam | own words | (none) | Always **full frame, never carded**. Captions sit beside the head in the empty background (left over the shelf, right over the window and desk, or bottom-centre over the shirt). Zooms 94-121% are applied to the raw, with blur transitions in and out. |

Watermarks: shutterstock (#2) and PFX (#9) are visible in the reference. That is a reference flaw; do not copy it.

---

## 3. TECHNIQUES (reusable, with measurements)

1. **Two-voice caption (setup + payoff).** Line 1: small sans Regular, white (on footage) or black (on white), often with **wide word spacing** (gaps 0.8-1.7 em). Line 2: the meaning words in a **large narrow serif** (x-height 1.5-2x the sans x-height; e.g. sans cap 45 px vs serif x-height 61 px in S4), set with the space almost removed.
   - Block centred on its own axis: centre x≈458 for left placements, x≈1382-1505 for right placements, x≈960-995 for bottom-centre.
   - Payoff colour over footage = mint #8efde8; on white = black; on dark grounds = white.

2. **Mint emphasis is reserved for speaker shots.** All mint words (entire world, do with weights, exciting, representation, properties of the, modify?, three years.) appear only on the talking head. B-roll and graphic scenes use white, black, or the serif for emphasis.

3. **Word timing.** Each word starts showing **0-8 frames before it is spoken** (typical 3-6). Captions build word by word and **stay complete** until the scene leaves. They never wipe out word by word.

4. **Opacity entry curve (graphic scenes).** The word starts at 25-55% opacity on its first frame, then eases out to 100% in about 8-10 frames (S1, S3). The slow variant on white is about 20% on frame 1, about 60% by frame 4, 100% by about frame 20 (S8). There is no blur on the word itself.

5. **Pop-on words (white page, S2).** Full opacity in 1 frame, no motion, 1 word per beat, scattered in a ring around a centred card: top row 4 words across x223-1736 at y≈230-264, bottom row 2 words at y≈831-871.

6. **Directional word landings (speaker shots).** Each word comes from its own direction and settles with an ease-out over 10-17 frames:
   - from above, 22-33 px ("you", "to")
   - from the right, 50-70 px ("can", "and", "modify?", "see")
   - from the left, 46-88 px ("do", "properties", "of")
   - **rising from below 60-100 px** for the serif payoff words ("with", "weights", "neural network")
   - Converging pairs: "of" from the left and "the" from the right meet in the middle (S13).

7. **Tracking-tighten settle.** Words land with gaps 2-3x too wide and the gaps contract to normal over about 15 frames, ease-out. S4 gaps went 17/51/62 → 24/19/21 px; the same happens in S19.

8. **Text lives inside the camera.** On speaker shots and cards the caption scales and moves with the zoom (in S4 the text even out-scales the camera slightly: 1.16x vs 1.10x). Text is never screen-locked there. On the full-frame hologram (S1) the text is screen-locked across cuts.

9. **Speaker zoom grammar.** Every speaker shot has an entry move, a hold, and an exit move.
   - Entry from the transition: 104-105% → 100% (zoom-out entry) or 96% → 100% (zoom-in entry) over 6-8 frames, ease-out, usually under blur.
   - Hold 5-10 frames.
   - Then either a **punch-in** (100 → 110.4% in 26 frames with 6% in the first 5 frames, S4; 98.5 → 120.9% in 35 frames, S12) or an **ease-in exit** into the cut (100 → 94% in 10 frames, S6; 100 → 103.7% in 6 frames, S7).
   - Fixed points are off-centre, biased toward the caption side (x≈-250 for a left caption, x≈1630-1880 for a right caption).

10. **Zoom-direction match cuts.**
    - S6 leaves zooming out (to 94%) and S7 enters zooming out (105 → 100%).
    - S11's grid leaves shrinking and S12 enters zooming out (103.8 → 97.6%).
    - S5 leaves pushing in and S6 enters pushing in (96 → 100%).
    - S4 leaves zooming out and S5 enters zooming out (cell 409 → 404 px).

11. **Blur-through transition (the main transition).**
    - Outgoing: motion blur builds over 2-4 frames, then 1-4 frames of full Gaussian blur (about 25 px radius, sharpness under 2) on the whole comp, text included.
    - Hard cut (or a 1-frame blurred crossfade, f1749 / f2038).
    - Incoming starts fully blurred and sharpens over 4-6 frames while doing its entry zoom.
    - Total length 6-12 frames. Used at 1263/1264, 1350-1358, 1747-1754, 1875-1883, 2038-2044.

12. **Strobe-invert transition (S7 → S8).** Sequence: negative frame → 2 positive sharp frames → 1 negative blurred frame → 7 positive frames de-blurring → sharp. 11 frames total, used on a beat drop.

13. **Focus-pull title in.** The title card opens fully defocused and the text sharpens and brightens over 9 frames (S9: sharpness 0 → 355, text brightness 125 → 247).

14. **Gradient stage ground.** #131313 top 55%, with two cyan glows (#11aec8 / #10b1cd at the bottom edge, #118a9d mid) rising from the bottom-left and bottom-right corners, leaving a dark V (#123f46 → #131a1a) at the bottom centre. The next CG shot (blocks) reuses the same ground so the cut is invisible.

15. **Line slam-swap.** A title line is replaced in 1 frame by the next line, whose first words slam in from the right 194 px in 4 frames (motion-blurred), then creep 25-40 px further over about 20 frames. Following words arrive by 40-110 px slides (S9).

16. **Decoder/scramble text.** Random glyphs resolve to the title left → right over 12 frames while opacity rises from about 40% to 100% (S10). Then the title scales up anchored on its left edge (1.13x) with accelerating motion blur into the cut.

17. **Card beside text (white page).** Card 925x521 at centre x1246; a 2-line centred text block on the left (centre x≈525), with 24 px between the text and the card. The card enters already moving (1.146x scale-up and +95 px right, 12 frames, ease-out).

18. **Card drops into a grid.**
    - The card shrinks and slides toward the centre over 8 frames (motion-blurred, text cut).
    - A full-frame 3x3 grid (2-3 px black lines) snaps on in 1 frame with its centre-cell lines **exactly on the card edges**.
    - Card and cell keep shrinking together 683 → 601 px over about 50 frames (ease-out), then accelerate out (601 → 505 px) with a 1-frame echo/blend before the cut.

19. **Type set into grid cells.** Caption phrases are distributed across the 3 columns, sitting on the top grid line (baseline 28 px above it):
    - left phrase right-aligned to the left line (16 px gap)
    - middle phrase filling the centre column (5 px from each line)
    - right phrase left-aligned to the right line (7 px gap)
    - A variant (S5) puts single serif words in the left and right cells of the middle row, flanking the footage cell.

20. **Hairline-grid scene (S5).** White ground; 1 px dark-grey lines across the full frame at x767 / 1171 and y322 / 756; footage exactly fills the square-ish centre cell (404x434). The whole layer zooms out 1.6% and pans 20 px left (ease-out, 14 frames), then reverses.

21. **Rotating 3D card stack.** 4 portrait clips in a Z-stack with a diagonal cascade (see the B-roll table #3). A Y-axis orbit of about 70 frames: fan → edge-on column (about 237 px wide) → mirrored fan → back. Eased at each fan pose, motion blur on the fast parts; back cards dimmed (about 60% brightness). Text blocks sit left (left-aligned at x138) and right (right edge x1892) on a shared baseline.

22. **Collapse-to-centre exit.** The flanking text blocks compress (scale down anchored on their outer edges) and slide toward the centre object with rising horizontal motion blur over about 10 frames, then 1 full-blur frame.

23. **Full frame → card shrink.**
    - Full-frame footage scales about the frame centre down to a 45.8% card (879x495) on white over 41 frames: ease-in-out, peak about 5.8%/frame at 60% progress, long ease-out tail. The caption inside scales with it.
    - Then the card **persists** as a frame while footage hard-cuts inside it (2 swaps), growing linearly about 0.09%/frame (45.8 → 51.2% over 65 frames).
    - Captions carry 2-4 frames past each inside-cut.

24. **Constant-speed card push with typewriter caption.** Card grows linearly 0.8%/frame (531 → 714 px over 46 frames) and drifts 46 px left. Below it a serif caption (about 55 px, word gaps about 49 px, baseline 83 px under the card) types on 1 character per 1-1.5 frames, synced to speech, re-centred on the card every frame. 1-frame echo blends every 15 frames.

25. **Letterbox reveal on the final shot.** Black bars 0 → 150 px top and bottom (picture 1920x779, 2.46:1) over 12 frames, ease-out (12/46/87/109/123/132/138/143/145/147/149/150), together with a gentle zoom-in toward the caption side.

26. **Final 3-line stacked caption.** Right side; ragged-left at x≈1316-1339 with the right edge 9 px from the frame; about 85 px sans with **negative leading (about 0.78)**; the last line ends with a mint serif payoff ("three years."). It builds word by word with the tracking-tighten settle and holds to the last frame (no fade-out).

27. **Flat finish.** No grain, no vignette, no glow or shadows on type or cards, hard-edged cards (no border or radius). Motion blur on fast moves and Gaussian blur only for transitions. The polish comes from the moves, spacing and type pairing, not from overlays.

28. **Rhythm.** B-roll scenes run 1.4-4.4 s (median about 2 s); speaker inserts 1.1-3.3 s. The pattern alternates: B-roll scene → speaker → 1-2 B-roll scenes → speaker. Card or grid scenes chain on white; dark scenes chain on near-black; speaker shots act as the bridge between them.

Evidence files (in `refs/zoom_twB/`): `f<frame>.jpg` full-res stills of every shot, `grid_*` per-frame contact grids of every transition and build, `strip_*` caption reveal strips, and `crop_*` zoomed type and edge details.
