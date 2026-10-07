-- DP-03/04: limites, variacion timbrica, controles y reinicio; WAV XY + XYZ crudo.
local ffi=require('ffi')
local function uint(n,b) local t='';for _=1,b do t=t..string.char(n%256);n=math.floor(n/256) end;return t end
local reports={}
for _,rate in ipairs({16000,44100,48000}) do
 for _,live in ipairs({false,true}) do
  local e=setmetatable({sample_rate=rate,step=0,slider_a=.25,slider_b=.5,slider_c=.5,slider_d=.3},{__index=_G})
  local f=setfenv(assert(loadfile('experiments/013-voz-robotica/vocales'..(live and '-control' or '')..'.lua')),e)
  local seconds=16;local pcm=ffi.new('int16_t[?]',rate*seconds*2);local raw=ffi.new('float[?]',rate*seconds*3)
  local peak,energy,delta=0,0,0;local previous={0,0,0};local axisEnergy={0,0,0}
  for i=0,rate*seconds-1 do
   e.step=i
   if live and i==rate*4 then e.slider_a=1;e.slider_b=1;e.slider_c=1;e.slider_d=0 end
   if live and i==rate*8 then e.slider_a=0;e.slider_b=0;e.slider_c=0;e.slider_d=1 end
   local p=f()
   for a=1,3 do assert(p[a]==p[a] and math.abs(p[a])<.3);peak=math.max(peak,math.abs(p[a]));delta=math.max(delta,math.abs(p[a]-previous[a]));axisEnergy[a]=axisEnergy[a]+p[a]^2;raw[3*i+a-1]=p[a] end
   for a=1,2 do pcm[2*i+a-1]=math.floor(p[a]*32767+.5);energy=energy+p[a]^2 end
   previous=p
  end
  for a=1,3 do assert(axisEnergy[a]>1) end
  e.step=0;f();assert(e.robot_voice.time<.001)
  if rate==48000 and not live then
   local bytes=rate*seconds*4;local out=assert(io.open('recordings/013-vocales.wav','wb'))
   out:write('RIFF',uint(36+bytes,4),'WAVEfmt ',uint(16,4),uint(1,2),uint(2,2),uint(rate,4),uint(rate*4,4),uint(4,2),uint(16,2),'data',uint(bytes,4),ffi.string(pcm,bytes));out:close()
   out=assert(io.open('recordings/013-vocales.xyz.f32','wb'));out:write(ffi.string(raw,rate*seconds*3*4));out:close()
  end
  local r=string.format('{"rate":%d,"controls":%s,"seconds":%d,"peak":%.9g,"rms_xy":%.9g,"max_delta":%.9g}',rate,tostring(live),seconds,peak,math.sqrt(energy/(2*rate*seconds)),delta)
  reports[#reports+1]=r;print(r)
 end
end
local o=assert(io.open('experiments/013-voz-robotica/validacion.json','w'));o:write('['..table.concat(reports,',')..']\n');o:close()
