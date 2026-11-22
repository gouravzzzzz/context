import cv2, numpy as np
c = cv2.VideoCapture('pin720.mp4'); fs = []
while True:
    ok, f = c.read()
    if not ok: break
    fs.append(f)
print('frames', len(fs), fs[0].shape)
prev = None
for i, f in enumerate(fs[:50]):
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    # non-blue: card paper + photo (blue bg has hue ~100-110, sat high)
    blue = (hsv[..., 0] > 90) & (hsv[..., 0] < 115) & (hsv[..., 1] > 120)
    m = (~blue).astype(np.uint8) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    n, lab, st, cen = cv2.connectedComponentsWithStats(m)
    comps = sorted([(st[k, 4], k) for k in range(1, n)], reverse=True)[:3]
    out = []
    for a, k in comps:
        if a < 400: continue
        ys, xs = np.where(lab == k); pts = np.stack([xs, ys], 1).astype(np.float32)
        (cx, cy), (w, h), ang = cv2.minAreaRect(pts)
        if w < h: w, h, ang = h, w, ang + 90
        if ang > 45: ang -= 90
        out.append(f'c=({cx:5.1f},{cy:5.1f}) wh=({w:5.1f},{h:5.1f}) ang={ang:5.2f} bb=({xs.min()},{ys.min()},{xs.max()},{ys.max()})')
    # background motion: phase correlation on blue mask region gray
    g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.float32)
    sh = ''
    if prev is not None:
        (dx, dy), r = cv2.phaseCorrelate(prev, g); sh = f'bg d=({dx:5.2f},{dy:5.2f})'
    prev = g
    print(i, sh, ' | '.join(out))
