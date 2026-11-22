---
name: edit-rule-transition-ease-pair
description: GLOBAL transition easing: outgoing half on graph 2 (ease-in, cubic-bezier(1,0,1,1)), incoming half on graph 1 (ease-out, cubic-bezier(0,0,0,1)) — speed peaks at the cut
metadata:
  type: feedback
---

Every transition between two animations or shots, such as a zoom-through, push or slide, uses one pair of curves:
- **Outgoing:** the old scene's exit move runs on Krish's **graph 2**, cubic-bezier(1, 0, 1, 1). It starts slowly and speeds up into the cut.
- **Incoming:** the new scene's entry move runs on **graph 1**, cubic-bezier(0, 0, 0, 1). It arrives at full speed and slows into place.
- **At the cut:** speed is highest exactly at the cut. Hide the join with a very short (about 2-frame) dissolve.

**Why:** Krish showed both graphs on 2026-11-19 (Ron short 02, Women → Solopreneur) and confirmed: "Out: Graph 2, In: Graph 1".

**How to apply:** this is global, for every reel and every skill. Each half lasts about 0.3 s. It's separate from [[ease-graph-user-smooth]], which is for moves inside a shot. Related: [[edit-rule-smooth-motion]].
