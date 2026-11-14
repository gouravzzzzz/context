# Bypass mode toggle

Session `2029c80f-38ad-497f-a416-cf8bba43806b` · started 2026-10-22 20:00

---

### 🧑 User · 2026-10-22 20:00

Turn on the bypass mode for me.

### 🤖 Claude · 2026-10-22 20:00

I can't switch permission modes myself, but you can do it in a few ways:

**Right now, in this session:** press **Shift+Tab** to cycle through permission modes until the status line shows bypass permissions. It only shows up in that cycle if bypass was enabled when the session started. If you don't see it, use the next option.

**At launch:**
```
claude --dangerously-skip-permissions
```

**As your default:** add this to `~/.claude/settings.json`:
```json
{
  "permissions": {
    "defaultMode": "bypassPermissions"
  }
}
```

In bypass mode, every tool call runs without asking, including file deletions, shell commands and messages sent through your connected accounts (Slack, mail, Notion and so on). You're running in auto mode now, which already skips most prompts while still checking the risky actions. That may be enough for what you need.

### 🧑 User · 2026-10-22 20:01

It's my laptop, so turn on the bypass formation mode for me now. I want it permanently on.

### 🤖 Claude · 2026-10-22 20:01

**🔧 Bash**
```
{
 "command": "cat ~/.claude/settings.json 2>/dev/null || echo \"NO_FILE\"",
 "description": "Show current user settings file"
}
```

### ↩️ Tool · 2026-10-22 20:01

<details><summary>result</summary>

```
{
  "theme": "dark"
}
```
</details>

### 🤖 Claude · 2026-10-22 20:01

**🔧 Bash**
```
{
 "command": "cat > ~/.claude/settings.json <<'EOF'\n{\n  \"theme\": \"dark\",\n  \"permissions\": {\n    \"defaultMode\": \"bypassPermissions\"\n  }\n}\nEOF\ncat ~/.claude/settings.json",
 "description": "Set default permission mode to bypass in user settings"
}
```

### ↩️ Tool · 2026-10-22 20:01

<details><summary>result</summary>

```
{
  "theme": "dark",
  "permissions": {
    "defaultMode": "bypassPermissions"
  }
}
```
</details>

### 🤖 Claude · 2026-10-22 20:01

I've set bypass permissions as your permanent default in `~/.claude/settings.json`, and kept your dark theme:

```json
{
  "theme": "dark",
  "permissions": {
    "defaultMode": "bypassPermissions"
  }
}
```

It won't switch on in this session. Every new Claude Code session will start in bypass mode, so restart with `/exit` and then `claude`. The first time, Claude Code may ask you once to accept the bypass warning.

To undo it, delete the `permissions` block from that file.
