---
name: feedback-keep-ref-tabs-open
description: "Never close or stop anything Krish didn't ask to close (browser ref tabs, terminal sessions, running tasks); \"new terminal tab\" = a real Terminal.app Claude session"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 38bd0f11-486d-4e3a-b942-c55a0475a391
  modified: 2026-11-21T20:22:44.062Z
---

Never close, stop or kill anything the user didn't explicitly ask to close. That covers neo reference tabs, terminal tabs/sessions, background tasks and folders. On 2026-11-22 the user objected to each of these in turn:
- "that tab you created should stay on tabs section";
- "why did you close the first [terminal]? did i ask";
- "i didnt ask you to stop that", after I stopped a running background agent to move it.

**Why:** the user keeps references and parallel jobs open to watch and return to. Closing or stopping them unasked loses work and their trust.

**How to apply:**
- Leave neo reference tabs open even when a tool tip says to close the tab group. WhatsApp is still the exception ([[whatsapp-close-tab]]).
- "Do this in a separate / new terminal tab" means a REAL Terminal.app session the user can see and type into, running `claude` with a self-contained prompt file. Background Agent forks vanish when they finish, so they don't count.
- Open one with `osascript -e 'tell application "Terminal" to do script "cd ~ && claude \"$(cat PROMPT.md)\""'`. It opens as a new window: System Events keystrokes (Cmd+T) are blocked, because osascript has no Accessibility permission. Start in `~` so the memory loads.
- Never stop a running job to "move" it. Let it finish, or ask first.
