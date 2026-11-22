---
name: edit-rule-music-bed-level
description: Music under speech is instrumental only (never lyrics) and sits at -35 to -38 LUFS; voice stays -14 LUFS
metadata:
  node_type: memory
  type: feedback
  originSessionId: b0ec8700-62e7-4f66-ba88-9a5af74d9123
  modified: 2026-11-14T23:18:32.431Z
---

**Never choose a song with lyrics.** Only true instrumentals: no sung words, rap, vocal chops, ad-libs or producer tags in the part used. The user said on 2026-11-15: "never choose a song that has lyrics in it remember this and add this rule to your skillfile as well". The Metro Boomin "Too Many Nights [Instrumental]" file still had a vocal, so a title saying "instrumental" proves nothing. Screen the used part with Whisper. A phrase with avg_logprob above -1 that isn't a stock hallucination ("Thank you.", "Music", a repeated loop) means a vocal, so drop the track. Royalty-free Pixabay-style instrumentals in ~/Downloads are the safe pool.

**Level:** the bed stem sits at **-35 to -38 LUFS** (use -37), the voice stays at -14 LUFS, and the mix is limited to -1 dBTP. The first ask was -29 to -25 dB, but the user then said it was too loud and asked for "-35 or -38db". The track should suit the topic, and its builds should land on the edit's cuts.

The rule is also written into the flourish-broll-reels SKILL.md (Krish's rules, above "Never."). Related: [[project-ron-foxcroft-kss-shorts]], [[flourish-edit-sop]].
