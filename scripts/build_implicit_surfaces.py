"""Extrae superficies implícitas con tetraedros, exporta OBJ y vista sombreada.

python3 scripts/build_implicit_surfaces.py
Biblioteca estándar + Pillow para la imagen. No es un render del audio.
"""
from collections import Counter
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parents[1] / "experiments/006-superficies-implicitas"


def field(name, p):
    x,y,z = p
    if name == "toro":
        R,r = 0.62,0.24
        s = x*x+y*y+z*z+R*R-r*r
        return s*s-4*R*R*(x*x+y*y), (4*x*s-8*R*R*x,4*y*s-8*R*R*y,4*z*s)
    a,b = 0.6,0.65
    s = x*x+y*y+z*z+a*a
    return s*s-4*a*a*x*x-b**4, (4*x*s-8*a*a*x,4*y*s,4*z*s)


def mesh(name, n=28, bound=1.12):
    coords = [-bound+2*bound*i/n for i in range(n+1)]
    points = [(x,y,z) for x in coords for y in coords for z in coords]
    values = [field(name,p)[0] for p in points]
    vertices, faces, edges = [], [], {}
    def index(i,j,k): return (i*(n+1)+j)*(n+1)+k
    def edge(a,b):
        key = tuple(sorted((a,b)))
        if key in edges: return edges[key]
        t = values[a]/(values[a]-values[b])
        p = [points[a][d]+t*(points[b][d]-points[a][d]) for d in range(3)]
        # Refinar la posición sobre F=0; conectividad del muestreo intacta.
        for _ in range(5):
            v,g = field(name,p)
            norm = sum(c*c for c in g)
            assert norm > 1e-15
            p = [p[d]-v*g[d]/norm for d in range(3)]
        edges[key] = len(vertices)
        vertices.append(p)
        return edges[key]
    tets = [(0,5,1,6),(0,1,2,6),(0,2,3,6),(0,3,7,6),(0,7,4,6),(0,4,5,6)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                cube = [index(i,j,k),index(i+1,j,k),index(i+1,j+1,k),index(i,j+1,k),
                        index(i,j,k+1),index(i+1,j,k+1),index(i+1,j+1,k+1),index(i,j+1,k+1)]
                if all(values[v]>=0 for v in cube) or all(values[v]<0 for v in cube): continue
                for tet in tets:
                    inside = [cube[v] for v in tet if values[cube[v]]<0]
                    outside = [cube[v] for v in tet if values[cube[v]]>=0]
                    if not inside or not outside: continue
                    if len(inside)==1 or len(outside)==1:
                        one,others = (inside,outside) if len(inside)==1 else (outside,inside)
                        faces.append(tuple(edge(one[0],v) for v in others))
                    else:
                        a,b=inside; c,d=outside
                        ac,ad,bc,bd=edge(a,c),edge(a,d),edge(b,c),edge(b,d)
                        faces.extend([(ac,ad,bc),(ad,bd,bc)])
    def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
    oriented=[]
    for face in faces:
        a,b,c=[vertices[v] for v in face]
        normal=cross([b[d]-a[d] for d in range(3)],[c[d]-a[d] for d in range(3)])
        assert sum(v*v for v in normal)>1e-20
        center=[(a[d]+b[d]+c[d])/3 for d in range(3)]
        _,gradient=field(name,center)
        oriented.append(face if sum(normal[d]*gradient[d] for d in range(3))>0 else (face[0],face[2],face[1]))
    counts=Counter(tuple(sorted((face[d],face[(d+1)%3]))) for face in oriented for d in range(3))
    assert all(v==2 for v in counts.values()), "superficie no cerrada"
    euler=len(vertices)-len(counts)+len(oriented)
    assert euler == (0 if name=="toro" else 2), "topología inesperada"
    residual=max(abs(field(name,p)[0]) for p in vertices)
    assert residual<1e-9
    return vertices,oriented,{"vertices":len(vertices),"caras":len(oriented),"aristas":len(counts),
        "euler":euler,"max_residuo_vertices":residual,"resolucion":n,"dominio":[-bound,bound]}


def preview(models):
    image=Image.new("RGB",(1400,760),(9,16,25))
    draw=ImageDraw.Draw(image)
    def rotate(p):
        x,y,z=p; c,s=math.cos(0.55),math.sin(0.55)
        x,z=c*x+s*z,-s*x+c*z
        c,s=math.cos(-0.85),math.sin(-0.85)
        return (x,c*y-s*z,s*y+c*z)
    for panel,(name,vertices,faces,_) in enumerate(models):
        points=[rotate(p) for p in vertices]
        for face in sorted(faces,key=lambda f:sum(points[v][2] for v in f)):
            center=[sum(vertices[v][d] for v in face)/3 for d in range(3)]
            _,normal=field(name,center); normal=rotate(normal)
            length=math.sqrt(sum(v*v for v in normal))
            light=0.28+0.72*max(0,(-0.25*normal[0]+0.35*normal[1]+0.90*normal[2])/length)
            color=(68,210,191) if panel==0 else (226,167,95)
            xy=[(350+700*panel+points[v][0]*275,365-points[v][1]*275) for v in face]
            draw.polygon(xy,fill=tuple(int(v*light) for v in color))
        draw.text((50+700*panel,45),name.upper()+" / SUPERFICIE IMPLICITA",fill=(225,235,245))
        draw.text((50+700*panel,665),"F(x,y,z)=0 -> malla con caras -> OBJ",fill=(170,188,201))
    draw.text((50,715),"Vista geometrica sombreada. No es una captura de osci-render ni una figura producida por audio.",fill=(140,162,178))
    image.save(OUT/"superficies.png")


def main():
    models=[]; report={}
    for name in ["toro","cassini"]:
        vertices,faces,info=mesh(name)
        with (OUT/(name+".obj")).open("w") as f:
            f.write("# Superficie implicita F=0; triangulos, no curva parametrica\n")
            for p in vertices: f.write("v %.10f %.10f %.10f\n"%tuple(p))
            for face in faces: f.write("f %d %d %d\n"%tuple(v+1 for v in face))
        report[name]=info; models.append((name,vertices,faces,info))
    preview(models)
    (OUT/"validacion.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))


if __name__=="__main__": main()
