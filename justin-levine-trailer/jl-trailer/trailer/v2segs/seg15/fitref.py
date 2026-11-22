import sys; sys.path.insert(0,'/Users/gourav/.claude/skills/jennifer-musselman-style/scripts3')
import jstyle3 as J3, numpy as np, cv2, json
from scipy.optimize import least_squares
cap=cv2.VideoCapture('/Users/gourav/jl-trailer/refs_cloud2/ref.mp4'); prev=None; dx=[]
while True:
    ok,f=cap.read()
    if not ok: break
    g=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY).astype(np.float32)
    if prev is not None: dx.append(-cv2.phaseCorrelate(prev,g)[0][0])
    prev=g
dx=np.array(dx)
peaks=[34+75*i for i in range(12)]
curves=[]
for pk in peaks:
    a=pk-32; b=a+75
    if a<0 or b>len(dx): continue
    v=dx[a:b]; c=np.concatenate([[0],np.cumsum(v)]); curves.append(c/c[-1])
C=np.mean(curves,0); u=np.linspace(0,1,76)
print('n periods',len(curves)); print('C', np.round(C[::5],3))
EUv=np.vectorize(J3.EASE_USER)
def model(p,u):
    a,b,u1,d1,u2,d2=p
    return a*u + b*EUv(np.clip((u-u1)/d1,0,1)) + (1-a-b)*EUv(np.clip((u-u2)/d2,0,1))
def res(p): return model(p,u)-C
r=least_squares(res,[0.25,0.5,0.3,0.35,0.1,0.8],bounds=([0,0,-0.5,0.05,-0.5,0.05],[1,1,1,2,1,3]))
print('fit',np.round(r.x,4),'max err',np.abs(r.fun).max())
M=model(r.x,u); vM=np.diff(M)*75; vC=np.diff(C)*75
print('vel ref',np.round(vC[::3],2)); print('vel fit',np.round(vM[::3],2))
json.dump(dict(p=list(r.x),C=list(C)),open('refcurve.json','w'))
