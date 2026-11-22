"""prep: (1) YuNet face + eyes on every A-roll cut frame -> faces_cut.json
(2) beat-10 split: Nic, Justin and Luke's own Riverside tracks over the same episode window -> broll/split_<who>.mp4 (24 fps, 1080p)
(3) exposed picture holds (the cut freezes the last frame under added room tone): replace with a slow-motion stretch of the
    segment's last real frames (minterpolate) -> patch/cut_<n>.jpg"""
import cv2, json, os, subprocess, numpy as np
FF = '/Users/gourav/ks-ron-build/reel1/ff'; H = os.path.dirname(os.path.abspath(__file__)) + '/'
CUT = '/Users/gourav/Downloads/Verticals_Justin_Levine_Trailer_Cut_v1.mp4'
D = '/Users/gourav/Downloads/'
SRC = {'justin': D + 'justin_levine-a179b1a2-3441-4183-baa5-1-CFR.mp4', 'luke': D + 'luke_sophinos-75b8dd46-261d-4272-b601-1-CFR.mp4',
       'nic': D + 'nic-1668c829-216b-48c0-ba6a-1-CFR.mp4'}
G = json.load(open(H + 'segs_cut.json'))
det = cv2.FaceDetectorYN.create('/Users/gourav/.claude/skills/jennifer-musselman-style/scripts3/yunet.onnx', '', (960, 540), 0.6)
def face(im):
    sm = cv2.resize(im, (960, 540)); det.setInputSize((960, 540)); _, fs = det.detect(sm)
    if fs is None: return None
    b = max(fs, key=lambda r: r[2] * r[3]); return [round(float(v) * 2, 1) for v in b[:8]]
if not os.path.exists(H + 'faces_cut.json'):
    c = cv2.VideoCapture(CUT); out = []
    while True:
        ok, f = c.read()
        if not ok: break
        out.append(face(f))
    json.dump(out, open(H + 'faces_cut.json', 'w')); print('faces', len(out), 'none', sum(o is None for o in out))
# (2) split window
win = [g for g in G if g['k'] >= 32]
ep0 = min(g['src0'] / 24 for g in win) - 0.5; ep1 = max(g['src0'] / 24 + (g['n'] + g['hold']) / 24 for g in win) + 0.5
json.dump({'ep0': ep0, 'ep1': ep1}, open(H + 'split_win.json', 'w'))
for who, p in SRC.items():
    o = H + f'broll/split_{who}.mp4'
    if not os.path.exists(o):
        subprocess.run([FF, '-v', 'error', '-y', '-ss', f'{ep0:.4f}', '-t', f'{ep1 - ep0:.4f}', '-i', p, '-an', '-vf', 'scale=1920:1080:flags=lanczos,fps=24,format=yuv420p',
                        '-c:v', 'libx264', '-crf', '12', '-g', '1', '-preset', 'fast', o], check=True)
print('split window', round(ep0, 2), round(ep1, 2))
# (3) exposed holds -> slow-motion stretch of the last K real frames over K + hold frames
os.makedirs(H + 'patch', exist_ok=True)
for k in (4, 16, 26):
    g = G[k]; n0 = round(g['t0'] * 24); K = 8; a = n0 + g['n'] - K; tot = K + g['hold']
    tmp = H + f'patch/_src{k}.mp4'
    subprocess.run([FF, '-v', 'error', '-y', '-i', CUT, '-vf', f"select='between(n\\,{a}\\,{a + K - 1})',setpts=N/24/TB", '-an', '-c:v', 'libx264', '-crf', '10', tmp], check=True)
    f = tot / K
    subprocess.run([FF, '-v', 'error', '-y', '-i', tmp, '-vf', f'setpts=PTS*{f:.5f},minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1',
                    '-frames:v', str(tot), '-q:v', '2', '-start_number', str(a), H + 'patch/cut_%05d.jpg'], check=True)
    print('patched hold', k, 'frames', a, '->', a + tot - 1)
