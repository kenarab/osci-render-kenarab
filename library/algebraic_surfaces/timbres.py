"""Genera bancos reutilizables desde mallas de la biblioteca; sin repertorio."""
import cmath,hashlib,json,math
from pathlib import Path
from .core import moments,cross
LIB=Path(__file__).resolve().parent
H=12;SIZE=1024

def lua(x):
    if isinstance(x,list):return '{'+','.join(map(lua,x))+'}'
    return f'{x:.9g}'

def generate_banks():
    registry=[];tables=[]
    for item in json.loads((LIB/'catalog.json').read_text())['surfaces']:
        path=LIB/'assets'/(item['name']+'.obj');vertices=[];samples=[]
        for line in path.read_text().splitlines():
            parts=line.split()
            if parts[0]=='v':vertices.append(list(map(float,parts[1:])))
            elif parts[0]=='f':
                a,b,c=[vertices[int(i)-1] for i in parts[1:]]
                normal=cross([b[d]-a[d] for d in range(3)],[c[d]-a[d] for d in range(3)])
                samples.append((tuple((a[d]+b[d]+c[d])/3 for d in range(3)),math.sqrt(sum(v*v for v in normal))/2))
        coeff=moments(samples,voice=0,harmonics=H);frames=[]
        for roll in [.4,.10]:
            axes=[]
            for axis,c in enumerate(coeff):
                cs=[v*1.4*math.exp(-roll*(h-1)) for h,v in enumerate(c,1)];cs[0]+=.58*(1 if axis==0 else -1j)
                axes.append([sum((v*cmath.exp(2j*math.pi*h*j/SIZE)).real for h,v in enumerate(cs,1)) for j in range(SIZE)])
            frames.append(axes)
        peak=max(abs(v) for frame in frames for axis in frame for v in axis)
        tables.append([[[v/peak*.85 for v in axis] for axis in frame] for frame in frames])
        registry.append(dict(id=item['name'],mesh_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),recipe='area-moments-v1',depth_index=0))
    report=dict(schema=1,harmonics=H,size=SIZE,banks=registry,recipe=dict(carrier=.58,geometry_gain=1.4,rolloffs=[.4,.10],description='momentos de todas las caras; no conserva F=0 en audio'))
    (LIB/'timbres.json').write_text(json.dumps(report,indent=2)+'\n')
    (LIB/'timbres.lua').write_text('-- Bancos de superficies reutilizables, sin partitura. Orden: Barth, Togliatti, Endrass, Kummer.\nreturn '+lua(tables)+'\n')
    return tables,report

if __name__=='__main__':generate_banks()
