"""Render de concierto XY: usa el WAV real, con persistencia óptica y capítulos.

python3 scripts/preview_bach_air.py [prefijo, por defecto recordings/005-aire]
Pillow + ffmpeg. Los colores y textos son editoriales; el trazo viene del audio.
"""
from array import array
import json
from pathlib import Path
import subprocess
import sys
import wave

from PIL import Image, ImageDraw, ImageFilter, ImageFont


def main():
    prefix = Path(sys.argv[1] if len(sys.argv)>1 else "recordings/005-aire")
    output = prefix.with_suffix(".mp4")
    if output.exists():
        raise SystemExit("El video ya existe; usar otro prefijo para conservarlo")
    report = json.loads(prefix.with_suffix(".json").read_text())
    with wave.open(str(prefix.with_suffix(".wav"))) as source:
        assert source.getnchannels()==2 and source.getsampwidth()==2
        rate = source.getframerate()
        samples = array("h",source.readframes(source.getnframes()))
    if sys.byteorder != "little": samples.byteswap()
    size, fps = 960, 30
    fonts = [ImageFont.load_default(size=s) for s in [56,21,16,13]]
    bg = Image.new("RGB",(size,size))
    draw = ImageDraw.Draw(bg)
    for y in range(size):
        v = int(5*(1-abs(y-size/2)/(size/2)))
        draw.line((0,y,size,y),fill=(5+v,9+v,17+v))
    trail = Image.new("RGB",(size,size))
    chapters = ["I  /  HILO", "II  /  BOVEDA", "III  /  PENUMBRA", "IV  /  LUZ"]
    colors = [(88,213,209),(144,189,248),(166,153,235),(239,199,126)]
    sections = report["sections"]
    frames = (len(samples)//2*fps+rate-1)//rate
    command = ["ffmpeg","-hide_banner","-loglevel","error","-n","-f","rawvideo",
               "-pix_fmt","rgb24","-s",f"{size}x{size}","-r",str(fps),"-i","-",
               "-i",str(prefix.with_suffix(".wav")),"-map","0:v","-map","1:a",
               "-c:v","libx264","-preset","fast","-crf","19","-pix_fmt","yuv420p",
               "-c:a","aac","-b:a","256k","-shortest","-movflags","+faststart",str(output)]
    process = subprocess.Popen(command,stdin=subprocess.PIPE)
    try:
        for frame in range(frames):
            time = frame/fps
            chapter = min(3,sum(time>=v for v in sections[1:]))
            color = colors[chapter]
            lo,hi = frame*rate//fps,min(len(samples)//2,(frame+1)*rate//fps)
            layer = Image.new("RGB",(size,size))
            line = ImageDraw.Draw(layer)
            points = [(480+samples[2*i]/32768*560,490-samples[2*i+1]/32768*560)
                      for i in range(lo,hi)]
            if len(points)>1: line.line(points,fill=color,width=2)
            # Persistencia temporal breve: solo trazos de muestras reales previas.
            trail = Image.blend(trail,layer,0.70)
            glow = trail.filter(ImageFilter.GaussianBlur(3))
            from PIL import ImageChops
            image = ImageChops.add(bg,ImageChops.add(trail,glow,scale=1.0))
            d = ImageDraw.Draw(image)
            d.text((58,42),"A I R E",font=fonts[0],fill=(226,231,229))
            d.text((61,108),("Adagio / respiracion y fraseo" if "adagio" in prefix.name else "Cuatro voces en el espacio"),font=fonts[1],fill=(158,178,187))
            d.text((61,146),"J. S. BACH  /  BWV 1068 - II",font=fonts[2],fill=(114,136,151))
            d.text((61,810),chapters[chapter],font=fonts[1],fill=color)
            d.text((61,852),"La misma senal dibuja y suena. Cuatro toros, una trayectoria.",font=fonts[2],fill=(142,163,174))
            d.line((61,897,899,897),fill=(35,48,61),width=2)
            d.line((61,897,61+838*time/report["duration"],897),fill=color,width=2)
            d.text((61,917),"Mutopia / jeff covey - Adaptacion CC BY-SA 3.0",font=fonts[3],fill=(103,122,139))
            d.text((794,917),f"{int(time)//60}:{int(time)%60:02d}",font=fonts[3],fill=(150,170,180))
            process.stdin.write(image.tobytes())
    finally:
        process.stdin.close()
        result=process.wait()
    if result: raise SystemExit(f"ffmpeg: {result}")
    print(output)


if __name__ == "__main__":
    main()
