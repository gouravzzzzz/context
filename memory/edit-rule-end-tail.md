---
name: edit-rule-end-tail
description: Never end a reel on the last syllable; let the final word finish, then a short held tail with music fading
metadata:
  type: feedback
---

The final spoken word must finish completely. Never end the video or the audio on the last syllable.

**Why:** Ron short 02 (2026-11-19): the reel ended 40 ms after "systems". The mix was still loud on the last frame, so the word sounded chopped. Krish: "she doesnt finish the word completely it gets off".

**How to apply:**
- Find the word's real end in the source audio: a high-pass band shows where the final "s"/fricative ends. Whisper word ends are rough.
- Stop the voice just after that, with a ~40 ms fade before the next word starts.
- Add a ~0.6 s tail. If the speaker keeps talking in the source, hold the last frame while the camera keeps its slow eased push. Keep the caption on and fade the music out to silence.

Related: [[edit-rule-cut-silence-and-fillers]], [[edit-rule-music-bed-level]].
