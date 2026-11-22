"""Trailer v2 tight recut (Krish 2026-11-22: "the cuts you made has empty gaps ... make tight cuts, no empty gaps").
Every pause between words longer than 0.30 s is cut down to ~0.20 s (0.12 s after the word, 0.08 s before the next),
frame-aligned so the picture shifts by whole frames, and only where the waveform is really silent.
Outputs: newtime.json (removed regions, old->new map), words_new.json, timeline_new.json, audio/voice_new.wav
  python newcut.py"""
import json, subprocess, numpy as np, os
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'
FF = '/Users/gourav/ks-ron-build/reel1/ff'; SR = 48000; FPS = 24
KEEP = [(12.24, 12.82)]            # "co-founder and CEO | of Shepherd." -- the 10-14 s 3D truck runs across this beat; left as is
PAD_A, PAD_B, MIN_GAP = 0.12, 0.08, 0.30

words = json.load(open(HERE + 'words_cut.json'))
T = json.load(open(HERE + 'timeline.json'))
raw = subprocess.run([FF, '-v', 'error', '-i', HERE + 'audio/voice_clean.wav', '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
voice = np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
mono = np.abs(voice).mean(1)
win = int(0.010 * SR)
rms = np.sqrt(np.convolve(mono ** 2, np.ones(win) / win, 'same'))
ref = np.percentile(rms[rms > 1e-5], 95)
quiet = rms < ref * 10 ** (-19 / 20)                       # room tone sits at -20..-25 dB under speech; speech/breaths above


def snap(t): return round(t * FPS) / FPS


regions = []
for i in range(len(words) - 1):
    a, b = words[i][1], words[i + 1][0]
    if b - a <= MIN_GAP or any(abs(a - k0) < 0.05 and abs(b - k1) < 0.05 for k0, k1 in KEEP): continue
    # cut only the truly quiet runs inside the pause (the transcript misses some words: never cut speech or breaths)
    s0, s1 = int((a + PAD_A) * SR), int((b - PAD_B) * SR)
    q = quiet[s0:s1]
    if len(q) == 0: continue
    edges = np.flatnonzero(np.diff(np.concatenate([[0], q.astype(np.int8), [0]])))
    for j in range(0, len(edges), 2):
        q0, q1 = (s0 + edges[j]) / SR + 0.03, (s0 + edges[j + 1]) / SR - 0.03
        r0, r1 = snap(q0 + 0.5 / FPS), snap(q1 - 0.5 / FPS)            # whole frames, inside the quiet run
        if r1 - r0 >= 3 / FPS: regions.append((round(r0, 6), round(r1, 6), words[i][2], words[i + 1][2]))

removed = sum(r1 - r0 for r0, r1, *_ in regions)


def M(t):
    """old cut time -> new time (a time inside a removed region lands on its cut point)"""
    d = 0.0
    for r0, r1, *_ in regions:
        if t >= r1: d += r1 - r0
        elif t > r0: return r0 - d
        else: break
    return t - d


# voice: keep everything outside the regions, 8 ms fades at each joint (the joints are in silence)
parts, prev = [], 0.0
for r0, r1, *_ in regions:
    parts.append(voice[int(round(prev * SR)):int(round(r0 * SR))]); prev = r1
parts.append(voice[int(round(prev * SR)):])
fd = int(0.008 * SR); ramp = np.linspace(0, 1, fd)[:, None]
for k in range(len(parts)):
    if k > 0: parts[k][:fd] *= ramp
    if k < len(parts) - 1: parts[k][-fd:] *= ramp[::-1]
vnew = np.concatenate(parts)
p = HERE + 'audio/_v.f32'; open(p, 'wb').write(vnew.astype(np.float32).tobytes())
subprocess.run([FF, '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', p, '-c:a', 'pcm_f32le', HERE + 'audio/voice_new.wav'], check=True)
os.remove(p)

wn = [[round(M(w[0]), 4), round(M(w[1]), 4)] + list(w[2:]) for w in words]
json.dump(wn, open(HERE + 'words_new.json', 'w'))
TN = {'END': round(M(T['END']), 4), 'VOICE_END': round(M(T['VOICE_END']), 4), 'BLACK': round(M(T['BLACK']), 4),
      'TITLE': round(M(T['TITLE']), 4), 'CAL_FLIPS': [round(M(x), 4) for x in T['CAL_FLIPS']],
      'shots': [[s[0], round(M(s[1]), 4), round(M(s[2]), 4), s[3]] for s in T['shots']]}
json.dump(TN, open(HERE + 'timeline_new.json', 'w'), indent=1)
json.dump({'regions': regions, 'removed': removed, 'pads': [PAD_A, PAD_B], 'min_gap': MIN_GAP, 'keep': KEEP}, open(HERE + 'newtime.json', 'w'), indent=1)
print(f'{len(regions)} cuts, removed {removed:.2f} s; END {T["END"]} -> {TN["END"]}; voice {len(voice) / SR:.2f} -> {len(vnew) / SR:.2f} s')
for r0, r1, a, b in regions: print(f'  {r0:7.3f}-{r1:7.3f} ({r1 - r0:.3f})  "{a}" | "{b}"  -> new {M(r0):7.3f}')
