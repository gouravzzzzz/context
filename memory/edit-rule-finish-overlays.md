---
name: edit-rule-finish-overlays
description: Finish pass on graphic/photo scenes - strong motion blur on all motion, vignette, radial fast blur overlay, Texturelabs paper textures as luminance-only overlays
metadata:
  type: feedback
---

On every reel's photo and graphic scenes (not the talking-head raw): real motion blur on every move, graphic animation and transition; a vignette; a subtle radial fast blur (AE CC Radial Fast Blur look) toward the edges as an overlay; and paper textures from ~/textures (Texturelabs_Paper_316L general, 317L with the crease for document/paper/table scenes) applied as overlays, taking only the texture, never the colour (high-pass the luminance, then multiply it in).

**Why:** User on CHASE_009 v4 preview3 (2026-11-14): "add motion blur to every movement, graphics and transitions... add a vignette and radial fast blur effect as an overlay and use these textures... dont take the colors from these images only take the textures."

**How to apply:** Build it into the renderer's final pass, weighted by scene type through crossfades. Related: [[edit-rule-smooth-motion]], [[edit-rule-real-assets-over-shapes]].
