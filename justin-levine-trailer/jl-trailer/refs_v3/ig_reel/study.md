# IG reel DfztsmVIC6x: opening scene study (for the JL 20 s transition, Autodesk -> Nic)
Source: video.mp4 (1916x1080, 23.98 fps, 90.67 s, VP9 1080p) + audio.mp4, downloaded via neo resource URLs.
Frames: full/0001.png = f0. Sheets: s_000_047.jpg, s_048_095.jpg.

## What the opening is (f0-f32 = 1.38 s)
The OpenAI-founders photo is built in a 3x3 grid of tiles. The tiles are separated by near-black gap lines. A white tile
flashes in each cell in turn, clockwise spiral, and each one fades away to reveal the clean picture under it. The whole
layer (photo + grid) slowly zooms in the whole time. At f33 there is a hard cut to the next idea (the photo as a print on
white, entered with a zoom/blur; at f48 a blurred zoom back). That f33/f48 blur is the "blur thing" Krish does NOT want, so it isn't copied.

## Per element (frame numbers at 24 fps, j = frame after the cut)
- **Zoom (picture + grid together, centred on the frame):** the grid spacing is 649 -> 710 px, so the scale is 0.914 -> 1.000.
  Normalised progress: j1 .20, j2 .29, j4 .47, j8 .63, j16 .85, j24 .95, j32 1.0. That fits Krish's G1 = bez(0,0,0,1)
  over 36 frames (1.5 s), fastest on the first frame (j1 .22, j4 .47, j8 .66, j16 .86, j24 .96).
- **Grid:** 3x3, the centre cell = 1.112 x the frame thirds x scale (final lines x 602/1312, y 338/740 on 1916x1080).
  Lines are near-black (lum about 8), about 4 px wide, on top of everything except the caption. They stay to f32 and leave with the cut at f33.
- **Global white wash (opening flash), opacity:** j0 .45, j1 .28, j2 .14, j3 0.
- **White tiles:** colour (234..245) neutral white, flat, exactly one cell each.
  - Order: TL f0, TM f2, TR f4, MR f6, BR f8, BM f10, BL f12, ML f14, MM f16. One new tile every 2 frames, in a clockwise spiral inwards.
  - Opacity per frame after its pop (measured): 1, 1, .80, .31, .13, .05, .01, 0.
    That is a hard pop, a 2-frame hold, then .8 x (1 - G1(u)) over 5 frames (G1 = Krish's incoming ease-out).
- **Cells before their flash:**
  - ML, MM, MR, BM and BR show the picture as a hard-edged mosaic with about 20 px blocks.
  - TL, TM, TR and BL show it clean (the first three are revealed under the wash anyway).
  - When a cell's white tile fades, the picture under it is clean. No blur anywhere in the tiles (pixel blocks only).
- **Captions** (white, centred) sit on top, unaffected by the zoom, tiles and wash.
