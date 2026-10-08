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
