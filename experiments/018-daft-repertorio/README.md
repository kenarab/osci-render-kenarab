# Daft Punk: cuatro arreglos largos para osci-render

EXP-055 / DFT-01…06. Experimento nuevo: los estudios vocales y groove de 013
permanecen intactos. Aquí se reproducen las notas de cuatro MIDI descargados,
de principio a fin, con una instrumentación propia del laboratorio.

**Completo se refiere al archivo fuente, no a una reconstrucción fiel del disco.**
Giorgio es un arreglo reducido. Las otras versiones también pueden omitir secciones
o alterar la instrumentación. No se han cotejado nota por nota con las grabaciones.

| Arreglo disponible | Duración aproximada | Lua preset | Lua controlable | WAV íntegro |
| --- | --- | --- | --- | --- |
| Something About Us | 3:22 | [abrir](something-about-us.lua) | [controles](something-about-us-control.lua) | [WAV](../../recordings/018-something-about-us.wav) |
| Instant Crush | 5:14 | [abrir](instant-crush.lua) | [controles](instant-crush-control.lua) | [WAV](../../recordings/018-instant-crush.wav) |
| Lose Yourself to Dance | 5:55 | [abrir](lose-yourself-to-dance.lua) | [controles](lose-yourself-to-dance-control.lua) | [WAV](../../recordings/018-lose-yourself-to-dance.wav) |
| Giorgio by Moroder, reducido | 5:49 | [abrir](giorgio-by-moroder.lua) | [controles](giorgio-by-moroder-control.lua) | [WAV](../../recordings/018-giorgio-by-moroder.wav) |

Todos los Lua musicales están **en esta carpeta**, disponibles localmente e
ignorados por Git. Los presets ignoran sliders y terminan en silencio; recargar
con reinicio de estado/step para volver al comienzo. No se alargan repitiendo un
bucle. El motor conserva las duraciones note-on/off, las velocidades y el mapa
de tempo. Pedal y pitch bend no se interpretan; los cuatro importados no contienen
CC según el parser existente. No se afirma ausencia de pitch bend en los originales.

## Interpretación e identidades

Melodías/coros usan formantes sintéticos, acompañamiento y bajo usan los bancos
de toro/Roman/Cassini. La batería se sintetiza según notas del canal MIDI 10:
bombo con caída de frecuencia, caja/clap y metales como componentes inarmónicos.
No son muestras ni recreación exacta de una batería acústica. **No hay voz humana,
letras cantadas ni análisis vocoder**: es síntesis de vocales sobre las notas MIDI.

La agrupación de pistas es una decisión artística explícita registrada en cada
JSON: 1 melodía/solos/coros, 2 acompañamiento, 3 bajo y 4 percusión. Se conserva
cada evento/pista de origen; los controles cambian un grupo completo. No hay un
knob independiente para cada una de las 12 pistas de Instant Crush en este estudio.

| Slider | Función | Inicio recomendado |
| --- | --- | --- |
| A | Identidad de melodía | .875, robot |
| B | Identidad de acompañamiento | .125, toro |
| C | Identidad de bajo | .375, Roman |
| D | Nivel de percusión | .65 |
| E | Tempo .5–1.5x sin transponer | .5 |
| F | Expresión global; 0 silencia | .7 |
| G | Vocal a/e/i/o/u, interpolación continua | .25, e |
| H | Brillo de voz robótica | .5 |

A/B/C: centros .125=toro, .375=Roman, .625=Cassini, .875=robot.
Son selectores con histéresis y mezcla de constante temporal 80 ms. G/H afectan
los grupos que estén usando robot. En preset la asignación es fija; en control
comprobar sliders Static y mapeo MIDI propio. MIDI físico y Pro pendientes.

La salida es **mezcla sonora XY**, no superficie F=0. Para geometría XYZ usar
015/016/017 y su galería. No presentar las figuras del audio mezclado como una
malla. Mejorar color/brillo se trata en docs/niveles-y-dinamica.md.

## Evidencia y reproducción

- Fuentes, hashes, duración, notas y asignación de pistas: [manifest.json](manifest.json).
- Motor independiente: library/robot_voice/song.lua.in; no contiene canciones.
- Generar: `python3 scripts/build_daft_repertoire.py` (requiere MIDI locales).
- Render/validación íntegra: `luajit scripts/check_daft_repertoire.lua`.
- Reporte: validacion.json. WAV estéreo de salida sin normalización ni reproducción.
- Cota por suma de polifonía para expresión máxima <=.6; pruebas verifican muestras,
  fin y todos los eventos. Armónicos de bancos/robot se acotan según tasa/nota;
  no se afirma ausencia de imágenes de interpolación o aliasing de envolventes.

Archivos MIDI públicos de MIDIfind, originales en downloads/daft-punk/originals.
Autoría y licencia abierta de arreglos no verificadas: no redistribuir en Git.
No se descargaron muestras de discos ni se compraron créditos. Aceptación sonora,
comparación con originales y performance en el host pendientes.
