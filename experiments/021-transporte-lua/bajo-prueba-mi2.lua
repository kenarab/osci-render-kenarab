-- TRN-05: tono Mi2 (82.406889 Hz), ciclos continuos de ocho segundos, sin MIDI/sliders.
-- Sólo sirve para comparar salida y registro: no es una pieza ni superficie XYZ.
if not bass_probe or bass_probe.rate~=sample_rate or step<bass_probe.last then
 bass_probe={rate=sample_rate,last=step,time=0,frames=0,p=0}
end
local s=bass_probe;s.last=step;local dt=1/sample_rate
local t=(s.frames/sample_rate)%8;s.frames=s.frames+1;s.time=t
s.p=(s.p+82.4068892282*dt)%1
local p=2*math.pi*s.p
local tone=(math.sin(p)+.35*math.sin(2*p)+.18*math.sin(3*p)+.1*math.sin(4*p)+.05*math.sin(5*p))/1.68
local function ease(v) v=math.max(0,math.min(1,v));return v*v*(3-2*v) end
local output=.2*tone*ease(t/.04)*ease((8-t)/.08)
return {output,output,0}
