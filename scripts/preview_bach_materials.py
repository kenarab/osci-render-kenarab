"""Comparacion A/B/C a igual RMS; 20s de cada version, mismo pasaje 30–50s."""
from array import array
import math
from pathlib import Path
import subprocess
import sys
import wave
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'recordings/008-comparacion'

def main():
    if OUT.with_suffix('.mp4').exists() or OUT.with_suffix('.wav').exists():
        raise SystemExit('La comparacion ya existe; conservarla antes de regenerar')
    rate=48000;samples=array('h')
    titles=['ADAGIO / referencia anterior','CUARTICAS / superficies + espectro','PRISMA / modulacion de fase']
    for name in ['005-aire-adagio','008-cuarticas','008-prisma']:
        with wave.open(str(ROOT/f'recordings/{name}.wav')) as f:
            assert (f.getframerate(),f.getnchannels(),f.getsampwidth())==(rate,2,2)
            f.setpos(rate*30);part=array('h',f.readframes(rate*20))
        if sys.byteorder!='little':part.byteswap()
        rms=math.sqrt(sum(float(v)*v for v in part)/len(part));gain=.13*32768/rms
        for j in range(len(part)//2):
            fade=min(1,j/(rate*.08),(rate*20-1-j)/(rate*.08))
            for a in range(2):
                v=round(part[j*2+a]*gain*fade);assert abs(v)<32767;samples.append(v)
    payload=array('h',samples)
    if sys.byteorder!='little':payload.byteswap()
    with wave.open(str(OUT.with_suffix('.wav')),'wb') as f:
        f.setparams((2,2,rate,0,'NONE','not compressed'));f.writeframes(payload.tobytes())
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s','1000x800','-r','25','-i','-',
         '-i',str(OUT.with_suffix('.wav')),'-c:v','libx264','-preset','fast','-crf','22','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-shortest',str(OUT.with_suffix('.mp4'))]
    process=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    reference=Image.open(ROOT/'experiments/008-bach-materias/superficies.png').resize((900,323))
    font=ImageFont.load_default(size=22);small=ImageFont.load_default(size=15)
    try:
        for frame in range(25*60):
            image=Image.new('RGB',(1000,800),(9,16,25));d=ImageDraw.Draw(image)
            section=frame//500;d.text((35,25),titles[section],font=font,fill='white')
            if section==1:
                image.paste(reference,(50,70))
            else:
                d.text((50,115),'XY audible: mezcla de las cuatro voces.',font=font,fill=(160,190,200))
                d.text((50,155),'La figura resultante no es una superficie completa.',font=small,fill=(160,190,200))
            lo=frame*rate//25;hi=(frame+1)*rate//25
            points=[(500+samples[i*2]/32768*430,565-samples[i*2+1]/32768*430) for i in range(lo,hi)]
            d.line(points,fill=[(210,195,150),(90,215,207),(179,159,236)][section],width=2)
            d.text((35,738),'Mismo pasaje 30–50 s / RMS 0.13 / audio del Lua, sin efectos del host',font=small,fill=(180,190,200))
            d.text((35,770),'Bach / Mutopia 242 / jeff covey / CC BY-SA 3.0',font=small,fill=(150,160,180))
            process.stdin.write(image.tobytes())
    finally:
        process.stdin.close();code=process.wait()
    if code:raise SystemExit(code)
    print(OUT.with_suffix('.mp4'))

if __name__=='__main__':main()
