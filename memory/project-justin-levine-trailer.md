---
name: project-justin-levine-trailer
description: "Verticals trailer for Justin Levine (Shepherd): 16:9 storyboard stills in Jennifer look with Twiml + Dime motion; build paths, sources, status"
metadata:
  node_type: memory
  type: project
  originSessionId: 38bd0f11-486d-4e3a-b942-c55a0475a391
  modified: 2026-11-21T21:50:25.203Z
---

Started 2026-11-21. Script: ~/Downloads/"Verticals Trailer Script v4, Justin Levine (Shepherd).pdf" (10 beats plus an edit map: music, SFX and on-screen text per beat). Episode tracks: ~/Downloads/justin_levine-…-CFR.mp4, nic-…-CFR.mp4, luke_sophinos-…-CFR.mp4. Exact line times: ~/jl-trailer/ep/*_win.json.

- **Look:** Jennifer theme (Instrument Serif, cyan→blue gradient key words and boxes, neon boxes, black "01" tech ground). **Motion/layout:** a mix of the Twiml Frame.io trailer and the Dime "Sports Bra" trailer. Frame-by-frame studies are in ~/jl-trailer/refs/study_twA/twB/dmA(/dmB).md.
  - From Twiml: hairline 3x3 grid with footage in the centre cell, card beside text, collage with a split-colour word, letterbox ending.
  - From Dime: a hero word or name behind the person (roto), a cut-out speaker with a sticker outline over a literal photo card, logo badge cards behind Nic, a retro TV.
- **Build:** ~/jl-trailer/storyboard/.
  - jl_look.py holds the helpers; jl_stills.py renders scenes s01–s10 into stills/ (39 PNGs).
  - build_pdf.py builds ~/Downloads/"Justin Levine (Shepherd) - Trailer Storyboard.pdf", one scene per page with links, stills and 2–3 sentences.
- **B-roll (all real, non-stock):**
  - Shepherd brand film (shepherdinsurance.com)
  - Brickeye LumiCon uUZU8QoGUlE
  - BuildingConnected/TradeTapp U05_dLMiqOo
  - Progressive late-90s ZymdJ-SAWwQ, in the Commons Sony KV-20FV300 TV
  - Oracle Abilene WkkgqXrg-Xg
  - OSHA inspection HA6bixDzeLY
  - Inside Lloyd's ugRFJv_93ZU
  - Logos from Commons / greenlightre.com
- **Status 2026-11-21:** storyboard PDF delivered (10 pages, 40 stills). No video rendered (ask first).
  - After dmB: 05a became the Dime CRT layout (TV fills the left, spot hard-cuts inside the screen, caption stacked right). The TV cut-out was cleaned to assets/tv/kv20_cut_clean.png.
  - The user asked for links to every B-roll/footage in each scene. build_pdf.py now has a SRC map: every still gets a caption with its exact source + timestamp, plus the per-scene link pills. Keep both on every rebuild.
  - The user asked for videos instead of logos for Autodesk and Intact. 02g = Autodesk Gallery film k4-SC5YxZFo 0:02 (AUTODESK on the big screen). 02k = 'Becoming Intact Insurance' aOjXSQGntWM 2:22 (letters on the office wall; burned-in subs cropped). Procore and Greenlight Re stay as badge cards behind Nic (no change asked).
  - More B-roll per the user:
    - 03 = sensor montage from the user's 3 Brickeye videos (FUPy-YfgGDs 0:46, CfwENc84sQc 0:31, jSVfpOEYbaU 0:57) plus LumiCon uUZU8QoGUlE.
    - 05d = 5-build commercial montage: CyrusOne IAnIk69PJvY 0:33, Intel Ohio i2HLl0Ewiao 1:06, Aligned Xs4DNe-QwdU 0:31, Microsoft Fairwater dx1vrbGIbYw 1:10, Oracle 0:44.
    - 06b = 4 OSHA HA6bixDzeLY shots (0:56, 3:46, 2:46, 3:50) cut inside one card.
  - 08c = the user's Pinterest motion ref pin.it/byqxYwpKP (thumbnail stream + photo-card burst on black). Built as ai_cloud() in jl_stills.py with 15 real AI images (assets/ai/ copied from the KSS build, plus this trailer's data-center frames), every source linked on the page. Frames of the pin are in refs/pin08c/.
  - **Sent 2026-11-22 12:14 am:** the storyboard PDF (10 pages, 51 stills, 9 MB) went to Krish on WhatsApp as a document with no text. Delivered. Before sending, every still was checked for a source caption and all web links were checked (19 YouTube IDs live; Axios blocks curl but opens in a browser). The 3 episode-track links are local file:// paths, so they only open on this Mac.
  - The user's pattern: a single B-roll per beat reads thin, so they want several real clips per beat (fast montage / hard cuts inside a card).
- **Video build (2026-11-22, user asked "render the trailer… really smooth, keyframe overlapping everywhere, use my graphs"):** ~/jl-trailer/trailer/.
  - engine.py: readers, mattes, face track, overlapped camera `chain()`, cached affine text items.
  - shots.py: all 31 shots from the storyboard, in motion.
  - render.py: transitions, motion blur and finish. Modes: `timeline | safe | speed | test t.. | full out.mp4 aud`.
  - mix.py builds audio/mix.wav. patch2.py makes the optical-flow slow-motion for the 3 exposed holds; the ffmpeg `select` version grabbed the wrong speaker.
  - Overlap: with EASE_USER, a next move starting at 50% makes the speed surge 7× every 1.4 s. The chain starts each 3 s move 20% into the previous one (about 2× ripple). The user hasn't reacted to this yet.
  - Transitions: zoom-through = G2 out 0.32 s (+24%), G1 in 0.85 s (+7%), 3-frame dissolve. Also whip, flash, and hard cuts with the camera already moving.
  - **v1 delivered 2026-11-22 1:18 am:** ~/Downloads/Verticals_Justin_Levine_Trailer_v1.mp4 (1080p24, 2462 frames = 102.58 s, video and audio lengths match, no stuck frames). Waiting for the user's notes.
- jl_stills.py was edited on disk by another process mid-session. Check the file's state before editing it.

**Why:** the next turn is likely to bring storyboard notes or a request for the video build.
**How to apply:** change scenes in jl_stills.py, re-run `python jl_stills.py sNN`, then `python build_pdf.py`, using ~/ks-ron-build/venv/bin/python. Related: [[project-kristina-shea-trailer]], [[feedback-trailer-v1-rules]], [[edit-rule-no-text-on-person]].
- **Scene redos (2026-11-22), rendered as separate clips:**
  - **10–14 s:** ~/Downloads/Verticals_JL_10-14s_3D_v2.mp4, built by alt_10_14/scene3d_v2.py.
    - The original Shepherd film comes from Vimeo 1157667900 at 23.98 fps (in ~/jl-trailer/src_shep). Frames 0–102 are Justin wide; 437–501 are Justin wide take 2; 526–553 is the sign; 4049+ is the end logo.
    - Nic whips left, Justin rises in, the card wipes in and whips out, then the 3D truck runs and it hard-cuts out.
  - **20 s:** ~/Downloads/Verticals_JL_20s_Autodesk_v1.mp4, built by alt_20/scene_adsk.py. It's the pin.it/27MYc2UDA asterisk → arrows → photo opening, with the Autodesk Toronto Commons photo on the right and big captions on the left.
  - **15–19 s:** alt_15_19.
    - v2 = scene2.py. Ref-speed 3D look-at camera, 17 elements, captions on the logo planes.
    - **v3** = scene3.py → alt_15_19/JL_trailer_15-19s_showcase_v3.mp4 (2026-11-22).
    - v3 opening move: on Krish's cubic-bezier(0,1,1,1), starting on the first frame. See [[ease-graph-opening-move]].
    - v3 line: a glowing purple line TT→BC copied from pin.it/2AbnLjOI5. The study is refs/study_pin_line.md and the data is assets/line_ref.json.
    - The Autodesk tile was lowered (cy 1105) so the line clears it.
    - **Trailer v2 segment 04** (NEW frames 353–434) = scene4.py → trailer/v2segs/04_showcase.mp4. Built from ~/jl-trailer/trailer/V2_BRIEF.md (newtime.py: M/A/n_old, words_new.json, mix2.wav).
      - Krish's v3 notes: the opening ZOOMS OUT on bez(0,1,1,1). The line is thin (1.5 px) and darker purple, with weaker, wider glows (σ12/35/80).
      - It lands pixel-exact by NEW frame 425 on a layer textured with the live v1 02ef frame (R.shot_frame), held to 433.
      - Import JL's render/shots by file path: ks-kristina-build/trailer is also on sys.path and its render.py shadows JL's.
  - None of these are spliced into the full trailer yet.
- **Latest (2026-11-22):**
  - **10–14 s:** v5 = alt_10_14/scene_v5.py. It's v2's 3D camera, plus a card behind Justin ending at his centre line, revealed by a feathered wipe right→left using the ref's profile. "Justin"/"Levine" sit on black boxes, block centred on the frame middle (stills_v5). The v6 render is waiting on Krish's OK.
  - **20 s Autodesk:** v3 = scene_adsk.py. The 02ef square closes to the centre, the lines meet and fade, the "to" carries over and becomes the star, and the photo reveal eases bez(0.3,0,0.02,1) over 1.6 s, still moving at the cut.
  - **15–19 s:** v2 at alt_15_19/JL_trailer_15-19s_showcase_v2.mp4, made by the background agent.
- **15–19 v3 asks (2026-11-22):**
  - The starting camera move uses Krish's graph cubic-bezier(0,1,1,1): fastest at the start, starting AT the scene's first frame.
  - Add a thin, purple, really-glowing line drawn from TradeTapp to BuildingConnected, like pin.it/2AbnLjOI5.
  - Delegated to the 15–19 agent; output will be alt_15_19/JL_trailer_15-19s_showcase_v3.mp4.
- **Status 2026-11-22: full trailer v2 delivered** → ~/Downloads/Verticals_Justin_Levine_Trailer_v2.mp4 (2175 f, 90.625 s, -14.1 LUFS).
  - **Recut:** newcut.py made 28 cuts. newtime.py provides M/A/n_old; n_old uses A(t+1e-4) so a cut point shows the first KEPT frame.
  - **Audio:** the voice went through Adobe Podcast Enhance Speech v2 (audio/adobe/) into mix2.py.
  - **Build:** 14 segments in trailer/v2segs, joined by assemble_v2.py.
    - My v1-based segments come from render_v2.py: 'zt' becomes a hard cut, PATCH_MAP is cleared, the calendar is moved down 80 px, and "No." sits on screen left in gradient colour.
    - fix_segs.py splices cut-point frames into those segments.
    - The OVR map in render_v2.py covers shot heads that land inside removed pauses.
  - **Agent segments:**
    - 04 scene4 (15–19)
    - 07 Procore pin
    - 09 $$$ / 15%
    - 10 TV / 4,000 counter / centred captions
    - 12 3D "manufactured"
    - 15 carousel collage → Lloyd's
- **v3 round (2026-11-22):** previews A/B/C are in ~/Downloads (Verticals_JL_v3_preview_*). The final waits for Krish's OK, then `python assemble_v3.py` writes Verticals_Justin_Levine_Trailer_v3.mp4.
  - **A, 20 s:** IG-reel 3x3 grid into Nic, in 05_06_v3.
  - **B:** 06b box (his tank-inspection footage) → pin RyU5xmNfN card layout → Jennifer `pixel_overlay` → 07a, in 11b_manu_v3.
  - **C:** photo strip slides R→L over Justin → background fade → collage, in 15_cloud_lloyds_v3.
  - **Opening:** Trailer 1 (11–16 s) cut-on word captions, no "UNDERWRITERS ARE NEXT", in 00_open_v3. Its captions are also installed in s1014.
  - **Calendar:** glides 122 → 2 px so it stays centred, with a blue gbox for "11 MONTHS".
  - **1:09:** 08b → 08c is one camera, "No." fades out.
  - **Purple accents:** `render_v2.PURPLE` (70,185,255) → (165,92,255) on construction, partnerships, manager, inception, AI bubble?, No., 100%, orchestrating, manufactured., underestimated (box).
- **v3 delivered 2026-11-22:** ~/Downloads/Verticals_Justin_Levine_Trailer_v3.mp4 (2175 f, 90.6 s, -14.1 LUFS), assembled by assemble_v3.py.
  - **Audio:** the Deep_Drone under "orchestrating" was removed from mix2.py ("hit sfx at 6 s").
  - **Final preview versions:** A v2 (grid uncover one cell per frame, no mosaic), B v4 (8-card wall, level, text centred with shadow), C v3 (strip enters at scene end on the centre line).
- **v4 delivered 2026-11-22:** ~/Downloads/Verticals_Justin_Levine_Trailer_v4.mp4 (assemble_v4.py).
  - **Audio:** Krish said remove ALL hits/risers. The booms, impacts, risers, stinger and bass drop are commented out in mix2.py; only the counter ticks, page flips and keyboard remain.
  - **Carousel glitch:** cards behind the ring were drawn in the same slot (fixed), and cv2 POS_FRAMES seeks were inaccurate. Always decode B-roll sequentially, never seek.
- **Sent 2026-11-22 6:28 am:** v4 trailer (177 MB) went to Krish on WhatsApp as a document with no text. Delivered, and the WhatsApp tab was closed.
