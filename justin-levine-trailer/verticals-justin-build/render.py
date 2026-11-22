"""Render the script cut: 1920x1080/24p, speaker's own track per span, room tone under the added air, picture holds."""
import json, os, sys, wave, subprocess
import numpy as np
B = os.path.expanduser('~/verticals-justin-build/')
sys.path.insert(0, B)
import edl, wav
FF = os.path.expanduser('~/ks-ron-build/reel1/ff')
D = os.path.expanduser('~/Downloads/')
SRC = {'justin': D + 'justin_levine-a179b1a2-3441-4183-baa5-1-CFR.mp4', 'luke': D + 'luke_sophinos-75b8dd46-261d-4272-b601-1-CFR.mp4',
       'nic': D + 'nic-1668c829-216b-48c0-ba6a-1-CFR.mp4'}
OUT = sys.argv[1] if len(sys.argv) > 1 else D + 'Verticals_Justin_Levine_Trailer_Cut_v1.mp4'
SR, FPS = 48000, 24
S = edl.build()
A = {}
for tr in SRC:
    with wave.open(B + f'work/{tr}48.wav') as w:
        A[tr] = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768


def rms_db(x): return 10 * np.log10(np.mean(x ** 2) + 1e-12)


# level-match the speakers on their spoken words (loudest 60% of 50 ms blocks)
lvl = {}
for tr in SRC:
    xs = np.concatenate([A[tr][int(s['onset'] * SR):int(s['offset'] * SR)] for s in S if s['spk'] == tr])
    bl = xs[:len(xs) // 2400 * 2400].reshape(-1, 2400); e = np.sort(np.mean(bl ** 2, 1))[::-1]
    lvl[tr] = 10 * np.log10(np.mean(e[:int(len(e) * 0.6)]) + 1e-12)
gain = {tr: 10 ** ((-20 - lvl[tr]) / 20) for tr in SRC}
print('speech level dB', {k: round(v, 1) for k, v in lvl.items()})


def roomtone(tr, t, n):
    """n samples of the speaker's own room tone: quietest stretch within 30 s of t (looped if short)."""
    s, i0 = wav.score(tr, max(0, t - 30), t + 30)
    best, k, run = None, 0, 0
    for j, v in enumerate(s):
        run = run + 1 if v <= -3 else 0
        if run * wav.HOP >= 0.6: best = (i0 + j) * wav.HOP - 0.55; break
    if best is None: return np.zeros(n, np.float32)
    seg = A[tr][int(best * SR):int((best + 0.5) * SR)]
    out = np.tile(seg, n // len(seg) + 1)[:n].copy()
    f = min(240, n // 2)
    if f: out[:f] *= np.linspace(0, 1, f); out[-f:] *= np.linspace(1, 0, f)
    return out


audio, segs, T = [], [], 0.0
for k, s in enumerate(S):
    x = A[s['spk']][int(s['a'] * SR):int(s['e'] * SR)].copy() * gain[s['spk']]
    fi, fo = int((0.008 if s['c_in'] else 0.015) * SR), int((0.02 if s['c_out'] else 0.015) * SR)
    x[:fi] *= np.linspace(0, 1, fi); x[-fo:] *= np.linspace(1, 0, fo)
    air = s.get('air', 0.0)
    if air > 0: x = np.concatenate([x, roomtone(s['spk'], s['e'], int(air * SR)) * gain[s['spk']]])
    if k == len(S) - 1: x[-int(0.4 * SR):] *= np.linspace(1, 0, int(0.4 * SR)) ** 2
    t0, T = T, T + len(x) / SR
    f0, f1 = round(t0 * FPS), round(T * FPS)
    nsrc = min(f1 - f0, max(1, round((s['e'] - s['a']) * FPS)))
    segs.append(dict(k=k, spk=s['spk'], src0=round(s['a'] * FPS), n=nsrc, hold=f1 - f0 - nsrc, t0=t0))
    audio.append(x)
mix = np.concatenate(audio)
nfr = round(T * FPS); mix = np.concatenate([mix, np.zeros(max(0, int(nfr / FPS * SR) - len(mix)), np.float32)])[:int(nfr / FPS * SR)]
mix = np.clip(mix, -1, 1)
os.makedirs(B + 'cut/segs', exist_ok=True)
with wave.open(B + 'cut/mix.wav', 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())


def render_seg(g):
    hold = f",loop=loop={g['hold']}:size=1:start={g['n'] - 1}" if g['hold'] > 0 else ''
    vf = f"trim=end_frame={g['n']}{hold},setpts=N/{FPS}/TB,scale=1920:1080:flags=lanczos,setsar=1,format=yuv420p"
    o = B + f"cut/segs/s{g['k']:02d}.mp4"
    subprocess.run([FF, '-y', '-loglevel', 'error', '-ss', f"{(g['src0'] - 0.1) / FPS:.4f}", '-t', f"{(g['n'] + 0.5) / FPS:.4f}", '-i', SRC[g['spk']], '-frames:v', str(g['n'] + g['hold']),
                    '-vf', vf, '-an', '-r', str(FPS), '-c:v', 'libx264', '-crf', '15', '-preset', 'fast', '-g', '48', o], check=True)
    return o


from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(6) as ex: files = list(ex.map(render_seg, segs))
open(B + 'cut/segs/list.txt', 'w').write(''.join(f"file '{f}'\n" for f in files))
subprocess.run([FF, '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', B + 'cut/segs/list.txt', '-i', B + 'cut/mix.wav',
                '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-ac', '2', '-shortest', '-movflags', '+faststart', OUT], check=True)
json.dump(segs, open(B + 'cut/segs.json', 'w'), indent=0)
print(f'{len(S)} pieces, {T:.2f} s ->', OUT)
