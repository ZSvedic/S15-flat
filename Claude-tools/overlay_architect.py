import sys, math, xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont
home, out = sys.argv[1], sys.argv[2]
S=300/72; K=0.56693
def P(x,y): return ((843.6+(x-1464.71)*K)*S, (207.7+(y-305.88)*K)*S)
im=Image.open("arch300.png").convert("RGBA"); ov=Image.new("RGBA",im.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
r=ET.parse(home).getroot()
def rect(cx,cy,w,dp,ang):
    c,s=math.cos(ang),math.sin(ang); pts=[]
    for dx,dy in ((-w/2,-dp/2),(w/2,-dp/2),(w/2,dp/2),(-w/2,dp/2)):
        pts.append(P(cx+dx*c-dy*s, cy+dx*s+dy*c))
    return pts
for w in r.iter('wall'):
    a=w.attrib; x1,y1,x2,y2,t=[float(a[k]) for k in('xStart','yStart','xEnd','yEnd','thickness')]
    L=math.hypot(x2-x1,y2-y1); ang=math.atan2(y2-y1,x2-x1)
    d.polygon(rect((x1+x2)/2,(y1+y2)/2,L,t,ang),fill=(255,0,0,70),outline=(255,0,0,255))
for e in r.iter('doorOrWindow'):
    a=e.attrib
    if 'balustrade' in a.get('name','') or 'Shower' in a.get('name',''): continue
    d.polygon(rect(float(a['x']),float(a['y']),float(a['width']),float(a['depth']),float(a.get('angle',0))),fill=(0,90,255,90),outline=(0,0,255,255))
for e in r.iter('room'):
    pts=[P(float(p.get('x')),float(p.get('y'))) for p in e.findall('point')]
    d.line(pts+[pts[0]],fill=(0,160,0,255),width=3)
if len(sys.argv)>3:
    for e in list(r.iter('pieceOfFurniture'))+list(r.iter('light')):
        a=e.attrib
        if a.get('visible')=='false': continue
        d.polygon(rect(float(a['x']),float(a['y']),float(a['width']),float(a['depth']),float(a.get('angle',0))),outline=(160,0,200,255))
im=Image.alpha_composite(im,ov).convert("RGB"); im.save(out+"_full.jpg",quality=85)
W,H=im.size; n=0
for j in range(3):
    for i in range(3):
        x0=int(i*(W-1450)/2); y0=int(j*(H-1500)/2)
        im.crop((x0,y0,x0+1450,y0+1500)).save(f"{out}_{j}{i}.jpg",quality=80)
