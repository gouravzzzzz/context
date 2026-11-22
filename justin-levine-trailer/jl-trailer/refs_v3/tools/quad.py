import sys
from PIL import Image, ImageDraw
d=sys.argv[1]; out=sys.argv[2]; ids=[int(x) for x in sys.argv[3:]]
S=Image.new('RGB',(1916, 1080*((len(ids)+1)//2)//2))
dr=ImageDraw.Draw(S)
for k,i in enumerate(ids):
    im=Image.open(f'{d}/{i+1:04d}.png').resize((958,540)); x,y=(k%2)*958,(k//2)*540
    S.paste(im,(x,y)); dr.rectangle([x,y,x+30,y+14],fill='black'); dr.text((x+2,y+1),str(i),fill='yellow')
S.save(out,quality=88)
