---
name: feedback-open-reel-after-render
description: Always open the rendered reel (open <file>) as soon as a render is delivered — never make the user ask
metadata:
  node_type: memory
  type: feedback
  originSessionId: 7dcfb924-5526-434b-b5ba-2576bc9038f4
  modified: 2026-11-17T13:53:05.885Z
---

As soon as a reel is rendered and copied to ~/Downloads, run `open <file>.mp4` so it plays for the user. Do this in the same turn as the delivery message.

**Why:** On 2026-11-17 v4 of the Ron documentry reel was delivered without opening it. The user was angry: "do i have to tell you every fucking time to open the reel when its rendered".

**How to apply:** On every video deliverable (any style, any version, previews included), the last step before reporting is `open` on the delivered file. Related: [[skill-documentry-style]].
