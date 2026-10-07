"""INS-03: fragmento privado de Oblivion para un reproductor desacoplado."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'library'))
from algebraic_surfaces.timbres import generate_banks, lua, H

def main():
    tables,registry=generate_banks();p=ROOT/'downloads/piazzolla/derived/oblivion-scorebase.events.json';src=json.loads(p.read_text())
    start=30.;duration=40.;notes=[];clipped=0;zero=0
    for n in src['notes']:
        if n['start_seconds']>=start+duration or n['end_seconds']<=start:continue
        a=max(0,n['start_seconds']-start);b=min(duration,n['end_seconds']-start)
        if b<=a:zero+=1;continue
        clipped+=int(n['start_seconds']<start or n['end_seconds']>start+duration)
        notes.append([a,b,n['pitch'],n['velocity'],{0:1,1:2,2:3,3:3}[n['track']]])
    notes.sort();highest=440*2**((max(n[2] for n in notes)-69)/12)*H;assert highest<44100*.45
    config=dict(schema=1,source=src['provenance'],excerpt_seconds=[start,start+duration],duration=duration,notes=len(notes),clipped_boundary_notes=clipped,zero_duration_skipped_in_excerpt=zero,
        instruments=[dict(id='flute',source_tracks=[0],surface='barthsextic'),dict(id='bassoon',source_tracks=[1],surface='togliatti'),dict(id='piano',source_tracks=[2,3],surface='kummerquartic')],max_partial_hz=highest)
    out=ROOT/'experiments/011-oblivion-asignable';(out/'config.json').write_text(json.dumps(config,indent=2)+'\n')
    template=(ROOT/'library/algebraic_surfaces/player.lua.in').read_text()
    for live in [False,True]:
        code=template.replace('@BANKS@',lua(tables)).replace('@NOTES@',lua(notes)).replace('@LIVE@',str(live).lower()).replace('@DURATION@',str(duration))
        (ROOT/'recordings'/('011-oblivion'+('-control' if live else '')+'.lua')).write_text(code)
    print(len(notes),'eventos; parciales hasta',highest,'Hz; notas originales/derivadas fuera de Git')

if __name__=='__main__':main()
