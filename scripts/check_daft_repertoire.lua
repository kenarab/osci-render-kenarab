-- DFT-02…05: render íntegro del arreglo fuente y comprobación del fin.
local ffi=require('ffi')
local function uint(n,b) local s='';for _=1,b do s=s..string.char(n%256);n=math.floor(n/256) end;return s end
local report={}
local names={'something-about-us','instant-crush','lose-yourself-to-dance','giorgio-by-moroder'}
-- Detectar límites de compilación de LuaJIT antes de empezar renders largos.
for _,name in ipairs(names) do
 for _,suffix in ipairs({'','-control'}) do
  assert(loadfile('experiments/018-daft-repertorio/'..name..suffix..'.lua'))
 end
end
for _,name in ipairs(names) do
 local base='experiments/018-daft-repertorio/'..name
 local rate=48000;local e=setmetatable({sample_rate=rate,step=0},{__index=_G})
 local play=setfenv(assert(loadfile(base..'.lua')),e);play()
 local duration=e.daft_song.duration+.25;local frames=math.ceil(duration*rate);local size=frames*4
 e.daft_song=nil
 local f=assert(io.open('recordings/018-'..name..'.wav','wb'))
 f:write('RIFF',uint(size+36,4),'WAVEfmt ',uint(16,4),uint(1,2),uint(2,2),uint(rate,4),uint(rate*4,4),uint(4,2),uint(16,2),'data',uint(size,4))
 local chunk=ffi.new('int16_t[?]',rate*2);local at=0;local peak,energy=0,0
 for i=0,frames-1 do
  e.step=i;local p=play()
  for a=1,3 do assert(p[a]==p[a] and math.abs(p[a])<.601) end
  for a=1,2 do peak=math.max(peak,math.abs(p[a]));energy=energy+p[a]^2;chunk[at*2+a-1]=math.floor(32767*p[a]+.5) end
  at=at+1
  if at==rate then f:write(ffi.string(chunk,at*4));at=0 end
 end
 if at>0 then f:write(ffi.string(chunk,at*4)) end;f:close()
 assert(e.daft_song.done,'fin no alcanzado')
 assert(e.daft_song.processed==#e.daft_song.notes,'faltan eventos')
 assert(energy/(frames*2)>1e-8,'salida silenciosa')
 e.step=0;play();assert(not e.daft_song.done and e.daft_song.time<.001)
 local v=setmetatable({sample_rate=16000,step=0,slider_a=.875,slider_b=.125,slider_c=.375,slider_d=.65,slider_e=.5,slider_f=.7,slider_g=.25,slider_h=.5},{__index=_G})
 local live=setfenv(assert(loadfile(base..'-control.lua')),v)
 for i=0,16000*3-1 do
  v.step=i;if i==16000 then v.slider_a=.125;v.slider_b=.875;v.slider_c=.625;v.slider_g=1 end
  local p=live();for a=1,3 do assert(p[a]==p[a] and math.abs(p[a])<.601) end
 end
 assert(v.daft_song.mix[1][1]>.999 and math.abs(v.daft_song.time-3)<1e-8)
 report[#report+1]=string.format('"%s":{"seconds":%.6f,"notes":%d,"peak":%.9f,"rms":%.9f,"complete_source_playback":true,"host_acceptance":false}',name,duration,#e.daft_song.notes,peak,math.sqrt(energy/(frames*2)))
 print(name,'render íntegro / notas / fin / reinicio / controles 16k OK',peak);io.stdout:flush()
end
local f=assert(io.open('experiments/018-daft-repertorio/validacion.json','w'));f:write('{',table.concat(report,',\n'),'}\n');f:close()
