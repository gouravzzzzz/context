"""Re-render only the cut-point frames that the old n_old() rounding got wrong (first REMOVED frame shown instead of the
first kept one), splice them into the finished segment, and extend/trim to new bounds.
  python fix_segs.py NAME"""
import sys, subprocess, numpy as np
sys.path.insert(0, '/Users/gourav/jl-trailer/trailer')
import render_v2 as RV
import engine
FF = '/Users/gourav/ks-ron-build/reel1/ff'
D = '/Users/gourav/jl-trailer/trailer/v2segs/'
W, H = engine.W, engine.H
# name: (src file, src n0, seg kind, out file, new n0, new n1, frames to re-render)
JOBS = {
    'autodesk': ('05_autodesk', 434, 'adsk', '05_autodesk_fx', 434, 485, {477, 484}),
    'nic':      ('06_nic', 484, 'v1', '06_nic_fx', 485, 692, {637}),
    'open':     ('00_open', 0, 'v1', '00_open_fx', 0, 206, {155}),
    'name3d':   ('01_name3d', 206, 's1014', '01_name3d_fx', 206, 317, {316}),
    'split':    ('16_split_end', 1846, 'v1', '16_split_end_fx', 1846, 2175, {1846, 1847, 1848}),
    'calendar': ('13_calendar_no', 1392, 'v1', '13_calendar_no_fx', 1392, 1689, {1392, 1546, 1581, 1626, 1637, 1639}),
}


def read_all(f):
    raw = subprocess.run([FF, '-v', 'error', '-i', f, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)


if __name__ == '__main__':
    src, s0, seg, out, n0, n1, fix = JOBS[sys.argv[1]]
    fr = read_all(D + src + '.mp4')
    p = subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '24', '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '12', '-pix_fmt', 'yuv420p', '-r', '24', D + out + '.mp4'], stdin=subprocess.PIPE)
    for n in range(n0, n1):
        k = n - s0
        if n in fix or not (0 <= k < len(fr)):
            img = np.ascontiguousarray(RV.frame(seg, n)); print('rendered', n, flush=True)
        else: img = fr[k]
        p.stdin.write(img.tobytes())
    p.stdin.close(); p.wait(); print('done', out, n1 - n0)
