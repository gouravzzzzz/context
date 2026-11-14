---
name: edit-rule-fonts-no-big-bold
description: "User dislikes big, bold display text in reels; CHASE_009 uses only Helvetica Regular/Bold + Playfair Display Regular"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 9802d9e8-f883-4a2c-9d65-9a2816a4ab5d
  modified: 2026-11-13T22:45:04.867Z
---

The user doesn't like big, heavy, bold text in reels. That rules out huge display words, Anton-style condensed caps and the heavy extended caps. For the CHASE_009 reel the only fonts allowed are **Helvetica Regular**, **Helvetica Bold** and **Playfair Display Regular**.

**Why:** User said this on 2026-11-14 after I proposed big stacked words from [[typography-board-reference]]: "I don't like to use big and bold text."
**How to apply:**
- Keep text at a modest, caption-to-subtitle scale and not frame-filling.
- Get hierarchy from weight (Helvetica Bold vs Regular), from switching to Playfair Display for an accent word, and from colour. Don't make key words huge.
- From the typography board, still use the layout and motion ideas: tight stacked lockups, word-by-word blur-in, one accent word, short phrases ending in a period. Apply them at restrained sizes.
- Stay inside [[edit-rule-reels-safe-zone]].
- **One baseline per line.** Every word in a line sits on the same baseline, worked out once from the font's ascent/descent. Never centre each word vertically on its own bounding box. v1 did that and "ends up being" came out with "up" 16 px higher and "being" 9 px higher. The user flagged it as misaligned on 2026-11-14. A word can rise during its entrance but must land on the shared baseline. Check in a zoomed test frame that words with descenders (p, g, y) and ascenders (d, b) line up.
- **Never put outline borders or stroked boxes around caption text.** The user called v1's orange stroke box drawn around "REFUSE" weird on 2026-11-14. To emphasise a word, use a **solid filled rectangle behind it**. It covers only that word or phrase's bounds plus small even padding, it wipes in **left → right** on the eased curve as the word is spoken, and it's solid with no stroke, gradient or glow. Text colour contrasts hard against it: in blue+gold, a gold box with deep-navy text, or a deep-blue box with champagne text. Use it on the one accent word per lockup at most.
- **Exception: money and numbers.** Whenever money or a number is counting or being shown ($10M → $1B+, deal values, scores), set it in **Helvetica Bold, BIG**, in the accent colour (gold for CHASE_009), as the emphasised element of the frame. The user asked for this on 2026-11-14 after v2 set the counter in Helvetica Regular at about 92 px: "they are numbers… it should be emphasized". Keep it inside the safe zone (≤694 px wide in the lower block) and keep the digits fixed-width so the counter doesn't jitter. Captions around it stay small.
- Default to the same restraint on future reels unless the user asks otherwise.
