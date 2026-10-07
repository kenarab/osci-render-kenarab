-- GRV-01: groove original a 100 BPM; no cover ni superficie algebraica.
-- DP-02/03/04: vocales sinteticas, estudio original. NO es una superficie F=0.
-- A articulacion 1–5 silabas/s; B desplazamiento de formantes; C brillo; D giro.
-- Portadora armonica + envolvente espectral. No analiza voz ni usa letras/muestras.
local LIVE=false
if not disco_voice or disco_voice.rate~=sample_rate or step<disco_voice.last then
 disco_voice={rate=sample_rate,last=step,time=0,clock=0,phase=0,angle=.4,a=.25,b=.5,c=.5,d=.3,w={},target={},tick=0,notes={48,55,60,58,53,57,55,50},vowels={{730,1090,2440},{530,1840,2480},{270,2290,3010},{570,840,2410},{300,870,2240}},widths={140,210,330},accents={1,0,.35,.7,0,.45,.85,0,.8,0,.4,.7,0,.65,0,.45}}
 for h=1,32 do disco_voice.w[h]=0;disco_voice.target[h]=0 end
end
local s=disco_voice;s.last=step;local dt=1/sample_rate
local function ctl(old,v,default)
 if not LIVE or type(v)~='number' or v~=v then v=default end
 return old+(1-math.exp(-dt/.04))*(math.max(0,math.min(1,v))-old)
end
s.a=ctl(s.a,slider_a,.25);s.b=ctl(s.b,slider_b,.5);s.c=ctl(s.c,slider_c,.5);s.d=ctl(s.d,slider_d,.3)
local speed=100/60*4;s.clock=s.clock+dt*speed;s.time=s.time+dt
local index=math.floor(s.clock)%32;local part=math.floor(index/8)
local notes,vowels=s.notes,s.vowels
local hz=440*2^((notes[index%8+1]+(part==2 and 12 or 0)-69)/12)
s.phase=(s.phase+hz*dt)%1;s.angle=s.angle+dt*.15*s.d
-- Formantes de demostracion, no modelo de una persona. Recalcular a 250 Hz.
if s.tick<=0 then
 local v=vowels[(index+part)%5+1];local total=0;local shift=.75+.5*s.b
 for h=1,32 do
  local f=h*hz;local weight=0
  if f<sample_rate*.4 then
   for j=1,3 do local width=s.widths[j];local u=(f-v[j]*shift)/width;weight=weight+math.exp(-.5*u*u)/j end
   weight=(weight+.04/h)*h^(-(.3+.8*(1-s.c)))
  end
  s.target[h]=weight;total=total+weight
 end
 for h=1,32 do s.target[h]=s.target[h]/math.max(total,1e-12) end
 s.tick=math.max(1,math.floor(sample_rate/250))
end
s.tick=s.tick-1
local x,y=0,0;local blend=1-math.exp(-dt/.012);local p=2*math.pi*s.phase
for h=1,32 do
 s.w[h]=s.w[h]+blend*(s.target[h]-s.w[h])
 -- Cortar pesos viejos que superarían el margen Nyquist tras salto de nota.
 if h*hz<sample_rate*.4 then x=x+s.w[h]*math.sin(h*p);y=y+s.w[h]*math.cos(h*p) end
end
local function ease(v) v=math.max(0,math.min(1,v));return v*v*(3-2*v) end
local fraction=s.clock%1;local gate=.96
if part==1 then gate=.72 elseif part==2 then gate=.60 elseif part==3 then gate=.84 end
local env=ease(fraction/(.025*speed))*ease((gate-fraction)/(.055*speed))*ease(s.time/.06)
local z=.18*math.sin(3*p+.7)
local accents=s.accents
local accent=accents[index%16+1]
x,y,z=.11*env*accent*x,.11*env*accent*y,.025*env*accent*z
-- Bombo analitico continuo: 105→48 Hz, ataque suave, sin ruido blanco.
local beat=s.time*100/60;local kickTime=(beat%1)*60/100
local kickPhase=2*math.pi*(48*kickTime+57*.025*(1-math.exp(-kickTime/.025)))
local kick=.045*math.sin(kickPhase)*math.exp(-kickTime/.10)*ease(kickTime/.003)
-- Bajo independiente, sincopado; mismas notas originales, no riff transcrito.
local bassHz=hz/2;local bp=p/2
-- Fase propia evita el salto al dividir una fase envuelta por dos.
s.bassPhase=((s.bassPhase or 0)+bassHz*dt)%1;bp=2*math.pi*s.bassPhase
local bassEnv=ease(fraction/(.008*speed))*ease((.78-fraction)/(.045*speed))
local bass=.065*accent*bassEnv*(math.sin(bp)+.20*math.sin(2*bp))/1.2
x=x+bass+kick;y=y+.7*bass+kick;z=z+.018*accent*bassEnv*math.cos(bp)
local fade=ease(s.time/.06);x,y,z=x*fade,y*fade,z*fade
local c,sn=math.cos(s.angle),math.sin(s.angle)
return {c*x+sn*z,y,-sn*x+c*z}
