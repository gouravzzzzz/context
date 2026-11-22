---
name: project-ray-lucia-style-reel
description: "New \"Ray Lucia / Quotient Episode 5\" reel style being tested on Ron Foxcroft short 1; build in ~/ks-ron-build/reel_rl; NOT the flourish-broll skill"
metadata:
  node_type: memory
  type: project
  originSessionId: 5aa6f583-a3bd-4fcc-8877-4eb7b08d0906
  modified: 2026-11-15T00:41:08.410Z
---

Started 2026-11-15. The user asked for Ron Foxcroft short 1 (same raw cut + script + audio as Ron_TH_001_v6) remade in the style of the 10 reels in their Dropbox folder "005 Episode 5/001 Talking Heads" (RayLucia_TH1..TH10, Quotient Advisor Partners). They said: **do not use anything from the flourish-broll skill**. If this style works, it gets saved as a new skill.

- Dropbox reference folder ("005 Episode 5/001 Talking Heads"): https://www.dropbox.com/scl/fo/r5n18766qxzptxlfz7elh/AKQ3xdkC5dB-ElGqJaem_qM/005%20Episode%205/001%20Talking%20Heads?rlkey=r6jsqw1kce6zb5xhydj4xwhkg&subfolder_nav_tracking=1&st=cbp3k58o&dl=0
- References downloaded to ~/ks-ron-build/refs_ep5/raw2/ (Dropbox shared-folder link + `dl=1` returns a zip; unzip fails on it, `ditto -x -k` works). Contact sheets in refs_ep5/sheets.
- Style measured: Helvetica Neue; white Regular lead line (~50 px) + gold Bold line (211,196,145, ~70 px); khaki highlight box (160,138,85) with cream bold text (252,243,217) wiping in; white Bold caps for punch lines; words fade in one by one from ~30% opacity; block re-centres as lines arrive; soft glow, no hard shadow. Strong bottom fade to black + vignette. Graphics: black with warm centre glow, gold rounded cards, count-ups, person icons, slow push. One warm white light-flash transition. Speaker: framing switches wide/close only on jump cuts, gentle eased zoom-out on entry.
- Build: ~/ks-ron-build/reel_rl/work (style.py, plan.py, graphics.py, render.py). `./py work/render.py test <secs>` / `full out.mp4`. Photos from Ron's/Fox 40's socials in reel_rl/photos/ (photo "card" mode = whole photo on a rounded card over its blurred copy, type below, so no text on people and no over-cropping).
- v1 delivered: ~/Downloads/Ron_TH_001_RL_v1.mp4 (photos on cards, too little camera). User rejected it: "doesn't look like references at all".
- v2 (2026-11-15): ~/Downloads/Ron_TH_001_RL_v2.mp4. Changes from the user's notes, all MEASURED from the refs (reel_rl/analysis: motion.py optical-flow per shot):
  - speaker: every shot starts ~1.32x and zooms OUT continuously, exponential decay tau ~1.4 s (refs: 25-30% over 3-6 s); restarts at each jump cut.
  - photos FULL SCREEN with type on them (like refs, faces kept clear): no zoom, horizontal slide ~360 px, fast start easing out, direction alternates; second photo in a sentence pushes in sideways (~8 frames, motion blur).
  - transitions: hard cuts + red-orange film-burn light leak (style.leak) at chapter changes (~3 per reel).
  - graphics kept (user liked them) but open with a zoom-out; the 400-icon grid was removed (user: replace with picture + text).

**Why:** next session must continue this exact style and build, not mix in the Gillian/Flourish style.
**How to apply:** apply the user's notes to plan.py/graphics.py/style.py and re-render. Related: [[project-ron-foxcroft-kss-shorts]].
