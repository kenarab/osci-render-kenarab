"""DP-02: genera un estudio de formantes independiente del repertorio."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'library/robot_voice/player.lua.in').read_text()
for live in [False,True]:
 (ROOT/'experiments/013-voz-robotica'/('vocales'+('-control' if live else '')+'.lua')).write_text(s.replace('@LIVE@',str(live).lower()))
