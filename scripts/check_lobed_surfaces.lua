-- LOB-02/03/05: ecuación real tras cambios, XYZ, cobertura, controles y pausa.
local reports={}
for kind,name in ipairs({'seis-lobulos','ocho-lobulos'}) do
 local maximum=kind==1 and .96 or .94
 for _,rate in ipairs({16000,44100,48000}) do
  local env=setmetatable({step=0,sample_rate=rate,slider_b=0},{__index=_G})
  local play=setfenv(assert(loadfile('experiments/019-cuarticas-vivas/'..name..'-control.lua')),env)
  local residual,peak=0,0;local energy={0,0,0};local cells={};local initialAngle=.65
  for i=0,2*rate-1 do
   env.step=i
   if i==rate then env.slider_a=1;env.slider_c=.7;env.slider_d=.8;env.slider_e=1 end
   local p=play();local s=env.lobed_surface
   assert(s.angle==initialAngle,'pausa cambia la cámara')
   assert(s.a>=0 and s.a<=maximum,'parámetro fuera de rango')
   for j=1,3 do assert(p[j]==p[j] and math.abs(p[j])<=.800001);peak=math.max(peak,math.abs(p[j]));energy[j]=energy[j]+p[j]^2 end
   -- Deshacer escala, inclinación y giro; no verificar únicamente s.raw.
   local x,y,z=p[1]/s.gain,p[2]/s.gain,p[3]/s.gain
   local cp,sp=math.cos(.45),math.sin(.45);local yy,zz=cp*y+sp*z,-sp*y+cp*z
   local c,sn=math.cos(s.angle),math.sin(s.angle);local xx,zzz=c*x-sn*zz,sn*x+c*zz
   local x2,y2,z2=xx*xx,yy*yy,zzz*zzz;local q=x2*x2+y2*y2+z2*z2
   local f=kind==1 and ((x2+y2+z2)^2-s.a*q-1) or (q-s.a*(x2*y2+y2*z2+z2*x2)-1)
   residual=math.max(residual,math.abs(f));assert(math.abs(f)<1e-10)
   if i<rate then cells[math.floor(s.u*32)..':'..math.floor(s.v*16)]=true end
  end
  local count=0;for _ in pairs(cells) do count=count+1 end
  assert(count==512,'cobertura angular incompleta: '..count)
  for j=1,3 do assert(energy[j]/(2*rate)>.005,'eje silencioso') end
  assert(math.abs(env.lobed_surface.a-maximum)<1e-5)
  assert(env.lobed_surface.hz>131 and env.lobed_surface.cover>9.3)
  local paused=env.lobed_surface.angle;env.slider_b=1
  for i=2*rate,3*rate-1 do env.step=i;play() end
  assert(math.abs(env.lobed_surface.angle-paused-.2)<1e-10)
  env.step=0;play();assert(env.lobed_surface.u<.02 and env.lobed_surface.a<maximum)
  -- El preset debe ignorar controles heredados; comparar dos estados idénticos.
  local preset=assert(loadfile('experiments/019-cuarticas-vivas/'..name..'.lua'))
  local a=setmetatable({step=0,sample_rate=rate},{__index=_G})
  local b=setmetatable({step=0,sample_rate=rate,slider_a=1,slider_b=1,slider_c=0,slider_d=0,slider_e=0},{__index=_G})
  local pa=setfenv(preset,a);local pb=setfenv(assert(loadfile('experiments/019-cuarticas-vivas/'..name..'.lua')),b)
  for i=0,99 do a.step=i;b.step=i;local x,y=pa(),pb();for j=1,3 do assert(x[j]==y[j]) end end
  reports[#reports+1]=string.format('{"id":"%s","rate":%d,"residual":%.12g,"peak":%.9f,"angular_cells":%d,"host_acceptance":false}',name,rate,residual,peak,count)
  print(name,rate,'ecuación / cobertura / controles / pausa / reinicio OK',residual,peak)
 end
end
local f=assert(io.open('experiments/019-cuarticas-vivas/validacion-lua.json','w'));f:write('[',table.concat(reports,',\n'),']\n');f:close()
