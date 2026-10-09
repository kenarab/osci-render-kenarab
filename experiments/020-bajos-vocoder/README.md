# Bajos de sintetizador y vocoder

EXP-057 / BVC-01…07. Dos estudios nuevos de bajo **aislado**, 24 segundos,
con notas de los arreglos MIDI locales de Daft Punk. Se conservan los estudios
completos de 018. La síntesis es propia; no reproduce el sonido del disco.

| Estudio | Bajo seco | Bajo vocoder | Controlable | Comparación WAV |
| --- | --- | --- | --- | --- |
| Lose Yourself to Dance | [Lua](lose-yourself-to-dance-bass.lua) | [Lua](lose-yourself-to-dance-bass-vocoder.lua) | [Lua](lose-yourself-to-dance-bass-control.lua) | [seco](../../recordings/020-lose-yourself-to-dance-bass.wav) / [vocoder](../../recordings/020-lose-yourself-to-dance-bass-vocoder.wav) |
| Giorgio by Moroder | [Lua](giorgio-by-moroder-bass.lua) | [Lua](giorgio-by-moroder-bass-vocoder.lua) | [Lua](giorgio-by-moroder-bass-control.lua) | [seco](../../recordings/020-giorgio-by-moroder-bass.wav) / [vocoder](../../recordings/020-giorgio-by-moroder-bass-vocoder.wav) |

Empezar con volumen bajo por el nivel y contenido grave del nuevo instrumento.
Primero comparar los presets: ignoran sliders heredados. Terminan después del
fragmento y su fundido; Reset Step Counter/reinicio de estado vuelve al comienzo.
Los WAV duran 24.5 s y conservan salida directa, sin normalización posterior.

## Bajo y modulador

El bajo mezcla dos sierras ligeramente desafinadas, filtro resonante de cuatro
polos con caída de corte, seno grave paralelo y saturación suave. Se conserva
afinación al cambiar tempo. Es monofónico con prioridad a la última nota empezada
y fases continuas. Notas/duraciones/velocidades provienen del MIDI; se recortan
las que cruzan los extremos del fragmento. Pedal/bend no se interpretan.

El vocoder analiza **otra señal** en 12 bandas y aplica sus envolventes a las
bandas de la portadora. El modulador predeterminado es una vocal sintética de
afinación independiente, no una voz humana ni letras de Daft Punk. Podés cambiar
a/e/i/o/u o reemplazarla con el primer canal de entrada de audio (`ext_x`).
El seno grave evita que desaparezca el cuerpo cuando el procesamiento resalta
los medios: para escuchar sólo vocoder, poner G=0 y C=1.

Salida mono duplicada en XY: puede verse una diagonal en el osciloscopio.
Es un ensayo de sonido; no visualiza una superficie XYZ. La geometría se conserva
en los ejercicios 016/019, y la futura portadora algebraica es otro paso.

## Controles

Abrir `-bass-control.lua` con sliders en Static para probar o mapear MIDI.

| Slider | Función | Inicio |
| --- | --- | --- |
| A | Corte base 100–3000 Hz; la envolvente añade apertura | .45 |
| B | Drive de saturación | .5 |
| C | Mezcla de bajo filtrado / vocoder | .65 |
| D | Vocal sintética a/e/i/o/u | .25, e |
| E | Tempo .5–1.5x | .5, velocidad fuente |
| F | Expresión; 0 silencia | .65 |
| G | Fundamental senoidal paralela | .55 |
| H | Mezcla modulador sintético / entrada externa | 0, sintético |
| I | Resonancia del filtro | .3 |

Se suavizan con constante temporal de 60 ms. A/I afectan la rama de bajo seco;
D afecta el modulador sintético. B/F afectan toda la salida. La portadora del
vocoder toma las sierras antes del filtro de corte para conservar armónicos.
E cambia el tempo del fragmento; no es giro ni cobertura de una escena.

Para usar tu voz: seleccionar un dispositivo de entrada válido en el host,
mantener desactivado **Audio Input Enabled** (para que siga sonando el Lua),
y subir H hacia 1. El canal 1 alimenta el modulador. Con H=1, C=1, G=0 y entrada
silenciosa, el resultado debe apagarse tras la cola. La entrada física sigue
pendiente de comprobar, aunque su interfaz está confirmada en el código local.

## Extender efectos

La [investigación de filtros y ruteos](../../docs/filtros-y-vocoder.md) explica Lua,
Custom Lua Effect y la alternativa osci-render VST/AU + Vocoder de Live.

[vocoder-effect.lua](vocoder-effect.lua) se **pega en el editor de Lua Effect**;
no se carga como fuente. Espera X=portadora y Y=modulador. Se puede preparar un
audio estéreo con esos dos canales o rutearlos como entrada; este empaquetado no
es estéreo musical. Activar el efecto con fuerza 1. A=mezcla (1), B=drive (.3),
C=nivel (.65). Su salida es mono. No combinarlo con el preset ya vocoderizado
para esta prueba; tampoco aplicar estos valores al banco de controles del bajo.
La comprobación del editor/ruteo en Pro queda pendiente.

## Evidencia

- [Procedencia y recortes](manifest.json): Lose 56–80 s, pista Bass 2; Giorgio
  96–120 s, pista Bass 0 del arreglo reducido. Originales/notas/Lua musicales
  locales, fuera de Git; biblioteca DSP y efecto sin repertorio versionados.
- [Pruebas Lua](validacion-lua.json): estabilidad/controles/externo a tres tasas,
  ausencia de modulador/portadora, cola, reinicio, presets independientes del
  slider, fin y todos los eventos. Cuatro WAV completos del fragmento a 48 kHz.
- [Prueba FFT](validacion-espectral.json): portadora de ruido idéntica y modulador
  400/2400 Hz. La energía se desplaza hacia la región del modulador, comprobando
  transferencia espectral. Esta prueba no mide inteligibilidad de voz ni calidad.
- Salida acotada por .65 con expresión máxima; picos de presets <.338 seco y
  <.259 vocoder. Potencia agradable, sonido y rendimiento en Pro pendientes.

Reproducir sin activar audio ni instalar dependencias:

```sh
python3 scripts/build_bass_vocoder.py
luajit scripts/check_bass_vocoder.lua
python3 scripts/check_vocoder_spectrum.py
```
