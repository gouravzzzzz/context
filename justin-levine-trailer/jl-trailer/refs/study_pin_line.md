# pin.it/2AbnLjOI5 — line draw-on reference (for JL trailer 15-19 v3)

Source: https://v1.pinimg.com/videos/iht/hls/8e/ed/06/8eed066a4a1d57f22782d95c28b5ea20_720w.m3u8 -> refs/pin_line/pin.mp4
(720x1280, 28 fps, 5.75 s; duplicate-frame cadence). Frames in refs/pin_line/f/, sheet.jpg, draw4.jpg, head24.png.

* Look: one thin (~4 px at 720w) flat white stroke on flat red, butt cap, no glow in the ref itself.
* Path: enters from the right edge low, dips (U), bends up, then an S-wiggle rising and leaving through the top.
* Draw-on (head tracked per frame, head_track.json): frames 7 -> 71 on screen. Progress comes in SURGES:
  burst 1 peaks ~110 px/f 0.15 s in, slows to ~11 px/f; burst 2 peaks ~98 px/f at ~1.3 s, slows to ~12 px/f;
  then a steady ~25 px/f exit. Frames 7-53 (both surges, 1.64 s) = the draw-on used in v3 (assets/line_ref.json).
* Tail: holds ~0.5 s once off-screen, then the tail chases along the path (frames 86-137) and the line drains out the top.
* Camera: static in the ref.

v3 use: path mirrored + fitted TT card bottom -> BC pill bottom-left on the logos' plane (z -120), perpendicular
excursion x0.56 so the head never leaves frame; draw-on time-scaled 1.64 s -> 1.00 s (17.60-18.60) so the camera
travel chases the head and it lands with "to". Look per Krish: 2.6 px lavender core (235,215,255), additive purple
(150,70,255) glows at 6/18/45 px, hot-spot head that fades once landed. No tail erase (scene ends on BC).
