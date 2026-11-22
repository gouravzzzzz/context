---
name: feedback-reel-style-overrides-ref-look
description: "When a reel has a named style (e.g. Jennifer), every animation ref the user sends sets only the MOTION; fonts/colours/ground/elements always come from the reel's style"
metadata:
  node_type: memory
  type: feedback
  originSessionId: dde13ef9-61ad-492b-9d95-72e6348c0a4f
  modified: 2026-11-20T13:19:24.612Z
---

When the user names a style for a reel ("this reel is gonna be in jennifer style") and then sends a Pinterest/IG ref for one animation, copy only the ref's motion and structure (e.g. the eBay word wheel: list steps up, active row with an arrow, contrast steps). Render it entirely in the reel's style: font, colours, background, elements and finish. Never import the ref's own palette or typeface.

**Why:** On the Kristina Shea trailer storyboard (2026-11-20) I copied the eBay pin's yellow ground and Helvetica Bold for "Because AI isn't just changing tools". The user said: "why the fuck are we using yellow and this font i told you to use jennifer style font and colors and background and elements and everything as this reel is gonna be in jennifer style".

**How to apply:**
- Before building any animation, check which style the reel is in.
- For Jennifer style, build it with the skill's own engine (`~/.claude/skills/jennifer-musselman-style/scripts2/jstyle2.py`: TechBG, number_row, binary_strip, glitch_blocks, text_rgba, typed_word, grad, glow_screen).
- [[feedback-copy-reference-exactly]] still applies to the motion: timing, layout and steps. It does not apply to the ref's look when the reel has its own style.

Related: [[feedback-animations-must-mean]], [[project-kristina-shea-trailer]].
