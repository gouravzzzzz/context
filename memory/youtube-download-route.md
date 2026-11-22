---
name: youtube-download-route
description: How to download YouTube B-roll on this laptop - y2meta-uk.com through BrowserOS neo (yt-dlp and cobalt.tools both fail here)
metadata:
  node_type: memory
  type: reference
  originSessionId: b0ec8700-62e7-4f66-ba88-9a5af74d9123
  modified: 2026-11-14T22:00:58.404Z
---

On 2026-11-15 yt-dlp (2025.10.14, Python 3.9 only) failed with "The page needs to be reloaded", and cobalt.tools' main instance has YouTube disabled. The team's own clips (files named "Title - Channel (1080p, h264).mp4" in ~/Downloads) come from **y2meta-uk.com** (tunnel dlXX.yt-dl.click).

Working neo flow: open https://y2meta-uk.com/, fill the link box, click Start, click the "Video" tab inside the iframe (retry until rows show), click the 1080p (else 720p) row's Download, wait until a link "Download" appears in the dialog, then clickAt the dialog's green button (about 595,447 in a 1193x815 viewport). The file lands in ~/Downloads. Some videos fail ("Please Try Again!"), e.g. a CNBC Shark Tank vault clip; pick another upload. yt-dlp's `ytsearch` still works for finding videos.

Gotcha: contact sheets made with a low-rate `fps=1/N` filter label frames up to N/2 s off; pick in/out points from exact `-ss` seeks.
