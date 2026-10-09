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
