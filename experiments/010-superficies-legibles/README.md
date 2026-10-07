# Dos ejercicios de legibilidad de superficies

EXP-038 / INS-01. Separados de Bach y Piazzolla. Primero probar
[esfera.mp4](../../recordings/010-esfera.mp4) y
[elipsoide.mp4](../../recordings/010-elipsoide.mp4); luego abrir un solo Lua en osci-render.
Volumen bajo: estos ejercicios priorizan cobertura visual, no un timbre terminado.

- `esfera.lua`: x²+y²+z²=0.42².
- `elipsoide.lua`: (x/0.55)²+(y/0.26)²+(z/0.38)²=1, antes de la proyección.
- Las variantes `-control.lua` activan A velocidad de escena (0 pausa), B barrido
  12–36 Hz (0.5→24 Hz), C ancho del elipsoide (0.5→escala original). Suavizado 80 ms.
  A no cambia la frecuencia del barrido. Se conserva audio cuando la escena se pausa.

Se usa x=rx·cos(v)·cos(12v), y=ry·cos(v)·sin(12v), z=rz·sin(v): una trayectoria
periódica distribuida sobre la superficie, con cobertura de franjas. **No rellena
un continuo bidimensional**. Cada punto previo a proyección satisface la ecuación;
la vista XY puede superponer frente y dorso. La entrada de 50 ms atenúa la señal.

El video dibuja los canales X/Y reales, sin sustituirlos por una malla sombreada.
Su ventana persistente de 50 ms contiene un ciclo completo a 24 Hz. Si el host
muestra menos recorrido, ajustar persistencia/ventana: falta comprobar la opción
exacta en el host instalado. No se declara aceptación visual dentro de osci-render.

`luajit scripts/render_small_studies.lua` verifica F=0 antes de proyección, cotas y
continuidad; genera estos WAV y también ensaya el reproductor de Oblivion.
`python3 scripts/preview_small_studies.py` genera los videos sin sobrescribirlos.
Las salidas WAV sí se reemplazan al renderizar: conservar tomas elegidas previamente.
