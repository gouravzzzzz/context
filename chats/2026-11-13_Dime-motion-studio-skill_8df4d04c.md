# Dime motion studio skill

Session `8df4d04c-7a05-4edd-a940-d03b81e0da24` · started 2026-11-13 21:09

---

### 🧑 User · 2026-11-13 21:09

~/.claude/skills/<dime motion studio>/SKILL.md

### 🤖 Claude · 2026-11-13 21:09

**🔧 Bash**
```
{
 "command": "ls -la ~/.claude/skills/ 2>&1; ls ~/.claude/skills/*/ 2>/dev/null",
 "description": "List installed skill folders"
}
```

### ↩️ Tool · 2026-11-13 21:09

<details><summary>result</summary>

```
total 0
drwxr-xr-x@  4 gourav  staff  128 23 Oct 01:31 .
drwxr-xr-x@ 17 gourav  staff  544 14 Nov 02:39 ..
drwxr-xr-x@  4 gourav  staff  128 14 Nov 00:46 browseros-neo
drwxr-xr-x   4 gourav  staff  128 23 Oct 01:31 synced
/Users/gourav/.claude/skills/browseros-neo/:
SKILL.md

/Users/gourav/.claude/skills/synced/:
7ca739cc-9c4e-48fc-b94d-8a6c26882a29_8d10cb92-415e-41f8-9fd3-6e6d8badb275
```
</details>

### 🤖 Claude · 2026-11-13 21:09

**🔧 Bash**
```
{
 "command": "find ~/.claude/skills -maxdepth 4 | head -50; grep -ril \"dime motion\" ~/.claude/skills 2>/dev/null | head",
 "description": "Search skill folders for Dime Motion"
}
```

### ↩️ Tool · 2026-11-13 21:09

<details><summary>result</summary>

```
/Users/gourav/.claude/skills
/Users/gourav/.claude/skills/synced
/Users/gourav/.claude/skills/browseros-neo
/Users/gourav/.claude/skills/synced/.bucket-7ca739cc-9c4e-48fc-b94d-8a6c26882a29_8d10cb92-415e-41f8-9fd3-6e6d8badb275
/Users/gourav/.claude/skills/synced/7ca739cc-9c4e-48fc-b94d-8a6c26882a29_8d10cb92-415e-41f8-9fd3-6e6d8badb275
/Users/gourav/.claude/skills/browseros-neo/SKILL.md
/Users/gourav/.claude/skills/browseros-neo/.browserclaw-managed.json
/Users/gourav/.claude/skills/synced/7ca739cc-9c4e-48fc-b94d-8a6c26882a29_8d10cb92-415e-41f8-9fd3-6e6d8badb275/morning
/Users/gourav/.claude/skills/synced/7ca739cc-9c4e-48fc-b94d-8a6c26882a29_8d10cb92-415e-41f8-9fd3-6e6d8badb275/.staging
/Users/gourav/.claude/skills/synced/7ca739cc-9c4e-48fc-b94d-8a6c26882a29_8d10cb92-415e-41f8-9fd3-6e6d8badb275/deep-research
/Users/gourav/.claude/skills/synced/7ca739cc-9c4e-48fc-b94d-8a6c26882a29_8d10cb92-415e-41f8-9fd3-6e6d8badb275/xlsx
/Users/gourav/.claude/skills/synced/7ca739cc-9c4e-48fc-b94d-8a6c26882a29_8d10cb92-415e-41f8-9fd3-6e6d8badb275/pdf
/Users/gourav/.claude/skills/synced/7ca739cc-9c4e-48fc-b94d-8a6c26882a29_8d10cb92-415e-41f8-9fd3-6e6d8badb275/import-memory
/Users/gourav/.claude/skills/synced/7ca739cc-9c4e-48fc-b94d-8a6c26882a29_8d10cb92-415e-41f8-9fd3-6e6d8badb275/docs
/Users/gourav/.claude/skills/synced/7ca739cc-9c4e-48fc-b94d-8a6c26882a29_8d10cb92-415e-41f8-9fd3-6e6d8badb275/the-humanizer
/Users/gourav/.claude/skills/synced/7ca739cc-9c4e-48fc-b94d-8a6c26882a29_8d10cb92-415e-41f
…[4630 chars truncated]
```
</details>

### 🤖 Claude · 2026-11-13 21:09

I couldn't find a file at `~/.claude/skills/<dime motion studio>/SKILL.md`. The `<dime motion studio>` part looks like a placeholder, and no folder by that name exists.

The only skills in `~/.claude/skills/` are:
- `browseros-neo/`
- `synced/…/`, which holds the claude.ai-synced skills. The only Dime Motion one there is **`flourish-broll-reels`** (B-roll reels for Flourish podcast clips).

What do you want to do?

1. **Use the existing skill.** I'll load `flourish-broll-reels` and start on a reel. Send me the episode or clip.
2. **Create a new `dime-motion-studio` skill** at `~/.claude/skills/dime-motion-studio/SKILL.md`. It could combine your saved Flourish Edit SOP and the notes on your Arnold reference reel with the Dime Motion portal workflow (episodes, going out next, approvals, captions). Tell me what it should cover, or I'll draft it from those and you can edit it.
3. **Point me to the file.** If the skill lives somewhere else, paste the real path.

### 🧑 User · 2026-11-13 21:10

is there any skill file is installed, named Dime Motion Studio.

### 🤖 Claude · 2026-11-13 21:10

**🔧 Bash**
```
{
 "command": "grep -rli \"dime motion studio\\|dime-motion-studio\\|dime_motion_studio\" ~/.claude ~/.agents 2>/dev/null | grep -v projects/ | head; find / -iname \"*dime*motion*\" -not -path \"*/proc/*\" 2>/dev/null | head",
 "description": "Search for any Dime Motion Studio skill",
 "timeout": 120000
}
```

### ↩️ Tool · 2026-11-13 21:10

<details><summary>result</summary>

```
/Users/gourav/.claude/history.jsonl
/Users/gourav/SFX/DIME motion SFX
/Users/gourav/Downloads/DimeMotion_Ray_TH23.mp4
/Users/gourav/Downloads/dime-motion-studio-skill (1).zip
/Users/gourav/Downloads/dime-motion-studio
/System/Volumes/Data/Users/gourav/SFX/DIME motion SFX
/System/Volumes/Data/Users/gourav/Downloads/DimeMotion_Ray_TH23.mp4
/System/Volumes/Data/Users/gourav/Downloads/dime-motion-studio-skill (1).zip
/System/Volumes/Data/Users/gourav/Downloads/dime-motion-studio
/System/Volumes/Data/Users/gourav/Library/Caches/claude-cli-nodejs/-Users-gourav/mcp-logs-claude-ai-dime-motion-portal
/Users/gourav/Library/Caches/claude-cli-nodejs/-Users-gourav/mcp-logs-claude-ai-dime-motion-portal
```
</details>

### 🤖 Claude · 2026-11-13 21:10

**🔧 Bash**
```
{
 "command": "find ~/Downloads/dime-motion-studio | head -30; unzip -l ~/Downloads/dime-motion-studio-skill\\ \\(1\\).zip | head -30",
 "description": "Inspect downloaded Dime Motion Studio files"
}
```

### ↩️ Tool · 2026-11-13 21:10

<details><summary>result</summary>

```
/Users/gourav/Downloads/dime-motion-studio
/Users/gourav/Downloads/dime-motion-studio/PRINCIPLES.md
/Users/gourav/Downloads/dime-motion-studio/tools
/Users/gourav/Downloads/dime-motion-studio/creativity-rater
/Users/gourav/Downloads/dime-motion-studio/projects
/Users/gourav/Downloads/dime-motion-studio/workflows
/Users/gourav/Downloads/dime-motion-studio/INSTALL.md
/Users/gourav/Downloads/dime-motion-studio/README.md
/Users/gourav/Downloads/dime-motion-studio/styles
/Users/gourav/Downloads/dime-motion-studio/.gitignore
/Users/gourav/Downloads/dime-motion-studio/refs
/Users/gourav/Downloads/dime-motion-studio/SKILL.md
/Users/gourav/Downloads/dime-motion-studio/prompts
/Users/gourav/Downloads/dime-motion-studio/stack
/Users/gourav/Downloads/dime-motion-studio/tools/board.py
/Users/gourav/Downloads/dime-motion-studio/creativity-rater/SKILL.md
/Users/gourav/Downloads/dime-motion-studio/projects/reel-02
/Users/gourav/Downloads/dime-motion-studio/projects/crwd-v3
/Users/gourav/Downloads/dime-motion-studio/projects/reel-01
/Users/gourav/Downloads/dime-motion-studio/projects/INDEX.md
/Users/gourav/Downloads/dime-motion-studio/workflows/revision.md
/Users/gourav/Downloads/dime-motion-studio/workflows/intake.md
/Users/gourav/Downloads/dime-motion-studio/styles/3d
/Users/gourav/Downloads/dime-motion-studio/styles/saas
/Users/gourav/Downloads/dime-motion-studio/refs/agentmorphy-skills
/Users/gourav/Downloads/dime-motion-studio/refs/prompt-library.txt
/Users/gourav/Downloads/dime-motion-s
…[2248 chars truncated]
```
</details>

### 🤖 Claude · 2026-11-13 21:10

**🔧 Bash**
```
{
 "command": "cd ~/Downloads/dime-motion-studio; head -20 SKILL.md; echo ----; cat INSTALL.md",
 "description": "Read skill header and install notes"
}
```

### ↩️ Tool · 2026-11-13 21:10

<details><summary>result</summary>

```
---
name: dime-motion-studio
description: The one skill for every Dime Motion animation and motion graphics job. Two styles. 3D is the three.js character reels (Reels 01 and 02, Claude skits, low-poly characters talking). SaaS is the 2D code films (the CRWD launch film: product and UI scenes, split screens, kinetic type). It picks the style from the ask or a past job ("the one from yesterday"), then runs the shared process: research, references (Krish's or found), story, a storyboard Krish approves, writing its own full build prompt, building from it, critique, delivery, saving new rules. When Krish asks for Blender, it opens Blender and works there. Use whenever Krish asks for an animation, motion graphic, reel, explainer, launch film, scene, 3D piece or character skit, or says "make a reel", "animate this", "build it out".
---

# Dime Motion studio

One skill, two styles. The process is shared, and each style keeps its own pipeline and rules in its own folder, so you can add to one style without touching the other.

```
SKILL.md                 this file: pick the style, then run the shared process
PRINCIPLES.md            rules for both styles
creativity-rater/        scoring ideas and references
prompts/BUILD-PROMPT.md  the template every job's build prompt is written from
tools/board.py           storyboard sheet: one labelled panel per beat, reference frame beside it
refs/                    prompt library, agentmorphy reel skills
stack/run.py             reference find
…[1140 chars truncated]
```
</details>

### 🤖 Claude · 2026-11-13 21:10

**No, it isn't installed.** `~/.claude/skills/` has no `dime-motion-studio` folder, and the skill doesn't show up in this session's skill list.

The files are on your Mac, though. You downloaded them but never moved them into the skills folder:

- **`~/Downloads/dime-motion-studio/`**: already unzipped. It contains the full skill (`SKILL.md` with `name: dime-motion-studio`, `PRINCIPLES.md`, `creativity-rater/`, `styles/3d` and `styles/saas`, `workflows/`, `tools/`, `stack/`, plus the projects reel-01, reel-02 and crwd-v3).
- **`~/Downloads/dime-motion-studio-skill (1).zip`**: the original zip.

Per its `INSTALL.md`, installing takes two steps:
1. Copy the folder to `~/.claude/skills/dime-motion-studio`.
2. Restart Claude Code.

Do you want me to copy it over now? Once you restart, it will load for any reel, animation or motion graphics request. It also needs Node 20+, ffmpeg, Python 3.11 with `uv`, and an ElevenLabs key in `~/.config/dimemotion/elevenlabs_token`. I can check which of those you already have.
