"""GRV-01: variante original, sin transcripcion ni samples de Daft Punk."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'library/robot_voice/player.lua.in').read_text().replace('@LIVE@','false').replace('robot_voice','disco_voice')
s=s.replace('local speed=1+4*s.a;', 'local speed=100/60*4;')
# Atenuar voz y aplicar patrón de acentos sin normalización ni clipping.
needle='x,y,z=.20*env*x,.20*env*y,.20*env*z'
assert s.count(needle)==1
s=s.replace(needle,'''local accents={1,0,.35,.7,0,.45,.85,0,.8,0,.4,.7,0,.65,0,.45}
local accent=accents[index%16+1]
x,y,z=.11*env*accent*x,.11*env*accent*y,.025*env*accent*z
-- Bombo analitico continuo: 105→48 Hz, ataque suave, sin ruido blanco.
local beat=s.time*100/60;local kickTime=(beat%1)*60/100
local kickPhase=2*math.pi*(48*kickTime+57*.025*(1-math.exp(-kickTime/.025)))
local kick=.045*math.sin(kickPhase)*math.exp(-kickTime/.10)*ease(kickTime/.003)
-- Bajo independiente, sincopado; mismas notas originales, no riff transcrito.
local bassHz=hz/2;local bp=p/2
-- Fase propia evita el salto al dividir una fase envuelta por dos.
s.bassPhase=((s.bassPhase or 0)+bassHz*dt)%1;bp=2*math.pi*s.bassPhase
local bassEnv=ease(fraction/(.008*speed))*ease((.78-fraction)/(.045*speed))
local bass=.065*accent*bassEnv*(math.sin(bp)+.20*math.sin(2*bp))/1.2
x=x+bass+kick;y=y+.7*bass+kick;z=z+.018*accent*bassEnv*math.cos(bp)
local fade=ease(s.time/.06);x,y,z=x*fade,y*fade,z*fade''')
# Patrón constante: no asignar una tabla por muestra.
s=s.replace('local accents={1,0,.35,.7,0,.45,.85,0,.8,0,.4,.7,0,.65,0,.45}', 'local accents=s.accents')
s=s.replace('widths={140,210,330}', 'widths={140,210,330},accents={1,0,.35,.7,0,.45,.85,0,.8,0,.4,.7,0,.65,0,.45}')
s='-- GRV-01: groove original a 100 BPM; no cover ni superficie algebraica.\n'+s
(ROOT/'experiments/013-voz-robotica/groove-disco.lua').write_text(s)
