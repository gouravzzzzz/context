# Pinterest ref pin.it/2boBV7c90 ("Showcase (09)"), for trailer 15.66–19.55 s

- **Source:** in.pinterest.com/pin/936326578789029352. The 720w mp4 is saved as refs/pin_15_19/pin.mp4: 720x1280, 30 fps, 8.99 s.
- **Cadence:** the clip holds every 3rd frame, so it is effectively about 20 fps.
- **Frames:** f_0001…f_0269.jpg. Sheets: sheet_all.jpg, s_a…s_d.jpg.
- **Camera measure:** motion.json is ECC affine per frame, with the fixed top nav and bottom caption masked out.

## Layout (wide, 0–0.9 s)

- **Centre:** a website hero card holds the white-horse video, about 58% of the width. It has a nav strip ("rico" logo plus items) and a hero headline lower-left, white plus a grey continuation.
- **Satellites, in front of the card:**
  - Above the card: a small label pill, "New Jitter Motion Template".
  - Top-left: a green leaf image tile overlapping the card corner. It sits nearest the camera and blurs most.
  - Bottom-left: a dark "Aa" type-specimen card (Inter / Space Mono label, "Heading" tag) overlapping the card corner.
  - Bottom-right: a steel-blue "VEEPS" pill overlapping the card corner.
  - On the card's right edge: a "95%" chip, plus two dots (peach and white).
  - Below the card: a small B&W photo tile.
- **Fixed overlays (not part of the scene):** the top nav and the "Showcase (09)" caption.

## Camera path

Speed is measured as displacement at 720 scale per 30 fps frame.

| Time | Move | Measured |
|---|---|---|
| 0–0.6 s | Near-still drift (+x 2–5 px/f) | |
| 0.6–2.0 s | **Dolly-in** onto the hero card | ×1.6. Speed peaks at 1.0 s (~38 px/f), then a long tail to about 2.0 s. Satellites fly outward and fall out of focus. |
| 2.0–2.6 s | Slow lateral drift | |
| 2.65–3.9 s | **Travel down-left + push** onto the Aa card | ×1.8. Peaks at about 3.05–3.1 s, long tail. The hero card goes soft. |
| 4.05–4.8 s | Second slow push / tilt while on the Aa card | |
| 4.83–6.3 s | **Whip right** onto the VEEPS pill | Mostly horizontal. Peaks at 5.2–5.45 s (heavy motion blur), decays to about 6.3 s. The hero card is a bokeh blur behind. |
| 6.3–6.85 s | Hold (near zero) | |
| 6.85–8.9 s | **Pull back out** to the wide | ×~2. Peaks at about 7.45 s. |

- **Ease shape:** every move runs 1.25–2.0 s with the speed peak about 30–35% in, then a long tail. That is the same family as EASE_USER.
- **Depth of field:** follows the element being showcased.

## Element animation

- **3.7–4.3 s:** the Aa glyph squashes to its baseline and re-forms in another font.
- **Other elements:** static. All motion is the camera.

## How v2 maps it (alt_15_19/scene2.py)

- Justin's A-roll card replaces the hero card.
- The TradeTapp card replaces the Aa card. Its mark squashes and comes back with the gradient.
- The BuildingConnected pill replaces the VEEPS pill.
- Extra tiles (B-roll unique frames and UI stills), chips, a far grid and the tech ground add depth.
- Two moves of the reference's length (2.5 s and 2.1 s) on EASE_USER, overlapped. Each pulls back and orbits 10–11°.
