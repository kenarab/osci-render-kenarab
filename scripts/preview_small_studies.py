"""XY real con persistencia explícita; no sustituye curvas por mallas sombreadas."""
from array import array
from pathlib import Path
import subprocess,wave,sys
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
fontpath='/System/Library/Fonts/Supplemental/Arial.ttf'
font=ImageFont.truetype(fontpath,26);small=ImageFont.truetype(fontpath,17)

def video(name,title,detail,seconds):
    source=ROOT/'recordings'/f'{name}.wav';out=source.with_suffix('.mp4')
    if out.exists():raise SystemExit('Conservar video existente: '+str(out))
    with wave.open(str(source)) as w:rate=w.getframerate();data=array('h',w.readframes(w.getnframes()))
    if sys.byteorder!='little':data.byteswap()
    proc=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s','1000x800','-r','25','-i','-','-i',str(source),'-t',str(seconds),'-c:v','libx264','-preset','fast','-crf','22','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k',str(out)],stdin=subprocess.PIPE)
    try:
        for frame in range(seconds*25):
            im=Image.new('RGB',(1000,800),(9,17,26));d=ImageDraw.Draw(im);d.text((30,25),title,font=font,fill='white')
            # Ventana de 50 ms, independiente del fps del video: una vuelta completa a 24 Hz.
            hi=min(len(data)//2,int((frame+1)/25*rate));lo=max(0,hi-int(.05*rate))
            pts=[(500+data[i*2]/32768*600,410-data[i*2+1]/32768*600) for i in range(lo,hi)]
            if len(pts)>1:d.line(pts,fill=(109,226,205),width=1)
            d.text((30,704),detail,font=small,fill=(180,200,210))
            d.text((30,737),'XY del mismo Lua que se escucha · ventana de 50 ms · no es captura del host',font=small,fill=(160,185,195))
            proc.stdin.write(im.tobytes())
    finally:proc.stdin.close();assert proc.wait()==0
    print(out)

for name in ['esfera','elipsoide']:video('010-'+name,name.capitalize()+' / ejercicio de cobertura','Una superficie; 24 barridos por segundo. Evaluar forma antes de valorar timbre.',10)
video('011-oblivion','Oblivion / fragmento con timbres asignables','Flauta: Barth · Fagot: Togliatti · Piano: Kummer. La suma XY no dibuja las mallas.',40)
