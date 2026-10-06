"""Referencia 3D, barrido original y señal XY audible en tres videos y un montaje.

python3 scripts/preview_surface_instrument.py [directorio, por defecto recordings]
Pillow + ffmpeg. La referencia sombreada NO es una captura del host.
"""
from array import array
import json
import math
from pathlib import Path
import subprocess
import sys
import wave

from PIL import Image, ImageDraw, ImageFont
from build_surface_instrument import torus_mesh


def read_wav(path):
    with wave.open(str(path)) as f:
        assert (f.getnchannels(), f.getsampwidth(), f.getframerate()) == (2,2,48000)
        data = array("h", f.readframes(f.getnframes()))
    if sys.byteorder != "little": data.byteswap()
    return data


def rotate(p, spin):
    x,y,z = p
    y,z = y*math.cos(.9)-z*math.sin(.9), y*math.sin(.9)+z*math.cos(.9)
    return x*math.cos(spin)+z*math.sin(spin), y, -x*math.sin(spin)+z*math.cos(spin)


def make_frame(name, frame, state, raw, audio, mesh, normals):
    vertices, faces = mesh
    image = Image.new("RGB", (1440,600), (8,14,23))
    draw = ImageDraw.Draw(image)
    large, medium, small = [ImageFont.load_default(size=s) for s in (28,19,15)]
    colors = {"suave": (100,218,192), "cuerpo": (237,184,112), "aire": (147,181,240)}
    color = colors[name]
    draw.text((35,24), f"TORO SONORO  /  {name.upper()}", fill=color, font=large)
    draw.text((35,65), "Una superficie, un barrido. Sin partitura ni notas MIDI.", fill=(186,200,213), font=medium)
    for col, label in enumerate(("Superficie F = 0 / referencia 3D", "XY del barrido sin tratar", "XY audible / timbre tratado")):
        draw.text((30+480*col,112), label, fill=(222,231,237), font=medium)
        if col: draw.line((480*col,105,480*col,503), fill=(38,48,61))
    points = [rotate(p,state["spin"]) for p in vertices]
    for idx in sorted(range(len(faces)), key=lambda k:sum(points[i][2] for i in faces[k])):
        face = faces[idx]
        nx,ny,nz = rotate(normals[idx],state["spin"])
        light=.24+.76*max(0,-.20*nx+.35*ny+.91*nz)
        xy=[(240+points[i][0]*195,323-points[i][1]*195) for i in face]
        draw.polygon(xy,fill=tuple(int(c*min(1,light)) for c in color))
    # Misma escala y ventana para ambas señales; sin normalizar por variante.
    start=frame*1600
    stop=min(len(audio)//2,(frame+1)*1600)
    scale=195/(.75*.35)
    for col,data in ((1,raw),(2,audio)):
        xy=[(240+480*col+data[2*i]/32768*scale,323-data[2*i+1]/32768*scale)
            for i in range(start,stop)]
        if len(xy)>1: draw.line(xy,fill=color if col==2 else (115,147,160),width=1)
    draw.text((35,469), "Malla con caras; no es salida de audio", fill=(152,175,191),font=small)
    draw.text((515,469), "Raster de 24 vueltas; resolucion finita", fill=(152,175,191),font=small)
    draw.text((995,469), f"Radio del tubo audible: {state['effective_r']:.3f}", fill=color,font=small)
    draw.text((35,521), "R = 0.62  /  r = 0.24  |  Barrido: 48.99 Hz  |  Movimiento: 0.0125 rad/s",fill=(202,213,225),font=medium)
    draw.text((35,558), "Comparacion fuera de osci-render. El audio corresponde al panel derecho; el WAV conserva X/Y sin compresion.",fill=(147,167,184),font=small)
    draw.text((1350,28),f"{frame/30:04.1f} s",fill=(202,213,225),font=medium)
    return image


def main():
    out=Path(sys.argv[1] if len(sys.argv)>1 else "recordings")
    names=("suave","cuerpo","aire")
    outputs=[out/f"007-{name}.mp4" for name in names]+[out/"007-comparacion.mp4"]
    if any(p.exists() for p in outputs):
        raise SystemExit("Ya existe un video de salida; usar otro directorio para conservarlo.")
    mesh=torus_mesh(nu=64,nv=24)
    vertices,faces=mesh
    normals=[]
    for face in faces:
        x,y,z=[sum(vertices[i][d] for i in face)/3 for d in range(3)]
        q=x*x+y*y+z*z+.62**2-.24**2
        n=(4*x*q-8*.62**2*x,4*y*q-8*.62**2*y,4*z*q)
        length=math.sqrt(sum(v*v for v in n))
        normals.append(tuple(v/length for v in n))
    for name,output in zip(names,outputs):
        prefix=out/f"007-{name}"
        audio=read_wav(prefix.with_suffix(".wav"))
        raw=read_wav(out/f"007-{name}-raw.wav")
        report=json.loads(prefix.with_suffix(".json").read_text())
        assert len(audio)==len(raw)==48000*12*2 and len(report["frames"])==360
        assert all(abs(f["r"]-.24)<1e-9 for f in report["frames"]), "malla de referencia no coincide"
        command=["ffmpeg","-hide_banner","-loglevel","error","-n","-f","rawvideo",
                 "-pix_fmt","rgb24","-s","1440x600","-r","30","-i","-",
                 "-i",str(prefix.with_suffix(".wav")),"-map","0:v","-map","1:a",
                 "-c:v","libx264","-preset","fast","-crf","20","-pix_fmt","yuv420p",
                 "-c:a","aac","-b:a","256k","-shortest","-movflags","+faststart",str(output)]
        p=subprocess.Popen(command,stdin=subprocess.PIPE)
        try:
            for frame,state in enumerate(report["frames"]):
                image=make_frame(name,frame,state,raw,audio,mesh,normals)
                if frame==180: image.save(out/f"007-{name}.png")
                p.stdin.write(image.tobytes())
        finally:
            p.stdin.close()
            code=p.wait()
        if code: raise SystemExit(f"ffmpeg: {code}")
        print(output,flush=True)
    # Re-encode el montaje para evitar huecos de timestamps/priming AAC entre clips.
    command=["ffmpeg","-hide_banner","-loglevel","error","-n"]
    for path in outputs[:3]: command.extend(["-i",str(path)])
    command.extend(["-filter_complex","[0:v][0:a][1:v][1:a][2:v][2:a]concat=n=3:v=1:a=1[v][a]",
                    "-map","[v]","-map","[a]","-c:v","libx264","-preset","fast",
                    "-crf","20","-pix_fmt","yuv420p","-c:a","aac","-b:a","256k",
                    "-movflags","+faststart",str(outputs[3])])
    subprocess.run(command,check=True)
    print(outputs[3])


if __name__=="__main__": main()
