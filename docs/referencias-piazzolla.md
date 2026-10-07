# Piazzolla — repertorio de referencia

Pedido del usuario: incorporar **Libertango, Oblivion, Violentango, Meditango y
Solitude** como referencias para desarrollar ideas. No confundir este registro
con cinco arreglos implementados o con una escucha analítica ya realizada.

| Obra | Fuente localizada | Próximo trabajo |
| --- | --- | --- |
| Libertango | Catálogo editorial A. Pagani; discografía Sony/Carosello | Elegir interpretación y estudiar pulso, articulación y forma |
| Oblivion | Edición de Hal Leonard para solista y cuerdas | Elegir interpretación y estudiar fraseo, respiración y acompañamiento |
| Violentango | Catálogo A. Pagani; discografía Sony/Carosello | Comparar contraste, densidad y acentos con Libertango |
| Meditango | Catálogo A. Pagani; discografía Sony/Carosello | Identificar desarrollo temporal y cambios de textura |
| Solitude | A. Pagani identifica Solitude de la Suite Lumière | Confirmado por el usuario el 2026-10-07: Soledad/Solitude de Suite Lumière; buscar arreglos de esa obra |

## Fuentes

- [Catálogo de partituras de A. Pagani](https://www.apagani.it/pdf/Partiture%20Astor%20Piazzolla.pdf):
  incluye Libertango, Meditango, Violentango y Solitude de la Suite Lumière.
- [Sony Music / Carosello: Ritratto di Astor Piazzolla](https://store.sonymusic.it/products/ritratto-di-astor-piazzolla):
  lista Meditango, Libertango y Violentango. Referencia discográfica, no audio importado.
- [Hal Leonard: Oblivion, solista y orquesta de cuerdas](https://www.halleonard.com/product/4491250/oblivion):
  edición para consultar; no se presupone que sea el arreglo que prefiere el usuario.

Estas fuentes identifican obras/ediciones. No se descargaron ni compraron
partituras, grabaciones o MIDI, y no se asume la licencia abierta usada para Bach.
Para analizar una versión concreta, registrar enlace/intérprete; para transformar
sus notas, trabajar con material aportado por el usuario o una fuente utilizable
con procedencia y condiciones registradas. No fabricar notas y rotularlas como Piazzolla.

## Método de estudio

1. Fijar interpretación y arreglo; el título solo no determina instrumentación,
   tempo ni duración.
2. Anotar secciones y marcas de tiempo, roles de las voces, ritmo, dinámica,
   articulación y espacios. Separar observaciones de hipótesis.
3. Proponer una relación comprobable con la geometría: deformación de una
   superficie, cambios en sus secciones, cámara o densidad de barrido.
4. Comparar una vista sombreada de la superficie con su representación XY.
5. Guardar prueba y valoración musical/visual. Identificar por separado un arreglo
   de la obra y un estudio original inspirado en una técnica general.

## Ideas preliminares del agente, no análisis de grabaciones

- Un mismo patrón rítmico podría modular un coeficiente polinómico, permitiendo
  reconocer repetición y variación sobre una superficie estable.
- Una frase larga podría deformar lentamente una superficie cerrada, manteniendo
  legible su silueta; los acentos podrían cambiar el barrido en vez de colapsarla.
- Contrastar música y geometría con parámetros fijos antes de animar todo: elegir
  una relación perceptible y explicarla al usuario.

No asignamos todavía ecuaciones definitivas a cada título. El siguiente paso
musical depende de la versión elegida; la infraestructura geométrica puede avanzar.

## Avance 2026-10-06 — fuentes MIDI e ingreso de repertorio

Pedido renovado EXP-032. Ya hay dos candidatos específicos de archivos de notas,
además del catálogo editorial. **No se adquirieron ni descargaron estos MIDI**:

| Obra | Archivo ofrecido por la fuente | Estado y utilidad |
| --- | --- | --- |
| Libertango | [GEERDES, artículo 11844](https://geerdes.media/apps/playback/en/libertango-astor-piazzolla-11844.01.html): MIDI, 3:12, 11 canales; SMF 0/1; 5,99 € consultados | Candidato para separar bajo, piano, guitarra y voces de acordeón; la ficha anuncia 40 cambios de tempo y variantes de final. No es el manuscrito original. |
| Oblivion | [Pianosolo, arreglo Play The Piano](https://pianosolo.me/en/piano-sheets-midi/oblivion-2/): paquete PDF + MIDI, USD 16 consultados | Candidato para reducción de piano; requiere distribuir polifonía entre instrumentos, no asumir cuatro pistas monofónicas. |

Son descripciones de vendedores consultadas en esa fecha, no evaluación auditiva
ni garantía independiente de fidelidad. No se inició compra, registro ni descarga
privada. También apareció una oferta gratuita en Songparts, pero no quedó aclarada
la procedencia del arreglo; no se incorporó al repositorio como material autorizado.
Se pidió al usuario enlace al arreglo/MIDI preferido y aclaración de Solitude.
Violentango, Meditango y Solitude siguen pendientes de fuente de notas seleccionada.

### Infraestructura utilizable ahora

`scripts/import_repertoire_midi.py` lee SMF 0/1 y conserva notas polifónicas,
canal, pista, velocidad, programas, CC y mapa de tempo. Calcula tiempos en segundos
a través de todos los cambios de tempo, sin forzar el rubato del Bach sobre Piazzolla.
Pide procedencia y condiciones de uso, registra SHA-256 y rechaza sobrescribir su
salida. No depende de paquetes nuevos ni modifica el importador específico de Bach.

```sh
python3 scripts/import_repertoire_midi.py /ruta/al/arreglo.mid \
  --source 'URL o referencia del archivo aportado' \
  --conditions 'Condiciones documentadas del material' \
  --output recordings/piazzolla-import.json
python3 scripts/check_repertoire_midi.py
```

Probado con MIDI sintético (acordes, velocidades, running status, dos tempos y
entradas erróneas) y con las 516 notas del MIDI fuente de Bach antes de desplegar
repeticiones. **Todavía no se probó con un MIDI de Piazzolla**. El pedal se conserva
como CC, pero no prolonga las notas automáticamente; pitch bend y otros eventos
expresivos necesitan soporte posterior. El JSON importado no es aún un arreglo
Lua reproducible: falta seleccionar pistas, resolver polifonía, asignar timbres
y comprobar el fraseo contra la interpretación elegida.

### Primeros arreglos propuestos, todavía no implementados

- **Oblivion:** melodía cantabile con apertura espectral lenta; acompañamiento de
  parciales amortiguados; bajo separado. Probar primero 30–45 s con el mapa de tempo
  del arreglo elegido, conservando notas y espacios. Paleta disponible: Cuárticas
  y Prisma del experimento 008; no se promete imitación acústica de bandoneón.
- **Libertango:** ataques más rápidos y contraste de funciones entre bajo, piano
  y voz principal; preservar los cambios de tempo del MIDI. Comparar un fragmento
  con brillo fijo y otro con articulación espectral, antes de hacer la pieza completa.

Estos son diseños del laboratorio, no análisis de una grabación que ya hayamos
escuchado. El paso pendiente para producir las versiones musicales es incorporar
el archivo concreto. No se sustituyó ninguna obra por notas inventadas.

## Proyecto independiente acordado

El usuario amplía el objetivo a una base de datos extensa de Piazzolla y pide
planificarla aquí para ejecutarla después en otro repositorio. El [traspaso de
Atlas Piazzolla](proyecto-piazzolla/README.md) conserva fuentes adicionales, modelo,
criterios y límites del importador. La búsqueda iniciada obtuvo un HTML de
Songparts; todavía no se descargaron arreglos musicales. La recolección masiva
se traslada al futuro proyecto; este laboratorio consumirá arreglos seleccionados.

## Actualización: lote semilla obtenido

El usuario autorizó continuar aquí con un lote pequeño para representar el Atlas.
Ya hay [19 archivos válidos y catálogo navegable](proyecto-piazzolla/semilla.md),
con variantes de Oblivion/Libertango, Violentango en PDF y una muestra de Meditango.
Soledad sigue sin archivo válido. Las afirmaciones anteriores de «ningún MIDI»
describen el estado previo; la semilla documenta el resultado actual y sus límites.

## Identificación confirmada de Soledad / Solitude (2026-10-07)

El usuario confirma que busca la obra de los años 70 perteneciente a **Suite Lumière**.
La otra Soledad homónima no es el objetivo de esta búsqueda; no se atribuye una
fecha a esa otra obra basándose sólo en su recuerdo. Tampoco fusionar Años de soledad.

- [Melos, Suite Lumiere](https://melos.com.ar/producto/suite-lumiere/): la ficha
  indexada enumera Soledad (Solitude), Muerte, El amor y La evasión. La apertura
  directa por la herramienta web agotó el tiempo; no se descargó una edición.
- [Soledad — Partitura completa](https://pdfcoffee.com/soledad-partitura-completa-2-pdf-free.html):
  el texto público identifica Suite Lumiere y partes de piano eléctrico, bandoneón,
  guitarra, violín, violonchelo y contrabajo. Es un candidato concreto, no un PDF
  validado: tanto el enlace de descarga como el recurso del visor devolvieron HTML.
- [Soledad (from Lumière), MuseScore](https://ja.musescore.com/user/82703944/scores/27846628):
  candidato localizado por búsqueda, con título explícito; descarga no probada.

Resultado: identidad resuelta y candidatos precisos registrados; todavía no hay
archivo musical descargado de esta obra. La semilla conserva 19 archivos válidos.

## Muestras obtenidas el 2026-10-07: Solitude de Suite Lumière

La [página de BackingtracksMusic](https://backingtracksmusic.com/en/product-tag/astor-piazzolla/page/4/)
identifica el producto 0239 como Suite Lumière, 1975. Descargados los dos enlaces
DEMO públicos: trío en si menor con flauta de referencia y acompañamiento. Archivos,
hashes y duración en [el catálogo semilla](proyecto-piazzolla/semilla-catalogo.json).
Son fragmentos, no partitura/MIDI ni obra completa; escucha pendiente. La ficha
vecina «Soledad» es otro producto y no se incorporó como equivalente.

La consulta directa de MuseScore devolvió HTTP 403; PDFCoffee devolvió HTML incluso
desde el recurso del visor. No se obtuvieron partituras de esos enlaces.
