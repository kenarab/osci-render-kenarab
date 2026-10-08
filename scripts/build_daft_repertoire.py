"""DFT-01…06: cuatro arreglos MIDI completos como archivos, no reconstrucción del disco."""
import hashlib,json,math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'library'))
from build_live_voices import palette
from import_repertoire_midi import parse
from algebraic_surfaces.timbres import lua
OUT=ROOT/'experiments/018-daft-repertorio'
SOURCES={
 'something-about-us':('Daft Punk — Something About Us',22605,[0,2,3],[4]),
 'instant-crush':('Daft Punk — Instant Crush',22595,[8,9],[2]),
 'lose-yourself-to-dance':('Daft Punk — Lose Yourself to Dance',22596,[3,4,5,6,7],[2]),
 'giorgio-by-moroder':('Daft Punk — Giorgio by Moroder (arreglo reducido)',22588,[3,4],[0])}
def formants():
 vowels=[(730,1090,2440),(530,1840,2480),(270,2290,3010),(570,840,2410),(300,870,2240)];result=[]
 for note in range(128):
  hz=440*2**((note-69)/12);frames=[]
  for vowel in vowels:
   weights=[(sum(math.exp(-.5*((h*hz-f)/w)**2)/(i+1) for i,(f,w) in enumerate(zip(vowel,(140,210,330))))+.04/h)/h**.45 for h in range(1,33)]
   total=sum(weights);frames.append([v/total for v in weights])
  result.append(frames)
 return result

def loaders(notes,banks,vowels):
 # Bloques cortos evitan el límite de saltos/bytecode de LuaJIT con partituras largas.
 parts=['local function load_notes() local result={}']
 for offset in range(0,len(notes),400):
  parts.append('do local function chunk() return '+lua(notes[offset:offset+400])+' end; for _,n in ipairs(chunk()) do result[#result+1]=n end end')
 parts.append('return result end')
 for name,data in [('banks',banks),('formants',vowels)]:
  parts.append('local function load_'+name+'() return '+lua(data)+' end')
 return '\n'.join(parts)

def main():
 # palette() escribe sólo su registro nuevo, determinista; no modifica los estudios 015.
 original=palette();banks=[original[0],original[1],original[3]];vowels=formants()
 template=(ROOT/'library/robot_voice/song.lua.in').read_text();catalog=[]
 for slug,(title,source_id,leads,basses) in SOURCES.items():
  path=ROOT/'downloads/daft-punk/originals'/(slug+'-candidate.mid');raw=path.read_bytes();data=parse(raw,allow_zero_duration=True)
  notes=[];mapping={}
  for n in data['notes']:
   group=4 if n['channel']==10 else 1 if n['track'] in leads else 3 if n['track'] in basses else 2
   mapping[str(n['track'])]=dict(name=data['tracks'].get(str(n['track']),str(n['track'])),group=group)
   if n['end_seconds']>n['start_seconds']:notes.append([n['start_seconds'],n['end_seconds'],n['pitch'],n['velocity'],group,n['track']])
  notes.sort();duration=max(n[1] for n in notes)+.15
  running=peak=0
  for _,delta in sorted([(a,v/127) for a,b,p,v,g,t in notes]+[(b,-v/127) for a,b,p,v,g,t in notes]):running+=delta;peak=max(peak,running)
  gain=.6/max(1,peak) # Cada fuente <=1 y pesos convexos: cota <=.6 con expresión máxima.
  urlslug='daft_punk_'+('giorgio_by_moroder_2' if slug=='giorgio-by-moroder' else slug.replace('-','_'))
  report=dict(id=slug,title=title,source_url=f'https://midifind.com/files/d/daft_punk/{urlslug}/791-1-0-{source_id}',download_url=f'https://midifind.com/files/0-0-1-{source_id}-20',retrieved='2026-10-08',sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),duration=duration,notes=len(notes),skipped_zero_duration=data['zero_duration_notes'],tracks=mapping,gain=gain,mix_peak_bound=.6,rights='Descarga pública; autoría del arreglo y licencia abierta no verificadas; derivados sólo locales',review='SMF parseado; reproducción completa del archivo; cotejo con grabación y escucha pendientes',scope='Arreglo reducido: no tema original completo' if slug=='giorgio-by-moroder' else 'Arreglo fuente de principio a fin; no certifica integridad respecto del disco',warnings=data['warnings'])
  for live in (False,True):
   code=template
   for key,value in dict(TITLE=title,LIVE=str(live).lower(),ID=slug+'-1-'+str(live),DURATION=repr(duration),LOADERS=loaders(notes,banks,vowels),GAIN=repr(gain)).items():code=code.replace('@'+key+'@',value)
   (OUT/(slug+('-control' if live else '')+'.lua')).write_text(code)
  (OUT/(slug+'.json')).write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');catalog.append(report)
  print(slug,len(notes),'notas',round(duration,2),'s',len(mapping),'pistas')
 (OUT/'manifest.json').write_text(json.dumps(catalog,indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
