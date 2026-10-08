"""VIV-01…06. Nuevos estudios; no escribir los experimentos 001–014."""
import cmath,hashlib,json,math,sys,bisect
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'library'))
from performance.geometry import IDENTITIES,point,field
from algebraic_surfaces.timbres import lua
LIB=ROOT/'library/performance'

def palette():
 banks=[];report=[]
 for kind,item in enumerate(IDENTITIES):
  pts=[point(kind,6*math.pi*j/1024,2*math.pi*j/1024) for j in range(1024)]
  coeff=[]
  for axis in (0,1):
   # Include depth in the audio recipe, not in geometry (which remains exact).
   vals=[(p[axis]+.31*p[2])/item['bound'] for p in pts]
   cs=[sum(v*cmath.exp(-2j*math.pi*h*j/1024) for j,v in enumerate(vals))*2/1024 for h in range(1,13)]
   cs=[c*.9*math.exp(-.10*(h-1)) for h,c in enumerate(cs,1)]
   cs[0]+=.4*(1 if axis==0 else -1j);coeff.append(cs)
  bands=[]
  for limit in (2,4,8,12):
   axes=[[sum((c*cmath.exp(2j*math.pi*h*j/512)).real for h,c in enumerate(cs[:limit],1)) for j in range(512)] for cs in coeff]
   rms=math.sqrt(sum(x*x for axis in axes for x in axis)/1024)
   gain=min(.3/rms,.8/max(abs(x) for axis in axes for x in axis))
   bands.append([[x*gain for x in axis] for axis in axes])
  banks.append(bands);report.append(dict(**item,recipe='parametric-fourier-v1',bands=[2,4,8,12],rms_target=.3))
 (LIB/'identities.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
 return banks

def bach():
 score=json.loads((ROOT/'experiments/005-aire-de-bach/score.json').read_text())
 times=[0];beat=0;t=0
 def smooth(a,b,x):u=max(0,min(1,(x-a)/(b-a)));return u*u*(3-2*u)
 while beat<score['beats']:
  cadence=0
  for end in (24,48,96,144):
   if end-3<beat<end+1:cadence=smooth(end-3,end-.25,beat)*(1-smooth(end,end+1,beat))
  beat+=.005*26/60*(1+.035*math.sin(2*math.pi*(beat%8)/8))*(1-.2*cadence-.25*smooth(140,144,beat));t+=.005;times.append(beat)
 notes=sorted([[bisect.bisect_left(times,a)*.005,bisect.bisect_left(times,b)*.005,p,89,i+1] for i,track in enumerate(score['notes']) for a,b,p in track])
 return notes,t,score['voices'],dict(source=score['source'],license=score['license'],source_sha256=score['source_sha256'],timing='Adagio 26 BPM con rubato y cadencias; adaptación en este generador')

def oblivion():
 source=ROOT/'downloads/piazzolla/derived/oblivion-scorebase.events.json'
 src=json.loads(source.read_text());start,end=41.4892,70
 notes=sorted([[max(0,n['start_seconds']-start),min(end-start,n['end_seconds']-start),n['pitch'],n['velocity'],{0:1,1:2,2:3,3:3}[n['track']]] for n in src['notes'] if n['start_seconds']<end and n['end_seconds']>start and n['end_seconds']>n['start_seconds']])
 return notes,end-start,['Flauta','Fagot','Piano'],dict(source=src['provenance'],excerpt_seconds=[start,end],events_sha256=hashlib.sha256(source.read_bytes()).hexdigest())

def build():
 banks=palette();template=(LIB/'player.lua.in').read_text();geo=(LIB/'geometry.lua').read_text()
 for name,folder,data in [('bach','015-bach-voces-vivas',bach()),('oblivion','017-oblivion-voces-vivas',oblivion())]:
  notes,duration,names,source=data;out=ROOT/'experiments'/folder
  # Cota para TODO el repertorio: cada tabla <=.8, mezcla convexa, env/exp <=1.
  edges=sorted([(a,v/127) for a,b,p,v,i in notes]+[(b,-v/127) for a,b,p,v,i in notes])
  running=peak=0
  for _,delta in edges:running+=delta;peak=max(peak,running)
  bound=peak*.12*.8;assert bound<.9
  manifest=dict(mix_peak_bound_expression_1=bound,source=source,voices=names,defaults=[x['id'] for x in IDENTITIES[:len(names)]],duration=duration,notes=len(notes),files=[])
  for focus,live in [(0,False),(0,True)]+[(i,True) for i in range(1,len(names)+1)]:
   filename=name+('-control' if focus==0 and live else f'-voz-{focus}-xyz-control' if focus else '')+'.lua'
   values={'TITLE':name,'ID':name+'-vivas-1-'+str(focus)+'-'+str(live),'FOCUS':str(focus),'LIVE':str(live).lower(),'GEOMETRY':geo,'DURATION':repr(duration),'NOTES':lua(notes),'BANKS':lua(banks) if not focus else '{}','DEFAULTS':lua(list(range(1,len(names)+1)))}
   code=template
   for key,value in values.items():code=code.replace('@'+key+'@',value)
   assert '@' not in code
   (out/filename).write_text(('-- J. S. Bach, Air BWV 1068; Mutopia 242; CC-BY-SA-3.0; adaptacion y creditos en README.\n' if name=='bach' else '')+code);manifest['files'].append(filename)
  (out/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
  print(name,len(notes),'eventos',round(duration,3),'s',len(manifest['files']),'Lua')
if __name__=='__main__':build()
