# TWIML trailer study, part A: frames 0-1043 (0.00-43.46 s)

Source: `/Users/gourav/jl-trailer/refs/dl/twiml_trailer.mp4`, 1920x1080, 24 fps.
How this was measured: all 29 every-frame sheets (`sheets/all_tw/00-28.jpg`) were read. About 340 full-res stills plus crop sheets are in `refs/zoom_twA/`. Positions come from pixel masks and bounding boxes on the 1920x1080 frames (OpenCV): text masks, card blobs, grid-line scans, YuNet face boxes for head position and size, ORB similarity for camera scale, and Laplacian variance for blur.
All coordinates are full-frame px (x right, y down). "f" = frame number (file 00001.jpg = f0). Word times come from `twiml_words.json`.

Useful crop sheets in `zoom_twA/`: `sheet_typeon.png`, `sheet_logos.jpg`, `sheet_perp1.jpg`, `sheet_gridwords_a/b.jpg`, `sheet_truerev.jpg`, `sheet_wipe.jpg`, `sheet_collage.jpg`, `sheet_blurs.jpg`, `sheet_wordentry_left/right.jpg`, `sheet_th1a_text.jpg`, `sheet_th1cd.jpg`, `sheet_ui.jpg`, `sheet_invert_grid3.jpg`, `sheet_negflash.jpg`, `sheet_astro.jpg`, `sheet_th2d.jpg`.

## 0. Global system (applies to every shot below)

- **Two worlds alternate.** (a) Dark full-bleed footage: talking heads (TH), cinematic B-roll, logos. (b) A flat paper-white ground, #FDFDFD, completely noise-free (std 0.0), holding a single B-roll card plus black type and hairlines. The edit alternates TH → white-ground card → TH. Of the 30 beats in this half, 9 are white-ground graphics.
- **Type system** (two families only):
  - **Sans.** Helvetica Neue Regular-like neo-grotesque, almost always lowercase. Tracking is tight: word spaces sometimes nearly close up ("productof", "thinkabout"). Used for the connective words.
  - **Serif.** A condensed Garamond/Times-like roman (ITC Garamond Condensed feel), used for emphasis words. An italic variant of the same family appears on TH1a "weights as". A higher-contrast italic appears on the collage "very essence?" and the grid-1 words "But" / "if".
  - **Bold sans** appears once ("weights" on the hologram, f1040).
  - No type is heavy or all-caps.
- **Colour.**
  - On footage: white #FEFCFA for the sans, mint #8BFBE6 (RGB 139,251,230) for the serif emphasis word. No drop shadow, no glow, no stroke.
  - On white ground: type is #0C0A0E. The serif on the collage is #2E2E2E.
  - Accent cyan #19ECEC (typed text in the dark card) and #1EF2F6 (UI button).
  - Hairlines are #1D1D1D, about 2 px core plus anti-alias.
- **Legibility on footage** comes from a **dynamic side-shade gradient** (Technique 9), not from shadows or boxes.
- **Text on talking heads is parented to the footage.** Every camera reframe, zoom and blur moves, scales and blurs the captions with the picture (measured in TH1b, TH1e and TH2d).
- **Finish.** No letterbox, no film grain on graphic grounds (pixel std 0.0 on #FDFDFD, #131313 and #000), no light leaks, no global vignette.
  - Motion blur is on every fast move: card shrink f72-74, collage fly-in f127-131, robot card slide f690-691, button zoom f495-498.
  - Gaussian/defocus blur is the main transition tool.
  - One-frame colour-negative ("invert") frames and blocks are a recurring glitch motif (f63, f78-82, f123-126, f574-576, f1025).
- **Caption timing.** Caption words usually appear 0-6 frames **before** the word is spoken. Some phrases are laid out whole at the start of a shot (salt-flat grid, TH1c), up to about 22 frames early.

## 1. SHOT LOG

### S01: f0-18 (0.00-0.79 s). City time-lapse plus type-on title
- **Words:** "For years," (0.00-0.58).
- **Picture:** full-bleed time-lapse of a Moscow highway, light-trail cars, storm-cloud sky, city skyline. Dark, desaturated grade.
- **Text:** "For years", white #F9FCFE, Helvetica Regular. Cap height 67 px (F top y513 → baseline y580). Final bbox x811-1176, y513-600. Centre x≈994 (34 px right of frame centre), cap centre y≈547.
- **Type-on:**
  - f2 "F" (f3 slightly dimmer), f4 "For", f8 "For ye", f10 "For yea", f11 "For year", f12 "For years". That is about 1 character per frame across f2-f12.
  - The text is centre-anchored, so every new letter shifts the whole word left by half a glyph width.
  - No cursor, no fade per letter. Typing is synced to speech ("For" f0-6, "years" f6-14).
- **Camera:** push-in measured by ORB. Scale 1.000 (f0), 1.0006 (f8), 1.004 (f12), 1.025 (f18): about 2.5 % in 18 frames, ease-in (accelerating) into the cut.
- **Out:** hard cut at f19.

### S02-S06: f19-62 (0.79-2.62 s). AI-logo montage (hard cuts)
- **Words:** "we've understood AI models through their outputs."
- **Cadence:** cuts at f19, 32, 41, 51, 57, 63, giving shot lengths of **13, 9, 10, 6, 6 frames** (accelerating).

| Shot | Frames | Logo / ground | Size and position | Scale move |
|---|---|---|---|---|
| S02 | f19-31 | OpenAI white knot on #000000 | 344x348 → 365x370 px, centre (946, 557) | Push-in +6 %: first frame jumps +2.3 %, then +1 px/frame (ease-out). f19 is slightly soft (1 frame). |
| S03 | f32-40 | Mistral AI pixel-M plus white wordmark on #000 | 949x150 → 1020x162, centre (979, 540) | Push-in +7.5 %, **ease-in**: +3 px/frame, then +10, +24 on the last frames. |
| S04 | f41-50 | Claude orange asterisk plus white serif wordmark on #000 | 633x574 → 672x610, centre (979, 553) | Push-in +6 %, ease-out (+7, +6, +9, then +4, +3, +2, 0). |
| S05 | f51-56 | "Command A" white wordmark over a full-bleed red→teal abstract 3D render (#B53C30 top, #0F5644 bottom) | full frame | Holds 3 frames, then **pulls out** 0.75 % over f54-56, anchored on frame centre. |
| S06 | f57-62 | Photo of a phone showing the Copilot logo in front of red/green/blue/yellow tiles, full bleed | full frame | **Pull-out** 3.1 %, accelerating (0.997, 0.992, 0.982, 0.976, 0.969), centre-anchored. |

- **Pattern:** three push-ins, then pull-outs. The pull-out continues straight into S07, which is how the reference sets up the card shrink.

### S07: f63-122 (2.62-5.12 s). Perplexity logo shrinks into a card in a 3x3 grid; grid words; type-on
- **Words:** "outputs. / But what if the true revolution".
- **f63-66, full frame to card.** The Perplexity slate (#081714 ground, white wordmark, teal icon) is already at 97.7 % scale (1876x1053) on a **black** ground and keeps shrinking: 1842 → 1821 → 1799 px wide.
  - **f63 has a 1-frame invert block.** A pale-pink rectangle (#F2E6E8, the colour negative of the slate) sits over the letters "pe", about x 750-850 / y 440-600, and the letters inside it read as dark.
- **f67, ground swap.** The ground behind the card switches from black to **white #FDFDFD**. White covers 15 % of the frame. The card edge shows a 1-2 px bluish rim from compression; there is no stroke.
- **Card shrink curve (card width per frame; height stays 16:9):**
  - f67: 1764; f68: 1708; f69: 1676; f70: 1637; f71: 1594.
  - f72: 1461; f73: 1307; f74: 1043. Peak speed is −264 px/frame, with heavy horizontal motion blur on f72-73.
  - Ease-out tail: f75: 1000; f76: 957; f78: 932; f80: 905; f84: 882; f90: 864; f96: 856; f102: 849 (settled).
  - **Final card:** x546-1395, y300-780 (849x480), centre (970.5, 540).
  - Total move from f63 to f102 is about 39 frames: fast in the middle (f72-74), long exponential settle.
- **Grid (3x3, hairlines through the card edges, extending to the frame edges):**
  - Lines pop on in single frames; they are not drawn on. Verticals first, at f75-76. Then the bottom horizontal at f79, then the top horizontal at f83. Lines are about 2-3 px, #1D1D1D.
  - Lines ride the shrinking card: the left vertical moves x492 (f76) → 545 (f100).
  - Settled lines: verticals x≈544/1396; horizontals y≈302 (left) → 298 (right) and y≈776 → 780.
  - Slight **3D perspective**: the right column is 8 px taller than the left, so the plane is turned a fraction of a degree in Y.
- **Grid words (outer cells, each sitting on a grid line, near the cell's horizontal centre, nudged toward the card):**
  - "**But**": serif **italic**, black, cap B 53 px, x262-368, baseline y771 on the bottom line. Bottom-left cell, **appears f76**.
  - "**what**": sans regular, ascender 53 px, x242-413, baseline y292 on the top line. Top-left cell, **appears f78**.
  - "**if**": serif italic, x1621-1670, y218-291. Top-right cell, **appears f80**.
  - "**the**": sans regular, x1577-1687, y705-769. Bottom-right cell, **appears f82**.
  - Reading order is a zig-zag (BL → TL → TR → BR). Styles alternate serif-italic / sans.
  - Words pop in every **2 frames**, ahead of the audio (spoken at f77, 81, 87, 93).
  - **Entry glitch:** on each word's first frame a black rectangle covers part of it with the letters knocked out white (an inverted box: "wha" in f78, the box right of "if" in f80, "he" in f82). The next frame is plain black text.
  - Because the camera is still pulling out, words drift toward centre until f102 ("what" x180 → 242).
- **Hold:** f102-116 is a full freeze of the layout (no motion).
- **Type-on inside the card:**
  - "true revolution": sans regular, cyan **#19ECEC**, centred in the card. Final bbox x741-1205, y495-560, ascender about 38 px.
  - f96-97 the logo is gone and the card is empty. Then f98 "t", f100 "tru", f102 "true", f104 "true r", f105 "true re", f106 "true rev", f108 "true revol", f110 "true revolu", f111 "true revolut", f112 "true revoluti", f113 "true revolutio", f114 "true revolution".
  - About 1 character per 1-2 frames, re-centring as it grows. Synced to "true" f97-103 and "revolution" f103-116.
- **Teardown (single-frame pops):**
  - Words: "But" off f109, "what" off f111, "if" off f112, "the" off f115.
  - Lines: top horizontal off f117, bottom horizontal off f121, left vertical off f124, right vertical off f128.

### S08: f123-126 (5.12-5.29 s). Invert-block shatter transition
- **Words:** "lies" (f116-126).
- **f123:** the card's bottom 87 px band (y≈693-780) becomes inverted (#F2E6E8); the dark area is now y300-693.
- **f124:** the lower-right quadrant of the card (x976-1393, y≈395-780) is inverted. "true revolution" turns **red #DB0E0E** where it crosses the inverted block (red is the negative of #19ECEC).
- **f125:** the card is reduced to a dark top strip (x544-1395, y300-493) plus an inverted lower-left block (x544-976, y493-690) holding red "true rev". Small grey sans "lies" appears at x≈600, y≈495.
- **f126:** dark block x544-966 / y300-491 next to an inverted block x968-1393 / y300-491. "lies" sits under it.
- **f127:** the first photo replaces the blocks (next shot). One remnant inverted block shows to its right (x≈860-970).

### S09: f127-172 (5.29-7.21 s). Three-photo collage with colour-flipping type
- **Words:** "hidden within their very essence?"
- **Fly-in (motion blur):**
  - f127: photo C (overhead shot of hands on a laptop, warm brown) appears at x464-858, y163-561.
  - f128-129: photo B (backlit man, blue) flies in from lower right with heavy blur.
  - f130: photo A (silhouette at a train window) appears behind C.
  - f131-132: the cards re-shuffle into their final arrangement.
- **Expansion:** the collage's outer extent grows from 761 px (f132, x394-1155) to 910 px (f147, x301-1211). That is ×1.2, ease-out over 15 frames.
- **Hold:** f147-167.
- **Exit:** a leftward move starts f168 (x300 → 265 at f172, accelerating) with slight skew, and sharpness drops f170-172. Hard cut at f173.
- **Final cards (f160).** No border, no radius, **no shadow** (edges go to #FDFDFD within 2 px). Each card is rotated about 1° (card A's top edge runs y154 at x490 → y160 at x860).
  - A, silhouette at a train window (dark/teal): x478-876, y154-557 (≈398x402).
  - B, backlit man (blue): x301-640, y401-800 (≈339x399).
  - C, laptop overhead (warm): x802-1200, y291-693 (≈398x402).
  - Z-order: C over A over B. The cards overlap 75-130 px.
- **Type:**
  - "lies hidden": sans white, x932-1191, y487-530 (inside card C, against its right edge).
  - "within their": sans **black #0C0A0E**, x1285-1550, y486-530 (on white, same baseline about y530).
  - "very essence?": **serif italic display**, big. x≈875-1612, y≈520-668, x-height about 60 px, "?" about 110 px tall. It sits 0-10 px below the small line, overlapping it.
  - **The colour flips at the card edge:** white where it lies over photo C ("very e"), #2E2E2E where it lies over the white ground ("ssence?"). This is a track-matte split, done per pixel.
- **Word entries** (each fades from about 30 % to 100 % over 2-3 frames, in place): "lies" f125, "hidden" f129, "within" f135, "their" f141, "very" f146, "essence?" f152.

### S10 (TH1a): f173-188 (7.21-7.88 s). Guest 1 close-up, caption right
- **Words:** "We think about weights".
- **Framing:** bald guest with headphones, against a beige wall (#AAA48E). Face centre x≈725-787 (left of centre), y≈465-496. Headphone span x≈384-1040 (≈605 px). Shoulders fill the bottom.
- **In:** cut at f173 into a frame with heavy zoom/defocus blur. There are echo rings of the head; sharpness index goes 2 → 4 → 10 → 115, so it is clear by f176. During this the face slides left x827 → 725 and settles −6 % in size (the tail of a whip from the collage).
- **Caption block (right side, left-aligned at x≈1240):**
  - "we" (f173, still blurred): x1243-1345, y452-498.
  - "think" (f176).
  - "about" (f178). It enters blurred, about 30 px to the right, and slides left to close the gap by f180.
  - "**weights as**" (f180): **mint serif italic**, x1233-1791, y560-711. x-height 76 px ("w"), ascender-to-descender 150 px. It enters about 25-35 px low, blurred, and rises into place by f182.
  - Leading is negative: the white lines touch each other, and the mint line's ascenders touch the white line above.
- **Side shade:** right edge, fading in f179-181 (edge luma 140 → 62 → 50) when the mint word lands.
- **Out (f184-188):** blur ramp (sharpness 101 → 2). The camera slides right and pushes (face x761 → 899, width +11 %), with a ghosted zoom-echo at f188. The caption is blurred along with the picture.

### S11 (TH1b): f189-283 (7.88-11.83 s). Guest 1 medium shot, caption left, then a second caption right
- **Words:** "as the product of training a model, but the".
- **In:** cut f189 into a **wider** framing (headphone span ≈520 px vs 605). The face continues the rightward slide x1013 → 1088 by f198 (ease-out). Defocus clears over 8 frames (sharpness 3, 7, 42, 71, 88, 99, 114, 135, 146).
- **Framing:** face centre x≈1060-1150 (right of centre), eye line y≈450-490.
- **Left caption block** (lines centred on one another, ragged; block centre x≈420):
  - "the" (f197): x300-425, y450-522.
  - "product" (f202) / "of" (f207): line x270-660, y≈459-608.
  - "**training**" (f235): mint **upright** condensed serif, x226-615, y598-729. x-height 71 px ("r"), "t" 85 px.
  - "a" (f240) / "model" (f244): x257-527, y723-775.
- **Word entry:** first frame blurred (f197 "the", f202 "product"), sharp on the 2nd frame. New lines rise from below: "training" y618 → 596 over f237-255 (22 px, ease-out).
- **Block breathing:**
  - "product of" width goes 327 (f214) → 358 px (f248), ×1.095, eased (fastest f224-232).
  - It shrinks back ×0.96 over f270-282.
  - This matches a slow camera push-in then pull-back, and the text moves with the footage.
- **Second block, right:** "but" (f270) and "the" (f276), mint condensed serif, x1446-1755, y573-668.
  - Each word fades over 3 frames: about 55 % → 80 % → 100 % ("but" f270-272, "the" f276-278).
- **Side shade:**
  - Left fades in f200-216 (edge luma 133 → 53, ease-in-out) and holds about 45.
  - Right fades in f264-272 (153 → 60), starting about 6 frames before "but".
  - With both on, the frame is dark at both edges.
- **Out:** f283 is a 1-frame full blur, then a hard cut to the grid.

### S12: f284-323 (11.83-13.50 s). Salt-flat video card in a 3-column grid
- **Words:** "idea seems to be that" (f278-328). All words are on screen from f284; no per-word animation.
- **Card:** portrait video, about 4:5: a boy walking on salt-flat stones under a cumulus cloud with a perfect sky reflection (the clip plays).
  - f285: x687-1376, y108-977.
  - Settles to x692-1366, y117-968 (674x851) by f300: −2.2 %, ease-out.
  - Holds f300-315.
  - Then pushes in, accelerating: f318 x691-1369; f320 690-1371; f322 687-1374; f323 680-1385, y97-988 (+5 % in 8 frames) into the cut.
- **Grid:** verticals at the card edges, horizontals at y≈117/968, running to the frame edges. About 0.15° off level (left 117, right 112).
- **Text:** black condensed serif roman (Times/Garamond-condensed), x-height 34 px, ascender 50 px, baseline y≈557 (vertically centred on the frame and card).
  - "idea  seems": x319-621, right-aligned 71 px from the card's left edge.
  - "to  be  that": x1425-1693, left-aligned 59 px from the card's right edge.
  - Word spacing is about 1.5-2 normal spaces (≈45-60 px gaps).
- **In:** f284 slightly soft (1 frame), sharp from f285.
- **Out:** the push-in above, then a cut to TH1c.

### S13 (TH1c): f324-354 (13.50-14.79 s). Guest 1, caption left
- **Words:** "there's so much more that".
- **In:** f324 is one fully blurred frame; sharp at f325.
- **Framing:** face centre x≈1060-1072, eye y≈467. Headphone span x795-1329.
- **Caption** (left-aligned at x≈205, set at shot start with 1-frame stagger: f324 "there's so", f325 "much", f326 "more", f327 "that"):
  - "there's so": white, x211-478, y488-535. "t" is 46 px, x-height 34 px.
  - "**much**": **mint sans** (not serif), x201-503, y536-635. x-height 72 px, "h" 97 px.
  - "more  that": white, x205-492, y651-701.
- **Side shade:** left, fading in f324-336 (115 → 52).
- **Out:** see S14 (whip reframe).

### S14 (TH1d): f355-398 (14.79-16.62 s). Guest 1 reframed left, caption right
- **Words:** "we can learn from these weights."
- **Transition in (f350-360):** a horizontal whip-reframe with blur dip (sharpness 167 → 50 → 121). The face moves x1046 → 908 at the cut (f355) and continues to 886 by f359, ease-out. Total −160 px. The old caption exits with the camera, smeared.
- **Framing:** face centre x≈840-890 (left of centre).
  - Head grows f355-375 (headphone span 553 → 619 px, push-in about 12 %, ease-out).
  - Then eases back to 585 px by f395.
- **Caption (right side, lines roughly centred on x≈1520-1560):**
  - "we" (f352) / "can" (f355): x1455-1668.
  - "learn" (f358) / "from" (f359): x1363-1684. White lines y443-533 overall.
  - "**these**" (f362) / "**weights**" (f364): mint **sans**, x1193-1831, y534-645.
- **Side shade:** right (edge luma about 52).

### S15 (TH1e): f399-430 (16.62-17.96 s). Guest 1 centred, bottom subtitle question
- **Words:** "Is that the general thought?"
- **Transition (f396-411):** zoom-out plus pan reframe with mild blur, cut hidden at f399. Face x843 → 1007, face width 403 → 328 (−19 %). Then a slow push back in to face width about 364 by f426 (+11 %).
- **Subtitle:** one line, centred at x≈939.
  - "Is that the general" in white sans and "**thought?**" in **mint sans**.
  - Settled bbox x519-1359, y964-1035. Cap "I" 53 px, x-height ≈40 px.
  - Builds left → right per word: "Is that the" f399, "general" f400 (grey → white over 2 frames), "thought?" f406.
  - It is parented to the footage: it rises from y998 (f400) to y964 (f424) and shrinks ×0.967 with the camera move.
- **Shade:**
  - Right side fades out f394-407 (70 → 137).
  - A **bottom shade** fades in f399-408 (bottom-row luma 64 → 33).
- **Out:** hard cut at f431.

### S16: f431-498 (17.96-20.79 s). 3D floating-UI scene, "Join" button click, zoom-through
- **Words:** "Join us as we dive into a groundbreaking concept".
- **Ground:** #131313 in the upper 60 %, with a cyan glow rising from the bottom (bottom-right ≈#11A6BE). A dark radial pool sits under the button.
- **Elements:** floating cards rotated in 3D around a centre pill button:
  - photo of two men in a meeting, tilted, lower left;
  - purple 3D product card, upper left;
  - grey particle sphere, upper right;
  - red tilted card, right;
  - blue 3D bar-chart card, bottom centre.
- **Button:** "Join" pill, cyan #1EF2F6, white sans label, white 2 px rim, soft cyan glow.
- **In:** hard cut into a defocused frame (sharpness 2 for f431-434), clearing by f439 (8 frames).
- **Camera:** slow push-in. The button grows 201x65 px (f431, centre ≈975,550) → 287x97 (f488): ×1.43 over 57 frames, eased. The side cards drift outward.
- **Cursor:**
  - A white arrow appears about f437, about 120 px below the button (≈x978, y683).
  - It glides up to the button centre by about f470 and switches to the **hand pointer** at about f470 (on "groundbreaking").
- **Click:**
  - Button squashes 287 → 246 px wide (−14 %) over f489-491.
  - The "Join" label fades out f491-494.
- **Zoom-through:** the button scales about ×1.3 per frame: f494 335 px, f495 461, f496 571, f497 749, f498 about 1300.
  - The side cards fly off-frame (gone by f497).
  - Motion blur: sharpness 327 → 64 → 35.
- **Out:** S17.

### S17: f499-504 (20.79-21.04 s). Cyan fill → white flash
- f499: the button interior fills the frame (#28E9EE), with its white rim visible as bands near the top and bottom edges.
- Fade to paper white over 4 frames: f500 #59F9FA, f501 #A5FCFA, f502 #E2FEFD, f503-504 #FDFDFD.

### S18: f505-576 (21.04-24.04 s). Portrait underwater-diver card in a grid, right-aligned text
- **Words:** "that's / redefining our understanding of artificial intelligence."
- **Card:** a **9:16 video** of a diver or astronaut sinking among floating rocks, teal water.
  - Pops on at f505 at 199x345 (x870-1069, y373-718).
  - Grows to 255x449 (x842-1097, y316-765) by f530: ×1.29, ease-out over 25 frames. Static after that.
- **Grid:** verticals pop with the card at f505; horizontals pop at f506. Lines follow the card edges (f506 y368/721 → y316/762).
- **Text** (right-aligned to x≈797, 45 px from the card's left edge):
  - Line 1, "redefining our understanding of": sans regular black, x407-797, y570-598. x-height 15 px, ascender 21 px.
  - Line 2, "artificial intelligence.": condensed serif roman, x400-797, y615-668. x-height 27 px, ascender 36 px.
  - The block sits just below the card's vertical centre (y570-668 against a card centre of y540).
  - Per word: "redefining" f508, "our" f514, "understanding" f520, "of" f527, "artificial" f532, "intelligence." f539. Each fades in light grey → black over 3-4 frames.
  - Because the text is right-aligned, each new word pushes the earlier words left.
- **Teardown and transition out:**
  - Horizontals off at f570, left vertical off at f572. The right vertical stays.
  - f574: the card becomes a **colour negative** (blue → orange/white).
  - f575-576: the text block region is inverted (black box behind white text, x≈780-1000 at sheet scale; a box around both lines).
  - Hard cut at f577.

### S19 (TH2a): f577-636 (24.04-26.54 s). Guest 2 (office), captions right then left
- **Words:** "What happens, actually, if we take the weights".
- **Framing:** blond guest with glasses in an office: dark bookshelf on the left (#1F211F), window blinds behind. Face centre x≈1005-1025, eye y≈403-437, face width about 335 px.
- **In:** hard cut into a defocused frame. Sharpness 4, 5, 7, 8, 11, 16, 52, 134, 441: ease-in clearing that is sharp at f585 (8 frames).
- **Camera:** push-in about 4 % over f580-596, ease-out.
- **Right caption:**
  - "What happens" (f580-582, inside the blur): white sans, x1370-1844, y490-561. Cap "W" 55 px.
  - "**actually**" (f596): mint condensed serif, x1357-1818, y560-719. x-height 89 px.
- **Left caption:**
  - "if" (f602) / "we" (f605): white, x395-560, y469-525.
  - "**take**" (f607), "**the**" (f609), "**weights**" (f611): mint serif, x214-745, y532-628.
  - Lines are centred on each other (centres x≈477/480).
- **Side shade:** right fades in f591-599 (102 → 44) as "actually" lands. The left is naturally dark (bookshelf).
- **Out:** f634-641 blur plus push. See S20.

### S20 (TH2b): f637-686 (26.54-28.62 s). Guest 2 closer, caption left
- **Words:** "of trained neural networks as the input".
- **Transition in:** blur f634-641 (sharpness 5 → 87, sharp f642). Across the cut the camera zooms ×1.244 and slides the face right (x1035 → 1157). The caption "of" appears inside the blur at f636.
- **Framing:** face width about 430 px, face centre x≈1140-1210.
- **Camera:** pull-out 2.6 %, ease-in. Scale 1.000 (f649), 0.995 (f670), 0.978 (f684), 0.974 (f686).
- **Caption (left; lines centred on one another, block x371-962):**
  - "of trained" (f640): white sans, x460-785, y458-519.
  - "**neural networks**" (f642/648): mint serif, smaller, x371-835, y528-585.
  - "as the" (f665/669): white, x437-645, y601-661.
  - "**input**" (f673): mint serif, **big**, x677-962, y580-736. x-height 75 px, "i" 120 px.
  - "input" shares a baseline with "as the" and overlaps the line above.
- **Side shade:** right fades out f636-648 (60 → 106). The left is naturally dark.
- **Out:** hard cut at f687.

### S21: f687-756 (28.62-31.54 s). Robot portrait card in a grid, captions either side
- **Words:** "to train a neural network to understand these weights".
- **Card:** 2:3 still or video of a white android with code overlays. Its lighting turns red/magenta from f699 (shift in the clip over f699-703).
  - Enters at f687 **off-centre right**: x959-1349 (390x577), centre x1154.
  - Slides left (f690 x936; f691 x856, a big step with motion blur, sharpness 158; f696 x819).
  - Settles at x787-1143, y277-805 (356x528), centre (965, 541) by about f730. Scale ×0.93.
- **Grid:** horizontals at the card edges from f687 (y253/828 → 277/805); verticals ride the card edges.
- **Left block** (lines centred on each other, centre x≈495, block right edge x743, 44 px from the card):
  - "to train a": sans regular, x367-625, y425-480. x-height ≈38-40 px.
  - "**neural network**": condensed serif, x248-743, y485-555. x-height ≈45 px.
  - The block sits in the upper half of the card height.
- **Right block** (centred, block left edge x1226, 83 px from the card):
  - "**to understand**": serif, x1226-1678, y572-641.
  - "these weights": sans, x1289-1636, y654-711.
  - The block sits in the lower half, so the two blocks form a diagonal reading line.
- **Per-word fade** (light grey → black over 2-3 frames): "to" f692, "train" f695, "a" f698, "neural" f700, "network" f703, "to" f714, "understand" f721, "these" f728-731, "weights" f735-738.
- **Out:** f755 the whole grid frame blurs instantly (sharpness 1009 → 2). Cut at f757.

### S22 (TH2c): f757-783 (31.54-32.66 s). Guest 2, caption left
- **Words:** "that we have out there".
- **In:** blurred, clearing over f757-763 (sharpness 5 → 281).
- **Framing:** face width about 370 px, centre x≈910-937.
- **Camera:** push-in 0.9 %, ease-out.
- **Caption (lines centred on each other):**
  - "that" (f759) / "we" (f763) / "have" (f765): x250-640, y477-530.
  - "**out**" (f767) / "**there**" (f771): mint serif, x225-696, y527-639. x-height 75 px.
- **Exit:** the caption disappears with the first punch-in cut at f784.

### S23: f784-807 (32.66-33.66 s). Triple punch-in on "much, much better"
- **Words:** "much, much better." ("much," spans f785-792; "much" f795; "better" f797-805).
- **Three hard-cut scale steps, 4 frames apart, with no caption:**
  - f784: ×1.089. Re-centred so the face jumps from x937 to x1072 (it moves to the right third).
  - f788: ×1.119, centre-anchored.
  - f792: ×1.058, centre-anchored.
  - Cumulative ×1.291 (face width about 375 → 520 px).
- **Then:** f792-807 slow pull-out 1.5 %, ease-in (accelerating) into the hard cut at f808.

### S24: f808-863 (33.66-36.00 s). Full-frame B-roll collapses into a portrait card; content swap
- **Words:** "Imagine a world where AI can analyze".
- **Picture:**
  - f808-854: an astronaut floating in an armchair before a dark wall of framed paintings.
  - f855-863 (hard cut **inside** the frame): an aquarium with a diver or astronaut seated in front of a huge tank.
- **Frame collapse:**
  - f812 onward: the **right edge** crops in (1914 → 1818 by f830, ease-in).
  - From f831-832 **both side edges** crop in, while the content zooms out inside (the astronaut shrinks). Card stays full height (1080). Width: f832 1649 (x150-1799); f840 1506; f848 1329; f856 1101; f860 949; f862 875 (x530-1405). The move accelerates.
  - The left 0-40 px of f816-830 shows a grey strip (the cropped edge of the clip).
- **Text inside the footage** (scales with it):
  - "Imagine a world where AI can analyze": small white sans with **wide word spacing** (≈40 px gaps).
  - At f850: x602-1183, y505-540, cap "I" about 30 px.
  - Left-aligned, words appended to the right: "Imagine" f812, "a" f822, "world" f828, "where" f835, "AI" f842, "can" f849 (grey → white over about 3 frames), "analyze" f857.
  - The text sits across the astronaut's chest.
- **Out:** blur f861-868 (sharpness 2) hides the change to a floating card.

### S25: f864-937 (36.00-39.04 s). Floating 9:16 card with parallax graph-paper grids, underline
- **Words:** "and even generate the very building blocks of other AI."
- **Card:**
  - f864 detaches from the top and bottom: x705-1224, y82-998 (519x916), blurred.
  - Shrinks with an ease-out to 350x621 at x788-1138, y229-851 (f930), centre (963, 540). Widths: 464 (f866), 420 (f870), 393 (f876), 383 (f880), 360 (f900), 354 (f912), 350 (f928).
  - Content: aquarium until f905, then a **hard cut inside the card at f906** to an astronaut lying in a red poppy field at dusk.
  - The tiny "Imagine a world where AI can analyze" line stays inside the card (about 14 px x-height at x862-1063, y535).
- **Graph-paper grids** (thin black lines on white, no fill) that dolly with **more parallax than the card**, so they read as nearer to the camera:
  - **Small grid, left.** Enters blurred from the left at f865 (motion-smeared). f870: x71-380, y398-705 (309 px). Settles at x387-586, y448-647 (199 px; 9x9 cells ≈22 px) by about f930. Scale ×1.55 → 1, versus ×1.2 for the card over the same span.
  - **Large grid, right.** Enters from beyond the right edge at f874 (x1834+, y212-839, motion-smeared). Settles at x1323-1752, y325-755 (429x430; 9 columns ≈47 px, 10 rows ≈43 px) by about f930. Scale about ×2.0 → 1.
- **Text (sans regular, black):**
  - "and even generate": x521-764, y505-549 (x-height ≈24 px). Right edge 24 px from the card; overlaps the right half of the small grid.
  - "the very building / blocks of other AI.": two lines, x1236-1664, y470-599 (ascender ≈45 px, x-height ≈33 px). Overlaps the left half of the large grid and overhangs it to the left by about 90 px.
  - Word fades (grey → black, 2-3 frames): "and" f871, "even" f875, "generate" f880, "the" f896, "very" f900, "building" f904, "blocks" f907, "of" f911, "other" f914, "AI." f919.
- **Hand-drawn underline** under "blocks of other AI.":
  - Black marker stroke, about 8-10 px thick, slightly bowed and tapered, at y≈600-613.
  - Writes on left → right from x1261 (f907) to its full length x1233-1642 by f923. Lengths: 4, 12, 91, 91, 157, 219, 264, 294, 336, 351, 364, 372, 386, 392, 396, 400, 404 px.
  - That is 16 frames, ease-out (fastest +45-60 px/frame over f910-915).
- **Out:** S26.

### S26: f938 (39.08 s). One-frame zoom-echo flash
- The card's content (astronaut, flowers, and the "Imagine a world..." line) is shown blown up about **×4.3** (x220-1720, full height) at about 50 % opacity over the whole grid composition. The result is washed-out pastel.
- Hard cut to S27 at f939.

### S27 (TH2d): f939-993 (39.12-41.42 s). Guest 2 wide, then reframed; caption right, running off-frame
- **Words:** "We do the same idea on all the weights".
- **Framing:** f939-949 wide (face width about 312-329, face x≈1002-1026).
- **Blur pulse with reframe (f950-957):** sharpness 5-29; the cut is hidden at about f957-959. The face slides left x1012 → 855 and zooms ×1.12. The caption blurs with the picture.
- **Caption (right):**
  - "We" (f942), "do" (f947), "the same" (in the blur).
  - Settled "We do the same": white sans, x1281-1817, y515-572.
  - "**idea**" (f960), "**on**" (f966), "**all**" (f972), "**the**" (f978), "**weights**" (f978-984): mint serif, x1080 → **beyond the right frame edge** (clipped at 1919), y584-689.
  - The clipped mint line deliberately bleeds off the frame.
- **Side shade:** right, about 49-51 at the edge.
- **Out (f987-1001):** whip right with blur. The face moves x851 → 1261 (about +410 px); sharpness 309 → 4 (f994-998) → 181 (f1002); the cut is hidden at f995. The caption moves right and off frame with the picture.

### S28 (TH2e): f995-1024 (41.46-42.71 s). Guest 2 framed right, single-line caption left
- **Words:** "of trained neural networks,".
- **Framing:** face centre x≈1260-1340 (right third), face width about 400-425. Camera ×1.01 (slight push).
- **Caption:** one line, baseline y≈530.
  - "of" (f996, in the blur), "trained" (f999): white sans, x164-460.
  - "**neural**" (f1003), "**networks**" (f1006): mint serif, x487-968, x-height 41 px.
  - The words keep the same x-height feel; here the emphasis is colour only, not size.
- **Side shade:** right fades out f995-1007 (58 → 138).
- **Out:** S29.

### S29: f1025 (42.71 s). One-frame colour-negative flash
- f1025 is the exact negative of f1026 (mean absolute difference from 255−f1026 is 5.5): an orange/white negative of the hologram shot. Hard cut.

### S30: f1026-1043+ (42.75-43.46 s, continues past this part). Hologram B-roll with text on the display
- **Words:** "so we can analyze weights of".
- **Picture:** a man seen from behind (left 40 % of the frame) facing a floating blue holographic data display (x≈350-1690, y≈240-650) in a dark room.
- **Focus:** soft at the start, sharpening steadily (sharpness 22 → 104 over f1026-1043): a slow rack-focus in.
- **Text** (laid on the hologram's right half, not on the person):
  - "so" (f1027), "we" (f1031), "can" (f1034), "analyze" (f1037): white sans regular with wide word spacing (≈40-50 px gaps), x1150-1610, y437-475.
  - "**weights**" (f1040): **bold** sans, light grey-white, x955-1283, y510-572.
  - "of" (f1043): bold, still fading in.
  - Each word fades in grey → white.

## 2. B-ROLL INTEGRATION

| # | Frames | What it shows | Relation to line | Integration |
|---|---|---|---|---|
| 1 | f0-18 | Time-lapse highway and storm sky, Moscow | Metaphor: "For years", time passing | Full bleed, centre type-on title on top. 2.5 % ease-in push. Hard cut. |
| 2 | f19-50 | OpenAI / Mistral / Claude logos on black | Literal: "AI models" | Full-frame logo cards (logo width 344-1020 px), ±6-7.5 % scale drift, 9-13 frame hard cuts. |
| 3 | f51-62 | Command A render, Copilot phone photo | Literal | Full bleed, 6-frame hard cuts, centre pull-outs (−0.75 %, −3.1 %). |
| 4 | f63-122 | Perplexity slate | Literal: "outputs" | Full frame **shrinks into a 16:9 card** (849x480, 44 % of the frame) on a white ground, inside a 3x3 hairline grid. The card later becomes a type panel. Exits via invert-block shatter. |
| 5 | f127-172 | Three photos: hands on a laptop overhead; silhouette at a train window; backlit man touching his chin | Metaphor: "hidden within their very essence", inner thought | **Overlapping card collage** (≈340-400 px squares, ±1° rotation, no border or shadow). Flies in with motion blur, ×1.2 ease-out expansion. Type straddles card C, with colour flipping at the card edge. |
| 6 | f284-323 | Boy walking on salt-flat stones, cloud reflection (video) | Metaphor: "the idea seems to be..." | **Portrait card (674x851) in the centre column of a 3-column grid**; words left and right of the card on the vertical centre. Settles −2.2 %, exits with an accelerating +5 % push. |
| 7 | f431-498 | Rendered 3D UI: floating tilted cards (meeting photo, product, sphere, chart) around a "Join" pill; a cursor clicks | Literal: "Join us as we dive into..." | Full-frame 3D scene. Slow ×1.43 push; the cursor clicks; **zoom through the button** into a cyan fill → white. |
| 8 | f505-576 | Diver sinking among floating rocks (9:16 video) | Metaphor: "redefining our understanding", going deep | **Small 9:16 card (255x449) in the centre grid column**, grows ×1.29 from a white flash. Text block right-aligned to the card's left edge. Exits as a negative (inverted card plus inverted text box). |
| 9 | f687-756 | Android/humanoid with code overlay, turning red | Literal: "train a neural network" | **2:3 card (356x528) in the grid**. Slides in from the right, offset 190 px, and settles centred. Text blocks on both sides, staggered high/low. Blur-out exit. |
| 10 | f808-854 | Astronaut in an armchair in a gallery of paintings | Metaphor: "Imagine a world" | **Full bleed → frame collapse**: the side edges crop in (1920 → 875 wide, still full height) while the content zooms out; small caption inside the footage. |
| 11 | f855-905 | Aquarium with diver/astronaut | Metaphor: "AI can analyze", observing | Hard cut **inside the collapsing frame**, then the card detaches and shrinks to a floating 9:16 card (350x621). |
| 12 | f906-937 | Astronaut lying in a red poppy field at dusk | Metaphor: "generate the very building blocks" | Hard cut **inside the same card** (card geometry continuous). Flanked by graph-paper grids (literal "blocks"). Exits with the ×4.3 zoom-echo frame. |
| 13 | f1026+ | Man before a holographic data display | Literal: "analyze weights" | Full bleed with a slow focus-in; text set on the hologram plane. Entered via a 1-frame negative flash. |
| TH | f173-430, 577-807, 939-1024 | Two remote podcast guests (webcam/phone quality) | — | Always full frame, never carded. Reframed by blurred whips/zooms; captions sit beside the head on the empty side. |

**Card rules used throughout:**
- Cards are rectangles with 0 radius, 0 border and 0 shadow. Grids hang off the card edges.
- One card per white-ground scene, centred horizontally (centre x 963-970).
- Card height is 41-79 % of the frame: 480, 851, 449, 528, 621 px.
- B-roll inside cards keeps playing.
- Content can hard-cut inside a persistent card (f855, f906).

## 3. TECHNIQUES (rebuild recipes)

1. **Centre-anchored type-on title over B-roll** (S01).
   - Helvetica Regular white, cap 67 px, centred (x≈994, y≈547).
   - Reveal 1 character per frame (9 characters in 10 frames, synced to the words). The layout re-centres every frame; no cursor.
   - Footage underneath: 2.5 % ease-in push over 18 frames, then a hard cut.

2. **Logo montage with an accelerating cut rhythm** (S02-S06).
   - Shot lengths 13 → 9 → 10 → 6 → 6 frames. Logos sit on #000 at 18-53 % of frame width.
   - Each shot has a 6-7.5 % centred scale drift: three push-ins, then pull-outs, so the last pull-out flows into the card shrink.

3. **Full frame → card shrink with a ground swap** (S07).
   - Scale from 1.0 to 0.442 (1920 → 849 px wide, 16:9) over about 39 frames: slow start (−2 %/frame), peak −264 px/frame at f74, long exponential settle (≈−2 px/frame by f100). Motion blur at the peak.
   - The ground behind is black for the first 4 frames, then cut to #FDFDFD.

4. **3x3 hairline grid built off the card edges** (S07, S12, S18, S21).
   - Lines are 2-3 px, #1D1D1D, running from the card edges to the frame edges. They **pop** (1 frame, no draw-on): verticals first, then the bottom horizontal (+3-4 frames), then the top horizontal (+4 frames).
   - Teardown in reverse with 1-4 frame gaps: top H, then bottom H, then left V, then right V (S07: f117, f121, f124, f128).
   - Lines follow the card while it scales. Optional perspective of about 8 px over the frame width.

5. **Scatter words in the outer grid cells** (S07).
   - One word per corner cell, sitting on the grid line (baseline 5-10 px above it), roughly at the cell's horizontal centre.
   - Alternate serif italic and sans regular (cap/ascender ≈53 px).
   - Zig-zag order BL → TL → TR → BR, **a 2-frame stagger**, ahead of the voice.
   - Each word's first frame carries a black box with the letters knocked out to white.

6. **Type-on inside a dark card** (S07). Cyan #19ECEC sans, centred, about 1 character per 1-2 frames, synced to the spoken word.

7. **Invert-block shatter** (S08, and the motif at f63, f574-576, f1025).
   - Over 4 frames, rectangular regions of the outgoing card flip to their colour negative: dark #081714 → #F2E6E8, cyan → red #DB0E0E.
   - The blocks change size and position each frame (bottom band → lower-right quadrant → lower-left block → side-by-side pair), then the next image takes the block's place.
   - Single-frame variants: an invert rectangle over part of a logo or word (f63, f78-82); an inverted card plus an inverted text box (f574-576); a full-frame negative (f1025).

8. **Overlapping photo collage plus colour-flipping type** (S09).
   - Three 340-400 px photo cards, ±1° rotation, overlapping 75-130 px, no shadow.
   - Fly in over 5 frames with motion blur, then expand ×1.2 with an ease-out over 15 frames.
   - The big italic serif line is split by a track matte: white over the photo, #2E2E2E over the white ground.
   - The small sans line above it is white on the photo and black off it.

9. **Talking-head caption stack beside the head** (S10-S15, S19-S22, S27-S28).
   - **Placement:**
     - On the empty side of the frame, about 40-150 px from the ear or edge of the head (occasionally touching the shoulder or ear).
     - Vertically between eye line and chin (y≈430-740).
     - Block centre x≈360-620 when on the left, ≈1500-1610 when on the right.
     - Lines are centre-aligned to each other, or left-aligned (TH1a x1240, TH1c x205).
   - **Hierarchy:**
     - Connective words: white sans, cap 45-55 px, x-height 34-43 px.
     - Key phrase: **mint #8BFBE6 condensed serif at about 2× the white x-height** (x-height 71-89 px, ascender 110-150 px). Sometimes italic ("weights as"); sometimes mint sans instead ("much", "these weights", "thought?").
   - **Leading:** negative (−5 to −25 px). The serif ascenders overlap the white line above.
   - **Word entry** (2-3 frames):
     - opacity from about 0-55 % to 100 %;
     - the first frame is defocus-blurred;
     - the word slides into place: about 30 px from the right when joining a line, about 22-35 px up from below when starting a new line, with an ease-out.
   - **Exit:** captions leave only with the picture (in the blur of the outgoing whip or cut) or vanish on a punch-in cut. They never animate out by themselves.
   - **Parenting:** captions are parented to the footage, so camera moves scale and move them (×1.095 breathing in TH1b; the subtitle rises 34 px in TH1e).

10. **Dynamic side shade (legibility gradient).**
    - A black gradient on the caption side covers the outer 30 % of the frame width (≈570 px).
    - Measured brightness multipliers: 1.0 at the 70 % mark, 0.85 at 78 %, 0.68 at 84 %, 0.50 at 91 %, 0.37 at the edge. That is about 63 % darkening at the edge, eased.
    - It fades in over 2-16 frames when the caption (or its mint word) appears, and fades out over 10-13 frames when the caption moves away. Both sides can be on at once (TH1b).
    - For a centred bottom subtitle, use the same gradient from the bottom edge (bottom luma 64 → 33).

11. **Blur-whip reframe between framings of the same speaker** (S10→S11, S13→S14, S14→S15, S19→S20, S27 pulse, S27→S28). The cut sits in the blurriest frame.
    - **Combined move:**
      - Translation of the face by 100-410 px horizontally.
      - A scale change of ×0.81-×1.24.
      - A defocus/motion-blur envelope: ramp up 4-7 frames, cut at peak blur, ramp down 3-8 frames.
    - **Example S10→S11:** blur f184-188, cut f189, clear f196.
    - Zoom-echo ghosting (multiple scaled copies of the head) on the peak frames (f173, f188).

12. **Rack-focus in on a hard cut** (S16 f431-438, S19 f577-584, S22 f757-763, S30). The new shot starts fully defocused and clears in 6-8 frames, ease-in (most of the clearing in the last 2 frames).

13. **Question as a centred bottom subtitle** (S15). One line centred at x≈940, baseline y≈1018, cap 53 px, white sans with the last word in mint. Words appear left → right; bottom shade on.

14. **White-ground card-plus-text layout** (S12, S18, S21).
    - Card centred in the middle grid column. Text blocks right-aligned to the card's left edge or left-aligned to its right edge, with a 44-90 px gap.
    - Two-line blocks mix sans and condensed serif. The serif line is the larger one (x-height 27-45 px against 15-40 px for the sans).
    - Word-by-word fade from light grey to black over 2-4 frames.
    - In S21 the blocks are staggered (left block upper half, right block lower half) to make a diagonal.
    - The card enters by popping small and growing ×1.29 with an ease-out (S18), or by sliding in from an off-centre position, about 190 px right (S21).

15. **UI-click zoom-through to a colour flash** (S16-S17).
    - Slow ×1.43 push over 57 frames. The cursor glides about 120 px to the button, then becomes a hand.
    - Click: the button squashes −14 % over 3 frames and its label fades out.
    - The button then scales about ×1.3 per frame for 6 frames with motion blur, and the side elements fly out.
    - The button fill becomes the full frame (#28E9EE), then fades to white over 4 frames (#59F9FA → #A5FCFA → #E2FEFD → #FDFDFD), which becomes the next white-ground scene.

16. **Triple punch-in on a repeated word** (S23). Three hard-cut scale steps 4 frames apart (×1.089, ×1.119, ×1.058; total ×1.29). The first step re-centres the face to the right third. Captions are removed on the first step. Follow with a slow ease-in pull-out (−1.5 % over 16 frames) into the next cut.

17. **Frame collapse into a floating card** (S24-S25).
    - The full-bleed clip is masked from the sides: first the right edge only (−100 px over 20 frames), then both sides, accelerating to 875 px wide, while the clip zooms out inside the mask.
    - Under a 7-frame blur the mask detaches from the top and bottom (519x916).
    - The card shrinks with an ease-out to 350x621 (9:16) over about 66 frames.
    - Hard-cut new clips **inside** the persistent card on phrase changes (f855, f906).

18. **Parallax graph-paper grids** (S25). Two square graph-paper grids (9x9 at ≈22 px cells; 9x10 at ≈45 px cells), thin black lines and no fill. They sit on nearer Z planes than the card, so they shrink ×1.55-2.0 while the card shrinks ×1.2. They enter from beyond the left and right frame edges with motion blur, as part of one global ease-out dolly-out. The text overlaps half of each grid.

19. **Hand-drawn underline write-on** (S25). A black marker stroke, about 8-10 px thick, bowed and tapered, about 410 px long, drawn left → right in 16 frames with an ease-out. It starts on the emphasised word ("blocks", f907).

20. **Zoom-echo flash frame** (S26). One frame in which the card's content is scaled about ×4.3 at about 50 % opacity over the outgoing layout, then a hard cut to the talking head.

21. **Negative flash frame** (S29). One frame showing the colour negative of the incoming shot, then the incoming shot.

22. **Caption bleeding off frame** (S27). The mint serif line runs past the right frame edge (clipped at x1919) and is then carried further out by the whip move.

23. **Type on a B-roll prop** (S30). Small white sans with wide word spacing (≈40-50 px) set on the hologram's surface. The key word moves to a **bold** sans line below, offset about 200 px left. Words fade in grey → white.

24. **Caption lead time.** Show each word 0-6 frames before it is spoken (median about 4). A whole short phrase can be laid out at the head of a shot (S12, S13) with a 1-frame stagger.
