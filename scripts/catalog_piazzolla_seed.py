"""Valida el lote semilla local; genera derivados privados e indice navegable.

No descarga ni hace OMR. Originales en downloads/piazzolla; metadatos en docs.
"""
from collections import Counter
from datetime import datetime,timezone
import hashlib
import html
import json
from pathlib import Path
import re
import subprocess
import zipfile
import xml.etree.ElementTree as ET
from PIL import Image
from import_repertoire_midi import parse

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/proyecto-piazzolla'
RAW=ROOT/'downloads/piazzolla'
DER=RAW/'derived'

def main():
    manifest=json.loads((DOC/'semilla-fuentes.json').read_text())
    DER.mkdir(parents=True,exist_ok=True)
    records=[];note_sets={}
    for item in manifest['resources']:
        r=dict(item);p=RAW/r['file'];r['path']=str(p.relative_to(ROOT));r['derived']=[]
        if not p.exists():
            r['status']='missing';records.append(r);continue
        data=p.read_bytes();r.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),
            file_mtime_utc=datetime.fromtimestamp(p.stat().st_mtime,timezone.utc).isoformat())
        r['status']='valid';r['derived']=[]
        try:
            if not data:raise ValueError('Respuesta vacia; no es un archivo musical')
            if r['format']=='MIDI':
                if not data.startswith(b'MThd'):raise ValueError('Firma MIDI ausente')
                music=parse(data,allow_zero_duration=True)
                dest=DER/(p.stem+'.events.json')
                music['provenance']={k:r[k] for k in ['source_url','download_url','sha256','rights_status']}
                r['derivation']=dict(tool='scripts/import_repertoire_midi.py',schema_version=1,
                    tool_sha256=hashlib.sha256((ROOT/'scripts/import_repertoire_midi.py').read_bytes()).hexdigest(),
                    options={'allow_zero_duration':True},review='validacion estructural; escucha pendiente')
                music['provenance']['derivation']=r['derivation']
                dest.write_text(json.dumps(music,ensure_ascii=False,indent=2)+'\n')
                r.update(notes=len(music['notes']),duration_seconds=round(max(n['end_seconds'] for n in music['notes']),6),
                    tracks_with_notes=len({n['track'] for n in music['notes']}),track_names=music['tracks'],
                    zero_duration_notes=music['zero_duration_notes'],tempos=len(music['tempo_map']),warnings=music['warnings'])
                r['derived']=[str(dest.relative_to(ROOT))]
                note_sets[r['id']]=Counter((n['channel'],n['pitch'],n['start_tick'],n['end_tick'],n['velocity']) for n in music['notes'])
            elif r['format']=='MXL':
                with zipfile.ZipFile(p) as z:
                    container=ET.fromstring(z.read('META-INF/container.xml'))
                    node=container.find('.//{*}rootfile');name=node.attrib['full-path']
                    xml=z.read(name);root=ET.fromstring(xml)
                if root.tag not in ('score-partwise','score-timewise'):raise ValueError('No es MusicXML de partitura')
                dest=DER/(p.stem+'.musicxml');dest.write_bytes(xml)
                r.update(parts=[x.findtext('part-name') for x in root.findall('.//score-part')],
                         creators=[x.text for x in root.findall('.//creator')])
                r['derived']=[str(dest.relative_to(ROOT))]
                r['derivation']=dict(tool='scripts/catalog_piazzolla_seed.py',schema_version=1,
                    tool_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                    operation='extraer XML indicado en META-INF/container.xml, bytes intactos',
                    review='XML bien formado y raiz musical; validacion XSD pendiente')
            elif r['format']=='PDF':
                if not data.startswith(b'%PDF-'):raise ValueError('Firma PDF ausente')
                info=subprocess.check_output(['pdfinfo',str(p)],text=True)
                r['pages']=int(re.search(r'Pages:\s*(\d+)',info)[1]);r['conversion']='OMR/transcripcion y revision pendientes'
            elif r['format']=='WebP':
                with Image.open(p) as im:r['dimensions']=list(im.size);im.verify()
                r['conversion']='Imagen de pagina; OMR/transcripcion pendiente'
        except (ValueError,KeyError,ET.ParseError,zipfile.BadZipFile,subprocess.CalledProcessError) as e:
            r['status']='invalid';r['error']=str(e)
        records.append(r)
    hashes={}
    for r in records:
        if r['status']=='valid':hashes.setdefault(r['sha256'],[]).append(r['id'])
    a,b='oblivion-sp1','oblivion-sp2';diff=None
    if a in note_sets and b in note_sets:
        diff={'ids':[a,b],'only_first_events':sum((note_sets[a]-note_sets[b]).values()),
              'only_second_events':sum((note_sets[b]-note_sets[a]).values()),
              'comparison':'canal, altura, tick inicio/fin y velocidad; no prueba igualdad de todos los mensajes MIDI'}
        ta=Counter();tb=Counter()
        for key,count in note_sets[a].items():ta[key[:4]]+=count
        for key,count in note_sets[b].items():tb[key[:4]]+=count
        diff.update(timed_events_only_first=sum((ta-tb).values()),
                    timed_events_only_second=sum((tb-ta).values()),
                    common_timed_events=sum((ta & tb).values()),
                    common_exact_events=sum((note_sets[a] & note_sets[b]).values()))
    candidates=[]
    for p in sorted(RAW.glob('scorebase-composer*.html')):
        text=p.read_text()
        for path,label in re.findall(r'<a\b[^>]*href="(/scores/\d+)"[^>]*>(.*?)</a>',text,re.S):
            label=html.unescape(re.sub('<[^>]+>',' ',label));label=' '.join(label.split())
            candidates.append(dict(url='https://scorebase.org'+path,label=label,listing=p.name,status='solo ficha localizada'))
    candidates=list({r['url']:r for r in candidates}.values())
    report=dict(schema_version=1,records=records,valid=sum(r['status']=='valid' for r in records),
                failed=sum(r['status']!='valid' for r in records),
                exact_duplicate_groups=[v for v in hashes.values() if len(v)>1],
                comparison=diff,scorebase_candidates=candidates,
                limitations=['Lote semilla; no busqueda exhaustiva de Internet.',
                             'Acceso publico no equivale a licencia abierta.',
                             'No se hicieron OMR, alineacion entre arreglos ni evaluacion auditiva.'])
    (DOC/'semilla-catalogo.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    def link(path,label):
        target=Path(path).relative_to('downloads/piazzolla')
        return '<a href="'+html.escape(str(target),quote=True)+'">'+html.escape(label)+'</a>'
    rows=[]
    for r in records:
        details='; '.join(f'{k}: {r[k]}' for k in ['notes','duration_seconds','pages','parts','zero_duration_notes','error'] if k in r)
        filelink=link(r['path'],r['format']) if r['status']=='valid' else html.escape(r['format'])
        rows.append('<tr>'+''.join('<td>'+v+'</td>' for v in [html.escape(r['work']),html.escape(r['variant']),filelink,
             ' / '.join(link(p,Path(p).suffix) for p in r['derived']),html.escape(r['status']),html.escape(details),
             '<a href="'+html.escape(r['source_url'],quote=True)+'">Fuente</a>',html.escape(r['scope'])])+'</tr>')
    index='''<!doctype html><html lang="es"><meta charset="utf-8"><title>Atlas Piazzolla — semilla</title>
<style>body{font:16px system-ui;margin:35px;background:#f8f6f1;color:#202830}table{border-collapse:collapse;width:100%}td,th{padding:12px;text-align:left;border-bottom:1px solid #ccc}a{color:#075b79}th{background:#e4e7e5}p{max-width:900px}</style>
<h1>Atlas Piazzolla — colección semilla</h1><p>Originales y variantes para comparar. Los formatos de un mismo arreglo no cuentan como arreglos nuevos. Los archivos públicos tienen licencia no verificada; no se presupone permiso de redistribución.</p>
<p>MIDI → eventos JSON; MXL → MusicXML. PDF e imágenes conservados, transcripción pendiente. No hay evaluación auditiva ni clasificación del mejor arreglo.</p>
<table><thead><tr><th>Obra</th><th>Variante</th><th>Original</th><th>Derivado</th><th>Validación</th><th>Datos</th><th>Procedencia</th><th>Alcance</th></tr></thead><tbody>'''+''.join(rows)+'</tbody></table></html>'
    (RAW/'index.html').write_text(index)
    print(json.dumps(dict(valid=report['valid'],failed=report['failed'],candidates=len(candidates),comparison=diff),ensure_ascii=False))

if __name__=='__main__':main()
