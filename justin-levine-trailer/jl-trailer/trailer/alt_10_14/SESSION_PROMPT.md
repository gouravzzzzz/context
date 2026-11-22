You are the session for the Justin Levine (Shepherd) trailer, section 10–14 s: the 3D z-space redo of the name card. Krish opened this terminal tab for it. Keep working in this tab, take Krish's notes, and deliver STILLS ONLY unless he says to render video.

Read these first:
- Memory: project-justin-levine-trailer plus every edit-rule/feedback memory. They auto-load.
- ~/jl-trailer/refs/study_wistia_4_5.md: the frame study of the reference (the Dime "Sports Bra" trailer, https://dimemotion.wistia.com/s/2zna71kiy7ku86m, 4–5 s). The video file is ~/jl-trailer/refs/dl/dime_trailer.mp4.
- ~/jl-trailer/trailer/alt_10_14/scene3d.py: the build. It imports ../engine.py and ../shots.py read-only. Never edit engine.py, shots.py, render.py or mix.py: they made the delivered v1 (~/Downloads/Verticals_Justin_Levine_Trailer_v1.mp4).
- ~/jl-trailer/trailer/alt_10_14/stills/: s_09.50 … s_14.25 .png plus sheet.jpg (current version, already shown to Krish).

Where it stands (v1 of this section, done 2026-11-22):
- **The ask:** "at 10 to 14 secs lets do this using justin levine's footage with shepherd broll … see from 4 sec to 5 sec do that with same text animation and move the text along with camera in a 3d way … use z axis movement … give me only stills".
- **What the ref does at 4–5 s:**
  - Settled layout: photo card on the left, a cut-out person with an ice-blue sticker outline right of centre, and a 2-line caption.
  - Text reveal: "Seats" fades in over 2–3 frames, then the bold word pops in over 1–2 frames.
  - "that's / Insane" types on letter by letter at the far right.
  - Camera: a 2.5D truck right plus a push forward past the person (slow ease-in, peak f146–147, 7-frame ease-out).
  - Parallax: card about 540 px, person about 500 px scaling 1.4× and going out of focus (nearest layer), headline about 280 px (farthest).
- **The build:**
  - Pinhole camera with focal 1600. Layers from back to front:
    - tech ground at Z 4300;
    - headline at Z 2850;
    - s_shep_sign card at Z 2050;
    - "Justin / Levine" caption at Z 1960;
    - Justin cut-out with sticker outline at Z 1600 (c_shep_1, then c_shep_20 frames 0–40 cut at 11.92; mattes in alt_10_14/matte/).
  - Camera: creep moves stacked every 0.6 s plus the main move from 10.80 over 2.5 s (truck 500, push 390, yaw to 2.6° and back), all on Krish's graph EASE_USER = cubic-bezier(0.68,0,0.03,1).
  - Effects: focus rack to the headline, up to 14 sub-frames of motion blur.
  - Transitions: G1 zoom-through in from Nic, G2 out into v1's 02d at 14.16.
  - Text: "Justin" fades with a 12 px rise; "Levine" (gradient) pops; "co-founder and CEO of / Shepherd." types on at the word times. All text is inside 90% title safe.
- **Flagged to Krish:**
  - "Justin" reads small and low-contrast over the grey sign.
  - Justin stays blurred about 2 s (12.9–14.1) while talking.
  - His second take plays at about 0.6× speed (a video would need optical-flow in-betweens).
  - The truck is 2.5 s, not the ref's 0.73 s.

Rules:
- Copy the reference's motion exactly, but keep the trailer's own look (Jennifer/Trailer-1 type, cyan→blue gradient key words, tech ground).
- Text lands straight, never on faces, aligned by side.
- Every move on EASE_USER with keyframe overlapping. Transitions are G2 out / G1 in.
- Never close browser tabs, terminal tabs or folders Krish didn't ask to close. The Wistia ref stays open in neo.
- New filenames only.
- Use ~/ks-ron-build/venv/bin/python. ffmpeg is /Users/gourav/ks-ron-build/reel1/ff.

Now: read the files above, `open ~/jl-trailer/trailer/alt_10_14/stills/sheet.jpg`, reply with a 3-line status, and wait for Krish's notes.
