---
name: github-context-repo
description: "Our GitHub repo" = github.com/gouravzzzzz/context (public). Holds chats/ + memory/ + README. Push via neo web upload (no gh, no git creds).
metadata:
  type: reference
---

When the user says "push everything to our github repo", they mean **https://github.com/gouravzzzzz/context**.
- **Visibility:** the repo is PUBLIC.
- **Contents:**
  - `chats/`: every Claude Code session as Markdown.
  - `memory/`: these memory notes.
  - `README.md`: chat index table.

**How to push:** there is no `gh` CLI, no git credentials and no local clone, so upload through the BrowserOS neo web UI.
1. **Export the chats.** Use `conv.py`; saved at `~/.claude/projects/-Users-gourav/tools/conv.py` (if that's gone, recover it from session a1803d75's transcript).
   - Command: `python3 -I conv.py ~/.claude/projects <out>/chats`.
   - Its output builds the README index.
   - Copy `~/.claude/projects/-Users-gourav/memory/*.md` into `<out>/memory`.
2. **Redact before uploading** (it's public). Remove:
   - the user's email, including escaped and fragment forms like `[email redacted]`
   - `[email redacted]`
   - `[email redacted]`
   - `token=` URL params
   - WeTransfer IDs
   - Frame.io `state=` values
   Then grep for keys, tokens and private keys.
3. **Upload** at `github.com/gouravzzzzz/context/upload/main/chats`, then `/memory`, then root for the README. Set the commit summary and commit straight to main. File names stay stable (`date_title_sid8.md`), so re-uploads overwrite instead of duplicating.
   - The upload page heading says "Uploading files to …", so don't use the word "uploading" as a busy signal.

**Log:** last full push 2026-11-22 (31 chats, 48 notes, 3 commits).
