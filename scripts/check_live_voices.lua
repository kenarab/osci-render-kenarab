-- VIV-02…05: cambios sobre notas sostenidas, conservación de transporte y XYZ.
local function environment(rate) return setmetatable({sample_rate=rate,step=0,slider_a=.125,slider_b=.375,slider_c=.625,slider_d=.875,slider_e=.5,slider_f=.65,slider_g=0},{__index=_G}) end
local function residual(kind,x,y,z)
 if kind==1 then return (x*x+y*y+z*z+.62^2-.25^2)^2-4*.62^2*(x*x+y*y)
 elseif kind==2 then return x*x*y*y+x*x*z*z+y*y*z*z-x*y*z
 elseif kind==3 then return x*x+y*y-z*z
 else return ((x-.65)^2+y*y+z*z)*((x+.65)^2+y*y+z*z)-.68^4 end
end
local function original(p,angle,gain)
 local cp,sp=math.cos(.45),math.sin(.45);local yy,zz=cp*p[2]+sp*p[3],-sp*p[2]+cp*p[3]
 return (math.cos(angle)*p[1]-math.sin(angle)*zz)/gain,yy/gain,(math.sin(angle)*p[1]+math.cos(angle)*zz)/gain
end
for _,rate in ipairs({16000,44100,48000}) do
 for _,name in ipairs({'bach','oblivion'}) do
  local folder=name=='bach' and '015-bach-voces-vivas' or '017-oblivion-voces-vivas'
  local path='experiments/'..folder..'/'..name
  local e=environment(rate);local play=setfenv(assert(loadfile(path..'-control.lua')),e)
  local ref=environment(rate);local baseline=setfenv(assert(loadfile(path..'-control.lua')),ref)
  local peak,energy,difference=0,0,0
  for i=0,rate*5-1 do
   e.step=i;ref.step=i
   if i==rate then e.slider_a=.875 end
   if i==2*rate then e.slider_b=.875;e.slider_c=.125;e.slider_d=.375 end
   local p=play();local q=baseline();local s=e.live_voices
   assert(math.abs(s.time-ref.live_voices.time)<1e-12 and s.index==ref.live_voices.index)
   assert(#s.active==#ref.live_voices.active)
   if i<2*rate then
    for voice=2,#s.defaults do for bank=1,4 do assert(s.mix[voice][bank]==ref.live_voices.mix[voice][bank],'cambio en otra voz') end end
   end
   for j,v in ipairs(s.active) do assert(v.phase==ref.live_voices.active[j].phase,'reinicio de fase al cambiar banco') end
   for a=1,3 do assert(p[a]==p[a] and math.abs(p[a])<.9);peak=math.max(peak,math.abs(p[a]));energy=energy+p[a]^2;difference=difference+(p[a]-q[a])^2 end
  end
  assert(energy>1 and difference>1 and e.live_voices.max_hz<rate*.42)
  assert(e.live_voices.mix[1][4]>.999)
  -- El solapamiento MIDI no debe volver una transición un reinicio.
  local time=e.live_voices.time
  for i=1,100 do e.step=e.step+1;e.slider_a=i%2==0 and .249 or .251;play() end
  local choice=e.live_voices.selected[1]
  for i=1,100 do e.step=e.step+1;e.slider_a=i%2==0 and .249 or .251;play();assert(e.live_voices.selected[1]==choice) end
  assert(e.live_voices.time>time)
  e.live_voices.time=e.live_voices.duration;e.step=e.step+1;play();assert(e.live_voices.cycles==1 and e.live_voices.time<.001)
  e.step=0;play();assert(e.live_voices.cycles==0 and e.live_voices.time<.001)
  print(name,rate,'cambios sostenidos/fases/tempo/jitter/loop/reinicio OK','pico',peak)
  for voice=1,(name=='bach' and 4 or 3) do
   local v=environment(rate);local solo=setfenv(assert(loadfile(path..'-voz-'..voice..'-xyz-control.lua')),v)
   local maxres,count=0,0
   for i=0,rate*2-1 do
    v.step=i;local p=solo();local s=v.live_voices
    for a=1,3 do assert(p[a]==p[a] and math.abs(p[a])<.8) end
    if s.geometry_gain and s.geometry_gain>1e-5 and (p[1]~=0 or p[2]~=0 or p[3]~=0) then
     local x,y,z=original(p,s.angle,s.geometry_gain)
     maxres=math.max(maxres,math.abs(residual(s.geometry_kind,x,y,z)));count=count+1
    end
   end
   assert(count>100 and maxres<1e-10,'solo sin superficie')
  end
 end
 for kind,name in ipairs({'toro','roman','cono','cassini'}) do
  local e=environment(rate);local play=setfenv(assert(loadfile('experiments/016-superficies-diversas/'..name..'.lua')),e)
  local sum={0,0,0};local res=0
  for i=0,rate-1 do
   e.step=i;local p=play();local s=e.diverse_surface
   local x,y,z=original(p,s.angle,s.gain);res=math.max(res,math.abs(residual(kind,x,y,z)))
   for a=1,3 do assert(p[a]==p[a] and math.abs(p[a])<.8);sum[a]=sum[a]+p[a]^2 end
  end
  assert(res<1e-10);for _,v in ipairs(sum) do assert(v>rate*.001) end
  print(name,rate,'XYZ/F=0',res)
 end
end
