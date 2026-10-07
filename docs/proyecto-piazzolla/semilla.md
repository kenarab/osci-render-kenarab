# Experimento semilla del Atlas

EXP-034 / SEM-01–06. Lote pequeño, recogido entre el 6 y el 7 de octubre de 2026
(según hora local/UTC). El usuario reserva la colección amplia para otro repositorio.
La búsqueda incluyó catálogos editoriales y comunitarios, páginas de reproductores,
PDF directos y consultas por los cinco títulos, aliases y formatos. **No es un censo
exhaustivo de Internet ni una descarga de todo el catálogo de Piazzolla.**

## Abrir la colección

[Índice local navegable](../../downloads/piazzolla/index.html): originales y derivados,
con una fila por archivo, fuente y validación. Los archivos descargados y sus notas
normalizadas permanecen fuera de Git, en `downloads/piazzolla/`.

Se obtuvieron **19 archivos musicales/visuales válidos por firma y parser básico**:
10 MIDI, 3 MXL, 5 PDF y 1 imagen WebP de vista previa. No hay duplicados binarios
entre ellos. Dos respuestas vacías quedan como fallos. Se conservaron además
**90 fichas distintas** de las primeras tres páginas del catálogo ScoreBase como
candidatos, sin descargarlas todas ni considerar verificada su atribución.

[Fuentes exactas del lote](semilla-fuentes.json) ·
[Catálogo, hashes, métricas y candidatos](semilla-catalogo.json).

## Variantes reunidas

| Obra / variante | Originales | Datos comprobados | Estado musical |
| --- | --- | --- | --- |
| Oblivion / Songparts 1 | MIDI | 1864 notas; 308.46 s | Comparar expresión con variante 2 |
| Oblivion / Songparts 2 | MIDI | 1865 notas; 308.46 s | Misma base de notas en gran parte; muchas diferencias de intensidad |
| Oblivion / Songparts 3 | MIDI | 485 notas; 167 s; guitarra según pista | La ficha lo marca parcial |
| Oblivion / ScoreBase 38762 | MIDI, MXL, PDF, imagen de página | 1875 notas; XML: flauta, fagot, piano; PDF 6 páginas | Crédito impreso: arr. José Bragato; atribución independiente pendiente |
| Libertango / Songparts 1 | MIDI | 2364 notas; 160 s | Integridad/escucha pendientes |
| Libertango / Songparts 2 | MIDI | 1962 notas; 163.5 s | Integridad/escucha pendientes |
| Libertango / Songparts 3 | MIDI | 3292 notas; 264.18 s | Integridad/escucha pendientes |
| Libertango / Songparts 4 | MIDI | 251 notas; 102.14 s | Versión corta; revisar alcance |
| Libertango / ScoreBase 185635 | MIDI, MXL, PDF | Dos violonchelos; 1342 notas; 307 s; PDF 3 páginas | Candidato para estudiar contrapunto de dos voces |
| Libertango / ScoreBase 136129 | MIDI, MXL, PDF | Piano; 2997 notas; PDF 9 páginas | Resolver polifonía antes de llevar a Lua |
| Violentango / Serge Robert | PDF | 9 páginas, tres guitarras; partitura y partes | Transcripción digital pendiente |
| Meditango / Thierry Caens, EMR 76130 | PDF | 6 páginas, incluye portada y catálogo | Muestra editorial; no edición completa |

La imagen WebP es una página del mismo Oblivion, no otra versión. MXL, PDF y MIDI
asociados a una ficha también representan formatos relacionados, no tres arreglos.
La duración se calcula hasta el último note-off, no necesariamente hasta el fin del
archivo; puede diferir de lo anunciado por un reproductor.

No se obtuvo un archivo musical de **Solitude/Soledad** en este lote. Sigue pendiente
identificar la obra exacta y obtener una fuente válida. Su ficha se conserva.

## Caso de estudio: conservar la interpretación

Oblivion 1 y 2 de Songparts tienen 1863 eventos coincidentes si se compara canal,
altura, inicio y fin en ticks. Sólo 130 coinciden también en velocidad MIDI. Hay
1 evento temporal exclusivo de la primera y 2 de la segunda. Eso muestra por qué
**una diferencia de una nota en el conteo no significa que sólo difieran en una nota**.
No se fusionan. No se compararon todos los CC ni se realizó alineación perceptual.

Este criterio amplía ATL-10: las variaciones de intensidad, articulación y tempo
son material de estudio, incluso cuando casi todas las alturas coinciden.

## Lengua franca: primer paso real y límites

- Los **10 MIDI** tienen un derivado JSON con notas, velocidades, canales/pistas,
  CC/programas conservados por el importador y mapa de tempo. Se preserva el MIDI
  original. JSON es nuestro formato técnico, no un sustituto universal de MIDI.
- Los **3 MXL** tienen su **MusicXML extraído**, sin reconstruir notas ni alterar
  sus bytes XML. Es descompresión, no una transcripción por reconocimiento.
- Los **5 PDF y la imagen** están catalogados; **no están convertidos a notas**.
  Requieren OMR o transcripción revisada. El texto extraído para títulos/créditos no
  cuenta como conversión de notación.
- MusicXML es la propuesta común para notación; MIDI/eventos para ejecución.
  El Atlas deberá registrar conversiones, pérdidas y revisiones antes de intercambiar
  automáticamente ambas representaciones. Esta semilla aún no genera MIDI desde XML
  ni MusicXML desde MIDI, y no convierte grabaciones de audio en partituras.

El parser estricto detectó notas de duración cero en dos MIDI de ScoreBase: 2 en
Oblivion y 32 en Libertango piano. Se implementó el modo opcional
`--allow-zero-duration`, que **las conserva y advierte**, sin inventar duración.
El modo estricto anterior sigue activo por defecto. Para sintetizar estos eventos
hará falta una decisión musical explícita; no se borraron del material fuente.

Limitaciones del derivado: pedal registrado pero no aplicado a duración; pitch bend,
SysEx y otros eventos no se preservan íntegramente. El original es la referencia.
La validación de MXL comprueba contenedor, XML y raíz de partitura, no todo el esquema
MusicXML ni equivalencia musical entre sus formatos. PDF e imágenes tienen lectura
estructural e inspección visual de extremos, no revisión nota por nota.

## Fuentes que rindieron y fallos útiles

- [Songparts / Oblivion](https://songparts.com/songs/astor-piazzolla/oblivion) y
  [Libertango](https://songparts.com/songs/astor-piazzolla/libertango): siete descargas
  públicas utilizables. Los enlaces se extrajeron de páginas, sin inicio de sesión.
- [ScoreBase / catálogo Piazzolla](https://scorebase.org/composers/piazzolla-astor):
  tres arreglos obtenidos en MIDI/MXL/PDF y 90 fichas candidatas conservadas.
  Los datos impresos/XML corrigen etiquetas genéricas de la ficha: Oblivion tiene
  flauta/fagot/piano, no asumir la instrumentación de un resumen automático.
- [Guitares Robert / Violentango](https://www.guitares-robert.ca/Piazzolla-Violentango-3G.pdf):
  fuente directa del arreglo de tres guitarras.
- [Reift / Meditango](https://files.reift.ch/files/scores/EMR76130.pdf): muestra de una
  edición identificable, útil para el catálogo aunque no complete la obra.
- SheetMusicGiant: Meditango y Soledad devolvieron **cero bytes** con HTTP 200.
  Meditango siguió vacío al reintentar con Referer. No se los cuenta como partituras.
  La ficha declara un uso de prueba temporal; no se etiqueta como licencia abierta.
- Scorely: timeout de 30 s en la consulta directa; queda como candidato, sin reiterar
  indefinidamente. Chrome e IAB informaron que no estaban disponibles en la herramienta;
  no se simuló una visita de navegador ni se afirmó haber superado un bloqueo.

Las fuentes son públicamente accesibles; **no se verificó licencia abierta** sobre
las composiciones/arreglos. Los originales se guardan localmente, sin incorporarlos
a Git ni publicarlos. Las fichas comerciales previas siguen como referencias,
no como adquisiciones del lote.

## Reproducibilidad y continuación

```sh
python3 scripts/check_repertoire_midi.py
python3 scripts/catalog_piazzolla_seed.py
```

El segundo comando valida archivos ya presentes y regenera derivados/catálogo/índice;
no descarga, no hace OMR y escribe los derivados en `downloads/piazzolla/derived/`.
El manifiesto conserva las URL exactas para reobtener originales. No automatizamos
una descarga masiva ni creamos infraestructura completa del Atlas aquí.

Siguiente paso musical propuesto: comparar las dos interpretaciones de Oblivion de
Songparts con el mismo timbre, y contrastar su estructura con el MusicXML de Bragato.
Para Libertango hay cuatro variantes MIDI y dos arreglos con notación. La selección
del mejor queda abierta hasta escuchar; no se infiere por número de notas.
