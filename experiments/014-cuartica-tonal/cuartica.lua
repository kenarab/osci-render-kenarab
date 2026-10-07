-- CUA-01/02: cuartica XYZ completa, sin partitura ni proyeccion previa.
-- A giro (0 pausa); B portadora 80–160 Hz; C k=.1–.9; D cobertura 4–12 Hz.
-- Preset: 110 Hz, cobertura 7 Hz, k=.5. Timbre experimental; no normalizar para zoom.
local LIVE=false
local TAKE=1
if not tonal_xyz or tonal_xyz.take~=TAKE or tonal_xyz.live~=LIVE or tonal_xyz.rate~=sample_rate or step<tonal_xyz.last then
 tonal_xyz={take=TAKE,live=LIVE,rate=sample_rate,last=step,u=0,v=0,angle=.65,hz=110,cover=7,k=.5,spin=.1}
end
local s=tonal_xyz;s.last=step;local dt=1/sample_rate
local smooth=1-math.exp(-dt/.08)
local function control(value,default)
 if not LIVE or type(value)~='number' or value~=value then return default end
 return math.max(0,math.min(1,value))
end
s.hz=s.hz+smooth*(80+80*control(slider_b,.375)-s.hz)
s.cover=s.cover+smooth*(4+8*control(slider_d,.375)-s.cover)
s.k=s.k+smooth*(.1+.8*control(slider_c,.5)-s.k)
-- Giro sin suavizado: A=0 congela la escena inmediatamente, no detiene audio.
s.spin=.2*control(slider_a,.5);s.angle=s.angle+dt*s.spin
s.u=(s.u+s.hz*dt)%1;s.v=(s.v+s.cover*dt)%1
local u,v=2*math.pi*s.u,2*math.pi*s.v
local dx,dy,dz=math.cos(v)*math.cos(u),math.cos(v)*math.sin(u),math.sin(v)
local q=dx^4+3*dy^4+6*dz^4
local radius=math.sqrt(2/(s.k+math.sqrt(s.k*s.k+4*q)))
local x,y,z=.42*radius*dx,.42*radius*dy,.42*radius*dz
s.raw={x,y,z}
local c,sn=math.cos(s.angle),math.sin(s.angle)
local xx,zz=c*x+sn*z,-sn*x+c*z
local cp,sp=math.cos(.45),math.sin(.45)
return {xx,cp*y-sp*zz,sp*y+cp*zz}
