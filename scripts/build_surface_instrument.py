"""Genera los tres Lua autónomos y la malla del toro de referencia. Sin paquetes.

python3 scripts/build_surface_instrument.py
"""
from collections import Counter
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "experiments/007-toro-sonoro"


def torus_mesh(radius=0.24, nu=96, nv=32):
    vertices = []
    for i in range(nu):
        u = 2*math.pi*i/nu
        for j in range(nv):
            v = 2*math.pi*j/nv
            vertices.append(((0.62+radius*math.cos(v))*math.cos(u),
                             (0.62+radius*math.cos(v))*math.sin(u), radius*math.sin(v)))
    faces = []
    for i in range(nu):
        for j in range(nv):
            a, b = i*nv+j, ((i+1)%nu)*nv+j
            c, d = ((i+1)%nu)*nv+(j+1)%nv, i*nv+(j+1)%nv
            faces.extend(((a,b,c),(a,c,d)))
    return vertices, faces


def main():
    template = (DEST/"engine.lua.in").read_text()
    assert template.count("@VOICE@") == 1
    for name in ("suave", "cuerpo", "aire"):
        (DEST/(name+".lua")).write_text(template.replace("@VOICE@", name))
    (DEST/"control.lua").write_text(template.replace("@VOICE@", "suave").replace(
        "local USAR_SLIDERS = false", "local USAR_SLIDERS = true", 1))
    vertices, faces = torus_mesh()
    edges = Counter(tuple(sorted((f[i],f[(i+1)%3]))) for f in faces for i in range(3))
    assert all(n == 2 for n in edges.values())
    assert len(vertices)-len(edges)+len(faces) == 0
    residual = max(abs((x*x+y*y+z*z+0.62**2-0.24**2)**2-4*0.62**2*(x*x+y*y))
                   for x,y,z in vertices)
    assert residual < 1e-12
    for a,b,c in faces:
        u=[vertices[b][i]-vertices[a][i] for i in range(3)]
        v=[vertices[c][i]-vertices[a][i] for i in range(3)]
        normal=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]
        assert sum(n*n for n in normal)>1e-14
    with (DEST/"toro.obj").open("w") as f:
        f.write("# Toro F=0, R=0.62 r=0.24; malla de referencia, no audio\n")
        for p in vertices: f.write("v %.15f %.15f %.15f\n" % p)
        for face in faces: f.write("f %d %d %d\n" % tuple(i+1 for i in face))
    print(f"Tres Lua; malla cerrada: {len(vertices)} vértices, {len(faces)} caras; residuo {residual:.3g}")


if __name__ == "__main__": main()
