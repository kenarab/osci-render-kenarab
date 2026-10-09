-- ocho-lobulos / LOB-01…05. XYZ de la ecuación; ruta geométrica sin filtro espectral.
-- A forma, B giro (0 pausa), C portadora, D cobertura, E escala.
local LIVE=false
-- LOB-02. Familias propias, no superficies récord. Sin partitura ni estado.
local function lobed_point(kind,u,v,a)
 local cv=math.cos(v)
 local x,y,z=cv*math.cos(u),cv*math.sin(u),math.sin(v)
 local x2,y2,z2=x*x,y*y,z*z
 local q=x2*x2+y2*y2+z2*z2
 local d=kind==1 and (1-a*q) or (q-a*(x2*y2+y2*z2+z2*x2))
 local r=1/math.sqrt(math.sqrt(d))
 return r*x,r*y,r*z
end
local function lobed_bound(kind,a)
 return ((kind==1 and 1 or 3)/(1-a))^.25
end
local function lobed_field(kind,x,y,z,a)
 local x2,y2,z2=x*x,y*y,z*z
 local q=x2*x2+y2*y2+z2*z2
 if kind==1 then return (x2+y2+z2)^2-a*q-1 end
 return q-a*(x2*y2+y2*z2+z2*x2)-1
end

local KIND=2
local ID='ocho-lobulos-'..tostring(LIVE)
if not lobed_surface or lobed_surface.id~=ID or lobed_surface.rate~=sample_rate or step<lobed_surface.last then
 lobed_surface={id=ID,rate=sample_rate,last=step,u=0,v=0,angle=.65,a=0.88,hz=110,cover=7,size=.7}
end
local s=lobed_surface;s.last=step
local dt=1/sample_rate;local k=1-math.exp(-dt/.08)
local function ctl(v,d)
 if not LIVE or type(v)~='number' or v~=v then return d end
 return math.max(0,math.min(1,v))
end
s.a=s.a+k*(0.94*ctl(slider_a,0.9361702127659575)-s.a)
s.hz=s.hz+k*(55+110*ctl(slider_c,.5)-s.hz)
s.cover=s.cover+k*(3+8*ctl(slider_d,.5)-s.cover)
s.size=s.size+k*(.4+.4*ctl(slider_e,.75)-s.size)
s.angle=s.angle+.2*ctl(slider_b,.5)*dt
s.u=(s.u+s.hz*dt)%1;s.v=(s.v+s.cover*dt)%1
local x,y,z=lobed_point(KIND,2*math.pi*s.u,2*math.pi*s.v,s.a)
s.raw={x,y,z};s.gain=s.size/lobed_bound(KIND,s.a)
local c,sn=math.cos(s.angle),math.sin(s.angle)
local xx,zz=c*x+sn*z,-sn*x+c*z
local cp,sp=math.cos(.45),math.sin(.45)
return {s.gain*xx,s.gain*(cp*y-sp*zz),s.gain*(sp*y+cp*zz)}
