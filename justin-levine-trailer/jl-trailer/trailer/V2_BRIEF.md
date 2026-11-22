# Justin Levine trailer v2: shared brief for every scene builder (read fully first)

Krish (the client/editor) wants the full trailer v2 FAST. You own one segment. Build it, render it frame-exact, report back.
Don't ask Krish anything, don't `open` any video, and never close neo tabs or terminals.

## Timeline (NEW, tight recut)
- Audio: `~/jl-trailer/trailer/audio/mix2.wav` (90.642 s). 24 fps, 1920x1080. `newtime.py` gives:
  - `WORDS`: word times on the NEW timeline (`words_new.json`: [t0, t1, word, speaker, ...]).
  - `TL['shots']`: the v1 shot names with NEW bounds.
  - `M(t_old)` and `A(t_new)` to convert between timelines.
- **OLD** = the v1 timeline: `timeline.json`, `words_cut.json`, `audio/mix.wav`, and all v1 code (`shots.py`, `render.py`, `engine.py`). Krish's timestamps (e.g. "31–36 s") are OLD.
- Lip-synced speaker footage at NEW time t is `engine.cut_frame(round(A(t)*24))` / `spk_frame(...)`, and mattes are `engine.matte('cut', n)`. Don't use the slow-motion patches: set `engine.PATCH_MAP.clear()` and skip `trailer/patch/` files (monkeypatch `engine.cut_frame` to read `Vid(CUT)` directly).
- To reuse a v1 shot as-is at NEW frame n: render v1 old frame `n_old(n)` via `render.py` (`R.frame(n_old)` / `R.shot_frame`). Before that, set every `R.SHOTS[i].tin/tout` that is `'zt'` to `'cut'`.

## Deliverable
- `~/jl-trailer/trailer/v2segs/<NN>_<name>.mp4`: exactly frames [n0, n1) of the NEW timeline, which is `n1-n0` frames.
  - Encode: H.264 `-preset medium -crf 16 -pix_fmt yuv420p -r 24`, no audio.
  - Use ffmpeg at `/Users/gourav/ks-ron-build/reel1/ff` and python at `~/ks-ron-build/venv/bin/python`. For rembg use `~/chase-009-build/venv/bin/python`.
- For your own check, also write `<NN>_<name>_check.mp4` with `mix2.wav` muxed (`-ss n0/24 -t (n1-n0)/24`).
- Verify:
  - the frame count is exactly `n1-n0`
  - no stuck frames
  - a per-frame motion print with no spikes, except intended cuts
- Use ≤3 render workers (`NW=3`); other builders share the 10 cores.
- Finish like v1 so segments match: `fin16.finish(np.clip(J3.grain(out, 4.5, seed=n), 0, 255), vig=0.60, tex=0.35, rb=0.50)` for graphics.
  - Speaker shots: grain 2.2, tex 0.0, rb 0.35.
  - Footage shots: grain 3.0, tex 0.18, rb 0.40.
  - See `render.frame`.
- Your first frame meets the previous segment, and your last frame meets the next, with HARD CUTS unless your brief says otherwise.
- Report back: the file path, what you did, and anything you couldn't match. Be short.

## Krish's rules (all hard requirements)
1. **NO zoom-in/zoom-out "zoom-through" transitions, ever.** Use the reference's own transitions or hard cuts.
2. **Copy the reference EXACTLY when one is given.**
   - Download it, extract frames, and study it frame by frame. Write a short per-element timeline (positions, durations, ease, speeds) BEFORE building.
   - Never invent motion that isn't there.
   - The reference sets the MOTION; the trailer's look sets the LOOK: black "01" tech ground (`engine.tech`), Instrument Serif white text, cyan→blue gradient key words (`L.grad_text`), blue gradient key-word boxes, grain and vignette.
3. **Pinterest video:** open the pin in a NEW neo tab (BrowserOS neo MCP; keep the tab open). Read `performance.getEntriesByType('resource')` for the `v1.pinimg.com/videos/...720w.m3u8` (or an mp4), then download it with ffmpeg.
4. **Captions:**
   - **Size and placement:** big and readable, close to the subject or centred as asked; never small text in a corner.
   - **Animation:** per word, fade in over 2–4 frames with a 10–16 px rise and blur clearing. Hero/key words (names, numbers, places) type on letter by letter, bigger, gradient or boxed. Laid out in place.
   - **Finish:** every caption gets a shadow and glow.
   - **Alignment:** left-placed text is left-aligned, right-placed right-aligned, centred text centred.
   - **No text on faces.**
5. **Camera:**
   - **Graphs:** smooth, using only Krish's graphs: EU = `J3.bez(0.68,0,0.03,1)` (his S-curve), G1 = `bez(0,0,0,1)` for incoming / fastest at the cut, G2 = `bez(1,0,1,1)` for outgoing.
   - **Overlap:** keyframes overlap, with the next move starting ~20–50 % into the previous, so the camera never parks or jerks.
   - **Blur:** real sub-frame motion blur.
   - **3D:** moves should read as 3D (z-depth parallax) where asked.
6. **Footage plays at NORMAL speed.** No slow-mo, no optical-flow, no frame interpolation, no stretching. Screen-recorded B-roll (`broll/c_*.mp4`, 30 fps) has duplicate frames, so use unique frames only and prefer clips with few duplicates. Speaker footage stays lip-synced via `A()`.
7. **Subject centred unless asked otherwise.** Real assets only (no flat drawn stand-ins); outpaint or crop properly; clean cut-outs (rembg).

## Useful code to read
- `trailer/engine.py`: `Vid`, `vid()`, `cut_frame`, `spk_frame`, `matte`, `tech`, `Item`, `apply_item`, `chain`, `mat`, `warp`, `compose`, `T_put`, `T_grad`.
- `trailer/shots.py`: the v1 shots and their content.
- `trailer/render.py`: `frame`, `shot_frame`, finishing.
- `storyboard/jl_look.py` (L): `put_text`, `grad_text`, `card`, `fit`, `grade`, `hairline_grid`, `gbox`.
- `~/.claude/skills/jennifer-musselman-style/scripts3/jstyle3.py` (J3): `bez`, `glow`, `grain`, `drop_shadow`, `font`, `text_rgba`.
- Worked examples:
  - `alt_10_14/scene_v5.py` and `scene3d.py`: 3D pinhole layers, rise, feathered wipe, Dime word build.
  - `alt_20/scene_adsk.py`: 2D overlay on a continuing v1 background, type-on hero, asterisk reveal.
  - `alt_15_19/scene3.py`: orbiting 3D camera, many layers, glowing line.
- B-roll: `trailer/broll/` (sheets `broll_sheet*.jpg`). Assets: `~/jl-trailer/assets/`.

## v3 round (Krish's notes on trailer v2, 2026-11-22). Read this too.
- **The timeline is unchanged:** same `mix2.wav`, same NEW frame numbers, and the current v2 is `~/Downloads/Verticals_Justin_Levine_Trailer_v2.mp4`. Its segments are in `v2segs/` and are listed in `assemble_v2.py`.
- **`newtime.n_old` is fixed:** it is now `round(A(t + 1e-4) * 24)`, so at a cut point it shows the first KEPT frame.
  - To get a v1 frame with all fixes, call `render_v2.frame('v1', n)` (or `'adsk'` / `'s1014'`).
  - That covers hard cuts instead of zoom-throughs, the `OVR` map for shot heads, the calendar centring, and "No." on the left with its clean exit.
- **Import gotcha:** `import render` can resolve to `~/ks-kristina-build/trailer/render.py`, so load JL's `render.py` / `shots.py` by file path (`render_v2.py` already does).
- **Previews:** Krish wants to SEE the transition pieces before the final.
  - Each preview goes to `~/Downloads/Verticals_JL_v3_preview_<X>.mp4` with `mix2.wav` muxed for its time range. Use new names and never overwrite.
  - Don't `open` it; I'll show them together.
- **Transitions:** copy the reference's motion frame by frame (positions, timing, ease), using only Krish's graphs. No zoom-throughs. Real sub-frame motion blur on moving things.
