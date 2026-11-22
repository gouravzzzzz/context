# Verticals trailer: Justin Levine (Shepherd)

A 16:9 trailer for the Verticals episode with Justin Levine, co-founder and CEO of Shepherd, with Nic and Luke Sophinos.
It is 1080p at 24 fps, 2175 frames long (90.6 s), and mixed to -14 LUFS.
Everything was built in Python (numpy, OpenCV, ffmpeg). Only the SFX pass is in After Effects.

This folder has all the code, notes and timing data for the trailer, from the script cut to v7.
- **Not included:** the video renders, episode recordings and B-roll. They are too large for GitHub and they stay on the edit Mac.
- **Storyboard:** [Trailer_Storyboard.pdf](Trailer_Storyboard.pdf).

## Versions

| Version | Date | What changed |
|---|---|---|
| Script cut | 2026-11-21 | Script v4 cut from the three episode tracks (`verticals-justin-build/`) |
| Storyboard | 2026-11-21 | 10 scenes / 51 stills in the Jennifer look with Twiml + Dime motion, every B-roll source linked |
| v1 | 2026-11-22 | First full render: 31 shots, overlapped camera chain, zoom-through / whip / flash transitions |
| v2 | 2026-11-22 | Recut (28 cuts on a new timeline), Adobe-enhanced voice, 14 segments, new 3D name card, 15–19 s showcase, Autodesk 20 s |
| v3 | 2026-11-22 | 3×3 grid into Nic, manufacturing card wall, photo strip → collage, cut-on-word opening captions, purple accents |
| v4 | 2026-11-22 | All hits and risers removed, carousel glitch fixed (sequential decode) |
| v5 | 2026-11-22 | Music removed, voice rebuilt with 0 dropouts, steady talking heads, every ease on Krish's 3 graphs only |
| v6 | 2026-11-22 | "Shepherd." exits up, founded cut-out rises, full-screen Breaking News on Luke, clean end, room-tone bed |
| v7 | 2026-11-22 | Breaking News box behind Luke (matte), voice through Adobe Enhance again |
| v7 SFX | 2026-11-22 | 84 SFX layers placed in an After Effects project over the v7 picture (`trailer/sfx_ae/`) |

## Easing

Every move uses one of Krish's three graphs (`trailer/engine.py`):

- **EU**: `cubic-bezier(0.68, 0, 0.03, 1)`, the S-curve for moves inside a shot.
- **G1**: `cubic-bezier(0, 0, 0, 1)`, for incoming moves. It is fastest on the cut.
- **G2**: `cubic-bezier(1, 0, 1, 1)`, for outgoing moves. It is fastest at the cut.

## Folder map

| Path | What it is |
|---|---|
| `verticals-justin-build/` | Script cut: word alignment, EDL, room tone, first cut render |
| `jl-trailer/storyboard/` | Storyboard stills (`jl_stills.py`) and PDF builder (`build_pdf.py`) |
| `jl-trailer/refs*/` | Frame-by-frame studies of the reference trailers and pins (`study_*.md`) plus their timing data |
| `jl-trailer/trailer/engine.py` | Shared engine: footage readers, mattes, face track, overlapped camera chain, text items, the 3 graphs |
| `jl-trailer/trailer/shots.py`, `render.py` | v1 shots, transitions, motion blur and finish |
| `jl-trailer/trailer/newcut.py`, `newtime.py` | The v2 recut and the old-to-new timeline map |
| `jl-trailer/trailer/render_v2.py` | Renders the v1-based segments on the new timeline, with every later fix |
| `jl-trailer/trailer/open_v3/` … `v2segs/seg15/` | One folder per redesigned segment (opening, 3D name, showcase, grid, Procore, $ / 15 %, TV counter, manufacturing, collage → Lloyd's) |
| `jl-trailer/trailer/audio_v5/`, `mix*.py` | Voice rebuild (joints, room tone, dropout repair) and the mixes |
| `jl-trailer/trailer/assemble_v*.py` | Joins the 13 segments with the mix into each delivered version |
| `jl-trailer/trailer/sfx_ae/` | SFX cue list, level measurement and the After Effects script that places the layers |
| `jl-trailer/trailer/v5log/`, `v6log/` | Parallel render lanes |

## Rendering v7

Use the Python venv with numpy, opencv, Pillow and scipy.

```
cd jl-trailer/trailer
python assemble_v7.py        # joins v2segs/* with audio/mix5.wav -> Verticals_Justin_Levine_Trailer_v7.mp4
```

To redo a segment, run its own script first. The lane scripts in `v5log/` and `v6log/` show every segment command.

## Chats

The full working chats for this trailer are in [`../chats`](../chats):

- [Verticals trailer recording cuts](../chats/2026-11-21_Verticals-trailer-recording-cuts_d40818a3.md) (and [part 2](../chats/2026-11-21_Verticals-trailer-recording-cuts_044e7b7b.md))
- [Script v4 → storyboard](../chats/2026-11-21_Verticals-trailer-script-v4-storyboard_a1d89f7a.md)
- [Storyboard → video v1–v4](../chats/2026-11-21_Verticals-trailer-script-v4-storyboard_38bd0f11.md)
- [10–14 s 3D name card](../chats/2026-11-21_Justin-Levine-trailer-10-14s-3D-name-card_e3efc8c3.md)
- [v5–v7, voice fixes and the AE SFX pass](../chats/2026-11-22_Trailer-voice-audio-and-stabilization-fixes_d3939120.md)
