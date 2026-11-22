"""quick music analysis: duration, tempo (onset autocorrelation), key (chroma), loudness envelope + drops (big RMS jumps)."""
import subprocess, sys, numpy as np
from PIL import Image, ImageDraw
FF = '/Users/gourav/ks-ron-build/reel1/ff'; SR = 22050
NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
MAJ = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]); MIN = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
def load(f):
    return np.frombuffer(subprocess.run([FF, '-v', 'error', '-i', f, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout, np.float32)
def analyse(f):
    x = load(f); hop = 512; n = len(x) // hop
    fr = x[:n * hop].reshape(n, hop); rms = np.sqrt((fr ** 2).mean(1) + 1e-12); db = 20 * np.log10(rms + 1e-9)
    # onset strength = positive spectral flux
    win = 2048; S = []
    for i in range(0, len(x) - win, hop): S.append(np.abs(np.fft.rfft(x[i:i + win] * np.hanning(win))))
    S = np.log1p(np.array(S)); flux = np.maximum(0, np.diff(S, axis=0)).sum(1)
    seg = flux[: min(len(flux), int(60 * SR / hop))]; seg = seg - seg.mean()
    ac = np.correlate(seg, seg, 'full')[len(seg) - 1:]
    lags = np.arange(len(ac)) * hop / SR; ok = (lags > 60 / 180) & (lags < 60 / 70)
    bpm = 60 / lags[ok][np.argmax(ac[ok])]
    freqs = np.fft.rfftfreq(win, 1 / SR); m = (freqs > 60) & (freqs < 2000)
    pc = (np.round(12 * np.log2(freqs[m] / 261.63)) % 12).astype(int)
    chroma = np.zeros(12)
    E = np.exp(S[:, m]) - 1
    for k in range(12): chroma[k] = E[:, pc == k].sum()
    best = max(((np.corrcoef(np.roll(P, k), chroma)[0, 1], NOTES[k] + q) for k in range(12) for P, q in ((MAJ, ''), (MIN, 'm'))))
    # 1 s energy envelope and the jumps
    sec = int(SR / hop); E1 = np.array([db[i:i + sec].mean() for i in range(0, len(db) - sec, sec)])
    jumps = [(i, round(E1[i] - E1[max(0, i - 2):i].mean(), 1)) for i in range(2, len(E1)) if E1[i] - E1[max(0, i - 2):i].mean() > 4.5]
    return len(x) / SR, bpm, best, E1, jumps
if __name__ == '__main__':
    rows = []
    for f in sys.argv[1:]:
        d, bpm, key, E1, jumps = analyse(f)
        print(f"{f.split('/')[-1][:55]:55} {d:6.1f}s {bpm:5.1f}bpm key {key[1]:3} ({key[0]:.2f}) jumps(s,dB): {jumps[:8]}", flush=True)
        rows.append((f.split('/')[-1][:60], E1))
    Wd, Hh = 1400, 70; im = Image.new('RGB', (Wd, Hh * len(rows)), (20, 20, 20)); d = ImageDraw.Draw(im)
    for r, (nm, E1) in enumerate(rows):
        y0 = r * Hh; mx = max(len(E1), 1)
        for i, e in enumerate(E1):
            x = int(i * (Wd - 10) / 240); h = int(np.clip((e + 45) / 40, 0, 1) * (Hh - 16))
            d.rectangle([x, y0 + Hh - 2 - h, x + max(1, (Wd - 10) // 240 - 1), y0 + Hh - 2], fill=(80, 170, 255))
        for s in range(0, 240, 10): d.line([(int(s * (Wd - 10) / 240), y0 + 12), (int(s * (Wd - 10) / 240), y0 + 16)], fill=(120, 120, 120))
        d.text((4, y0 + 1), nm, fill=(255, 220, 0))
    im.save('audio/env_sheet.png')
