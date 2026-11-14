# Always on installer

Session `809e60db-6442-4317-9b8c-d63f8a05b8a8` · started 2026-10-23 12:20

---

### 🧑 User · 2026-10-23 12:20

Check my Downloads folder. There's a repository called Always on installer. Install that.

### 🤖 Claude · 2026-10-23 12:20

**🔧 Bash**
```
{
 "command": "ls -la ~/Downloads | grep -i -E \"always|install\"",
 "description": "Find the Always On installer in Downloads"
}
```

### ↩️ Tool · 2026-10-23 12:20

<details><summary>result</summary>

```
-rw-r--r--@    1 gourav  staff    12445893 26 May 20:58 aescripts + aeplugins zxp installer (setup).dmg
-rw-r--r--@    1 gourav  staff   226963587 24 Aug 20:33 AirtableInstaller.dmg
drwxr-xr-x@    4 gourav  staff         128 23 Oct 17:47 always-on-installer
-rw-r--r--@    1 gourav  staff        2797 23 Oct 17:48 always-on-installer.zip
-rw-r--r--@    1 gourav  staff     3633967  7 Aug 15:57 CapCut_7671234348363956232_installer.dmg
-rw-r--r--@    1 gourav  staff     3879067 25 Mar  2026 FXConsole_1.0.6_Installer_2026.dmg
-rw-r--r--@    1 gourav  staff    15478023 24 Sep 15:23 Jeff Bezos on Why It's Always Day 1 at Amazon  Amazon News - Amazon News (1080p, h264).mp4
-rw-r--r--@    1 gourav  staff     2474557 19 Jun 20:27 People will always tell you whats realistic.Based on their fears. Their limitations. Their vers.mp4
-rw-r--r--@    1 gourav  staff       60789 13 May 19:39 This just means money is always appreciated _).jpg
-rw-r--r--@    1 gourav  staff        5773  5 May 18:23 Why Installed Porcelain Veneers Are The Secret_..
```
</details>

### 🤖 Claude · 2026-10-23 12:20

**🔧 Bash**
```
{
 "command": "cd ~/Downloads/always-on-installer && find . -type f | head -50 && echo ---- && for f in $(find . -type f -not -path '*/.git/*'); do echo \"=== $f\"; cat \"$f\"; done",
 "description": "List and print the installer's files"
}
```

### ↩️ Tool · 2026-10-23 12:20

<details><summary>result</summary>

```
./install-always-on.sh
./README.txt
----
=== ./install-always-on.sh
#!/bin/bash
# Always-on mode for a Mac: keeps it awake, even with the lid closed, until you switch it off.
#
# Install:    bash install-always-on.sh            (asks for your Mac password once, then turns always-on ON right away)
# Remove:     bash install-always-on.sh uninstall
#
# After installing, use these from any Terminal window (no password needed):
#   awake on       keep the Mac on (lid can be closed)
#   awake off      back to normal sleep
#   awake status   show whether it's on
#
# It switches itself off if the battery gets hot (45C), the CPU starts throttling,
# or the battery drops to 10% while unplugged.

set -e
BIN=/usr/local/bin
ME="${SUDO_USER:-$USER}"

if [[ "$1" == "uninstall" ]]; then
  echo "Removing always-on mode (your Mac password may be asked)..."
  sudo pkill -f "$BIN/stayon" 2>/dev/null || true
  sudo pmset -a disablesleep 0
  sudo rm -f "$BIN/stayon" "$BIN/awake" /etc/sudoers.d/stayon
  echo "Removed. Sleep works normally again."
  exit 0
fi

echo "Installing always-on mode. Your Mac password will be asked once."
sudo mkdir -p "$BIN"

# 1) the background worker
sudo tee "$BIN/stayon" >/dev/null <<'EOF'
#!/bin/zsh
# stayon: keep the Mac awake with the lid closed. Started and stopped by "awake".
MAX_TEMP=45
MIN_BATT=10
CHECK=30
[[ $EUID -ne 0 ]] && { echo "Run it through: awake on"; exit 1; }
restore() { trap - INT TERM EXIT; pmset -a disablesleep 0; echo "$(date +%T) sleep re-enable
…[3408 chars truncated]
```
</details>

### 🤖 Claude · 2026-10-23 12:21

**🔧 Bash**
```
{
 "command": "sudo -n true 2>&1 && echo SUDO_OK",
 "description": "Check whether sudo works without a password prompt"
}
```

### ↩️ Tool · 2026-10-23 12:21

<details><summary>result</summary>

```
Exit code 1
sudo: a password is required
```
</details>

### 🤖 Claude · 2026-10-23 12:21

I haven't installed it yet. The installer needs your Mac password, and I can't type it for you. To run it here, enter this in the prompt:

```
! bash ~/Downloads/always-on-installer/install-always-on.sh
```

Type your password when it asks; nothing shows on screen while you type. The installer then turns always-on mode on straight away.

I read the script first. It matches what the README describes:
- **What it adds:** two commands in `/usr/local/bin`. `stayon` is the background process that keeps the Mac awake, and `awake on`, `awake off` and `awake status` control it.
- **Password rule:** it adds `/etc/sudoers.d/stayon`, which lets only those specific commands run without your password.
- **Safety cut-offs:** it switches itself off if the battery reaches 45°C, the CPU starts slowing down from heat, or the battery drops to 10% while unplugged.
- **Removal:** `bash ~/Downloads/always-on-installer/install-always-on.sh uninstall` takes it all out.

Once you've run it, I can check that it worked with `awake status`.

### 🧑 User · 2026-10-23 12:22

Run it yourself.

### 🤖 Claude · 2026-10-23 12:22

I can't type your password, but macOS can show its own password dialog for this. I'll run the installer through that dialog, so a password prompt should appear on your screen.

### 🤖 Claude · 2026-10-23 12:22

**🔧 Bash**
```
{
 "command": "osascript -e 'do shell script \"SUDO_USER=gourav HOME=/Users/gourav /bin/bash /Users/gourav/Downloads/always-on-installer/install-always-on.sh 2>&1\" with administrator privileges' 2>&1",
 "description": "Run the installer with admin rights via the macOS password dialog",
 "timeout": 300000
}
```

### ↩️ Tool · 2026-10-23 12:22

<details><summary>result</summary>

```
Exit code 1
0:163: execution error: /bin/bash: /Users/gourav/Downloads/always-on-installer/install-always-on.sh: Operation not permitted (126)
```
</details>

### 🤖 Claude · 2026-10-23 12:22

macOS privacy protection stopped the admin process from reading the Downloads folder. I'll copy the script somewhere it can read and run it again.

### 🤖 Claude · 2026-10-23 12:22

**🔧 Bash**
```
{
 "command": "D=/private/tmp/claude-501/-Users-gourav/809e60db-6442-4317-9b8c-d63f8a05b8a8/scratchpad/installer && mkdir -p \"$D\" && cp ~/Downloads/always-on-installer/install-always-on.sh \"$D/\" && diff -q ~/Downloads/always-on-installer/install-always-on.sh \"$D/install-always-on.sh\" && osascript -e \"do shell script \\\"cd /tmp && SUDO_USER=gourav HOME=/Users/gourav /bin/bash $D/install-always-on.sh 2>&1\\\" with administrator privileges\" 2>&1",
 "description": "Copy installer to scratchpad and run it with admin rights",
 "timeout": 300000
}
```

### ↩️ Tool · 2026-10-23 12:22

<details><summary>result</summary>

```
Installing always-on mode. Your Mac password will be asked once.Didn't start, see /tmp/stayon.logDone, and it's ON now. The screen can go dark or the lid can close; the Mac keeps running.From any Terminal window:  awake on       keep the Mac awake (lid can be closed)  awake off      back to normal  awake status   check it
```
</details>

### 🤖 Claude · 2026-10-23 12:22

**🔧 Bash**
```
{
 "command": "cat /tmp/stayon.log; echo ---; ls -l /usr/local/bin/stayon /usr/local/bin/awake /etc/sudoers.d/stayon; sudo -n -l 2>&1 | tail -5; echo ---; awake status; pmset -g | grep -i sleep",
 "description": "Check the startup log, installed files, and sleep state"
}
```

### ↩️ Tool · 2026-10-23 12:22

<details><summary>result</summary>

```
nohup: can't detach from console: Inappropriate ioctl for device
---
-r--r-----  1 root  wheel   125 23 Oct 17:52 /etc/sudoers.d/stayon
-rwxr-xr-x  1 root  wheel   755 23 Oct 17:52 /usr/local/bin/awake
-rwxr-xr-x  1 root  wheel  1013 23 Oct 17:52 /usr/local/bin/stayon
    env_reset, env_keep+=BLOCKSIZE, env_keep+="COLORFGBG COLORTERM", env_keep+=__CF_USER_TEXT_ENCODING, env_keep+="CHARSET LANG LANGUAGE LC_ALL LC_COLLATE LC_CTYPE", env_keep+="LC_MESSAGES LC_MONETARY LC_NUMERIC LC_TIME", env_keep+="LINES COLUMNS", env_keep+=LSCOLORS, env_keep+=SSH_AUTH_SOCK, env_keep+=TZ, env_keep+="DISPLAY XAUTHORIZATION XAUTHORITY", env_keep+="EDITOR VISUAL", env_keep+="HOME MAIL", lecture_file=/etc/sudo_lecture, !log_allowed

User gourav may run the following commands on Gouravs-MacBook-Air:
    (ALL) ALL
    (root) NOPASSWD: /usr/local/bin/stayon, /usr/bin/pkill -f /usr/local/bin/stayon, /usr/bin/pmset -a disablesleep 0
---
Off (normal sleep).
 Sleep On Power Button 1
 hibernatefile        /var/vm/sleepimage
 networkoversleep     0
 disksleep            10
 sleep                1 (sleep prevented by coreaudiod, runningboardd, runningboardd, runningboardd, runningboardd, caffeinate, powerd)
 displaysleep         120
```
</details>

### 🤖 Claude · 2026-10-23 12:23

**🔧 Bash**
```
{
 "command": "awake on; sleep 2; awake status; cat /tmp/stayon.log; pmset -g | grep -i disablesleep; pmset -g | grep SleepDisabled",
 "description": "Turn always-on mode on and verify it"
}
```

### ↩️ Tool · 2026-10-23 12:23

<details><summary>result</summary>

```
/usr/local/bin/awake:6: permission denied: /tmp/stayon.log
Didn't start, see /tmp/stayon.log
Off (normal sleep).
nohup: can't detach from console: Inappropriate ioctl for device
```
</details>

### 🤖 Claude · 2026-10-23 12:23

The leftover log file from the first attempt is owned by root, so `awake` can't write to it. Removing it needs admin rights once more, so another password dialog will appear.

### 🤖 Claude · 2026-10-23 12:23

**🔧 Bash**
```
{
 "command": "osascript -e 'do shell script \"rm -f /tmp/stayon.log\" with administrator privileges' 2>&1 && awake on; sleep 2; awake status; cat /tmp/stayon.log; pmset -g | grep -i -E \"SleepDisabled|disablesleep\"",
 "description": "Remove the root-owned log, then turn always-on mode on",
 "timeout": 300000
}
```

### ↩️ Tool · 2026-10-23 12:23

<details><summary>result</summary>

```
On. The Mac stays awake, lid closed or not. Turn off with: awake off
On (keeping the Mac awake).
17:53:23 awake. The lid can be closed.
 SleepDisabled		1
```
</details>

### 🤖 Claude · 2026-10-23 12:23

**🔧 Bash**
```
{
 "command": "awake status; pgrep -fl stayon; pmset -g | grep SleepDisabled",
 "description": "Confirm always-on mode is still running"
}
```

### ↩️ Tool · 2026-10-23 12:23

<details><summary>result</summary>

```
On (keeping the Mac awake).
29009 sudo -n /usr/local/bin/stayon
29011 /bin/zsh /usr/local/bin/stayon
 SleepDisabled		1
```
</details>

### 🤖 Claude · 2026-10-23 12:23

Always-on mode is installed and running now. Your Mac will stay awake even with the lid closed, and I checked that it was still running after my command finished (`SleepDisabled 1`).

It took two macOS password dialogs:
- **First dialog:** ran the installer. macOS wouldn't let the admin process read your Downloads folder, so I copied the script out and ran that identical copy instead. Everything installed, but the installer's own attempt to switch it on at the end failed.
- **Second dialog:** that failed attempt had left a log file owned by root, which blocked `awake on`. I used the second dialog to delete that file, then turned it on.

From any Terminal window, no password needed:
- `awake off` — back to normal sleep
- `awake on` — keep the Mac awake
- `awake status` — check whether it's on

It switches itself off if the battery reaches 45°C, the CPU slows down from heat, or the battery drops to 10% while unplugged. It also won't come back on by itself after a restart; run `awake on` again.

Keep in mind that a Mac running in a closed bag can get hot, so use `awake off` when you don't need it. To remove it completely, run `bash ~/Downloads/always-on-installer/install-always-on.sh uninstall`.

### 🧑 User · 2026-10-23 12:28

Is it done.

### 🤖 Claude · 2026-10-23 12:28

**🔧 Bash**
```
{
 "command": "awake status; pmset -g | grep SleepDisabled",
 "description": "Check always-on status"
}
```

### ↩️ Tool · 2026-10-23 12:28

<details><summary>result</summary>

```
On (keeping the Mac awake).
 SleepDisabled		1
```
</details>

### 🤖 Claude · 2026-10-23 12:28

Yes, it's done. I just checked again: always-on mode is installed and on, and sleep is disabled, so your Mac will stay awake even with the lid closed.

To turn it off, run `awake off` in Terminal. After a restart it won't come back on by itself, so run `awake on` again.
