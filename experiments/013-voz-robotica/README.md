# 013 — Vocales robóticas, ensayo original

DP-02…04 / EXP-045. Abrir `vocales.lua` en osci-render; mantiene valores propios
para evitar los LFO que quedaron asignados a los sliders de la sesión.
`vocales-control.lua` permite A–D; poner cada control en **Static** antes de probar.

- A: articulación, 1–5 sílabas por segundo; .25 = 2.
- B: desplazamiento conjunto de formantes, .75–1.25×; .5 = neutro.
- C: brillo por inclinación del espectro, sin subir la amplitud máxima.
- D: giro del recorrido XYZ, 0 pausa el giro sin detener sonido.

Secuencia original de 32 sílabas; al valor predeterminado se repite cada 16 s.
Cuatro secciones contrastan duración, registro y sucesión de vocales. Es síntesis
aditiva de formantes sobre portadora armónica, **no análisis de voz ni cover**.
No contiene letras, muestras o melodías transcritas de Daft Punk. La biblioteca
`library/robot_voice/player.lua.in` es independiente del repertorio.

Escucha: [WAV XY de 16 s](../../recordings/013-vocales.wav). No incluye proyección
ni efectos de osci-render y no sirve para demostrar su imagen 3D. Captura completa
`recordings/013-vocales.xyz.f32`: float32 nativo little endian, intercalado XYZ,
48 kHz, 768000 tripletas. El dibujo es un recorrido de síntesis espacial, **no**
una superficie algebraica F=0. Mantener esa distinción con los ejercicios 012.

Prueba: `python3 scripts/build_robot_voice.py` y `luajit scripts/check_robot_voice.lua`.
Ver `validacion.json`: presets y cambios de controles a 16/44.1/48 kHz, salida
finita, energía en tres ejes y reinicio. Pico observado .20, margen antes del host.
Cada armónico activo queda bajo .4×sample_rate; eso no es una garantía de ausencia
total de aliasing (modulación y cambios de notas generan bandas laterales).
No se usa limitador ni saturación como maquillaje. Escucha/aceptación en host pendiente.

Para comparar con los estudios anteriores: Volume .30, Threshold 1.00; evitar
recorte posterior. El volumen físico se ajusta con prudencia según tus auriculares.

El usuario prefirió volver a Bach por fatiga con el sonido de superficies.
Esta prueba vocal se entrega para escucha voluntaria; no quedó cargada ni fue
aceptada en el host. El ajuste Volume .30 es provisional, no una configuración
final de escucha o tamaño visual.

## Groove original (GRV-01/02)

`groove-disco.lua` añade bajo sincopado y bombo a negras, con vocales cortas y
acentos de semicorcheas. 100 BPM elegidos para el ensayo; inspirado por el pedido
Lose Yourself to Dance, no es su transcripción ni una reproducción de la grabación.
Preset autónomo, sin depender de los LFO del host. Se mantiene intacto `vocales.lua`.
[WAV de 24 s](../../recordings/013-groove-disco.wav); mezcla XY para escuchar, sin
afirmar superficie F=0 o identidad con la perspectiva del host. No se carga solo.

Generar: `python3 scripts/build_disco_groove.py`.
Verificar/renderizar: `luajit scripts/check_disco_groove.lua`.
Prueba a 16/44.1/48 kHz: salida finita, pico <.145, reinicio; ver
`groove-validacion.json`. La agradabilidad y el parecido estilístico son pendientes
humanos. No hay limitador que maquille el estudio ni garantías de ausencia de aliasing.
