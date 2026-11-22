"""frame count, stuck frames, per-frame motion print (mean |diff| of consecutive frames) with spike flags
  python verify.py seg.mp4 n_expected [cut frames...]"""
import sys, subprocess, numpy as np
FF = '/Users/gourav/ks-ron-build/reel1/ff'
f, nexp = sys.argv[1], int(sys.argv[2]); cuts = {int(a) for a in sys.argv[3:]}
raw = subprocess.run([FF, '-v', 'error', '-i', f, '-vf', 'scale=480:270', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'],
                     capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, 270, 480).astype(np.float32)
print('frames', len(fr), 'expected', nexp, 'OK' if len(fr) == nexp else 'MISMATCH')
d = np.array([np.abs(fr[k] - fr[k - 1]).mean() for k in range(1, len(fr))])
stuck = [k for k in range(1, len(fr)) if d[k - 1] < 0.05]
print('stuck frames (identical to previous):', stuck)
spikes = []
for k in range(3, len(fr)):
    v = d[k - 1]; ref = max(np.median(d[max(0, k - 7):k - 1]), 0.3)
    if v > 2.5 * ref + 1.0 and k not in cuts: spikes.append((k, round(float(v), 2), round(float(ref), 2)))
print('motion print (mean |diff| per frame, x10 rounded):')
for a in range(1, len(fr), 24):
    print(f'{a:4d}:', ' '.join(f'{int(round(x * 10)):3d}' for x in d[a - 1:a + 23]))
print('spikes (not at listed cuts):', spikes)
