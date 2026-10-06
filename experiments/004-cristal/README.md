# Cristal de cuarto grado

Estudio de 71.11 segundos con sliders en cero: 32 compases en 4/4 a 108 BPM.
Arpegios menores, registro más grave y un recorrido más denso que Órbitas.
Abrir `estudio.lua` en osci-render. Reiniciar incrementando `TAKE`.

La curva se mantiene sobre `(x/a)⁴+(y/b)⁴+(z/c)⁴=1` antes de cámara y envolvente.
Es una superficie algebraica cuártica, de aspecto más cuadrado que un elipsoide;
se obtiene por normalización radial, sin generar una malla ni resolver raíces
de un polinomio implícito general durante el audio.

- 0–17.78 s: presentación.
- 17.78–53.33 s: desarrollo y mayor profundidad.
- 53.33–71.11 s: retorno y salida.

Estas duraciones corresponden a A=0. [Controles A–E, MIDI y videos](../../docs/controlador-y-visuales.md).
Previsualización local: `recordings/004-cristal.mp4`; audio: `recordings/004-cristal.wav`.
La verificación comprueba el polinomio y la señal; la escucha en el host queda pendiente.
