---
name: whatsapp-close-tab
description: Always close the WhatsApp Web tab in neo as soon as a WhatsApp job (sending a file or message) is done
metadata:
  node_type: memory
  type: feedback
  originSessionId: b0ec8700-62e7-4f66-ba88-9a5af74d9123
  modified: 2026-11-14T23:24:22.020Z
---

After any WhatsApp job in BrowserOS neo (sending a reel to Krish, deleting a message), close the web.whatsapp.com tab right away once the send is confirmed. Don't leave it open.

**Why:** On 2026-11-15, after v6 was sent to Krish, the user said: "always close whatsapp tab after the job is done remember that".

**How to apply:** Send, confirm the message shows Sent or Delivered, then close the tab in the same turn, before reporting back. Related: [[project-ron-foxcroft-kss-shorts]].
