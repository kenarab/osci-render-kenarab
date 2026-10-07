"""Geometría y momentos de área reutilizables; sin partitura ni dependencias de Bach."""
import math
import cmath
from collections import Counter
from PIL import Image, ImageDraw

def field(item):
    # Sólo fórmulas locales versionadas; no aceptar texto de red/editor como código.
    code=compile(item['equation'].replace('^','**'),'<SURFER equation>','eval')
    constants={'__builtins__':{},'sqrt':math.sqrt,'sin':math.sin,'cos':math.cos,'a':item['a']}
    def evaluate(p):
        x,y,z=p
        return eval(code,constants,dict(x=x,y=y,z=z))
    return evaluate


def cross(a,b):
    return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])


def mesh(item,n=32,output_dir=None):
    f=field(item);bound=item['bound']
    # Desfase pequeño del grid para evitar vértices situados exactamente en F=0.
    coords=[-bound+2*bound*(i+.137)/(n+.274) for i in range(n+1)]
    points=[(x,y,z) for x in coords for y in coords for z in coords]
    values=[f(p) for p in points];verts=[];faces=[];edges={}
    def index(i,j,k):return (i*(n+1)+j)*(n+1)+k
    def edge(a,b):
        key=tuple(sorted((a,b)))
        if key in edges:return edges[key]
        pa,pb=points[a],points[b];va=values[a]
        lo,hi=0.,1.
        for _ in range(32):
            t=(lo+hi)/2;p=tuple(pa[d]+t*(pb[d]-pa[d]) for d in range(3))
            if (f(p)<0)==(va<0):lo=t
            else:hi=t
        edges[key]=len(verts);verts.append(p);return edges[key]
    tets=[(0,5,1,6),(0,1,2,6),(0,2,3,6),(0,3,7,6),(0,7,4,6),(0,4,5,6)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                cube=[index(i,j,k),index(i+1,j,k),index(i+1,j+1,k),index(i,j+1,k),index(i,j,k+1),index(i+1,j,k+1),index(i+1,j+1,k+1),index(i,j+1,k+1)]
                if all(values[v]<0 for v in cube) or all(values[v]>=0 for v in cube):continue
                for tet in tets:
                    inside=[cube[v] for v in tet if values[cube[v]]<0];outside=[cube[v] for v in tet if values[cube[v]]>=0]
                    if not inside or not outside:continue
                    if len(inside)==1 or len(outside)==1:
                        one,others=(inside,outside) if len(inside)==1 else (outside,inside)
                        faces.append(tuple(edge(one[0],v) for v in others))
                    else:
                        a,b=inside;c,d=outside
                        ac,ad,bc,bd=edge(a,c),edge(a,d),edge(b,c),edge(b,d)
                        faces.extend([(ac,ad,bc),(ad,bd,bc)])
    samples=[];valid=[]
    for face in faces:
        a,b,c=[verts[v] for v in face]
        normal=cross([b[d]-a[d] for d in range(3)],[c[d]-a[d] for d in range(3)])
        area=math.sqrt(sum(x*x for x in normal))/2
        if area<1e-16:continue
        valid.append(face);samples.append((tuple((a[d]+b[d]+c[d])/3 for d in range(3)),area))
    faces=valid
    counts=Counter(tuple(sorted((face[d],face[(d+1)%3]))) for face in faces for d in range(3))
    residual=max(abs(f(p)) for p in verts)
    assert verts and faces and residual<1e-5
    assert all(math.isfinite(v) for p in verts for v in p)
    if output_dir is not None:
      with (output_dir/(item['name']+'.obj')).open('w') as dest:
          dest.write('# SURFER F=0; recorte en caja, muestreo aproximado de nodos\n')
          for p in verts:dest.write('v %.10f %.10f %.10f\n'%p)
          for face in faces:dest.write('f %d %d %d\n'%tuple(v+1 for v in face))
    report=dict(name=item['name'],vertices=len(verts),faces=len(faces),grid=n,
        domain=[coords[0],coords[-1]],residual=residual,area=sum(a for _,a in samples),
        boundary_edges=sum(v==1 for v in counts.values()),nonmanifold_edges=sum(v>2 for v in counts.values()),
        caveat='Recorte espacial; la malla no certifica topologia ni cuenta singularidades')
    return verts,faces,samples,report


def rotate(p,angle=.6):
    x,y,z=p;c,s=math.cos(angle),math.sin(angle);x,z=c*x+s*z,-s*x+c*z
    return (x,.91*y-.414*z,.414*y+.91*z)


def panel(verts,faces,bound,color,angle=.6,size=420):
    image=Image.new('RGB',(size,size),(10,17,27));draw=ImageDraw.Draw(image)
    ps=[rotate(p,angle) for p in verts];scale=size/(bound*3.3)
    for face in sorted(faces,key=lambda f:sum(ps[v][2] for v in f)):
        a,b,c=[ps[v] for v in face];normal=cross([b[d]-a[d] for d in range(3)],[c[d]-a[d] for d in range(3)])
        norm=math.sqrt(sum(x*x for x in normal))
        if norm<1e-15:continue
        light=.23+.77*abs((-.25*normal[0]+.35*normal[1]+.902*normal[2])/norm)
        draw.polygon([(size/2+p[0]*scale,size/2-p[1]*scale) for p in (a,b,c)],fill=tuple(min(255,int(v*light)) for v in color))
    return image


def moments(samples,voice=0,harmonics=12):
    # Cuadratura en TODAS las caras: ángulo en una proyección oblicua + fase de profundidad.
    # Dos canales espaciales; no pretende simular modos físicos de una membrana.
    result=[]
    for axis in range(2):
        cs=[0j]*harmonics
        for (x,y,z),area in samples:
            u=x+.31*z+.13*y;v=y-.27*z+.11*x
            theta=math.atan2(v,u);radius=math.sqrt(u*u+v*v)
            depth=(.9+.2*voice)*z+(axis*.65)*x
            weight=area*(.25+radius)
            for h in range(1,harmonics+1):
                cs[h-1]+=weight*cmath.exp(-1j*(h*theta+depth))
        # Normalización relativa conserva contraste espectral y limita color agregado.
        norm=sum(abs(c) for c in cs) or 1
        cs=[c/norm for c in cs]
        result.append(cs)
    return result


