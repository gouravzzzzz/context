---
name: project-kristina-shea-trailer
description: "The Kristina Shea Show trailer reel (36 s, take 4) in Jennifer style: storyboard build, footage sync, asset sources, user decisions per scene"
metadata:
  node_type: memory
  type: project
  originSessionId: dde13ef9-61ad-492b-9d95-72e6348c0a4f
  modified: 2026-11-20T13:19:37.709Z
---

Started 2026-11-20. This is a vertical reel of Kristina's show trailer, built in **Jennifer style** throughout. Storyboard first: stills with asset links on top and 2–3 sentences under each. The user wants no extra detail. Ask before rendering video.

- **Script:** Dropbox "Kristina-Shea-Show-Trailer-Script.pdf", 8 lines. Ideas PDF: ~/Downloads/"Kristina Shea Show - Trailer B-roll & Animation Ideas.pdf".
- **Footage:** ~/Downloads/pmacguinness_2026-11-14-kristina-shea-updated-solos_2026-11-14_2341.zip (51 GB, stored).
  - It's never unzipped because the disk can't hold it. ffmpeg reads members via `subfile,,start,<off>,end,<off+len>,,:<zip>`.
  - Offsets: CAM A 107, CAM B 9143570308, CAM C 19272939795, Stereo Mix 37410410702.
  - Sync: cam_time = mix_time − 6.0963 (A wide frontal), −11.7193 (B medium, her right), −3.4420 (C medium-close, her left).
- **Take 4:** "Hey" at mix 332.38 s, ends ~367.5 s. Excerpts start at mix 325: ~/ks-kristina-build/work/take4_cam{A,B,C}.mp4 and take4_mix.wav. Word timings in take4_words.json. She says "sparked", not "sparks".
- **Storyboard build:** ~/ks-kristina-build/storyboard/
  - make_stills.py: HTML/Chrome stills (CEO match cut `ceo`, XP desktop `xp` -> assets/xp_desktop.png).
  - jen_stills.py: every other scene, on the Jennifer engine (jstyle2). build_pdf.py builds the storyboard PDF.
  - Output: stills/ 01–12 (23 stills). PDF at ~/Downloads/"Kristina Shea Show - Trailer Storyboard.pdf" (one scene per page: links / stills / 2–3 sentences). Photos album "KSS Trailer Storyboard".
- **A-roll cut (2026-11-20):** ~/ks-kristina-build/cut/make_cut.py -> ~/Downloads/KSS_Trailer_Take4_Cut_v1.mp4. 30.2 s, pauses shrunk, one angle per line, 608x1080 face windows (A x648, B x735, C x570). Whisper-checked, no clipped words.
- **User decisions:**
  - Scene 02 "AI meets ambition and impact" = AMD CES 2023 keynote OMxU4BDIm4M at 24:35 (user's pick), then the 25:05 stage wide for "and impact". Two ~1 s shots, never rushed. "ambition" sits in a neon box.
  - Scene 04 "behind the scenes" = Axios scoop "OpenAI's annual recurring revenue nears $70B" (4x neo capture, assets/axios_openai_70b.jpg). The whole line gets a Vox-style salmon-red highlighter (pin.it/2u519QJuj; `highlight()` multiply band, wipes L->R). The user rejected the red outline box. It tears to reveal the PayPal Mafia photo (pin.it/2HcLca94Y, 2x upscale).
  - **Article highlights everywhere = that same line highlighter** (04 Axios, 05 Al Jazeera, 06 IMF 40%).
  - Scene 05 = everything inside the framed 16:9 box (900x506, bottom y1110; the user wants the box kept). Order: The Social Network formula-on-window (KdtPNRzuKrk 5:00) for "ambition", then the Al Jazeera "X to shut operations in Brazil" headline for "decisions", then a founders match cut (Zuckerberg F8, Pichai Hanoi, Amodei Disrupt, Huang Stanford, Whitney Wolfe Herd wolfe_0; eyes locked, F_FACE 280). Captions above and below the box, key words in neon boxes, typing on.
  - Scene 06 = Pexels 6611069 (woman's eyes over a laptop, the user's pick, teal grade, "Let's talk about the future of" on the left of her face), then BMW humanoid robots (bCkl9hIEb6k, the user's picks 0:15 and 0:28, two cuts) for "work,", then Fei-Fei Li on the TED stage (y8NtMZ7VGmU 0:32) for "leadership,". Her name card goes in the middle of the frame on her chest, never over her head, with captions above her head. Then the IMF 40%-of-jobs line highlighted for "society itself."
  - Scene 09 = extreme close-ups so only half her face shows (CAM C, then CAM B, 3x), text beside it, straight. Then a 3D swing-back revealing the XP desktop, caption neon box low (y1500), not mid. **No chrome hearts anywhere** (the user had them removed).
  - Scene 03 "powered by WomenUp" = 8 iconic women-rising photos (Commons, assets/wu/sources.json) on an aligned 4-column grid around a glowing centre bar. The WomenUp wordmark (keyed off the official Mailchimp banner: assets/womenup_wordmark.png; there's no other logo file) lands with jstyle3.pixel_wipe_down. Show only "Women Up / AI": the user had "Ambition + Impact" removed.
  - "changing tools" = the eBay word-wheel motion (pin.it/258dR99wJ) in Jennifer look, landing on "Power".
  - "changing power" = match cut of OpenAI CEOs (Altman 2019 → Murati → Shear → Altman back → Simo). Each has an "OPENAI CEO" box above the head. Stage photos are cut out (Vision) with glow + vignette, all eyes aligned and filling the frame.
  - "leading it or watching it happen" = Kristina, with "So the question is" on the left. The camera moves and "are you leading it" appears, 3D text in Jennifer style. Then it zooms out to a Windows XP / Media Player desktop (pin.it/5C0OtikIR) as a viewer's POV, with the text in a 3D box.
  - "lean in" line: "sparked" = Pexels 7986752 (woman lit by her laptop in the dark, from the user's "laptop glow face dark" search, night_grade into blue). The caption goes left of her face with "sparked" in a neon box. Then CAM C for "lean in". The match-flare B-roll is dropped.
  - "You're part of the conversation now" = full-screen match cut of studio chair portraits like pin.it/tE3nugifB: Pexels 7957702, 7764118, 7206362 (t=1 s, calm), 35313951. Eyes aligned at C_FACE 370, dark filter, centred neon box. 39303056 and 7761099 were rejected as "not professional"; avoid casual or arms-up poses.
  - When the user picks a B-roll themselves, stop searching right away and build with their pick.

- **Sent (2026-11-20 8:02 pm):** the storyboard PDF (12 pages, 38 stills) went to Krish on WhatsApp as a document with no text. Delivered.

- **16:9 version (2026-11-20):** the user asked to convert the storyboard to horizontal, changing only the ratio ([[edit-rule-ratio-conversion]]).
  - Scripts: jen_stills_h.py (reuses jen_stills helpers at J.W/J.H 1920x1080) and make_stills_h.py (CEO cut + assets/xp_desktop_h.png). Output goes to stills_h/ (38 stills).
  - PDF: `python build_pdf.py h` -> ~/Downloads/"Kristina Shea Show - Trailer Storyboard (16x9).pdf". Photos album "KSS Trailer Storyboard 16x9".
  - Layout: raw talking heads full-frame. Graphics centred. Captions centred or at the 96 px left/right margins. 10b caption on the left beside her head. Match-cut faces on the centre line (scene 11 at C_FACE 520 so the vertical 4K portraits fill 16:9).
  - Edit both versions when a scene changes.

- **Trailer video v1 (2026-11-20, 16:9):** ~/Downloads/KSS_Trailer_16x9_v1.mp4 (31.96 s, 1920x1080). Build: ~/ks-kristina-build/trailer/.
  - edl.py = the take-4 cut. words_cut.json = Whisper word times on the cut. prep.py caches sources in src/ (all-intra cams + Pexels, portrait JPEG frames).
  - render.py `test t..` / `full out.mp4 audio/mix.wav` uses scene functions sc01..sc12 on the jstyle3 engine (~2 min, 9 workers). mix.py does the audio. fin16.py is the 16:9 finish.
  - B-roll recorded live from YouTube in neo (MediaRecorder on the <video>, 1080p) into broll/: Lisa 24:35/25:05, BMW 0:15/0:28, Social Network 5:00. Skip ads by clicking the "Skip" button ref from a snapshot. Disk is nearly full (~7 GB), so don't download whole videos.
  - Voice is the studio mix cleaned locally (high-pass 85 + afftdn). Adobe Enhance was not used. The XP windows play live CAM B/C (masks from xp_key.png).

**Why:** this is a multi-step build across turns and the user reviews stills in Photos.
**How to apply:** continue from the storyboard folder. Every scene uses the Jennifer engine look. Related: [[feedback-reel-style-overrides-ref-look]], [[project-jennifer-musselman-style]].

- **v2 notes (2026-11-20; v2 + v3 rendered, v3 = ~/Downloads/KSS_Trailer_16x9_v3.mp4 after the v2 review):** render.py = v2 (render_v1.py kept); stills in ~/Downloads/"KSS Trailer v2 stills".
  - All text is drawn in screen space after the camera, inside 90 % title safe (x 96-1824, y 54-1026, SMPTE ST 2046-1).
  - 04: the photo is card-sized, so it only shows through the tear; decaying shake at the tear.
  - 05: the box zooms 1.0->1.16 the whole time. AJ -> Engadget -> SCMP headlines carry one continuous highlighter. 14 eye-locked founders, 0.215 s each (assets/s05/founders14.json). 'leaders' stays ~1 s. At 13.30 only the box slides out (G2); 06a slides in from the right (G1).
  - 09: one CAM C shot, zoom 1.0->2.0 (face ~45 %) with Trailer-1 type on her left, left-aligned. Then a pan with right-aligned text. Then a pull-out of the WMP screen with the same frame playing; no transitions.
  - 10a: 4K crop, z 2.0, palette-vibrant grade, big gradient 'sparked' with no box. 10b: only "lean in." on screen right; PX overlay after it.
  - mix.py SFX still on the v1 timeline: update before rendering.
- **v4 final (2026-11-21):** ~/Downloads/KSS_Trailer_16x9_v4_final.mp4.
  - CEO scene: faces cut in place on the tech ground with a teal->blue glow.
  - Flashback riser into 22 s; quieter whooshes; pixel overlay de-duplicated and frame-blended.
  - Sent to Krish on WhatsApp as a document (87 MB, no text) at 12:22 am; delivered.
