-- Ejercicio de cobertura de superficie. Volumen bajo: prioriza dibujo, no timbre.
-- A velocidad de escena (0=pausa), B barrido 12–36 Hz, C ancho del elipsoide.
local LIVE=true
local RADII={.55,.26,.38}
if not surface_scan or surface_scan.kind~="elipsoide" or surface_scan.rate~=sample_rate or step<surface_scan.last then
 surface_scan={kind="elipsoide",rate=sample_rate,last=step,phase=0,elapsed=0,angle=.7,a=.3,b=.5,c=.5}
end
local s=surface_scan;s.last=step;local dt=1/sample_rate;local k=1-math.exp(-dt/.08)
local function smooth(old,v,default)
 if not LIVE or type(v)~='number' or v~=v then v=default end
 return old+k*(math.max(0,math.min(1,v))-old)
end
s.a=smooth(s.a,slider_a,.3);s.b=smooth(s.b,slider_b,.5);s.c=smooth(s.c,slider_c,.5)
s.angle=s.angle+dt*.3*s.a;s.phase=(s.phase+dt*(12+24*s.b))%1
local v=2*math.pi*s.phase;local u=12*v
local rx=RADII[1]*((.7+.6*s.c));local ry,rz=RADII[2],RADII[3]
local x=rx*math.cos(v)*math.cos(u);local y=ry*math.cos(v)*math.sin(u);local z=rz*math.sin(v)
s.raw={x,y,z};s.radii={rx,ry,rz}
local xx=x*math.cos(s.angle)+z*math.sin(s.angle)
local zz=-x*math.sin(s.angle)+z*math.cos(s.angle)
s.elapsed=s.elapsed+dt
local fade=math.min(1,s.elapsed/.05) -- entrada suave de 50 ms
return {fade*xx,fade*(.88*y-.475*zz),fade*(.475*y+.88*zz)}
