---
name: project-ron-foxcroft-kss-shorts
description: "Kristina Shea Show x Ron Foxcroft shorts in the Gillian B-roll style; build folder, renderer, raw offset, status of reel 1 and the plan to save the style as a new skill"
metadata:
  node_type: memory
  type: project
  originSessionId: b0ec8700-62e7-4f66-ba88-9a5af74d9123
  modified: 2026-11-14T22:00:53.316Z
---

Started 2026-11-15. The user asked for KSS Ron Foxcroft short 01 ("400 REFEREES. ONE 2AM WHISTLE.") in the Gillian B-roll style from the flourish-broll-reels skill ONLY (they said not to use the talking-head skill). They will send their own references and changes; after one perfect reel the style gets saved as a new skill (dime-studio-skillmaker).

- Script: ~/Downloads/"KSS Ron Foxcroft Shorts (raw timecodes).docx" (4 shorts; red struck text = cut). Raw camera: ~/Downloads/DSC_6680.MP4 (Ron, 1920x1080 29.97). DSC_6681 = Natalie Pierre's camera. Doc times are on Stereo Mix.wav (Dropbox, not on laptop); the camera runs 4:51 behind (doc 57:38 = camera 52:47).
- Build: ~/ks-ron-build/reel1/ (work/plan.py = blocks/shots/captions, work/render.py = compositor, work/edl.py + edl2.py = cut list, work/audio_cut2.py). Run `./py work/render.py test <secs> --half` for frames, `full <out.mp4>` for the reel. Multi-face Vision tool: ~/ks-ron-build/tools/allfaces.
- v1 draft: ~/Downloads/Ron_TH_001_v1.mp4. v2 (2026-11-15): ~/Downloads/Ron_TH_001_v2.mp4 + Ron_TH_001_v2.srt, notes out/REEL-NOTES.md.
- v2 = new combined style: Gillian B-roll style kept as is + the user's reference short (BigDeal x Robert Greene, youtube.com/shorts/L4VfeQ57AkE, every frame studied in refs/codie/STUDY.md): black Inter on white box captions for speaker/seam, serif (Instrument Serif) glow stacks with blur-in on speaker punch lines, guest intro card (name + blue tick + title), drop shadow on all text. Fonts in reel1/fonts/. Audio = Adobe Enhance of cam 3160-3260 (src/ron_enhanced.wav). Opener = Trump whistle, Easter Egg Roll 1080p.
- v3 (2026-11-15): glitch frame fixed, music bed (Too Many Nights instr., -27 LUFS; user wants beds at -29 to -25 dB), sent to Krish on WhatsApp (chat "Krish") as a document. Render muxes work/final_mix.wav.
- v6 (2026-11-15 4:50 am): Night Riser instrumental at -37 LUFS, steady Ron framing, interpolated HISTORY clips. Sent to Krish on WhatsApp with no text (v3/v4 deleted for everyone). Only v6 kept in ~/Downloads (Ron_TH_001_v6.mp4 + .srt); older versions deleted at the user's request.
- Next: user reviews v6; once "perfect", package the combined style as a new skill with dime-studio-skillmaker.

**Why:** the style is being defined on this reel, so the next session must pick up the exact build rather than restart.
**How to apply:** read REEL-NOTES.md and plan.py before changing anything; apply the user's notes to plan.py/render.py and re-render. Related: [[flourish-edit-sop]], [[youtube-download-route]].
