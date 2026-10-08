-- Render offline de presets nuevos. No abre dispositivo de audio.
local ffi=require('ffi')
local function uint(n,b) local s='';for _=1,b do s=s..string.char(n%256);n=math.floor(n/256) end;return s end
for _,name in ipairs({'bach','oblivion'}) do
 local folder=name=='bach' and '015-bach-voces-vivas' or '017-oblivion-voces-vivas'
 local rate,seconds=48000,20
 local env=setmetatable({sample_rate=rate,step=0},{__index=_G})
 local play=setfenv(assert(loadfile('experiments/'..folder..'/'..name..'.lua')),env)
 local data=ffi.new('int16_t[?]',rate*seconds*2);local peak,energy=0,0
 for i=0,rate*seconds-1 do
  env.step=i;local p=play()
  for a=1,2 do assert(p[a]==p[a] and math.abs(p[a])<.9);peak=math.max(peak,math.abs(p[a]));energy=energy+p[a]^2;data[2*i+a-1]=math.floor(32767*p[a]+.5) end
 end
 assert(energy>1)
 local size=rate*seconds*4;local f=assert(io.open('recordings/'..folder..'.wav','wb'))
 f:write('RIFF',uint(size+36,4),'WAVEfmt ',uint(16,4),uint(1,2),uint(2,2),uint(rate,4),uint(rate*4,4),uint(4,2),uint(16,2),'data',uint(size,4),ffi.string(data,size));f:close()
 print(name,'WAV 20 s',peak,math.sqrt(energy/(rate*seconds*2)))
end
