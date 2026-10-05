-- Estudio de un toro — 32 compases, 4/4, 96 BPM = 80 segundos.
-- Abrir como Lua en osci-render. No requiere MIDI; usa su propio secuenciador.
-- Para reiniciar: cambiar TAKE. Para live coding: BPM, ROOT_HZ y LEVEL.
local TAKE = 1
local BPM = 96
local ROOT_HZ = 55
local LEVEL = 0.75

-- Estado persistente: tablas y funciones se crean solo al iniciar una toma.
if not torus_study or torus_study.take ~= TAKE
    or torus_study.rate ~= sample_rate or step < torus_study.last_step then
    torus_study = {
        take = TAKE, rate = sample_rate, origin = step, last_step = step,
        phase = 0,
        melody = {0, 7, 12, 3, 10, 7, 3, 7},
        answer = {12, 15, 7, 10, 19, 15, 10, 7},
        roots = {0, -2, -5, -2},
        turns = {{2, 5}, {3, 7}, {2, 7}, {3, 8}}
    }
    function torus_study.smooth(a, b, x)
        local v = math.max(0, math.min(1, (x-a)/(b-a)))
        return v*v*(3-2*v)
    end
end
local s = torus_study
s.last_step = step
local time = (step-s.origin)/sample_rate
local beat = time * BPM/60
if beat >= 128 then
    return {0, 0, 0}
end
local bar = math.floor(beat/4)
local note = math.floor(beat*2)
local within = (beat*2)%1
local development = beat >= 32 and beat < 96
local climax = s.smooth(32, 64, beat) * (1-s.smooth(80, 112, beat))

-- Motivo menor relativo a ROOT_HZ; respuesta cada dos compases en desarrollo.
local motif = development and bar%4 >= 2 and s.answer or s.melody
local semitone = motif[note%8+1] + s.roots[math.floor(bar/4)%4+1]
-- Últimos cuatro compases: regreso a la tónica, con espacio entre frases.
if beat >= 112 then semitone = s.melody[note%8+1] end
local hz = ROOT_HZ * 2^(semitone/12)
local theta = s.phase
s.phase = (s.phase + 2*math.pi*hz/sample_rate) % (2*math.pi)

-- Envolvente suave: cero en cada cambio de nota/recorrido; sin salto de fase.
local attack = s.smooth(0, 0.035, within)
local release = 1-s.smooth(0.70, 1, within)
local accent = note%8 == 0 and 1 or (note%2 == 0 and 0.86 or 0.65)
local rest = (bar%4 == 3 and note%8 == 7) or (beat >= 120 and note%2 == 1)
local envelope = attack * release * accent
if rest then envelope = 0 end
local fade = s.smooth(0, 4, beat) * (1-s.smooth(120, 128, beat))

-- Cada punto previo a la rotación pertenece al toro implícito:
-- (x²+y²+z²+R²-r²)² - 4R²(x²+y²) = 0.
-- El par de enteros determina el recorrido; no sumamos voces XY independientes.
local p, q = 2, 3
if development then
    local turns = s.turns[math.floor(bar/2)%4+1]
    p, q = turns[1], turns[2]
end
local R = 0.36 + 0.035*math.sin(beat*math.pi/8)
local r = 0.10 + 0.055*climax + 0.015*math.sin(beat*math.pi/4)
local u = p*theta
local v = q*theta + 0.45*math.sin(beat*math.pi/16)
local x = (R+r*math.cos(v))*math.cos(u)
local y = (R+r*math.cos(v))*math.sin(u)
local z = r*math.sin(v)

-- Cámara ortográfica animada: rotaciones que preservan la norma.
local tilt = 0.8 + 0.45*math.sin(beat*math.pi/32)
local spin = beat*math.pi/24
local yy = y*math.cos(tilt)-z*math.sin(tilt)
local zz = y*math.sin(tilt)+z*math.cos(tilt)
local xx = x*math.cos(spin)+zz*math.sin(spin)
z = -x*math.sin(spin)+zz*math.cos(spin)
local gain = LEVEL*envelope*fade
return {gain*xx, gain*yy, gain*z}
