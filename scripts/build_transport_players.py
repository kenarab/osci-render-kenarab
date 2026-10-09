"""TRN-01…05: variantes nuevas; no regenerar 018 ni 020."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'library'))
from algebraic_surfaces.timbres import lua
from import_repertoire_midi import parse
from build_daft_repertoire import SOURCES,loaders,formants
from build_bass_vocoder import SOURCES as BASS_SOURCES
from build_live_voices import palette
OUT=ROOT/'experiments/021-transporte-lua';LIB=ROOT/'library'

def buckets(notes,duration):
 result=[[] for _ in range(int(duration)+2)]
 # Añadir intervalos de un segundo solapados. Orden de candidatos = orden de notas.
 import math
 for i,n in enumerate(notes,1):
  for sec in range(max(0,math.floor(n[0])),min(len(result)-1,math.ceil(n[1])-1)+1):result[sec].append(i)
 return result

def adapt(template,kind):
 transport=(LIB/'performance/transport.lua').read_text()
 template='-- J posición, K pausa (0 reproduce), L volver al inicio (0→1).\n'+transport+'\n'+template
 if kind=='bass':
  marker='local t=s.time;s.time=t+dt*s.speed'
  reset='s.dsp=bvc_engine(sample_rate);s.tick=0'
  poly='false'
  template=template.replace('return {output,output,0}','return {output*s.transport.gain,output*s.transport.gain,0}')
 else:
  marker='local t=s.time;s.time=t+dt*s.speed;s.seconds=s.seconds+dt'
  reset='s.seconds=0'
  poly='true'
  template=template.replace('return {x*fade,y*fade,0}','return {x*fade*s.transport.gain,y*fade*s.transport.gain,0}')
 assert template.count(marker)==1
 block=f'''if not s.transport then s.transport=tr_new(s.duration);s.seekBuckets=load_seek_buckets() end
tr_tick(s.transport,sample_rate,slider_j,slider_k,slider_l,function(target)
 s.time=target;s.done=false;s.active,s.index=tr_active(s.notes,s.seekBuckets,target,{poly},s.speed)
 s.processed=s.index-1
 {reset}
end)
if not s.transport.playing and s.transport.gain==0 then return {{0,0,0}} end
local t=s.time;if s.transport.playing then s.time=t+dt*s.speed end
'''
 if kind!='bass':block+='s.seconds=s.seconds+dt\n'
 return template.replace(marker,block)

def write(template,values,path):
 for key,value in values.items():template=template.replace('@'+key+'@',str(value))
 assert '@' not in template
 path.write_text(template)

def main():
 OUT.mkdir(parents=True,exist_ok=True);manifest=[]
 bass=adapt((LIB/'robot_voice/bass.lua.in').read_text(),'bass')
 dsp=(LIB/'robot_voice/vocoder.lua').read_text();vowels=formants()
 for slug,track,start,title in BASS_SOURCES:
  score=parse((ROOT/'downloads/daft-punk/originals'/(slug+'-candidate.mid')).read_bytes(),allow_zero_duration=True)
  notes=sorted([[max(0,n['start_seconds']-start),min(24,n['end_seconds']-start),n['pitch'],n['velocity']]
   for n in score['notes'] if n['track']==track and n['channel']!=10 and n['end_seconds']>max(start,n['start_seconds']) and n['start_seconds']<start+24])
  data='local function load_notes() return '+lua(notes)+' end\nlocal function load_vowels() return '+lua(vowels[48])+' end\nlocal function load_seek_buckets() return '+lua(buckets(notes,24))+' end'
  for suffix,live,wet in [('bass-transport',False,0),('bass-vocoder-transport',False,.85),('bass-control-transport',True,.65)]:
   filename=slug+'-'+suffix+'.lua'
   write(bass,dict(TITLE=title,LIVE=str(live).lower(),DSP=dsp,DATA=data,ID=filename+'-1',DURATION=24,WET=wet),OUT/filename)
   manifest.append(dict(file=filename,kind='bass',duration=24,notes=len(notes),parent='020-bajos-vocoder',controls=live))
 # Los bancos se calculan sin generar ningún archivo de repertorio anterior.
 original=palette();banks=[original[0],original[1],original[3]]
 song=adapt((LIB/'robot_voice/song.lua.in').read_text(),'song')
 for slug,(title,source_id,leads,basses) in SOURCES.items():
  score=parse((ROOT/'downloads/daft-punk/originals'/(slug+'-candidate.mid')).read_bytes(),allow_zero_duration=True)
  notes=[]
  for n in score['notes']:
   if n['end_seconds']<=n['start_seconds']:continue
   group=4 if n['channel']==10 else 1 if n['track'] in leads else 3 if n['track'] in basses else 2
   notes.append([n['start_seconds'],n['end_seconds'],n['pitch'],n['velocity'],group,n['track']])
  notes.sort();source=json.loads((ROOT/'experiments/018-daft-repertorio'/(slug+'.json')).read_text());duration=source['duration']
  data=loaders(notes,banks,vowels)+'\nlocal function load_seek_buckets() return '+lua(buckets(notes,duration))+' end'
  for live in (False,True):
   filename=slug+('-control' if live else '')+'-transport.lua'
   write(song,dict(TITLE=title,LIVE=str(live).lower(),ID=filename+'-1',DURATION=duration,LOADERS=data,GAIN=source['gain']),OUT/filename)
   manifest.append(dict(file=filename,kind='song',duration=duration,notes=len(notes),parent='018-daft-repertorio',controls=live,scope=source['scope']))
 (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 print('021: seis bajos y ocho temas con transporte J/K/L; anteriores intactos')

if __name__=='__main__':main()
