"""XYZ-03/04: geometría XYZ con caras; datos musicales privados separados."""
import json,math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'library'))
from algebraic_surfaces.core import mesh
LIB=ROOT/'library/algebraic_surfaces'

def regular(name):
 def point(v,u):
  x,y,z=math.cos(v)*math.cos(u),math.cos(v)*math.sin(u),math.sin(v)
  if name=='esfera':return [.42*x,.42*y,.42*z]
  if name=='elipsoide':return [.55*x,.26*y,.38*z]
  q=x**4+3*y**4+6*z**4;r=math.sqrt(2/(.5+math.sqrt(.25+4*q)))
  return [.45*r*x,.45*r*y,.45*r*z]
 n,m=32,64;vs=[point(-math.pi/2+math.pi*i/n,2*math.pi*j/m) for i in range(n+1) for j in range(m)];fs=[]
 for i in range(n):
  for j in range(m):
   a=i*m+j;b=i*m+(j+1)%m;c=(i+1)*m+j;d=(i+1)*m+(j+1)%m
   if i>0:fs.append([a,b,c])
   if i<n-1:fs.append([b,d,c])
 trace=json.loads((ROOT/'recordings'/f'012-{name}.xyz.json').read_text())
 return dict(id=name,vertices=vs,faces=fs,bound=.65,trace=trace,source='procedural F=0; mismo generador que ejercicios XYZ')

def main():
 models=[regular(n) for n in ['esfera','elipsoide','cuartica']]
 for item in json.loads((LIB/'catalog.json').read_text())['surfaces']:
  v,f,_,info=mesh(item,n=24)
  models.append(dict(id=item['name'],vertices=v,faces=f,bound=item['bound'],trace=[],source=item['equation'],validation=info));print(item['name'],len(f),flush=True)
 (LIB/'geometry3d.js').write_text('// Geometría XYZ independiente de repertorio; generada sin OBJ intermedio.\nwindow.XYZ_MODELS='+json.dumps(models,separators=(',',':'))+';\n')
 # Los eventos musicales se guardan fuera de Git, como los derivados de la semilla.
 oblivion=json.loads((ROOT/'downloads/piazzolla/derived/oblivion-scorebase.events.json').read_text())
 notes=[]
 for n in oblivion['notes']:
  if n['end_seconds']>30 and n['start_seconds']<70 and n['end_seconds']>n['start_seconds']:
   notes.append([max(0,n['start_seconds']-30),min(40,n['end_seconds']-30),{0:0,1:1,2:2,3:2}[n['track']],n['pitch'],n['velocity']/127])
 score=json.loads((ROOT/'experiments/005-aire-de-bach/score.json').read_text());beat=0;t=0;times=[0]
 def smooth(a,b,x):u=max(0,min(1,(x-a)/(b-a)));return u*u*(3-2*u)
 while beat<144:
  cadence=0
  for end in [24,48,96,144]:
   if end-3<beat<end+1:cadence=smooth(end-3,end-.25,beat)*(1-smooth(end,end+1,beat))
  beat+=.005*26/60*(1+.035*math.sin(2*math.pi*(beat%8)/8))*(1-.2*cadence-.25*smooth(140,144,beat));t+=.005;times.append(beat)
 import bisect
 bach=[[bisect.bisect_left(times,n[0])*.005,bisect.bisect_left(times,n[1])*.005,i,n[2],.7] for i,track in enumerate(score['notes']) for n in track]
 data=dict(bach=dict(duration=t,names=['Violino I','Violino II','Viola','Continuo'],defaults=['barthsextic','togliatti','endrass','kummerquartic'],events=bach),oblivion=dict(duration=40,names=['Flauta','Fagot','Piano'],defaults=['barthsextic','togliatti','kummerquartic'],events=notes))
 (ROOT/'recordings/012-repertoire.js').write_text('window.XYZ_REPERTOIRE='+json.dumps(data,separators=(',',':'))+';\n')
 print('Geometría 3D y timelines preparados; sin audio plano ni OBJ de transporte')
if __name__=='__main__':main()
