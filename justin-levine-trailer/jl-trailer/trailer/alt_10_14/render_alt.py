"""Render the 10-14 s 3D section (scene3d.py) as video, 9.0-14.6 s on the trailer timeline, with the trailer mix.
All footage plays at its normal speed (no slow-motion, no in-betweens); only the camera moves are eased/overlapped.
scene3d.py is not edited: the two footage sources are patched in here.
  python render_alt.py [out.mp4]"""
import sys, os, math, subprocess
import numpy as np, cv2
from PIL import Image
HERE = '/Users/gourav/jl-trailer/trailer/alt_10_14/'
sys.path.insert(0, HERE)
import scene3d as S3
from engine import vid, matte, W, H, FPS, L

FF = '/Users/gourav/ks-ron-build/reel1/ff'
A0, A1 = 9.0, 14.6                                     # clip window: Nic's end -> into 02d, so both transitions are in it
# ---- footage plays at its normal speed (Krish: "play the video normally, only smoothen the camera movements")
SH20B_FACE = (1004.7 + 286.3 / 2, 110.0 + 403.3 / 2)      # c_shep_20 f44: the closer take after its own cut at f41
K20B = 232.0 / 286.3
A20B = np.float32([[K20B, 0, S3.SH1_FACE[0] - K20B * SH20B_FACE[0]], [0, K20B, S3.SH1_FACE[1] - K20B * SH20B_FACE[1]]])


def n20(t): return int(min(70, max(0, round((t - S3.CUT_IN) * 30))))


def justin_src(t):
    if t < S3.CUT_IN:
        n = int(min(77, max(0, round((t - S3.T0) * 30)))); return vid('c_shep_1').frame(n), matte('shep', n), None
    n = n20(t)
    m = np.asarray(Image.open(HERE + f'matte/s20_{n:05d}.png')).astype(np.float32) / 255
    return vid('c_shep_20').frame(n), m, (S3.A20 if n <= 40 else A20B)


S3.justin_src = justin_src
S3.Justin.key = lambda s, t: ('a', int(round((t - S3.T0) * 30))) if t < S3.CUT_IN else ('b', n20(t))


def sign_tex(s, t):
    img = L.grade(vid('s_shep_sign').at(min(2.95, t - S3.T0)))         # the sign film at its own speed (as in v1)
    ox, oy = s.cx0 - s.rect[0], s.cy0 - s.rect[1]
    def fn(d): L.card(d, img, ox, oy, s.cw, s.ch, fx=0.20, fy=0.50, zoom=1.0, shadow=True)
    return S3.mc_draw(s.tw, s.th, fn)


S3.SignCard.tex = sign_tex


def frame(n):
    t = n / FPS
    if t < S3.T0 - 1.5 / FPS: return S3.v1().frame(n)          # Nic (v1) before the zoom-through dissolve
    return S3.finished(t)[0]


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/Downloads/Verticals_JL_10-14s_3D_v1.mp4')
    n0, n1 = int(round(A0 * FPS)), int(round(A1 * FPS))
    tmp = HERE + 'render_tmp.mp4'
    p = subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '24', '-i', '-',
                          '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-pix_fmt', 'yuv420p', '-r', '24', tmp], stdin=subprocess.PIPE)
    import multiprocessing as mp
    nw = int(os.environ.get('NW', 8)); ns = list(range(n0, n1))
    with mp.get_context('fork').Pool(nw) as pool:
        for k, img in enumerate(pool.imap(frame, ns, chunksize=4)):
            p.stdin.write(np.ascontiguousarray(img).tobytes())
            if k % 24 == 0: print(f'frame {k}/{len(ns)}', flush=True)
    p.stdin.close(); p.wait()
    dur = len(ns) / FPS
    subprocess.run([FF, '-v', 'error', '-y', '-i', tmp, '-ss', f'{A0:.4f}', '-t', f'{dur:.4f}', '-i', '/Users/gourav/jl-trailer/trailer/audio/mix.wav',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '320k', '-t', f'{dur:.4f}', '-movflags', '+faststart', out], check=True)
    os.remove(tmp)
    print('done', out, len(ns), 'frames', dur, 's')


if __name__ == '__main__':
    main()
