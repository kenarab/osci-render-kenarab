-- TORO SONORO / barrido de una superficie, sin partitura ni notas MIDI.
-- Generado por scripts/build_surface_instrument.py. Ver README.md.
local VARIANTE = "cuerpo"
local USAR_SLIDERS = false -- true: A movimiento, B barrido, C forma, D calidez, E nivel
local TAKE = 1 -- incrementar para reiniciar
if not surface_voice or surface_voice.take ~= TAKE or surface_voice.voice ~= VARIANTE
    or surface_voice.rate ~= sample_rate or step < surface_voice.last then
    local warmth = VARIANTE == "suave" and 0.90 or (VARIANTE == "cuerpo" and 0.15 or 0.55)
    surface_voice = {
        take=TAKE, voice=VARIANTE, rate=sample_rate, last=step,
        phase=0, spin=0, seconds=0, a=0.25, b=0.5, c=0.5, d=warmth, e=0.35,
        defaults={0.25,0.5,0.5,warmth,0.35},
        alpha=1-math.exp(-1/(sample_rate*0.08))
    }
    function surface_voice.control(old,value,k)
        -- Un dato inválido conserva el último estado válido, nunca inyecta NaN.
        if type(value)~="number" or value~=value or math.abs(value)==math.huge then return old end
        return old+k*(math.max(0,math.min(1,value))-old)
    end
end
local s=surface_voice
s.last=step
local defaults=s.defaults
local k=s.alpha
local a,b,c,d,e
if USAR_SLIDERS then
    a,b,c,d,e=slider_a,slider_b,slider_c,slider_d,slider_e
else
    a,b,c,d,e=defaults[1],defaults[2],defaults[3],defaults[4],defaults[5]
end
s.a=s.control(s.a,a,k)
s.b=s.control(s.b,b,k)
s.c=s.control(s.c,c,k)
s.d=s.control(s.d,d,k)
s.e=s.control(s.e,e,k)
local dt=1/sample_rate
local theta=s.phase
local hz=20*6^s.b
-- Dos relojes independientes. No usar tiempo * velocidad actual.
s.phase=(theta+2*math.pi*hz*dt)%(2*math.pi)
s.spin=(s.spin+0.20*s.a*s.a*dt)%(2*math.pi)
s.seconds=s.seconds+dt

-- Toro F=(x²+y²+z²+R²-r²)²-4R²(x²+y²)=0.
-- Una vuelta azimutal y 24 vueltas poloidales: raster cerrado a resolución finita.
-- La superficie se conserva además como malla con caras, generada fuera del audio.
local R,r=0.62,0.18+0.12*s.c
local cu,su=math.cos(theta),math.sin(theta)
local cv,sv=math.cos(24*theta),math.sin(24*theta)
local gx,gy,gz=(R+r*cv)*cu,(R+r*cv)*su,r*sv

-- Los términos del tubo ocupan armónicos 23,24,25; el círculo central, el 1.
-- Atenuarlos por igual equivale exactamente a reducir el radio menor del toro.
-- No hay un oscilador musical independiente ni filtrado de una pista externa.
local warmth=s.d
if VARIANTE=="aire" then warmth=math.max(0,math.min(1,warmth+0.20*math.sin(40*s.spin))) end
local partial_gain=1-0.75*warmth
local fx,fy,fz=(R+r*partial_gain*cv)*cu,(R+r*partial_gain*cv)*su,r*partial_gain*sv
local tilt=0.90
local ct,st=math.cos(tilt),math.sin(tilt)
local cs,ss=math.cos(s.spin),math.sin(s.spin)
local raw_y,raw_z=gy*ct-gz*st,gy*st+gz*ct
local out_y,out_z=fy*ct-fz*st,fy*st+fz*ct
local raw_x=gx*cs+raw_z*ss
local out_x=fx*cs+out_z*ss
-- Ataque sin clic; E se suaviza para silenciar y liberar el sonido.
local t=math.min(1,s.seconds/0.30)
local gain=0.75*s.e*t*t*(3-2*t)
-- Diagnóstico para el render/verificador externo: no modifica la salida del host.
s.gx,s.gy,s.gz=gx,gy,gz
s.rawx,s.rawy=raw_x*gain,raw_y*gain
s.radius,s.effective_radius,s.hz,s.gain=r,r*partial_gain,hz,gain
return {out_x*gain,out_y*gain,0}
