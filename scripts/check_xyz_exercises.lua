-- XYZ-02/03, NIV-02: verifica el retorno deshaciendo giro/tilt.
-- Exporta XYZ en marco del objeto para superponer malla, sin descartar Z.
local names={'esfera','elipsoide','cuartica'}
local report={}
for kind,name in ipairs(names) do
 local env=setmetatable({sample_rate=48000,step=0},{__index=_G})
 local play=setfenv(assert(loadfile('experiments/012-superficies-xyz/'..name..'.lua')),env)
 local pts={};local residual=0;local sums={0,0,0};local products={{0,0,0},{0,0,0},{0,0,0}}
 for i=0,1999 do
  env.step=i;local p=play();local angle=env.algebraic_xyz.angle
  local cp,sp=math.cos(.45),math.sin(.45)
  local yy,zz=cp*p[2]+sp*p[3],-sp*p[2]+cp*p[3]
  local x,y,z=math.cos(angle)*p[1]-math.sin(angle)*zz,yy,math.sin(angle)*p[1]+math.cos(angle)*zz
  local reference={x,y,z};local f
  if kind==1 then f=(x/.42)^2+(y/.42)^2+(z/.42)^2-1
  elseif kind==2 then f=(x/.55)^2+(y/.26)^2+(z/.38)^2-1
  else x,y,z=x/.45,y/.45,z/.45;f=x^4+3*y^4+6*z^4+.5*(x*x+y*y+z*z)-1 end
  residual=math.max(residual,math.abs(f));pts[#pts+1]=reference
  for a=1,3 do
   assert(p[a]==p[a] and math.abs(p[a])<.8)
   sums[a]=sums[a]+p[a]
   for b=1,3 do products[a][b]=products[a][b]+p[a]*p[b] end
  end
 end
 assert(residual<1e-10,'retorno fuera de F=0')
 local c=products;for a=1,3 do for b=1,3 do c[a][b]=c[a][b]/2000-sums[a]*sums[b]/4000000 end end
 local det=c[1][1]*(c[2][2]*c[3][3]-c[2][3]*c[3][2])-c[1][2]*(c[2][1]*c[3][3]-c[2][3]*c[3][1])+c[1][3]*(c[2][1]*c[3][2]-c[2][2]*c[3][1])
 assert(det>1e-6,'geometria aplanada')
 local file=assert(io.open('recordings/012-'..name..'.xyz.json','w'));file:write('[')
 for i,p in ipairs(pts) do if i>1 then file:write(',') end;file:write(string.format('[%.9g,%.9g,%.9g]',p[1],p[2],p[3])) end
 file:write(']\n');file:close()
 print(name,'residuo',residual,'det covarianza',det)
 report[#report+1]=string.format('"%s":{"residual":%.12g,"covariance_determinant":%.12g,"samples":2000}',name,residual,det)
 for _,rate in ipairs({44100,48000}) do
  local e=setmetatable({sample_rate=rate,step=0,slider_a=0,slider_b=.5,slider_c=.5},{__index=_G})
  local control=setfenv(assert(loadfile('experiments/012-superficies-xyz/'..name..'-control.lua')),e)
  local previous=nil;local maxdelta=0
  for i=0,rate*2 do
   e.step=i;if i==rate then e.slider_a=1;e.slider_c=1;e.slider_b=1 end
   local p=control();local raw=e.algebraic_xyz.raw
   local oldnorm,newnorm=0,0
   for a=1,3 do oldnorm=oldnorm+raw[a]^2;newnorm=newnorm+p[a]^2;if previous then maxdelta=math.max(maxdelta,math.abs(p[a]-previous[a])) end end
   assert(math.abs(oldnorm-newnorm)<1e-12);previous=p
  end
  assert(maxdelta<.15);e.step=0;control();assert(e.algebraic_xyz.phase<.002)
 end
end
local f=assert(io.open('experiments/012-superficies-xyz/validacion.json','w'));f:write('{'..table.concat(report,',')..'}\n');f:close()
