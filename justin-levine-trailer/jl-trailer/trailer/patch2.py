"""exposed holds -> optical-flow slow motion of the segment's last 8 real frames, stretched over the held frames too (patch/cut_<n>.jpg)"""
import cv2, json, numpy as np
H = '/Users/gourav/jl-trailer/trailer/'
CUT = '/Users/gourav/Downloads/Verticals_Justin_Levine_Trailer_Cut_v1.mp4'
G = json.load(open(H + 'segs_cut.json'))
dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
def flow(a, b):
    return dis.calc(cv2.cvtColor(a, cv2.COLOR_BGR2GRAY), cv2.cvtColor(b, cv2.COLOR_BGR2GRAY), None)
def bwarp(img, fl, s):
    h, w = fl.shape[:2]; gx, gy = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
    return cv2.remap(img, gx + fl[..., 0] * s, gy + fl[..., 1] * s, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
c = cv2.VideoCapture(CUT)
for k in (4, 16, 26):
    g = G[k]; n0 = round(g['t0'] * 24); K = 8; a = n0 + g['n'] - K; tot = K + g['hold']
    c.set(cv2.CAP_PROP_POS_FRAMES, a); src = [c.read()[1] for _ in range(K)]
    fl = [(flow(src[i], src[i + 1]), flow(src[i + 1], src[i])) for i in range(K - 1)]
    for j in range(tot):
        p = j * (K - 1) / (tot - 1); i = min(K - 2, int(p)); fr = p - i
        if fr < 1e-3: out = src[i]
        elif fr > 1 - 1e-3: out = src[i + 1]
        else:
            fab, fba = fl[i]
            A = bwarp(src[i], fba, fr)          # sample A where the pixel came from
            B = bwarp(src[i + 1], fab, 1 - fr)
            out = np.clip(A.astype(np.float32) * (1 - fr) + B.astype(np.float32) * fr, 0, 255).astype(np.uint8)
        cv2.imwrite(H + f'patch/cut_{a + j:05d}.jpg', out, [cv2.IMWRITE_JPEG_QUALITY, 96])
    print('seg', k, g['spk'], 'frames', a, '->', a + tot - 1, f'({K} real over {tot})')
