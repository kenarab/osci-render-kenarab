"""CUA-01: referencia con caras y muestra XYZ real; no captura del host."""
import csv, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]
font='/System/Library/Fonts/Supplemental/Arial.ttf'
im=Image.new('RGB',(1500,680),(13,20,31));d=ImageDraw.Draw(im)
def text(x,y,s,size=22):d.text((x,y),s,font=ImageFont.truetype(font,size),fill=(217,231,240))
def rotate(p,yaw=.65,pitch=.45):
 x,y,z=p;c,s=math.cos(yaw),math.sin(yaw);x,z=c*x+s*z,-s*x+c*z
 c,s=math.cos(pitch),math.sin(pitch);return x,c*y-s*z,s*y+c*z
# Camera adicional común a los dos paneles XYZ, nunca modifica el Lua.
def camera(p):return rotate(p,-.4,.2)
def screen(p,panel):return (250+500*panel+430*p[0],350-430*p[1])
def point(u,v):
 a,b,c=math.cos(v)*math.cos(u),math.cos(v)*math.sin(u),math.sin(v)
 q=a**4+3*b**4+6*c**4;r=.42*math.sqrt(2/(.5+math.sqrt(.25+4*q)))
 return camera(rotate((r*a,r*b,r*c)))
faces=[]
for j in range(32):
 for i in range(64):
  u=i*2*math.pi/64;v=-math.pi/2+j*math.pi/32
  quad=[point(u,v),point(u+2*math.pi/64,v),point(u+2*math.pi/64,v+math.pi/32),point(u,v+math.pi/32)]
  for inds in [(0,1,2),(0,2,3)]:
   tri=[quad[k] for k in inds];a=[tri[1][k]-tri[0][k] for k in range(3)];b=[tri[2][k]-tri[0][k] for k in range(3)]
   n=[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
   norm=math.sqrt(sum(x*x for x in n));light=.25+.75*abs(sum(n[k]*[-.3,.5,.8][k] for k in range(3)))/(norm or 1)
   faces.append((sum(p[2] for p in tri)/3,tri,tuple(int(c*light) for c in (80,190,205))))
for _,tri,color in sorted(faces,key=lambda t:t[0]):d.polygon([screen(p,0) for p in tri],fill=color)
with (ROOT/'recordings/014-cuartica-tonal.xyz.csv').open() as f:points=[tuple(float(r[k]) for k in ('x','y','z')) for r in csv.DictReader(f)]
d.line([screen(camera(p),1) for p in points],fill=(103,220,205),width=1)
d.line([screen(p,2) for p in points],fill=(244,190,118),width=1)
text(35,25,'Cuártica algebraica · portadora 110 Hz · cobertura 7 Hz',30)
for panel,title,sub in [(0,'Referencia con caras','Malla de F=0 · k=0.5'),(1,'Barrido XYZ real','143 ms del retorno Lua · cámara 3D'),(2,'XY del mismo retorno','143 ms · Z existe, aquí no se muestra')]:
 text(30+panel*500,95,title);text(30+panel*500,560,sub,18)
text(35,605,'X^4 + 3Y^4 + 6Z^4 + 0.5(X^2 + Y^2 + Z^2) = 1 · escala uniforme 0.42',22)
text(35,643,'Vista offline: no captura de osci-render. Caras y persistencia no implican timbre aceptado.',17)
out=ROOT/'recordings/014-cuartica-tonal.png';im.save(out);print(out)
