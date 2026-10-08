# Bach: cuatro voces con timbres intercambiables

**Nuevo experimento** VIV-01/02/04/05. No reemplaza Adagio ni los estudios 005–014.
Bach completo, aproximadamente 5:39, Adagio a 26 BPM con rubato/cadencias y loop.

## Archivos para abrir en osci-render

- [bach.lua](bach.lua): mezcla con asignación fija, ignora sliders. Primero comparar éste.
- [bach-control.lua](bach-control.lua): misma música, identidades por voz en vivo.
- [Violín I XYZ](bach-voz-1-xyz-control.lua), [Violín II XYZ](bach-voz-2-xyz-control.lua),
  [Viola XYZ](bach-voz-3-xyz-control.lua), [Continuo XYZ](bach-voz-4-xyz-control.lua).
- [WAV de 20 segundos](../../recordings/015-bach-voces-vivas.wav).

| Slider | Función | Inicio recomendado | MIDI CC valor aproximado |
| --- | --- | --- | --- |
| A | Identidad Violín I | .125: toro | 16 |
| B | Identidad Violín II | .375: Roman | 48 |
| C | Identidad Viola | .625: doble cono | 79 |
| D | Identidad Continuo | .875: Cassini | 111 |
| E | Tempo .5–1.5x, sin cambiar altura | .5 | 64 |
| F | Expresión global; 0 silencia | .65 | 83 |
| G | Giro de escena 0–.2 rad/s; 0 pausa | .5 | 64 |

Los cuatro selectores ofrecen las mismas identidades: elegir en los centros de
cuatro zonas iguales; hay histéresis alrededor de .25/.5/.75. Cambiar A no cambia
B/C/D ni reinicia fases, notas o tempo. Pasar del archivo preset al control sí
inicia otra reproducción. El controlador mueve sliders existentes: verificar el
mapeo en tu Pro; no se ha configurado automáticamente ni probado tu hardware.
Ponerlos en Static si quedaron LFO asignados. **F=0 deja todo en silencio**.

## Qué verás

La mezcla utiliza timbres derivados de estas superficies, no sus coordenadas
sumadas: el dibujo XY musical no tiene por qué parecerse a cada objeto. Para ver
una identidad sobre F=0 abrir el archivo XYZ de esa voz. A/B/C/D siguen indicando
la asignación por instrumento, pero se escucha/ve sólo el elegido por el archivo.
Las superficies XYZ no tienen filtrado espectral; pueden sonar ásperas. No son
el mismo audio suave de bancos. El continuo polifónico muestra la nota más aguda.
Al cambiar identidad, la vista XYZ cambia discretamente (no se inventa F=0 en el
fundido). Para comparar sin ruido usar la [galería 3D](../016-superficies-diversas/index.html).

Tamaño: usar Image Scale del visualizador Pro aumentando ambos ejes igual hasta
antes del borde. No subir Volume para hacer zoom. Configuración actual del host
no modificada; tamaño/sonido con tu controlador todavía requieren aceptación.

Fuente: J. S. Bach, Air BWV 1068, [Mutopia 242](https://www.mutopiaproject.org/cgibin/piece-info.cgi?id=242),
CC-BY-SA-3.0 según score.json existente. Notas originales y su hash en manifest.json;
adaptación temporal de este laboratorio. Ver [licencia](https://creativecommons.org/licenses/by-sa/3.0/).

Reproducir: `python3 scripts/build_live_voices.py`; validar con
`luajit scripts/check_live_voices.lua`. Pruebas de señal/transportes aprobadas fuera
del host; no equivalen a aceptación sonora ni a ausencia perceptual de clics.
