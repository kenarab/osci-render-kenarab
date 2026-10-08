-- toro. F=0 y controles en README; coordenadas XYZ sin proyeccion previa.
-- A giro (0 pausa), B portadora 80–160 Hz, C cobertura 4–12 Hz. Preset ignora sliders.
local LIVE=true
-- Parametrizaciones XYZ. Biblioteca sin partitura ni estado de transporte.
local function geometry(kind,u,v)
 local c,s=math.cos,math.sin
 if kind==1 then return (.62+.25*c(v))*c(u),(.62+.25*c(v))*s(u),.25*s(v)
 elseif kind==2 then
  local a,b,z=c(v)*c(u),c(v)*s(u),s(v);return b*z,a*z,a*b
 elseif kind==3 then local z=.7*s(v);return z*c(u),z*s(u),z
 else
  local x=math.sqrt(.65^2+.68^2)*s(v)
  local rho=math.sqrt(math.max(0,math.sqrt(.68^4+4*.65^2*x*x)-x*x-.65^2))
  return x,rho*c(u),rho*s(u)
 end
end
local bounds={.9,.55,1,1}
local function orient(x,y,z,angle,gain)
 local c,s=math.cos(angle),math.sin(angle);local xx,zz=c*x+s*z,-s*x+c*z
 local cp,sp=math.cos(.45),math.sin(.45)
 return {gain*xx,gain*(cp*y-sp*zz),gain*(sp*y+cp*zz)}
end

local ID='toro-'..tostring(LIVE)
if not diverse_surface or diverse_surface.id~=ID or diverse_surface.rate~=sample_rate or step<diverse_surface.last then
 diverse_surface={id=ID,rate=sample_rate,last=step,u=0,v=0,angle=.65,hz=110,cover=7}
end
local s=diverse_surface;s.last=step;local dt=1/sample_rate;local k=1-math.exp(-dt/.08)
local function control(v,d) if not LIVE or type(v)~='number' or v~=v then return d end;return math.max(0,math.min(1,v)) end
s.hz=s.hz+k*(80+80*control(slider_b,.375)-s.hz)
s.cover=s.cover+k*(4+8*control(slider_c,.375)-s.cover)
s.angle=s.angle+.2*control(slider_a,.5)*dt
s.u=(s.u+s.hz*dt)%1;s.v=(s.v+s.cover*dt)%1
local x,y,z=geometry(1,2*math.pi*s.u,2*math.pi*s.v)
s.raw={x,y,z};s.kind=1;s.gain=.7/bounds[1]
return orient(x,y,z,s.angle,s.gain)
