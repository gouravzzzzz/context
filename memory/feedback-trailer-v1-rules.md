---
name: feedback-trailer-v1-rules
description: Krish's rules from the KSS trailer v1 review — title safe, tear reveals, key-word hold time, eye-locked fast match cuts, zoom out of a screen, Trailer 1 type
metadata:
  type: feedback
---
From the review of the Kristina trailer v1 (2026-11-20):
- **Text never leaves the frame.** For 16:9 trailers, every text goes inside the 90 % title safe (SMPTE ST 2046-1 / Netflix: 5 % margin per side). Draw text in screen space after camera moves.
- **A reveal under a tear/wipe must be hidden until the tear.** Size the revealed photo exactly like the card. Add a quick decaying shake on the impact.
- **Key words stay readable.** A boxed key word holds ≥ ~1 s; it doesn't flash on and off.
- **Match cuts:** every face is eye-locked to the same point, size and roll (similarity transform on the eye pair). Use many images and cut fast (~0.2 s).
- **"Zoom out of a computer screen" = no transition.** The same frame keeps playing inside the window as the camera pulls out to the interface.
- **Speaker captions in trailers = Trailer 1 type** ('~/Krish works/Trailer 1.mp4' 0:41-end): big natural-width serif, tight leading, the key word on a solid gradient box, shadows. Aligned to the side the text sits on.
- Camera moves are slower and overlapped; cuts stay fast.
**Why:** v1 had text out of frame, an early reveal, misaligned slow founders, a 0.4 s key word, and tiny shadowless captions. Krish was angry about the scene-09 captions.
**How to apply:** check these on every trailer/reel before stills. Related: [[project-kristina-shea-trailer]], [[edit-rule-text-alignment-by-side]], [[technique-keyframe-overlapping]].

From the v2 review (2026-11-20):
- **Never repeat a caption that's already on screen.** Each shot shows only its new words (e.g. after the "leaders" box, the next lead is just "and"; "the future of" doesn't repeat on the next shot).
- **Text over a moving speaker shot is tracked to the footage.** It zooms and pans with it (rgba layer warped by the camera).
- **A shake starts on the impact frame** (the tear rips open at once) with sub-frame motion blur over the whole frame.
- **Slides keep a finite, matched speed.** Out = ease-in, in = ease-out at the same speed, real motion blur. Never graph-1 jumps.
- **Cut-out faces + tags slide up from below** on each match cut. Cut-out photo backgrounds have no visible edges.
- **Typed words never re-centre while typing** (lay out the full word first).
- **The vignette must be clearly visible** (fin16 vig ~0.6).
- **"Slide in from below" on a match cut = ONE slow rise for the whole group** (all faces + tags ride the same move; the cuts happen during it). Not a separate fast slide per face. Start only ~150 px below (faces already clearly visible) and rise steadily into the transition. Mask the people: only the cut-out + tag on a clean dark ground, no photo or blurred fill behind.
- **SFX choices:** show 3–4 options per scene as preview clips (prev_sfx.py) before adding anything. Krish picked only the Flashback riser into 22 s and kept the other scenes as they were.
- **No stuck frames:** a 24 fps overlay (the pixel transition .mov) in a 29.97 timeline repeats frames and reads as the video "getting stuck". Blend between overlay frames. Before delivery, scan every render for stuck frames (blurred frame diff ≈ 0 between moving neighbours).
- **Never overwrite a preview/render the user already opened.** QuickTime / Quick Look keep showing the cached old file, which looks "stuck". Write every new render to a new file name and close the old QuickTime documents first.
- **Never close or delete a video the user has open or is watching.** No `osascript ... close every document` and no rm of their files. Write fixes to a new file name and tell them.
