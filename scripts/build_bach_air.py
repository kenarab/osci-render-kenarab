"""Importa el MIDI Mutopia 242, despliega las repeticiones y genera Lua autónomo.

No requiere paquetes Python. Las notas derivadas conservan CC BY-SA 3.0.
"""
import hashlib
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "experiments/005-aire-de-bach"


def midi_notes(data):
    assert data[:4] == b"MThd" and int.from_bytes(data[4:8], "big") == 6
    fmt, track_count, division = struct.unpack(">HHH", data[8:14])
    assert fmt == 1 and 0 < division < 32768
    tracks, offset = [], 14
    for _ in range(track_count):
        assert data[offset:offset+4] == b"MTrk"
        size = int.from_bytes(data[offset+4:offset+8], "big")
        track = data[offset+8:offset+8+size]
        assert len(track) == size
        offset += 8+size
        pos, tick, running = 0, 0, None
        active, notes = {}, []

        def vlq():
            nonlocal pos
            value = 0
            for _ in range(4):
                byte = track[pos]; pos += 1
                value = (value << 7) | (byte & 127)
                if byte < 128:
                    return value
            raise ValueError("VLQ inválido")

        while pos < len(track):
            tick += vlq()
            status = track[pos]
            if status >= 128:
                pos += 1
                if status < 240:
                    running = status
            else:
                assert running is not None
                status = running
            if status == 255:
                pos += 1  # tipo de metadato; se preservan alturas/duraciones, no tempo
                length = vlq(); pos += length
            elif status in (240, 247):
                length = vlq(); pos += length
                running = None
            else:
                kind, channel = status >> 4, status & 15
                assert 8 <= kind <= 14
                a = track[pos]; pos += 1
                b = None
                if kind not in (12, 13):
                    b = track[pos]; pos += 1
                key = (channel, a)
                if kind == 9 and b:
                    assert key not in active
                    active[key] = tick
                elif kind == 8 or (kind == 9 and b == 0):
                    start = active.pop(key)
                    assert tick > start
                    notes.append([start/division, tick/division, a])
        assert not active
        if notes:
            tracks.append(sorted(notes))
    assert offset == len(data)
    return tracks


def main():
    midi = (DEST / "source/bach-air-score.mid").read_bytes()
    tracks = midi_notes(midi)
    assert len(tracks) == 4
    assert [t[0][2] for t in tracks] == [78, 74, 69, 50]  # F#5, D5, A4, D3
    assert all(abs(max(n[1] for n in t)-76) < 0.01 for t in tracks)
    # LilyPond: 5 compases + dos casillas de 1 compás + 12 compases.
    # A1, A2 (casilla 2), B1, B2: 36 compases interpretados, 144 negras.
    spans = [(0,24), (0,20), (24,28), (28,76), (28,76)]
    expanded = []
    for track in tracks:
        events, cursor = [], 0
        for lo, hi in spans:
            for start, end, pitch in track:
                if start < hi and end > lo:
                    events.append([round(cursor+max(start,lo)-lo,9),
                                   round(cursor+min(end,hi)-lo,9),pitch])
            cursor += hi-lo
        assert cursor == 144
        for prev, nxt in zip(events, events[1:]):
            assert prev[1] <= nxt[0]+1e-8, "voz no monofónica"
        expanded.append(events)
    metadata = {"source_sha256": hashlib.sha256(midi).hexdigest(),
                "source": "https://www.mutopiaproject.org/cgibin/piece-info.cgi?id=242",
                "license": "CC-BY-SA-3.0", "beats":144,
                "voices":["Violino I","Violino II","Viola","Continuo"],
                "source_counts":[len(t) for t in tracks], "notes":expanded}
    (DEST/"score.json").write_text(json.dumps(metadata,indent=2)+"\n")
    lua = "{\n"+",\n".join("{"+",".join("{%s,%s,%s}" % tuple(n) for n in t)+"}" for t in expanded)+"\n}"
    for template, output in [("engine.lua.in", "aire.lua"),
                             ("engine-adagio.lua.in", "aire-adagio.lua"),
                             ("engine-expresivo.lua.in", "aire-expresivo.lua"),
                             ("engine-expresivo.lua.in", "aire-control.lua")]:
        engine = (DEST/template).read_text()
        assert engine.count("@SCORE@") == 1
        (DEST/output).write_text(engine.replace("@SCORE@",lua).replace(
            "@LIVE@", "true" if output=="aire-control.lua" else "false"))
    print("Importación:",metadata["source_counts"],"→",[len(t) for t in expanded],"notas; 144 negras")


if __name__ == "__main__":
    main()
