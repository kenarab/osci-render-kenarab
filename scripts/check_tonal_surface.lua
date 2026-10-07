-- CUA-01/03: retorno XYZ, cobertura y transporte; WAV exacto sin reproducción.
local ffi=require('ffi')
local function uint(n,b) local t='';for _=1,b do t=t..string.char(n%256);n=math.floor(n/256) end;return t end
local reports={}
for _,rate in ipairs({16000,44100,48000}) do
 local e=setmetatable({sample_rate=rate,step=0},{__index=_G})
 local play=setfenv(assert(loadfile('experiments/014-cuartica-tonal/cuartica.lua')),e)
 local trace=rate==48000 and assert(io.open('recordings/014-cuartica-tonal.xyz.csv','w')) or nil
 if trace then trace:write('x,y,z\n') end
 local pcm=ffi.new('int16_t[?]',rate*6*2)
 local residual,peak,delta=0,0,0;local bins={};local energy={0,0,0};local previous
 for i=0,rate*6-1 do
  e.step=i;local p=play();local s=e.tonal_xyz
  local cp,sp=math.cos(.45),math.sin(.45)
  local yy,zz=cp*p[2]+sp*p[3],-sp*p[2]+cp*p[3]
  local x,y,z=(math.cos(s.angle)*p[1]-math.sin(s.angle)*zz)/.42,yy/.42,(math.sin(s.angle)*p[1]+math.cos(s.angle)*zz)/.42
  residual=math.max(residual,math.abs(x^4+3*y^4+6*z^4+s.k*(x*x+y*y+z*z)-1))
  if i<rate then
   local az=math.atan2(y,x);local lat=math.asin(z/math.sqrt(x*x+y*y+z*z))
   local a=math.min(15,math.floor((az+math.pi)/(2*math.pi)*16))
   local b=math.min(7,math.floor((lat+math.pi/2)/math.pi*8))
   bins[a*8+b]=true
  end
  for a=1,3 do
   assert(p[a]==p[a] and math.abs(p[a])<.5)
   energy[a]=energy[a]+p[a]^2;peak=math.max(peak,math.abs(p[a]))
   if previous then delta=math.max(delta,math.abs(p[a]-previous[a])) end
  end
  for a=1,2 do pcm[2*i+a-1]=math.floor(p[a]*32767+.5) end
  if trace and i<rate/7 then trace:write(string.format('%.10g,%.10g,%.10g\n',p[1],p[2],p[3])) end
  previous=p
 end
 if trace then trace:close() end
 local count=0;for _ in pairs(bins) do count=count+1 end
 assert(count>=120 and residual<1e-10 and delta<.1)
 for _,v in ipairs(energy) do assert(v>rate*.01) end
 if rate==48000 then
  local size=rate*6*4;local f=assert(io.open('recordings/014-cuartica-tonal.wav','wb'))
  f:write('RIFF',uint(36+size,4),'WAVEfmt ',uint(16,4),uint(1,2),uint(2,2),uint(rate,4),uint(rate*4,4),uint(4,2),uint(16,2),'data',uint(size,4),ffi.string(pcm,size));f:close()
 end
 local live=setfenv(assert(loadfile('experiments/014-cuartica-tonal/cuartica-control.lua')),e)
 e.slider_a=0;e.slider_b=1;e.slider_c=1;e.slider_d=1
 e.step=e.step+1;live();local angle=e.tonal_xyz.angle
 for i=1,rate do e.step=e.step+1;live() end
 assert(e.tonal_xyz.angle==angle and e.tonal_xyz.hz>159.9 and e.tonal_xyz.k>.899 and e.tonal_xyz.cover>11.99)
 e.step=0;live();assert(e.tonal_xyz.u<.02)
 reports[#reports+1]=string.format('{"rate":%d,"peak":%.9g,"max_delta":%.9g,"residual":%.9g,"direction_bins":%d,"total_bins":128}',rate,peak,delta,residual,count)
 print(rate,'F=0',residual,'cobertura',count..'/128','pico',peak,'pausa/controles/reinicio OK')
end
local f=assert(io.open('experiments/014-cuartica-tonal/validacion.json','w'));f:write('[',table.concat(reports,',\n'),']\n');f:close()
