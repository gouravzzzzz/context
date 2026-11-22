"""cut detection on an extracted frame folder: mean abs diff of 64x36 greyscale; prints cut frames + diff profile"""
import sys, os, numpy as np, json
from PIL import Image
d = sys.argv[1]; fps = float(sys.argv[2])
fs = sorted(os.listdir(d))
prev = None; diffs = []
for f in fs:
    a = np.asarray(Image.open(os.path.join(d, f)).convert('L').resize((64, 36)), dtype=np.float32)
    diffs.append(0 if prev is None else float(np.abs(a - prev).mean())); prev = a
diffs = np.array(diffs)
med = np.median(diffs)
cuts = [i for i in range(1, len(diffs)) if diffs[i] > max(18, 3.5 * np.median(diffs[max(0, i-6):i+7]))]
json.dump({'cuts': cuts, 'diffs': diffs.round(2).tolist()}, open(sys.argv[3], 'w'))
print(len(fs), 'frames, median diff', round(med, 2), 'cuts:', len(cuts))
print(' '.join(f'{c}({c/fps:.2f})' for c in cuts))
