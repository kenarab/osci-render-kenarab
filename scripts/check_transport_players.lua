-- TRN-03/04/06: pruebas independientes de índice/notas, audio y comandos.
local ffi=require('ffi')
local files={}
for name in io.popen('find experiments/021-transporte-lua -name "*-transport.lua"'):lines() do
 assert(loadfile(name));files[#files+1]=name
end
table.sort(files);assert(#files==14)
local reports={}
for _,file in ipairs(arg[1]=='--probe-only' and {} or files) do
 for _,rate in ipairs({16000,44100,48000}) do
  local env=setmetatable({step=0,sample_rate=rate,slider_j=0,slider_k=0,slider_l=0},{__index=_G})
  local play=setfenv(assert(loadfile(file)),env);local frame=0;local peak=0;local initialEnergy=0
  local function state() return env.bass_voice or env.daft_song end
  local function call()
   env.step=frame;frame=frame+1
   local before=state() and state().transport and state().transport.seeks or 0
   local p=play();local s=state()
   for j=1,3 do assert(p[j]==p[j] and math.abs(p[j])<=.650001);peak=math.max(peak,math.abs(p[j])) end
   if s.transport.seeks>before then assert(p[1]==0 and p[2]==0,'salto sin fundido a cero') end
   return p,s
  end
  local function run(seconds) for _=1,math.ceil(seconds*rate) do call() end end
  for _=1,math.ceil(.1*rate) do local p=call();initialEnergy=initialEnergy+p[1]^2 end
  local s=state();assert(s.time>.09 and s.time<.11)
  env.slider_k=1;run(.04);local paused=s.time
  for _=1,rate/10 do local p=call();assert(p[1]==0 and p[2]==0) end
  assert(s.time==paused,'pausa no congela reloj')
  -- Destinos en notas reales y cruce de nota sostenida; comparar contra scan completo.
  for _,fraction in ipairs({.15,.5,.85}) do
   local note=s.notes[math.max(1,math.floor(#s.notes*fraction))]
   local target=(note[1]+note[2])/2
   env.slider_j=target/s.duration;call()
   assert(math.abs(s.time-target)<1e-8)
   local expected={};local processed=0
   for i,n in ipairs(s.notes) do
    if n[1]<=target then processed=i end
    if n[1]<=target and target<n[2] then expected[#expected+1]=n end
   end
   assert(s.index==processed+1 and s.processed==processed,'índice incorrecto')
   assert(#s.active==#expected and #expected>0,'sostenidas omitidas')
   for i,n in ipairs(expected) do assert((env.bass_voice and s.active[i] or s.active[i].n)==n) end
  end
  local position=s.time;env.slider_k=0;run(.06);assert(math.abs(s.time-position-.06)<1e-8)
  -- Posición J estable y jitter: el reproductor continúa, no vuelve al destino.
  local requests=s.transport.seeks;local j=env.slider_j
  for i=1,rate/10 do env.slider_j=j+(i%2==0 and 1e-5 or -1e-5);call() end
  assert(s.transport.seeks==requests and s.time>position+.15)
  env.slider_j=j
  -- Último destino gana durante el fundido de salida.
  env.slider_j=.7;call();env.slider_j=.2;call();run(.04)
  assert(math.abs(s.transport.lastTarget-s.duration*.2)<1e-8)
  assert(s.transport.seeks==requests+1)
  -- Rewind por flanco, no reinicio cada muestra mientras L queda alto.
  env.slider_l=1;run(.04);assert(s.transport.lastTarget==0 and s.time<.05)
  requests=s.transport.seeks;run(.04);assert(s.transport.seeks==requests and s.time>.04)
  env.slider_l=0;call()
  -- Fin, seek posterior y reinicio con slider J actual.
  env.slider_j=1;run(.3);assert(s.done)
  env.slider_j=.3;run(.05);assert(not s.done and math.abs(s.transport.lastTarget-s.duration*.3)<1e-8)
  env.step=0;frame=1;play();s=state();assert(math.abs(s.time-s.duration*.3-1/rate)<1e-8)
  reports[#reports+1]=string.format('{"file":"%s","rate":%d,"peak":%.9f,"initial_rms":%.9f,"seek_pause_rewind":true,"host_acceptance":false}',file:match('[^/]+$'),rate,peak,math.sqrt(initialEnergy/math.ceil(.1*rate)))
  print(file:match('[^/]+$'),rate,'saltos / sostenidas / pausa / jitter / rewind / fin OK');io.stdout:flush()
 end
 collectgarbage()
end
local function uint(n,b) local s='';for _=1,b do s=s..string.char(n%256);n=math.floor(n/256) end;return s end
local rate=48000;local frames=math.ceil(8.2*rate);local bytes=frames*4
local f=assert(io.open('recordings/021-bajo-prueba-mi2.wav','wb'))
f:write('RIFF',uint(bytes+36,4),'WAVEfmt ',uint(16,4),uint(1,2),uint(2,2),uint(rate,4),uint(rate*4,4),uint(4,2),uint(16,2),'data',uint(bytes,4))
local env=setmetatable({step=0,sample_rate=rate,slider_f=0,slider_k=1,slider_h=1},{__index=_G})
local play=setfenv(assert(loadfile('experiments/021-transporte-lua/bajo-prueba-mi2.lua')),env)
local buffer=ffi.new('int16_t[?]',rate*2);local at=0;local energy,afterLoop=0,0
for i=0,frames-1 do
 env.step=i;local p=play();assert(math.abs(p[1])<=.2 and p[1]==p[2])
 if i==rate*8 then assert(p[1]==0,'borde del loop sin fundido') end
 if i>=rate*8 then afterLoop=afterLoop+p[1]^2 end
 if i<rate then energy=energy+p[1]^2 end
 for j=1,2 do buffer[at*2+j-1]=math.floor(32767*p[j]+.5) end
 at=at+1;if at==rate then f:write(ffi.string(buffer,at*4));at=0 end
end
if at>0 then f:write(ffi.string(buffer,at*4)) end;f:close()
assert(math.sqrt(energy/rate)>.07,'calibración silenciosa')
assert(math.sqrt(afterLoop/(frames-8*rate))>.05,'calibración no continúa')
if #reports>0 then
 local f=assert(io.open('experiments/021-transporte-lua/validacion.json','w'));f:write('[',table.concat(reports,',\n'),']\n');f:close()
end
local f=assert(io.open('experiments/021-transporte-lua/calibracion.json','w'))
f:write(string.format('{"rate":48000,"frequency":82.4068892282,"loop_seconds":8,"first_second_rms":%.9f,"after_loop_rms":%.9f,"host_acceptance":false}\n',math.sqrt(energy/rate),math.sqrt(afterLoop/(frames-8*rate))));f:close()
print('Calibración Mi2: primer segundo / ignora sliders / loop continuo OK')
