"""Contrato del importador: cambios de tempo, polifonia, running status y errores."""
from pathlib import Path
import struct
from import_repertoire_midi import parse

def midi(track,fmt=0):
    return b'MThd'+struct.pack('>IHHH',6,fmt,1,96)+b'MTrk'+struct.pack('>I',len(track))+track

track=(b'\x00\xff\x51\x03\x07\xa1\x20' # 120 bpm
       b'\x00\x90\x3c\x60\x00\x40\x40' # acorde y running status
       b'\x60\x80\x3c\x00' # 0.5 s
       b'\x00\xff\x51\x03\x0f\x42\x40' # 60 bpm
       b'\x60\x80\x40\x00\x00\xff\x2f\x00')
r=parse(midi(track))
assert [n['end_seconds'] for n in r['notes']]==[.5,1.5]
assert [n['velocity'] for n in r['notes']]==[96,64]
for bad in [b'bad',midi(b'\x00\x90\x3c\x50'),midi(b'\x00\x80\x3c\x00'),midi(track,2)]:
    try:parse(bad)
    except (ValueError,struct.error):pass
    else:raise AssertionError('MIDI invalido aceptado')
r=parse(Path('experiments/005-aire-de-bach/source/bach-air-score.mid').read_bytes())
assert len({n['track'] for n in r['notes']})==4
assert len(r['notes'])>400
print('OK: tempo, polifonia, velocidad, running status, errores y MIDI real de Bach',len(r['notes']))

# SEM-06: preservar eventos de duración cero sólo cuando se pide explícitamente.
zero=midi(b"\x00\x90\x3c\x60\x00\x80\x3c\x00\x00\xff\x2f\x00")
try:parse(zero)
except ValueError:pass
else:raise AssertionError("El modo estricto aceptó duración cero")
r=parse(zero,allow_zero_duration=True)
assert r["zero_duration_notes"]==1 and len(r["notes"])==1
assert r["notes"][0]["start_seconds"]==r["notes"][0]["end_seconds"]==0
assert "cero" in r["warnings"][0]
print("SEM-06 OK: modo estricto y preservación tolerante con advertencia")
