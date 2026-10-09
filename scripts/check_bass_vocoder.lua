-- BVC-06: renders completos de estudios, controles, efectos y estímulos DSP.
local ffi=require('ffi')
local function read(path) local f=assert(io.open(path));local s=f:read('*a');f:close();return s end
local dsp=read('library/robot_voice/vocoder.lua')
local factory=assert(loadstring(dsp..'\nreturn {vocoder=bvc_vocoder,vocode=bvc_vocode,biquad=bvc_biquad,filter=bvc_filter}'))()
local function uint(n,b) local s='';for _=1,b do s=s..string.char(n%256);n=math.floor(n/256) end;return s end
local function wave(path,rate,seconds,play)
 local frames=math.ceil(seconds*rate);local f=assert(io.open(path,'wb'));local bytes=frames*4
 f:write('RIFF',uint(bytes+36,4),'WAVEfmt ',uint(16,4),uint(1,2),uint(2,2),uint(rate,4),uint(rate*4,4),uint(4,2),uint(16,2),'data',uint(bytes,4))
 local buf=ffi.new('int16_t[?]',rate*2);local at=0;local peak,energy=0,0
 for i=0,frames-1 do
  local p=play(i)
  for j=1,2 do assert(p[j]==p[j] and math.abs(p[j])<=.650001);peak=math.max(peak,math.abs(p[j]));energy=energy+p[j]^2;buf[at*2+j-1]=math.floor(32767*p[j]+.5) end
  at=at+1;if at==rate then f:write(ffi.string(buf,at*4));at=0 end
 end
 if at>0 then f:write(ffi.string(buf,at*4)) end;f:close();return peak,math.sqrt(energy/(frames*2))
end
local report={}
for _,rate in ipairs({16000,44100,48000}) do
 -- Una de las dos señales ausente: salida cero desde reposo.
 local noMod,noCarrier=factory.vocoder(rate),factory.vocoder(rate)
 for i=0,rate-1 do
  local tone=math.sin(2*math.pi*400*i/rate)
  assert(factory.vocode(noMod,tone,0)==0)
  assert(factory.vocode(noCarrier,0,tone)==0)
 end
 -- Ataque/cola: el análisis debe extinguirse después de retirar modulador.
 local v=factory.vocoder(rate)
 for i=0,rate-1 do factory.vocode(v,math.sin(i*.1),.4*math.sin(2*math.pi*400*i/rate)) end
 local before=0;for _,b in ipairs(v.bands) do before=math.max(before,b.env) end
 assert(before>.05)
 for i=0,rate-1 do factory.vocode(v,math.sin(i*.1),0) end
 for _,b in ipairs(v.bands) do assert(b.env<1e-5) end
 -- Efecto pegable: salida estable, wet=1 y modulador cero silencia portadora.
 local e=setmetatable({sample_rate=rate,step=0,x=.4,y=0,slider_a=1},{__index=_G})
 local fx=setfenv(assert(loadfile('experiments/020-bajos-vocoder/vocoder-effect.lua')),e)
 for i=0,rate-1 do e.step=i;e.x=.4*math.sin(i*.1);local p=fx();assert(p[1]==0 and p[2]==0) end
 e.step=0;e.y=.5;fx();assert(e.bvc_effect.last==0)
 for _,slug in ipairs({'lose-yourself-to-dance','giorgio-by-moroder'}) do
  local env=setmetatable({sample_rate=rate,step=0},{__index=_G})
  local live=setfenv(assert(loadfile('experiments/020-bajos-vocoder/'..slug..'-bass-control.lua')),env)
  local energy=0;local peak=0
  for i=0,rate*4-1 do
   env.step=i
   if i==rate then env.slider_a=1;env.slider_b=1;env.slider_c=1;env.slider_d=1;env.slider_i=1;env.slider_f=1 end
   if i==2*rate then env.slider_a=0;env.slider_h=1;env.slider_g=0 end
   if i>=2*rate then env.ext_x=.5*math.sin(2*math.pi*400*i/rate) end
   if i>=3*rate then env.ext_x=0 end
   local p=live();assert(p[1]==p[1] and math.abs(p[1])<=.650001);peak=math.max(peak,math.abs(p[1]))
   if i>=2*rate and i<3*rate then energy=energy+p[1]^2 end
   if i>=rate*3.8 then assert(math.abs(p[1])<1e-5,'modulador cero deja señal húmeda') end
  end
  assert(energy/rate>1e-8,'entrada externa no modula')
  env.step=0;live();assert(env.bass_voice.time<.001 and not env.bass_voice.done)
  report[#report+1]=string.format('{"id":"%s-control","rate":%d,"peak":%.9f,"external_modulator":true}',slug,rate,peak)
 end
 print(rate,'ausencia / cola / FX / controles / externo / reinicio OK');io.stdout:flush()
end
for _,slug in ipairs({'lose-yourself-to-dance','giorgio-by-moroder'}) do
 for _,suffix in ipairs({'bass','bass-vocoder'}) do
  local name=slug..'-'..suffix
  local env=setmetatable({sample_rate=48000,step=0,slider_a=1,slider_c=0},{__index=_G})
  local play=setfenv(assert(loadfile('experiments/020-bajos-vocoder/'..name..'.lua')),env)
  local peak,rms=wave('recordings/020-'..name..'.wav',48000,24.5,function(i) env.step=i;return play() end)
  assert(env.bass_voice.done and env.bass_voice.processed==#env.bass_voice.notes)
  assert(rms>.002,'preset demasiado silencioso')
  assert(env.bass_voice.wet==(suffix=='bass' and 0 or .85),'preset depende del slider')
  env.step=0;play();assert(not env.bass_voice.done)
  report[#report+1]=string.format('{"id":"%s","rate":48000,"peak":%.9f,"rms":%.9f,"notes":%d,"complete_excerpt":true,"host_acceptance":false}',name,peak,rms,#env.bass_voice.notes)
  print(name,'render / fin / notas / preset / reinicio OK',peak,rms);io.stdout:flush()
 end
end
-- Para análisis espectral independiente: misma portadora de ruido determinista.
for _,modHz in ipairs({400,2400}) do
 local rate=48000;local state=factory.vocoder(rate);local seed=12345
 wave('recordings/020-test-mod-'..modHz..'.wav',rate,2,function(i)
  seed=(seed*16807)%2147483647
  local carrier=.4*(seed/2147483647*2-1)
  local signal=factory.vocode(state,carrier,.5*math.sin(2*math.pi*modHz*i/rate))*.2
  return {signal,signal}
 end)
end
local f=assert(io.open('experiments/020-bajos-vocoder/validacion-lua.json','w'));f:write('[',table.concat(report,',\n'),']\n');f:close()
