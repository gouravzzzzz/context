import sys, numpy as np, subprocess
from PIL import Image, ImageDraw
FF = '/Users/gourav/ks-ron-build/reel1/ff'; SR = 22050
def load(f): return np.frombuffer(subprocess.run([FF, '-v', 'error', '-i', f, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout, np.float32)
rows = []
for f in sys.argv[1:]:
    x = load(f); hop = 2205   # 0.1 s
    n = len(x) // hop; win = 4096; lo, hi, tot = [], [], []
    fr = np.fft.rfftfreq(win, 1 / SR)
    for i in range(n):
        s = x[i * hop:i * hop + win]
        if len(s) < win: s = np.pad(s, (0, win - len(s)))
        P = np.abs(np.fft.rfft(s * np.hanning(win))) ** 2
        lo.append(P[(fr > 30) & (fr < 150)].sum()); hi.append(P[fr > 4000].sum()); tot.append(P.sum())
    db = lambda a: 10 * np.log10(np.array(a) + 1e-9)
    rows.append((f.split('/')[-1][:50], db(lo), db(hi), db(tot)))
    # beat: onset autocorr over 30-90 s with fine lags
    hop2 = 256; S = np.array([np.abs(np.fft.rfft(x[i:i + 1024] * np.hanning(1024))) for i in range(int(20 * SR), min(len(x) - 1024, int(80 * SR)), hop2)])
    fl = np.maximum(0, np.diff(np.log1p(S), axis=0)).sum(1); fl -= fl.mean(); ac = np.correlate(fl, fl, 'full')[len(fl) - 1:]
    lag = np.arange(len(ac)) * hop2 / SR; c = [(ac[i], 60 / lag[i]) for i in range(1, len(ac) - 1) if 0.28 < lag[i] < 1.0 and ac[i] > ac[i - 1] and ac[i] > ac[i + 1]]
    print(f.split('/')[-1][:50], 'bpm cands', [round(b, 1) for a, b in sorted(c, reverse=True)[:4]], flush=True)
Wd, Hh = 1600, 90; im = Image.new('RGB', (Wd, Hh * len(rows)), (20, 20, 20)); d = ImageDraw.Draw(im)
for r, (nm, lo, hi, tot) in enumerate(rows):
    y0 = r * Hh; sc = (Wd - 10) / 1800
    for arr, col, base in ((tot, (90, 170, 255), 0), (lo, (255, 120, 60), 0), (hi, (120, 255, 140), 0)):
        m = arr.max()
        pts = [(int(i * sc), y0 + Hh - 4 - int(np.clip((v - m + 45) / 45, 0, 1) * (Hh - 20))) for i, v in enumerate(arr[:1800])]
        d.line(pts, fill=col, width=1)
    for s in range(0, 180, 5): d.line([(int(s * 10 * sc), y0 + 14), (int(s * 10 * sc), y0 + (18 if s % 10 else 24))], fill=(160, 160, 160))
    d.text((4, y0 + 1), nm + '   ticks = 5 s (blue total, orange sub-bass, green highs)', fill=(255, 220, 0))
im.save('audio/env2.png')
