"""frame count, stuck frames, per-frame motion print for a segment; diff vs the v2 segments outside the transition"""
import sys, subprocess, numpy as np
FF = '/Users/gourav/ks-ron-build/reel1/ff'
D = '/Users/gourav/jl-trailer/trailer/v2segs/'


def read_small(f, w=480, h=270):
    raw = subprocess.run([FF, '-v', 'error', '-i', f, '-vf', f'scale={w}:{h}', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(np.float32)


f = sys.argv[1]; n0 = int(sys.argv[2]); expect = int(sys.argv[3])
a = read_small(f)
print('frames', len(a), 'expected', expect, 'OK' if len(a) == expect else 'MISMATCH')
d = np.abs(np.diff(a, axis=0)).mean((1, 2))
stuck = [n0 + k + 1 for k, v in enumerate(d) if v < 0.05]
print('stuck (identical to previous):', stuck)
med = np.median(d)
print('motion print (NEW frame: mean abs diff vs previous), * = spike > 4x median %.2f' % med)
row = []
for k, v in enumerate(d):
    n = n0 + k + 1
    row.append(f'{n}:{v:5.1f}{"*" if v > 4 * med else " "}')
    if len(row) == 10: print('  '.join(row)); row = []
if row: print('  '.join(row))
if len(sys.argv) > 4:
    b5 = read_small(D + '05_autodesk_fx.mp4'); b6 = read_small(D + '06_nic_fx.mp4')
    e5 = [float(np.abs(a[k] - b5[k]).mean()) for k in range(len(b5))]
    e6 = [float(np.abs(a[51 + k] - b6[k]).mean()) for k in range(len(b6))]
    print('vs 05_autodesk_fx (434-484) max mean diff %.2f' % max(e5))
    print('vs 06_nic_fx: j0-32 mean %.1f | j33+ max %.2f at NEW %d' % (np.mean(e6[:33]), max(e6[33:]), 485 + 33 + int(np.argmax(e6[33:]))))
