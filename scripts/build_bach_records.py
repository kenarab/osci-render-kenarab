"""REC-01–04: mallas SURFER y sonificación de áreas, sin dependencias nuevas."""
import hashlib
import json
import math
from pathlib import Path
from build_bach_materials import lua, table, H, TABLE

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'experiments/009-bach-surfer-records'
LIB=ROOT/'library/algebraic_surfaces'
import sys
sys.path.insert(0,str(ROOT/'library'))
from algebraic_surfaces.core import moments
from algebraic_surfaces.build import build_assets
def main():
    # Bach consume la biblioteca; la extracción también se ejecuta sin este proyecto.
    resources=build_assets()
    geometry=[report for _,_,report in resources]
    raw=[moments(samples,voice) for voice,(_,samples,_) in enumerate(resources)]
    score=json.loads((ROOT/'experiments/005-aire-de-bach/score.json').read_text())
    template=(ROOT/'experiments/008-bach-materias/engine.lua.in').read_text().replace('scripts/build_bach_materials.py','scripts/build_bach_records.py').replace('local TAKE = 301','local TAKE = 401')
    report=dict(geometry=geometry,harmonics=H,table_size=TABLE,raw_moments=[[[[c.real,c.imag] for c in axis] for axis in voice] for voice in raw],families={})
    for family,softness in [('seda',.26),('cristal',.065)]:
        banks=[];spectra=[]
        for voice,coeffs in enumerate(raw):
            frames=[];spec=[]
            for frame in range(2):
                cs=[]
                for axis,coeff in enumerate(coeffs):
                    roll=softness+[.035,.10,.065,.23][voice]+(.19 if frame==0 else 0)
                    c=[v*1.4*math.exp(-roll*(h-1)) for h,v in enumerate(coeff,1)]
                    # Fundamental explícita: fija la altura de Bach aunque la simetría suprima h=1.
                    c[0]+=.58*(1 if axis==0 else -1j)
                    cs.append(c)
                frames.append([table(c) for c in cs]);spec.append(cs)
            norm=max(abs(x) for frame in frames for axis in frame for x in axis)
            banks.append([[[x/norm*.88 for x in axis] for axis in frame] for frame in frames])
            spectra.append([[[[c.real/norm*.88,c.imag/norm*.88] for c in axis] for axis in frame] for frame in spec])
        report['families'][family]={'coefficients':spectra}
        for live in [False,True]:
            code=template.replace('@FAMILY@','records-'+family).replace('@LIVE@',str(live).lower()).replace('@BANKS@',lua(banks)).replace('@SCORE@',lua(score['notes']))
            (OUT/f'aire-{family}{"-control" if live else ""}.lua').write_text(code)
    report['score_sha256']=hashlib.sha256((ROOT/'experiments/005-aire-de-bach/score.json').read_bytes()).hexdigest()
    report['max_partial_hz']=440*2**((max(n[2] for t in score['notes'] for n in t)-69+.06)/12)*H
    assert report['max_partial_hz']<44100*.45
    assert len({json.dumps(v) for v in report['raw_moments']})==4
    (OUT/'validacion.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
