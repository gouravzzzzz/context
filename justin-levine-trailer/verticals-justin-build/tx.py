"""Word-level transcripts of every script window, on each speaker's own track (times = recording seconds)."""
import json, sys, wave, numpy as np, mlx_whisper, os
B = os.path.expanduser('~/verticals-justin-build/')
WIN = [(0, 75), (140, 200), (240, 300), (1095, 1140), (1205, 1250), (1395, 1455), (1605, 1655),
       (1820, 1880), (2380, 2420), (2685, 2730), (2955, 2995), (3000, 3105)]
PROMPT = ("Welcome back to Verticals. Justin Levine, co-founder and CEO of Shepherd. Building Connected, Autodesk, "
          "Procore, Greenlight Re, Intact, Progressive. Luke, Nic. Um, uh, like, you know.")
tracks = sys.argv[1:] or ['justin', 'nic', 'luke']
for tr in tracks:
    with wave.open(B + f'work/{tr}16.wav') as w:
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    out = []
    for a, b in WIN:
        r = mlx_whisper.transcribe(x[a * 16000:b * 16000], path_or_hf_repo="mlx-community/whisper-large-v3-turbo", language="en",
                                   word_timestamps=True, condition_on_previous_text=False, initial_prompt=PROMPT)
        for s in r['segments']:
            for wd in s['words']:
                out.append([round(wd['start'] + a, 3), round(wd['end'] + a, 3), wd['word'].strip(), round(wd['probability'], 2)])
    json.dump(out, open(B + f'tx/{tr}.json', 'w'))
    print(tr, len(out), 'words', flush=True)
