"""Dos orquestaciones del Adagio. Python estándar + Pillow; sin solver en audio."""
import cmath
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'experiments/008-bach-materias'
PARAMS = [(1.,3.,6.), (5.,1.,2.), (2.,5.,1.), (1.,1.,4.)]
N, H, TABLE = 1024, 12, 2048


def point(direction, abc, k):
    norm=math.sqrt(sum(v*v for v in direction))
    d=[v/norm for v in direction]
    q=sum(a*v**4 for a,v in zip(abc,d))
    # q*r^4+k*r^2=1; forma estable sin cancelación.
    r=math.sqrt(2/(k+math.sqrt(k*k+4*q)))
    return tuple(r*v for v in d)


def field(p, abc, k):
    return sum(a*v**4+k*v*v for a,v in zip(abc,p))-1


def coefficients(values):
    return [sum(v*cmath.exp(-2j*math.pi*h*j/N) for j,v in enumerate(values))*2/N
            for h in range(1,H+1)]


def table(coeff):
    return [sum((v*cmath.exp(2j*math.pi*h*j/TABLE)).real
                for h,v in enumerate(coeff,1)) for j in range(TABLE)]


def lua(obj):
    if isinstance(obj,list): return '{'+','.join(map(lua,obj))+'}'
    return f'{obj:.8g}'


def geometry():
    image=Image.new('RGB',(1200,430),(9,16,25)); draw=ImageDraw.Draw(image)
    report=[]
    for voice,abc in enumerate(PARAMS):
        k=.05; rings,segments=24,48
        vertices=[point((0,0,1),abc,k)]
        for i in range(1,rings):
            t=math.pi*i/rings
            for j in range(segments):
                u=2*math.pi*j/segments
                vertices.append(point((math.sin(t)*math.cos(u),math.sin(t)*math.sin(u),math.cos(t)),abc,k))
        south=len(vertices); vertices.append(point((0,0,-1),abc,k))
        faces=[]
        for j in range(segments):
            nxt=(j+1)%segments
            faces.append((0,1+j,1+nxt))
            for i in range(rings-2):
                a=1+i*segments+j; b=1+i*segments+nxt
                faces.extend([(a,a+segments,b),(b,a+segments,b+segments)])
            a=1+(rings-2)*segments+j; b=1+(rings-2)*segments+nxt
            faces.append((a,south,b))
        residual=max(abs(field(p,abc,k)) for p in vertices)
        assert residual<1e-12
        from collections import Counter
        edges=Counter(tuple(sorted((f[j],f[(j+1)%3]))) for f in faces for j in range(3))
        assert set(edges.values())=={2} and len(vertices)-len(edges)+len(faces)==2
        with (OUT/f'cuartica-{voice+1}.obj').open('w') as f:
            f.write(f'# a*x^4+b*y^4+c*z^4+k*(x^2+y^2+z^2)=1; abc={abc}, k={k}\n')
            for p in vertices: f.write('v %.10f %.10f %.10f\n'%p)
            for face in faces: f.write('f %d %d %d\n'%tuple(v+1 for v in face))
        def rot(p):
            x,y,z=p; x,z=.825*x+.565*z,-.565*x+.825*z
            return x,.90*y-.436*z,.436*y+.90*z
        projected=list(map(rot,vertices))
        for face in sorted(faces,key=lambda f:sum(projected[v][2] for v in f)):
            center=[sum(vertices[v][d] for v in face)/3 for d in range(3)]
            normal=rot([4*a*v**3+2*k*v for a,v in zip(abc,center)])
            length=math.sqrt(sum(v*v for v in normal))
            light=.24+.76*max(0,(-.2*normal[0]+.3*normal[1]+.93*normal[2])/length)
            color=[(95,205,215),(209,176,104),(161,146,221),(125,197,147)][voice]
            draw.polygon([(150+300*voice+110*projected[v][0],205-110*projected[v][1]) for v in face],fill=tuple(int(c*light) for c in color))
        draw.text((20+300*voice,35),f'VOZ {voice+1} / {abc}',fill='white')
        report.append(dict(abc=abc,k=k,vertices=len(vertices),faces=len(faces),residual=residual))
    draw.text((20,390),'Mallas completas F=0. Referencia geometrica sombreada; no es salida de audio.',fill='white')
    image.save(OUT/'superficies.png')
    return report


def main():
    report={'geometry':geometry(),'harmonics':H,'table_size':TABLE,'families':{}}
    score=json.loads((ROOT/'experiments/005-aire-de-bach/score.json').read_text())
    maxhz=440*2**((max(n[2] for t in score['notes'] for n in t)-69+.06)/12)
    assert maxhz*H < 44100*.45
    report['max_partial_hz']=maxhz*H
    for family in ['cuarticas','prisma']:
        banks=[]; spectra=[]
        for voice,abc in enumerate(PARAMS):
            frames=[]; cs=[]
            for frame,k in enumerate([.8,.05]):
                xy=[[],[]]
                for j in range(N):
                    t=2*math.pi*j/N
                    if family=='cuarticas':
                        p=point((math.cos(t),math.sin(t),.48*math.sin((voice%3+2)*t+.4*voice)),abc,k)
                        assert abs(field(p,abc,k))<1e-12
                        x,y=p[0]+.35*p[2],p[1]-.22*p[2]
                    else:
                        ratio=[2,3,1,2][voice]
                        index=[1.25,.65,1.7,.38][voice]*(.3+.7*frame)
                        phase=t+index*math.sin(ratio*t+.18*math.sin(t))
                        x,y=math.cos(phase),math.sin(phase)
                    xy[0].append(x); xy[1].append(y)
                c=[coefficients(v) for v in xy]
                # Damping de parciales, sin DC, con envolvente de brillo por voz.
                rolloff=[.11,.22,.15,.32][voice]+(.18 if frame==0 else 0)
                c=[[v*math.exp(-rolloff*(h-1)) for h,v in enumerate(axis,1)] for axis in c]
                cs.append(c); frames.append([table(axis) for axis in c])
            norm=max(abs(v) for frame in frames for axis in frame for v in axis)
            banks.append([[[v/norm*.88 for v in axis] for axis in frame] for frame in frames])
            spectra.append([[[[v.real/norm*.88,v.imag/norm*.88] for v in axis] for axis in frame] for frame in cs])
        report['families'][family]={'coefficients':spectra}
        template=(OUT/'engine.lua.in').read_text()
        for live in [False,True]:
            code=template.replace('@FAMILY@',family).replace('@LIVE@',str(live).lower()).replace('@BANKS@',lua(banks)).replace('@SCORE@',lua(score['notes']))
            (OUT/f'aire-{family}{"-control" if live else ""}.lua').write_text(code)
    (OUT/'validacion.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Mallas cerradas, residuos y limite espectral OK; parcial maximo',maxhz*H)

if __name__=='__main__': main()
