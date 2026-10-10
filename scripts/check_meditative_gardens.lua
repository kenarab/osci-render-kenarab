-- MED-02/04/06. Separar pruebas geométricas, DSP y aceptación perceptual.
local ffi=require('ffi');local folder='experiments/022-jardines-meditativos/'
local names={'claustro','jardin','memoria'};local reports={}
local function field(kind,x,y,z,a)
 if kind==3 then x=x/(.7+.6*a);return x*x*y*y+x*x*z*z+y*y*z*z-x*y*z end
 local q=x^4+y^4+z^4;local k=.5+(kind==1 and .46 or .44)*a
 return (kind==1 and ((x*x+y*y+z*z)^2-k*q) or (q-k*(x*x*y*y+y*y*z*z+z*z*x*x)))-1
end
for kind,name in ipairs(names) do
 for _,rate in ipairs({16000,44100,48000}) do
  for _,mode in ipairs({'xyz','sonido'}) do
   local env=setmetatable({sample_rate=rate,step=0,slider_b=0},{__index=_G})
   local play=setfenv(assert(loadfile(folder..name..'-'..mode..'-control.lua')),env)
   local peak,residual,energy=0,0,0;local cells={};local startAngle=.65
   for i=0,3*rate-1 do
    env.step=i;if i==rate then env.slider_a=1;env.slider_c=1;env.slider_f=1;env.slider_g=1;env.slider_h=1 end
    local p=play();local s=env.meditation
    assert(s.angle==startAngle,'B=0 no congela escena')
    for j=1,3 do assert(p[j]==p[j] and math.abs(p[j])<=.8);peak=math.max(peak,math.abs(p[j])) end
    if i>=rate*2 then energy=energy+p[1]^2+p[2]^2 end
    if mode=='xyz' and i>rate/2 then
     local x,y,z=p[1]/s.gain,p[2]/s.gain,p[3]/s.gain
     local cp,sp=math.cos(.45),math.sin(.45);local yy,zz=cp*y+sp*z,-sp*y+cp*z
     local c,sn=math.cos(s.angle),math.sin(s.angle);local xx,zzz=c*x-sn*zz,sn*x+c*zz
     local f=field(kind,xx,yy,zzz,s.shape);residual=math.max(residual,math.abs(f));assert(math.abs(f)<1e-9,'F!=0')
     cells[math.floor(s.u*32)..':'..math.floor(s.v*16)]=true
    elseif mode=='sonido' then assert(p[3]==0,'mezcla no es XYZ') end
   end
   local s=env.meditation;local count=0;for _ in pairs(cells) do count=count+1 end
   if mode=='xyz' then assert(count==512,'cobertura incompleta: '..count) end
   assert(energy/(2*rate)>.001,'sin señal')
   assert(s.shape>.99999 and s.hz>109.99 and s.bright>.99999,'CC no responde')
   local angle=s.angle;env.slider_b=1;env.slider_e=0
   for i=3*rate,6*rate-1 do env.step=i;local p=play();if i==6*rate-1 then assert(math.abs(p[1])<1e-8 and math.abs(p[2])<1e-8) end end
   assert(math.abs(s.angle-angle-.36)<1e-9,'giro no independiente')
   env.step=0;play();assert(env.meditation.time==1/rate,'reinicio')
   -- Preset independiente de todos los controles heredados.
   local a=setmetatable({sample_rate=rate,step=0},{__index=_G})
   local b=setmetatable({sample_rate=rate,step=0,slider_a=1,slider_b=1,slider_c=0,slider_d=0,slider_e=0,slider_f=1,slider_g=1,slider_h=1},{__index=_G})
   local pa=setfenv(assert(loadfile(folder..name..'-'..mode..'.lua')),a)
   local pb=setfenv(assert(loadfile(folder..name..'-'..mode..'.lua')),b)
   for i=0,99 do a.step=i;b.step=i;local x,y=pa(),pb();for j=1,3 do assert(x[j]==y[j]) end end
   reports[#reports+1]=string.format('{"id":"%s","mode":"%s","rate":%d,"peak":%.9f,"field_residual":%.12g,"angular_cells":%d,"host_acceptance":false}',name,mode,rate,peak,residual,count)
   print(name,mode,rate,'ecuación / cobertura / CC / silencio / reinicio OK');io.stdout:flush()
  end
 end
end
local f=assert(io.open(folder..'validacion.json','w'));f:write('[',table.concat(reports,',\n'),']\n');f:close()
local function uint(n,b) local s='';for _=1,b do s=s..string.char(n%256);n=math.floor(n/256) end;return s end
-- Tres extractos sin normalizar, separados X/Y, sin efectos globales del host.
for _,name in ipairs(names) do
 local rate,seconds=48000,36;local env=setmetatable({sample_rate=rate,step=0},{__index=_G})
 local play=setfenv(assert(loadfile(folder..name..'-sonido.lua')),env)
 local bytes=rate*seconds*4;local f=assert(io.open('recordings/022-'..name..'.wav','wb'))
 f:write('RIFF',uint(bytes+36,4),'WAVEfmt ',uint(16,4),uint(1,2),uint(2,2),uint(rate,4),uint(rate*4,4),uint(4,2),uint(16,2),'data',uint(bytes,4))
 local buffer=ffi.new('int16_t[?]',rate*2);local peak,energy=0,0
 for i=0,rate*seconds-1 do
  env.step=i;local p=play()
  for j=1,2 do assert(p[j]==p[j] and math.abs(p[j])<=.8);peak=math.max(peak,math.abs(p[j]));energy=energy+p[j]^2;buffer[(i%rate)*2+j-1]=math.floor(p[j]*32767+.5) end
  if i%rate==rate-1 then f:write(ffi.string(buffer,rate*4)) end
 end
 f:close();assert(energy/(rate*seconds*2)>.001);print(name,'WAV 36 s pico',peak,'RMS',math.sqrt(energy/(rate*seconds*2)));io.stdout:flush()
end
