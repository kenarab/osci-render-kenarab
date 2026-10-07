-- INS-06: continuidad del transporte, no aceptación auditiva ni del host.
for _,base in ipairs({'011-oblivion','012-oblivion-solo-xyz'}) do
 for _,rate in ipairs({16000,44100,48000}) do
  local key=base:find('011') and 'surface_player' or 'solo_xyz'
  local e=setmetatable({sample_rate=rate,step=0,slider_a=.5,slider_b=0,slider_c=.5,slider_d=.5,slider_e=.4},{__index=_G})
  local loop=setfenv(assert(loadfile('recordings/'..base..'-loop.lua')),e)
  loop();local duration=e[key].duration or 40
  if key=='solo_xyz' then assert(math.abs(e[key].notes[1][1]-.25)<1e-9,'entrada tardia') end
  e.step=0; e[key]=nil
  local energy={0,0,0};local peak=0;local boundary=0;local prev={0,0,0}
  for i=0,math.floor(rate*(2*duration+3))-1 do
   e.step=i;local p=loop();local cycle=math.floor(i/rate/duration)+1
   for a=1,3 do
    assert(p[a]==p[a] and math.abs(p[a])<.98)
    energy[cycle]=energy[cycle]+p[a]^2;peak=math.max(peak,math.abs(p[a]))
    if math.abs(i/rate-duration)<.002 or math.abs(i/rate-2*duration)<.002 then boundary=math.max(boundary,math.abs(p[a]-prev[a])) end
   end
   prev=p
  end
  assert(e[key].cycles==2 and energy[1]>1 and energy[2]>1 and energy[3]>1)
  assert(boundary<.005,'discontinuidad en limite del fragmento')
  local once=setfenv(assert(loadfile('recordings/'..base..'.lua')),e)
  e.step=e.step+1;once();assert(e[key].time<.001 and not e[key].loop,'cambio de variante sin reset')
  -- Saltar el reloj permite comprobar fin sin render redundante.
  e[key].time=duration;local p=once();assert(e[key].done and p[1]==0 and p[2]==0 and p[3]==0)
  e.step=0;once();assert(not e[key].done and e[key].time<.001)
  local live=setfenv(assert(loadfile('recordings/'..base..'-loop-control.lua')),e)
  e.step=1;live();assert(e[key].live and e[key].loop and e[key].time<.001)
  print(base,rate,'2 repeticiones/fin/reinicio/modos OK','peak',peak,'salto limite',boundary)
 end
end
