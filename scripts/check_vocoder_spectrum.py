"""BVC-06: análisis FFT independiente, sólo biblioteca estándar; no requiere instalar."""
import cmath,json,math,struct,wave
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def fft(data):
 n=len(data);a=list(map(complex,data));j=0
 for i in range(1,n):
  bit=n>>1
  while j&bit:j^=bit;bit>>=1
  j^=bit
  if i<j:a[i],a[j]=a[j],a[i]
 length=2
 while length<=n:
  angle=cmath.exp(-2j*math.pi/length)
  for start in range(0,n,length):
   w=1
   for k in range(length//2):
    u=a[start+k];v=w*a[start+k+length//2]
    a[start+k],a[start+k+length//2]=u+v,u-v;w*=angle
  length*=2
 return a[:n//2+1]

def main():
 reports=[]
 for hz in (400,2400):
  with wave.open(str(ROOT/f'recordings/020-test-mod-{hz}.wav')) as w:
   rate=w.getframerate();assert w.getnchannels()==2 and w.getsampwidth()==2
   w.setpos(rate//2);raw=w.readframes(32768)
  samples=struct.unpack('<'+'h'*(len(raw)//2),raw)[::2];assert len(samples)==32768
  spectrum=fft([v/32768*(.5-.5*math.cos(2*math.pi*i/(len(samples)-1))) for i,v in enumerate(samples)])
  power=[abs(v)**2 for v in spectrum];total=sum(power);assert total>1
  low=sum(v for i,v in enumerate(power) if 180<i*rate/32768<850)/total
  high=sum(v for i,v in enumerate(power) if 1500<i*rate/32768<3400)/total
  centroid=sum(i*rate/32768*v for i,v in enumerate(power))/total
  assert (low>5*high if hz==400 else high>5*low),'No hay transferencia espectral del modulador'
  reports.append(dict(modulator_hz=hz,low_fraction=low,high_fraction=high,centroid_hz=centroid))
 assert reports[1]['centroid_hz']>reports[0]['centroid_hz']*2.5
 (ROOT/'experiments/020-bajos-vocoder/validacion-espectral.json').write_text(json.dumps(reports,indent=2)+'\n')
 print('Transferencia espectral 400 → 2400 Hz aprobada:',reports)

if __name__=='__main__':main()
