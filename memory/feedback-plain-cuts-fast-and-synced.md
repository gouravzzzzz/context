---
name: feedback-plain-cuts-fast-and-synced
description: "A plain script cut must be quick, and A/V sync must be checked before handing it over (Justin trailer cut, 2026-11-21)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: d40818a3-e4d8-4ac8-86d0-9226ed7d375e
  modified: 2026-11-21T17:45:46.357Z
---

When the user asks only to cut recordings to a script, deliver quickly. Transcribe, snap the cuts to the waveform, render, check, done. Don't spend a long time on analysis.

Before opening or delivering any render, check that:
- the video length equals the audio length;
- every segment has the frame count it should;
- the whole output transcribes to the full script.

**Why:** On 2026-11-21 (Verticals / Justin Levine trailer cut) the user complained twice about the time it took ("how much fucking tim u need just to pput cuts"). Then v1 shipped with its freeze-frame holds dropped: ffmpeg `tpad` after `trim` silently didn't pad, and `-shortest` cut the audio to match. The voices drifted off their faces and the ending went missing.

**How to apply:**
- Use the `loop=loop=N:size=1:start=n-1` filter for holds. Don't use `tpad`.
- Never mux with `-shortest` without first confirming that the video and audio lengths match.
- Build: ~/verticals-justin-build (edl.py = script spans, align.py = wav2vec2 alignment, wav.py = waveform boundaries, render.py).
- Related: [[edit-rule-cut-silence-and-fillers]], [[project-justin-levine-trailer]].
