---
name: edit-rule-no-text-on-person
description: "Never put text on a face. Documentry style (2026-11-17): text on bodies is allowed; other styles: keep text off people entirely"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 01d5ebb5-e3f5-41de-acc8-d68152ee9db3
  modified: 2026-11-14T17:34:21.246Z
---

No caption, title, text or graphic may sit on any part of a person in photo or graphic scenes: not the face, not the head or hair, not the body. Exception (user, 2026-11-14): normal talking-head captions may sit on the speaker's chest as before. Place type only in empty background around them, and check it with a person mask (rembg) on every frame, not by eye.

**Why:** CHASE_009 v4 preview 2 put the photo-scene type over Chase's head and face. The user was angry ("why tf is that?? remember this from now on").

**How to apply:** On every reel, for every scene with a person (talking head, photos, cutouts): compute the person mask, keep all text boxes off it with a margin, and fail the test render if any box overlaps. If there is no empty space, reframe the shot (within [[edit-rule-talking-head-framing]]) or move the type, never overlap. Related: [[edit-rule-reels-safe-zone]].

**Update (user, 2026-11-17, documentry style / Ray Lucia reels):** "let's now put text on people's bodies like it's done in the reference, but only thing is don't put any text on the face." In the documentry style, captions may sit on bodies and clothing, never on a face (or head). Still check faces with a mask. The no-person rule above still applies to the Flourish/Chase styles unless the user says otherwise.
