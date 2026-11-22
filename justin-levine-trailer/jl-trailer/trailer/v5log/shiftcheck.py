import sys, subprocess, numpy as np, cv2
FF='/Users/gourav/ks-ron-build/reel1/ff'
def frames(f):
    raw=subprocess.run([FF,'-v','error','-i',f,'-vf','scale=480:270','-f','rawvideo','-pix_fmt','gray','-'],capture_output=True).stdout
    return np.frombuffer(raw,np.uint8).reshape(-1,270,480).astype(np.float32)
for f in sys.argv[1:]:
    F=frames(f); sh=[]; sc=[]
    win=cv2.createHanningWindow((480,270),cv2.CV_32F)
    for a,b in zip(F[:-1],F[1:]):
        (dx,dy),r=cv2.phaseCorrelate(a,b,win); sh.append(np.hypot(dx,dy)*4)   # px at 1920 wide
    sh=np.array(sh)
    print(f.split('/')[-1], 'frames',len(F),'median shift %.2f px/f  p90 %.2f  frames>1px: %d'%(np.median(sh),np.percentile(sh,90),(sh>1).sum()))
