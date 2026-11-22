"""Cut a preview from the FINAL v3 segments (exact frames) + mix2.wav.
  python make_preview.py OUT n0 n1 seg:start [seg:start ...]      seg = file name in v2segs/ (no .mp4), start = its first NEW frame"""
import sys, subprocess, numpy as np
FF = '/Users/gourav/ks-ron-build/reel1/ff'
D = '/Users/gourav/jl-trailer/trailer/v2segs/'
W, H = 1920, 1080
out, n0, n1 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
segs = [(a.split(':')[0], int(a.split(':')[1])) for a in sys.argv[4:]]


def nframes(f):
    import re
    o = subprocess.run([FF, '-i', f, '-map', '0:v', '-c', 'copy', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return int(re.findall(r'frame=\s*(\d+)', o)[-1])


plan = []
for name, s0 in segs:
    k = nframes(D + name + '.mp4'); plan.append((name, s0, s0 + k))
p = subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '24', '-i', '-',
                      '-ss', f'{n0 / 24:.4f}', '-t', f'{(n1 - n0) / 24:.4f}', '-i', '/Users/gourav/jl-trailer/trailer/audio/mix2.wav',
                      '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'medium', '-crf', '15', '-pix_fmt', 'yuv420p',
                      '-c:a', 'aac', '-b:a', '320k', '-t', f'{(n1 - n0) / 24:.4f}', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
n = n0
for name, s0, s1 in plan:
    a, b = max(n, s0), min(n1, s1)
    if b <= a: continue
    assert a == n, f'gap at {n} (next piece {name} starts {s0})'
    raw = subprocess.run([FF, '-v', 'error', '-i', D + name + '.mp4', '-vf', f'select=between(n\\,{a - s0}\\,{b - s0 - 1})',
                          '-vsync', '0', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3); assert len(fr) == b - a, (name, len(fr), b - a)
    p.stdin.write(fr.tobytes()); n = b
assert n == n1, f'preview ends at {n}, wanted {n1}'
p.stdin.close(); p.wait(); print('done', out, n1 - n0, 'frames')
