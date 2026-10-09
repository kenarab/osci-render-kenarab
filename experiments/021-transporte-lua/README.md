# Adelantar, retroceder y pausar Lua

EXP-058 / TRN-01…06. Nuevas variantes de 018/020, sin cambiar los anteriores.

## Primero escuchar algo simple

Abrir [bajo-prueba-mi2.lua](bajo-prueba-mi2.lua): Mi2 (82.4 Hz) continuo, en ciclos
de 8 s, sin MIDI ni sliders. No termina mientras buscás controles; ignora F=0.
[WAV de referencia](../../recordings/021-bajo-prueba-mi2.wav).

Después abrir [Lose — bajo seco con transporte](lose-yourself-to-dance-bass-transport.lua).
Lee sólo J/K/L: los sliders de timbre heredados no lo silencian. Empieza a los
0.1 s y termina a los 24 s. Para escuchar otra vez, disparar L como indica la tabla.
Mantener inicialmente volumen bajo.

En la ventana observada estaba `lose-yourself-to-dance-bass-vocoder.lua` dentro
de `delay.osci`, con Polygonizer (.874) y Delay (.685, 433 ms) activos. Cambian el
sonido respecto del WAV directo. Lua Effect tenía fuerza 0. F estaba en 0: eso
silencia variantes controlables, pero el preset abierto declara LIVE=false y lo
ignora. No se cambió la sesión. Comparar en una copia con Polygonizer/Delay
desactivados. El fin a los 24 s es otra explicación posible, aún no confirmada.

Si el tono fijo tampoco se escucha como su WAV, revisar cadena/dispositivo. Si
se escucha y el vocoder no convence, hay que trabajar el timbre: las métricas
no dan por aceptado el sonido.

## Transporte

En **Lua Sliders**, desplazar hacia abajo hasta J/K/L y ponerlos en Static.

| Slider | Función | Inicio |
| --- | --- | --- |
| J | Posición solicitada: `J × duración`, hacia delante o atrás | 0 |
| K | 0 reproduce; 1 pausa, silencia y congela el reloj musical | 0 |
| L | Pasar 0→1 vuelve al comienzo; bajar a 0 para rearmar | 0 |

En bajos: J=.25 → 6 s, .5 → 12 s, .75 → 18 s. En Lose completo, J=.5 → 177.7 s.
J es un mando para **pedir un salto**, no un indicador que siga el reloj: dejarlo
quieto permite seguir tocando. Control MIDI de 128 valores da pasos más grandes
en temas largos; para precisión, escribir el valor o usar un control más fino.

Podés pausar, mover J y reanudar. Funciona después del final. Durante un salto
rápido gana el último destino; hay fundidos de hasta 20 ms antes y 20 ms después.
Se recuperan sostenidas e índice, reiniciando DSP y aproximando fase según destino
y tempo actual; no se reproduce el historial anterior de filtros. Jitter menor
que .0005 se ignora. Mantener L alto no repite el retorno.

Reset Step Counter reinicializa estas variantes respetando J. Usar L para ir al
comienzo independientemente de J. En archivos con `control`, F=0 silencia y E
cambia tempo. En los de sonido fijo, sólo se leen J/K/L.

## Archivos

| Material | Sonido fijo + transporte | Timbre + transporte |
| --- | --- | --- |
| Lose, bajo seco | [Lua](lose-yourself-to-dance-bass-transport.lua) | [Lua](lose-yourself-to-dance-bass-control-transport.lua) |
| Lose, bajo vocoder | [Lua](lose-yourself-to-dance-bass-vocoder-transport.lua) | mismo control de bajo, C mezcla |
| Giorgio, bajo seco | [Lua](giorgio-by-moroder-bass-transport.lua) | [Lua](giorgio-by-moroder-bass-control-transport.lua) |
| Giorgio, bajo vocoder | [Lua](giorgio-by-moroder-bass-vocoder-transport.lua) | mismo control de bajo, C mezcla |
| Something About Us, arreglo | [Lua](something-about-us-transport.lua) | [Lua](something-about-us-control-transport.lua) |
| Instant Crush, arreglo | [Lua](instant-crush-transport.lua) | [Lua](instant-crush-control-transport.lua) |
| Lose Yourself to Dance, arreglo | [Lua](lose-yourself-to-dance-transport.lua) | [Lua](lose-yourself-to-dance-control-transport.lua) |
| Giorgio, arreglo reducido | [Lua](giorgio-by-moroder-transport.lua) | [Lua](giorgio-by-moroder-control-transport.lua) |

Los MIDI se convierten **antes de generar** los Lua: las notas quedan dentro del
código. Mientras suenan no abren `.mid` ni reciben del MIDI las notas de esta
partitura. Los CC pueden controlar sliders mapeados. Otro MIDI exige regenerar.
Estos motores mantienen reloj propio: no siguen automáticamente el cursor DAW.

El host documenta [Reset Step Counter y sliders Lua](https://github.com/jameshball/osci-render/wiki#lua-settings-panel).
La barra de animación de otros formatos no reposiciona las tablas de estos motores.

## Evidencia

[validacion.json](validacion.json): 14 variantes a 16/44.1/48 kHz; sostenidas
comparadas con toda la tabla, índice, saltos, pausa, jitter, último destino, retorno,
fin/seek posterior y silencio al cambiar destino. [calibracion.json](calibracion.json):
tono activo desde el inicio, ignora sliders y continúa después de cada ciclo.
Escucha, UI/controlador físico y diagnóstico causal en Pro pendientes.

Candidatos de seek precalculados por segundo, sin escanear la partitura por
muestra. Lua musical local fuera de Git; procedencia/timbres en 018/020 y
[manifiesto de variantes](manifest.json). No se modificó 001–020 ni .osci.

```sh
python3 scripts/build_transport_players.py
luajit scripts/check_transport_players.lua
```
