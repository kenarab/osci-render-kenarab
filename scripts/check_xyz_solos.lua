-- XYZ-01/02/04: comprobar el retorno, deshaciendo escala uniforme y giro.
for _,name in ipairs({'bach','oblivion'}) do
 for _,rate in ipairs({44100,48000}) do
  local e=setmetatable({sample_rate=rate,step=0,slider_a=.5,slider_b=0,slider_c=.5},{__index=_G})
  local play=setfenv(assert(loadfile('recordings/012-'..name..'-solo-xyz-control.lua')),e)
  local residual,count=0,0;local sums={0,0,0};local cov={{0,0,0},{0,0,0},{0,0,0}}
  for i=0,rate*42 do
   e.step=i
   if i==rate*10 then e.slider_b=1;e.slider_c=1 end
   local p=play();local s=e.solo_xyz
   for a=1,3 do assert(p[a]==p[a] and math.abs(p[a])<.5) end
   if not s.done and s.amplitude and s.amplitude>1e-5 then
    local c,sn=math.cos(s.angle),math.sin(s.angle)
    local x,y,z=(c*p[1]-sn*p[3])/s.amplitude,p[2]/s.amplitude,(sn*p[1]+c*p[3])/s.amplitude
    residual=math.max(residual,math.abs(x^4+3*y^4+6*z^4+s.k*(x*x+y*y+z*z)-1))
    count=count+1
    for a=1,3 do sums[a]=sums[a]+p[a];for b=1,3 do cov[a][b]=cov[a][b]+p[a]*p[b] end end
   end
  end
  assert(e.solo_xyz.done and count>rate and residual<1e-10)
  for a=1,3 do for b=1,3 do cov[a][b]=cov[a][b]/count-sums[a]*sums[b]/count^2 end end
  local c=cov
  local det=c[1][1]*(c[2][2]*c[3][3]-c[2][3]*c[3][2])-c[1][2]*(c[2][1]*c[3][3]-c[2][3]*c[3][1])+c[1][3]*(c[2][1]*c[3][2]-c[2][2]*c[3][1])
  assert(det>1e-8,'retorno aplanado')
  e.step=0;play();assert(not e.solo_xyz.done and e.solo_xyz.time<.001)
  e.slider_a=1;for i=1,rate do e.step=i;play() end;assert(e.solo_xyz.speed>1.49)
  print(name,rate,'residuo',residual,'det covarianza',det,'fin/reinicio/tempo OK')
 end
end
