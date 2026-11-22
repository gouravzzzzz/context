import cv2, json, glob, os, sys
det = cv2.FaceDetectorYN.create('/Users/gourav/.claude/skills/jennifer-musselman-style/scripts3/yunet.onnx', '', (1920, 1080), 0.6)
out = {}
for f in sorted(glob.glob(sys.argv[1] + '/*.jpg')):
    im = cv2.imread(f); im = cv2.resize(im, (1920, 1080)) if im.shape[1] != 1920 else im
    det.setInputSize((im.shape[1], im.shape[0])); _, fs = det.detect(im)
    if fs is None: out[os.path.basename(f)] = None; continue
    b = max(fs, key=lambda r: r[2] * r[3])
    out[os.path.basename(f)] = [round(float(v)) for v in b[:4]] + [round(float(b[4])), round(float(b[5])), round(float(b[6])), round(float(b[7]))]
    print(os.path.basename(f), out[os.path.basename(f)][:4], 'eyes', out[os.path.basename(f)][4:8])
json.dump(out, open(sys.argv[2], 'w'))
