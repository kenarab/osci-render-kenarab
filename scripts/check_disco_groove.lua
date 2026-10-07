-- GRV-02: render real del preset, margen y reinicio.
local ffi=require('ffi')
local function uint(n,b) local t='';for _=1,b do t=t..string.char(n%256);n=math.floor(n/256) end;return t end
local reports={}
for _,rate in ipairs({16000,44100,48000}) do
 local e=setmetatable({sample_rate=rate,step=0},{__index=_G})
 local f=setfenv(assert(loadfile('experiments/013-voz-robotica/groove-disco.lua')),e)
 local count=rate*24;local pcm=ffi.new('int16_t[?]',count*2);local peak,energy=0,0
 for i=0,count-1 do
  e.step=i;local p=f()
  for a=1,3 do assert(p[a]==p[a] and math.abs(p[a])<.35);peak=math.max(peak,math.abs(p[a])) end
  for a=1,2 do pcm[2*i+a-1]=math.floor(p[a]*32767+.5);energy=energy+p[a]^2 end
 end
 assert(energy/count>.0001);e.step=0;f();assert(e.disco_voice.time<.001)
 if rate==48000 then
  local bytes=count*4;local out=assert(io.open('recordings/013-groove-disco.wav','wb'))
  out:write('RIFF',uint(36+bytes,4),'WAVEfmt ',uint(16,4),uint(1,2),uint(2,2),uint(rate,4),uint(rate*4,4),uint(4,2),uint(16,2),'data',uint(bytes,4),ffi.string(pcm,bytes));out:close()
 end
 local r=string.format('{"rate":%d,"seconds":24,"peak":%.9g,"rms_xy":%.9g}',rate,peak,math.sqrt(energy/(2*count)));reports[#reports+1]=r;print(r)
end
local out=assert(io.open('experiments/013-voz-robotica/groove-validacion.json','w'));out:write('['..table.concat(reports,',')..']\n');out:close()
