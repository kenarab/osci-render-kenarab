"""Importa SMF 0/1 a eventos con segundos, tempo, velocidad y procedencia.

No compra ni descarga archivos. Salida JSON privada en recordings/ por defecto.
Conserva polifonia; pedal/otros CC se registran pero no se aplican a la duracion.
"""
import argparse
from collections import defaultdict, deque
import hashlib
import json
from pathlib import Path
import struct


def parse(data):
    if data[:4]!=b'MThd': raise ValueError('No es MIDI SMF')
    size=int.from_bytes(data[4:8],'big')
    fmt,tracks,division=struct.unpack('>HHH',data[8:14])
    if size<6 or fmt not in (0,1) or not division or division&0x8000:
        raise ValueError('Se requieren SMF 0/1 y tiempo PPQ; SMPTE no soportado')
    offset=8+size; notes=[]; tempos=[(0,500000)]; controls=[]; programs=[]; names={}
    for track_id in range(tracks):
        if data[offset:offset+4]!=b'MTrk': raise ValueError('Falta MTrk')
        length=int.from_bytes(data[offset+4:offset+8],'big');offset+=8
        chunk=data[offset:offset+length];offset+=length
        if len(chunk)!=length: raise ValueError('Pista truncada')
        pos=0;tick=0;running=None;active=defaultdict(deque)
        def byte():
            nonlocal pos
            if pos>=len(chunk): raise ValueError('Evento truncado')
            v=chunk[pos];pos+=1;return v
        def vlq():
            n=0
            for _ in range(4):
                b=byte();n=n*128+(b&127)
                if b<128:return n
            raise ValueError('VLQ demasiado largo')
        def blob(n):
            return bytes(byte() for _ in range(n))
        while pos<len(chunk):
            tick+=vlq();status=byte()
            if status<128:
                if running is None:raise ValueError('Running status sin antecedente')
                pos-=1;status=running
            elif status<240:running=status
            if status==255:
                kind=byte();payload=blob(vlq())
                if kind==81:
                    if len(payload)!=3 or not int.from_bytes(payload,'big'):raise ValueError('Tempo invalido')
                    tempos.append((tick,int.from_bytes(payload,'big')))
                elif kind==3:names[str(track_id)]=payload.decode('utf-8',errors='replace')
                elif kind==47:break
            elif status in (240,247):
                blob(vlq());running=None
            elif 128<=status<240:
                kind,channel=status>>4,status&15
                a=byte();b=byte() if kind not in (12,13) else None
                if a>=128 or (b is not None and b>=128):raise ValueError('Datos MIDI invalidos')
                key=(channel,a)
                if kind==9 and b:active[key].append((tick,b))
                elif kind==8 or (kind==9 and b==0):
                    if not active[key]:raise ValueError('Note-off sin note-on')
                    start,velocity=active[key].popleft()
                    if tick<=start:raise ValueError('Nota de duracion no positiva')
                    notes.append(dict(track=track_id,channel=channel+1,pitch=a,velocity=velocity,start_tick=start,end_tick=tick))
                elif kind==11:controls.append(dict(track=track_id,channel=channel+1,tick=tick,cc=a,value=b))
                elif kind==12:programs.append(dict(track=track_id,channel=channel+1,tick=tick,program=a))
            else:raise ValueError(f'Evento no soportado: {status:x}')
        if any(active.values()):raise ValueError('Notas abiertas al finalizar la pista')
    if offset!=len(data):raise ValueError('Datos sobrantes')
    tempo_map=dict(sorted(tempos,key=lambda v:v[0]));ticks=sorted(tempo_map)
    segments=[];seconds=0;previous=0;tempo=500000
    for tick in ticks:
        seconds+=(tick-previous)*tempo/(division*1e6)
        tempo=tempo_map[tick];segments.append((tick,seconds,tempo));previous=tick
    def time(tick):
        from bisect import bisect_right
        t,s,u=segments[bisect_right(ticks,tick)-1]
        return s+(tick-t)*u/(division*1e6)
    for note in notes:
        note['start_seconds']=time(note['start_tick']);note['end_seconds']=time(note['end_tick'])
    notes.sort(key=lambda n:(n['start_tick'],n['track'],n['channel'],n['pitch']))
    return dict(format=fmt,ppq=division,tracks=names,notes=notes,
                tempo_map=[dict(tick=t,seconds=s,microseconds_per_quarter=u) for t,s,u in segments],
                controls=controls,programs=programs,
                warnings=['Pedal, pitch bend y expresion requieren interpretacion posterior; duraciones note-on/off.',
                          'No se asignan automaticamente las pistas a voces monofonicas.'])


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('midi',type=Path);p.add_argument('--source',required=True)
    p.add_argument('--conditions',required=True,help='Procedencia/condiciones de uso documentadas por quien aporta el archivo')
    p.add_argument('--output',type=Path,default=Path('recordings/repertoire-import.json'))
    args=p.parse_args();data=args.midi.read_bytes();result=parse(data)
    result['provenance']=dict(source=args.source,conditions=args.conditions,sha256=hashlib.sha256(data).hexdigest(),file=args.midi.name)
    with args.output.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(f'{len(result["notes"])} notas; {len(result["tempo_map"])} tempos; {args.output}')

if __name__=='__main__':main()
