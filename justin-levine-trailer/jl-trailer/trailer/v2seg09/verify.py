import subprocess, numpy as np, sys
FF = '/Users/gourav/ks-ron-build/reel1/ff'
p = sys.argv[1]
raw = subprocess.run([FF, '-v', 'error', '-i', p, '-vf', 'scale=480:270', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], capture_output=True).stdout
f = np.frombuffer(raw, np.uint8).reshape(-1, 270, 480).astype(np.float32)
print('frames', len(f))
d = np.abs(np.diff(f, axis=0)).mean((1, 2))
print('stuck (mad<0.05):', [i + 1 for i, v in enumerate(d) if v < 0.05])
print('per-frame MAD (frame index from 850):')
print(' '.join(f'{850 + i + 1}:{v:.1f}' for i, v in enumerate(d)))
med = np.median(d)
print('spikes (>3x median of neighbours):', [(850 + i + 1, round(float(v), 1)) for i, v in enumerate(d)
      if v > 3 * max(np.median(d[max(0, i - 3):i + 4]), 0.5)])
