"""XYZ-01: ejercicios independientes del repertorio y sin proyección precalculada."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
template=(ROOT/'library/algebraic_surfaces/xyz.lua.in').read_text()
for kind,name in enumerate(['esfera','elipsoide','cuartica'],1):
 for live in [False,True]:
  code=template.replace('@NAME@',name).replace('@KIND@',str(kind)).replace('@LIVE@',str(live).lower())
  (ROOT/'experiments/012-superficies-xyz'/f'{name}{"-control" if live else ""}.lua').write_text(code)
