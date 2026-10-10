"""MED-01…05. Genera sólo 022; bancos de todas las caras, sin dependencias externas."""
import cmath,json,math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'library'))
from algebraic_surfaces.core import cross,moments
from algebraic_surfaces.timbres import lua
OUT=ROOT/'experiments/022-jardines-meditativos'
STUDIES=[dict(id='claustro',title='Claustro de luz',kind=1,range=.46,shape=.91,hz=65.4063913,period=42,third=3,seventh=10),
 dict(id='jardin',title='Jardín suspendido',kind=2,range=.44,shape=.86,hz=73.416192,period=56,third=4,seventh=11),
 dict(id='memoria',title='Memoria de agua',kind=3,range=0,shape=.5,hz=55.,period=70,third=3,seventh=7)]
def point(kind,u,v,a):
 x,y,z=math.cos(v)*math.cos(u),math.cos(v)*math.sin(u),math.sin(v)
 if kind==3:return y*z*(.7+.6*a),x*z,x*y
 aa=.5+(.46 if kind==1 else .44)*a;q=x**4+y**4+z**4
 d=1-aa*q if kind==1 else q-aa*(x*x*y*y+y*y*z*z+z*z*x*x)
 r=d**(-.25);return x*r,y*r,z*r
def bound(kind,a):
 if kind==3:return .5*math.sqrt((.7+.6*a)**2+2)
 return ((1 if kind==1 else 3)/(1-.5-(.46 if kind==1 else .44)*a))**.25
def mesh(kind,a,n=24,m=48):
 vertices=[point(kind,2*math.pi*j/m,-math.pi/2+math.pi*i/n,a) for i in range(n+1) for j in range(m)]
 faces=[];samples=[]
 for i in range(n):
  for j in range(m):
   p=i*m+j;q=i*m+(j+1)%m;r=(i+1)*m+j;s=(i+1)*m+(j+1)%m
   for face in ([p,q,r],[q,s,r]):
    a0,b,c=[vertices[k] for k in face];normal=cross([b[k]-a0[k] for k in range(3)],[c[k]-a0[k] for k in range(3)])
    area=math.sqrt(sum(v*v for v in normal))/2
    if area>1e-12:
     faces.append(face);samples.append((tuple((a0[k]+b[k]+c[k])/3 for k in range(3)),area))
 return vertices,faces,samples
def banks(kind):
 frames=[]
 for frame in range(8):
  _,_,samples=mesh(kind,frame/7);coeff=moments(samples,harmonics=12);bands=[]
  for harmonics in (2,4,8,12):
   brightness=[]
   for roll in (.7,.24):
    channels=[]
    for channel in range(2):
     cs=[.5*c*math.exp(-roll*h) for h,c in enumerate(coeff[channel][:harmonics])]
     cs[0]+=.72*cmath.exp(-.045j*channel)
     # Cota L1 global y fundamental explícita; sin normalización por nota.
     norm=sum(abs(c) for c in cs)
     channels.append([sum((c*cmath.exp(2j*math.pi*(h+1)*i/256)).real for h,c in enumerate(cs))/norm for i in range(256)])
    brightness.append(channels)
   bands.append(brightness)
  frames.append(bands)
 return frames
def main():
 OUT.mkdir(parents=True,exist_ok=True);template=(ROOT/'library/performance/meditative.lua.in').read_text();models=[];manifest=[]
 for study in STUDIES:
  tables=banks(study['kind'])
  for audio in (False,True):
   for live in (False,True):
    filename=study['id']+('-sonido' if audio else '-xyz')+('-control' if live else '')+'.lua'
    values={k.upper():v for k,v in study.items()};values.update(ID=filename,LIVE=str(live).lower(),AUDIO=str(audio).lower(),REGISTER=math.log2(study['hz']/55),GEOMETRY=(ROOT/'library/algebraic_surfaces/lobed.lua').read_text(),BANKS=lua(tables) if audio else '{}')
    code=template
    for key,value in values.items():code=code.replace('@'+key+'@',str(value))
    assert '@' not in code;(OUT/filename).write_text(code)
  vertices,faces,_=mesh(study['kind'],study['shape']);trace=[point(study['kind'],2*math.pi*study['hz']*i/16000,2*math.pi*7*i/16000,study['shape']) for i in range(3200)]
  models.append(dict(id=study['id'],vertices=vertices,faces=faces,trace=trace,bound=bound(study['kind'],study['shape'])))
  manifest.append(dict(**study,register=math.log2(study['hz']/55),bank_shape_frames=8,bank_bands=[2,4,8,12],bank_samples=256,recipe='momentos de área de todas las caras + fundamental explícita; no modelo físico',host_acceptance=False))
 (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 (OUT/'models.js').write_text('window.XYZ_MODELS='+json.dumps(models,separators=(',',':'))+';\n')
 stage=(ROOT/'apps/xyz-stage/stage.js').read_text().replace("['esfera']","[models[0].id]").replace('Recorrido del Lua y malla de la misma ecuación.','Referencia con caras; no conectada a MIDI ni al audio.')
 (OUT/'gallery.js').write_text(stage)
 print('022: doce Lua, tres mallas de referencia, bancos precalculados; anteriores intactos')
if __name__=='__main__':main()
