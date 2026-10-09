"""BVC-01…05: dos bajos de archivos MIDI locales, biblioteca de vocoder sin repertorio."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'library'))
from import_repertoire_midi import parse
from build_daft_repertoire import formants
from algebraic_surfaces.timbres import lua
OUT=ROOT/'experiments/020-bajos-vocoder';LIB=ROOT/'library/robot_voice'
SOURCES=[('lose-yourself-to-dance',2,56.,'Lose Yourself to Dance'),('giorgio-by-moroder',0,96.,'Giorgio by Moroder')]

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 dsp=(LIB/'vocoder.lua').read_text();template=(LIB/'bass.lua.in').read_text()
 vowels=formants()[48];manifest=[]
 for slug,track,start,title in SOURCES:
  path=ROOT/'downloads/daft-punk/originals'/(slug+'-candidate.mid');raw=path.read_bytes();score=parse(raw,allow_zero_duration=True)
  notes=[]
  for n in score['notes']:
   a,b=n['start_seconds'],n['end_seconds']
   if n['track']==track and n['channel']!=10 and b>start and a<start+24 and b>a:
    notes.append([max(0,a-start),min(24,b-start),n['pitch'],n['velocity']])
  notes.sort();assert notes
  original=json.loads((ROOT/'experiments/018-daft-repertorio'/(slug+'.json')).read_text())
  report=dict(id=slug,title=title,source_url=original['source_url'],sha256=hashlib.sha256(raw).hexdigest(),track=track,
   track_name=score['tracks'].get(str(track)),source_start=start,source_end=start+24,duration=24,notes=len(notes),
   pitches=sorted(set(n[2] for n in notes)),voice='Monofónico, prioridad a última nota; fases continuas',
   rights=original['rights'],modulator='Vocales sintéticas o canal externo ext_x; no voz del disco',host_acceptance=False)
  data='local function load_notes() return '+lua(notes)+' end\nlocal function load_vowels() return '+lua(vowels)+' end'
  for suffix,live,wet in [('bass',False,0),('bass-vocoder',False,.85),('bass-control',True,.65)]:
   code=template
   for key,value in dict(TITLE=title,LIVE=str(live).lower(),DSP=dsp,DATA=data,ID=slug+'-'+suffix+'-1',DURATION=24,WET=wet).items():code=code.replace('@'+key+'@',str(value))
   (OUT/(slug+'-'+suffix+'.lua')).write_text(code)
  manifest.append(report);print(slug,len(notes),'notas de bajo, recorte',start,start+24)
 effect=(LIB/'vocoder_effect.lua.in').read_text().replace('@DSP@',dsp)
 (OUT/'vocoder-effect.lua').write_text(effect)
 (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')

if __name__=='__main__':main()
