-- INS-01/04: renders exactos de Lua y pruebas de geometria/cambio de bancos.
local ffi=require('ffi')
local function uint(n,b) local t='';for _=1,b do t=t..string.char(n%256);n=math.floor(n/256) end;return t end
local function run(path,prefix,seconds,controls,rate)
 local file=assert(io.open(path));local code=file:read('*a');file:close()
 local e=setmetatable({sample_rate=rate,step=0,slider_a=0,slider_b=.33,slider_c=1,slider_d=.5,slider_e=.4},{__index=_G})
 local play=setfenv(assert(loadstring(code)),e);local pcm=ffi.new('int16_t[?]',rate*seconds*2)
 local peak,delta,energy,maxactive=0,0,0,0;local prev={0,0,0}
 for i=0,rate*seconds-1 do
  e.step=i
  if controls then
   local n=math.floor(i/rate/3)%4;e.slider_a=n/3;e.slider_b=(3-n)/3;e.slider_c=n/3
  end
  local p=play()
  for axis=1,3 do assert(p[axis]==p[axis] and math.abs(p[axis])<.98);peak=math.max(peak,math.abs(p[axis]));delta=math.max(delta,math.abs(p[axis]-prev[axis])) end
  if i>0 then assert(delta<.25,'salto de señal') end
  if e.surface_scan then
   local r=e.surface_scan.raw;local a=e.surface_scan.radii
   assert(math.abs((r[1]/a[1])^2+(r[2]/a[2])^2+(r[3]/a[3])^2-1)<1e-12)
  end
  if e.surface_player then
   maxactive=math.max(maxactive,#e.surface_player.active)
   for _,weights in ipairs(e.surface_player.mix) do local sum=0;for _,w in ipairs(weights) do sum=sum+w end;assert(math.abs(sum-1)<1e-10) end
  end
  for a=1,2 do pcm[2*i+a-1]=math.floor(p[a]*32767+.5);energy=energy+p[a]^2 end
  prev=p
 end
 if e.surface_player and not controls then assert(e.surface_player.done and prev[1]==0 and maxactive>3) end
 e.step=0;play();assert(not e.surface_player or e.surface_player.time<.01)
 if prefix then
  local size=rate*seconds*4;local f=assert(io.open(prefix..'.wav','wb'))
  f:write('RIFF',uint(36+size,4),'WAVEfmt ',uint(16,4),uint(1,2),uint(2,2),uint(rate,4),uint(rate*4,4),uint(4,2),uint(16,2),'data',uint(size,4),ffi.string(pcm,size));f:close()
  local report=assert(io.open(prefix..'.json','w'));report:write(string.format('{"seconds":%d,"rate":%d,"peak":%.9f,"rms":%.9f,"max_delta":%.9f,"max_active":%d}\n',seconds,rate,peak,math.sqrt(energy/(2*rate*seconds)),delta,maxactive));report:close()
 end
 print(path,rate,peak,delta,maxactive,'OK')
end
for _,name in ipairs({'esfera','elipsoide'}) do
 run('experiments/010-superficies-legibles/'..name..'.lua','recordings/010-'..name,10,false,48000)
end
run('recordings/011-oblivion.lua','recordings/011-oblivion',41,false,48000)
for _,rate in ipairs({44100,48000}) do run('recordings/011-oblivion-control.lua',nil,12,true,rate) end
