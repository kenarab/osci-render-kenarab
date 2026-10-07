"""CUA-01/02: ejercicio de biblioteca independiente del repertorio."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
template = (ROOT / 'library/algebraic_surfaces/tonal_xyz.lua.in').read_text()
for live in (False, True):
    name = 'cuartica' + ('-control' if live else '') + '.lua'
    (ROOT / 'experiments/014-cuartica-tonal' / name).write_text(
        template.replace('@LIVE@', str(live).lower()))
