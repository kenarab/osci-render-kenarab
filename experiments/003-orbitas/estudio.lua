-- Órbitas de un elipsoide — composición autónoma con sliders Lua A–E (0..1).
-- Incrementar TAKE para reiniciar. LOOP=true repite la pieza.
local TAKE = 1
local LOOP = false
local KEY = "orbitas"
local BASE_BPM, TOTAL_BEATS, METER = 72, 72, 3
local POWER = 2
if not algebra_score or algebra_score.key ~= KEY or algebra_score.take ~= TAKE
    or algebra_score.rate ~= sample_rate or step < algebra_score.last then
    algebra_score = {
        key=KEY, take=TAKE, rate=sample_rate, last=step, beat=0, phase=0,
        spin=0, hz=55, a=0, b=0, c=0, d=0, e=0,
        melody={0,7,12,4,7,14}, answer={16,12,7,14,19,12}, roots={0,-2,-5,-2}, done=false
    }
    function algebra_score.smooth(a,b,x)
        local t=math.max(0,math.min(1,(x-a)/(b-a)))
        return t*t*(3-2*t)
    end
    function algebra_score.control(old,value,alpha)
        value=type(value)=="number" and value==value and value or 0
        return old+alpha*(math.max(0,math.min(1,value))-old)
    end
end
local s=algebra_score
s.last=step
local dt=1/sample_rate
local alpha=1-math.exp(-dt/0.035)
-- Suavizado de potenciómetros: evita saltos de CC, incluidos tempo y cámara.
s.a=s.control(s.a,slider_a,alpha)
s.b=s.control(s.b,slider_b,alpha)
s.c=s.control(s.c,slider_c,alpha)
s.d=s.control(s.d,slider_d,alpha)
s.e=s.control(s.e,slider_e,alpha)
local beat=s.beat
if beat>=TOTAL_BEATS then
    if LOOP then s.beat=0; beat=0 else s.done=true; return {0,0,0} end
end
local tempo=BASE_BPM*(1+0.75*s.a)
s.beat=s.beat+tempo*dt/60
local bar=math.floor(beat/METER)
local note=math.floor(beat*2)
local within=(beat*2)%1
local development=beat>=TOTAL_BEATS/4 and beat<TOTAL_BEATS*3/4
local motif=development and bar%4>=2 and s.answer or s.melody
local semitone=motif[note%#motif+1]+s.roots[math.floor(bar/4)%4+1]
local target=55*2^((semitone+12*s.e)/12)
s.hz=s.hz+(1-math.exp(-dt/0.012))*(target-s.hz)
local theta=s.phase
s.phase=(theta+2*math.pi*s.hz*dt)%(2*math.pi)
s.spin=(s.spin+dt*(0.12+0.65*s.c))%(2*math.pi)
local intensity=s.smooth(TOTAL_BEATS/4,TOTAL_BEATS/2,beat)
    *(1-s.smooth(TOTAL_BEATS*0.70,TOTAL_BEATS*0.95,beat))
-- Recorrido continuo. Normalización radial a una superficie de grado 2 o 4.
local u=2*theta
local v=(0.65+0.30*intensity+0.30*s.b)*math.sin(3*theta)
local dx=math.cos(u)*math.cos(v)
local dy=math.sin(u)*math.cos(v)
local dz=math.sin(v)
local norm=(dx^POWER+dy^POWER+dz^POWER)^(1/POWER)
local aa=0.55
local bb=0.30+0.15*s.b+0.045*math.sin(beat*math.pi/12)
local cc=0.25+0.13*intensity+0.08*s.b
local x,y,z=aa*dx/norm,bb*dy/norm,cc*dz/norm
-- Ecuación antes de cámara: (x/aa)^POWER+(y/bb)^POWER+(z/cc)^POWER=1.
local tilt=0.65+0.28*math.sin(beat*math.pi/18)
local yy=y*math.cos(tilt)-z*math.sin(tilt)
local zz=y*math.sin(tilt)+z*math.cos(tilt)
local xx=x*math.cos(s.spin)+zz*math.sin(s.spin)
z=-x*math.sin(s.spin)+zz*math.cos(s.spin)
local pulse=s.smooth(0,0.06,within)*(1-s.smooth(0.5,1,within))
local floor=0.60+0.30*s.d
local accent=note%(METER*2)==0 and 1 or 0.8
local envelope=floor+(1-floor)*pulse*accent
local fade=s.smooth(0,3,beat)*(1-s.smooth(TOTAL_BEATS-6,TOTAL_BEATS,beat))
local gain=0.85*envelope*fade
return {gain*xx,gain*yy,gain*z}
