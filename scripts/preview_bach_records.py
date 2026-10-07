"""REC-05: 60s A/B/C, mismo pasaje y RMS; superficies de referencia + XY audible."""
from array import array
import math
from pathlib import Path
import subprocess
import sys
import wave
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'recordings/009-comparacion'

def main():
    if OUT.with_suffix('.mp4').exists() or OUT.with_suffix('.wav').exists():
        raise SystemExit('Comparacion existente: conservar antes de regenerar')
    rate=48000;samples=array('h')
    names=['005-aire-adagio','009-seda','009-cristal']
    for name in names:
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
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s','1440x900','-r','25','-i','-',
         '-i',str(OUT.with_suffix('.wav')),'-c:v','libx264','-preset','fast','-crf','22','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-shortest',str(OUT.with_suffix('.mp4'))]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    sheet=Image.open(ROOT/'experiments/009-bach-surfer-records/superficies.png')
    grid=Image.new('RGB',(760,760),(10,17,27));gd=ImageDraw.Draw(grid)
    font_path='/System/Library/Fonts/Supplemental/Arial.ttf'
    if Path(font_path).exists():
        font=ImageFont.truetype(font_path,27);small=ImageFont.truetype(font_path,18)
    else:
        font=ImageFont.load_default(size=27);small=ImageFont.load_default(size=18)
    labels=['I / Barth · grado 6','II / Togliatti · grado 5','III / Endrass · grado 8','IV / Kummer · grado 4']
    for i in range(4):
        x=(i%2)*380;y=(i//2)*380
        grid.paste(sheet.crop((i*420,55,i*420+420,475)).resize((360,360)),(x,y+20))
        gd.text((x+15,y),labels[i],font=small,fill='white')
    titles=['ADAGIO ORIGINAL / referencia','SEDA / superficies, espectro suave','CRISTAL / superficies, más parciales']
    try:
        for frame in range(1500):
            section=frame//500;image=Image.new('RGB',(1440,900),(10,17,27));d=ImageDraw.Draw(image)
            d.text((30,22),titles[section],font=font,fill='white')
            if section:
                image.paste(grid,(15,78))
            else:
                d.text((55,290),'Tu Adagio favorito',font=font,fill=(225,195,145))
                d.text((55,335),'Referencia para comparar el cambio de timbre.',font=small,fill=(170,185,200))
            d.text((810,115),'XY de la mezcla audible',font=font,fill='white')
            lo=frame*rate//25;hi=(frame+1)*rate//25
            points=[(1100+samples[i*2]/32768*660,460-samples[i*2+1]/32768*660) for i in range(lo,hi)]
            d.line(points,fill=[(225,195,145),(96,216,219),(186,151,234)][section],width=2)
            d.text((810,725),'Mismo pasaje 30–50 s / RMS igualado',font=small,fill=(170,185,200))
            d.text((810,755),'La suma XY no reproduce las mallas.',font=small,fill=(170,185,200))
            d.text((30,850),'Izquierda: referencia geométrica recortada. Bach / Mutopia 242 / jeff covey / CC BY-SA 3.0',font=small,fill=(160,180,195))
            proc.stdin.write(image.tobytes())
    finally:
        proc.stdin.close();code=proc.wait()
    assert code==0
    print(OUT.with_suffix('.mp4'))

if __name__=='__main__':main()
