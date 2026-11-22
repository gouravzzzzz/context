import sys, os, json
sys.path.insert(0, os.path.expanduser("~/verticals-justin-build"))
import wav, numpy as np
# usage: spark.py tr a b [mark ...]   one char per 10 ms: score (max dB over thresholds) as ' .:-=+*#%@'
tr, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]); marks = [float(m) for m in sys.argv[4:]]
s, i0 = wav.score(tr, a, b); s = s.reshape(-1, 2).max(1) if len(s) % 2 == 0 else s[:-1].reshape(-1, 2).max(1)
ch = ' .:-=+*#%@'
row = ''.join(ch[int(np.clip((v + 5) / 3, 0, 9))] if v > -5 else ' ' for v in s)
al = json.load(open(wav.B + 'cut/align.json'))
words = {}
for k, v in al.items():
    if k.startswith(tr + '@'):
        for w in v['words']:
            if w[0] and a <= w[0] <= b: words[round(w[0], 2)] = w
lab = [' '] * len(row)
for t0, w in sorted(words.items()):
    i = int((t0 - a) / 0.01)
    for k, c in enumerate(w[2][:12]):
        if 0 <= i + k < len(lab): lab[i + k] = c
mk = [' '] * len(row)
for m in marks:
    i = int((m - a) / 0.01)
    if 0 <= i < len(mk): mk[i] = '^'
print(f"{a:.2f} |{row}| {b:.2f}"); print(' ' * len(f"{a:.2f} |") + ''.join(lab)); print(' ' * len(f"{a:.2f} |") + ''.join(mk))
