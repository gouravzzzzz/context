import sys, os
sys.path.insert(0, os.path.expanduser("~/verticals-justin-build"))
import wav, numpy as np
tr, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
T = wav.track(tr); fb, fh = wav.floors(tr, (a+b)/2)
W = [w for w in T['words'] if a-0.5 <= w[0] <= b]
print(f"thr bb {fb:.1f} hf {fh:.1f}")
for t in np.arange(a, b, 0.02):
    i = int(t / wav.HOP); x = T['bb'][i:i+4].max() - fb; y = T['hf'][i:i+4].max() - fh
    lab = ' '.join(w[2] for w in W if t <= w[0] < t + 0.02)
    print(f"{t:9.2f} {'#'*int(max(0,x)/1.5):<40}|{'+'*int(max(0,y)/1.5):<30} {x:5.1f} {y:5.1f} {lab}")
