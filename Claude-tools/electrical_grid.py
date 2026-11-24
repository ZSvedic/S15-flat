import pymupdf, sys
from PIL import Image, ImageDraw, ImageFont
Z=6.0; X0,X1,Y0,Y1=240,700,575,1020
AX5=float(sys.argv[1]); AYC=float(sys.argv[2])
d=pymupdf.open("../../Building-docs/Mapa III_Elektrotehnički projekt.pdf"); p=d[55]; p.set_rotation(0)
pix=p.get_pixmap(matrix=pymupdf.Matrix(Z,Z),clip=pymupdf.Rect(X0,Y0,X1,Y1))
im=Image.frombytes("RGB",(pix.width,pix.height),pix.samples).rotate(90,expand=True)
k=0.28346
def M(x,y):  # model -> px
    Y=595.08+(x-AX5)*k; X=621.36-(y-AYC)*k
    return ((Y-Y0)*Z,(X1-X)*Z)
dr=ImageDraw.Draw(im)
try: f=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",15)
except: f=None
for x in range(0,1600,100):
    a=M(x,0);b=M(x,1700); dr.line([a,b],fill=(0,170,255),width=1)
    for yy in range(50,1700,200): dr.text((M(x,yy)[0]+2,M(x,yy)[1]),str(x),fill=(0,110,220),font=f)
for y in range(0,1700,100):
    a=M(0,y);b=M(1600,y); dr.line([a,b],fill=(255,140,0),width=1)
    for xx in range(50,1600,200): dr.text((M(xx,y)[0],M(xx,y)[1]+1),str(y),fill=(220,90,0),font=f)
im.save("elg_full.png"); W,Hh=im.size; print(W,Hh)
import json; json.dump(dict(Z=Z,X0=X0,X1=X1,Y0=Y0,Y1=Y1,AX5=AX5,AYC=AYC),open("elgrid.json","w"))
n=0
for j in range(3):
    for i in range(2):
        x0=int(i*(W-1400)); y0=int(j*(Hh-1000)/2)
        im.crop((x0,y0,x0+1400,y0+1000)).save(f"elg_{j}{i}.png")
