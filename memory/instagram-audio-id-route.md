---
name: instagram-audio-id-route
description: "How to grab an Instagram reel's audio and identify the song (Shazam) on this machine"
metadata:
  node_type: memory
  type: reference
  originSessionId: 7ac22dc7-5b8d-4cac-b87f-ce8b404af8c6
  modified: 2026-11-21T19:57:09.615Z
---

Instagram reel → song ID route (worked 2026-11-22):
1. yt-dlp fails (login wall). Open the post in neo (logged in); evaluateInPage → performance.getEntriesByType('resource') filtered to fbcdn .mp4 URLs.
2. Strip `bytestart/byteend` params; base64-decode each URL's `efg` param — the one with `vencode_tag` ending `dash_ln_heaac_vbr3_audio` and `duration_s` matching the post is the audio. curl it.
3. No system ffmpeg, and afconvert can't read the fragmented mp4 → decode with PyAV from ~/ks-ron-build/venv (av.AudioResampler → wav).
4. `shazamio` (pip in a scratch venv) on the wav → title/artist.

Related: [[youtube-download-route]]
