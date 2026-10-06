# Control con potenciómetros y visualización

Los estudios `003-orbitas` y `004-cristal` leen los sliders Lua A–E de osci-render.
Funcionan con todos en cero; no necesitan un controlador para comenzar. El estudio
original del toro conserva su versión ya escuchada y no tiene estos mapeos.

## Cinco controles comunes

| Slider | Parámetro | Rango / efecto |
| --- | --- | --- |
| A | Tempo | 72–126 BPM en Órbitas; 108–189 en Cristal |
| B | Forma | Ensancha los ejes y amplía el recorrido sobre la superficie |
| C | Rotación | Aumenta la velocidad de cámara de 0.12 a 0.77 rad/s |
| D | Presencia visual | Sube el mínimo entre notas de 60% a 90%; reduce la pulsación de tamaño |
| E | Registro | Transposición continua de 0 a +12 semitonos |

Los cambios tienen suavizado de 35 ms y las notas un deslizamiento de 12 ms.
El tempo se integra: mover A no salta de sección. Los controles alteran el sonido
y la imagen juntos; D no es un brillo óptico independiente. Los sliders fuera
de 0–1 se acotan. Mantener la ganancia de salida del host moderada.

## Conectar un controlador MIDI

Actualización 2026-10-06: el usuario confirma el requisito premium para MIDI Learn
interno. Recomendamos probar el mapeo del host en REAPER; ver
[comparativa premium, Live y REAPER](midi-premium-live-reaper.md).
La ruta física hacia el plugin gratuito sigue pendiente de verificación.

### Encontrar los controles con el mouse

**Comprobación posterior en la app 2.9.9.10:** el panel Lua estaba abierto pero
desplazado a **H–O**, con M editado. Los estudios entregados usan **A–E**; M no
tiene función en ellos. Desplazar la lista hacia arriba. Esto confirma la presencia
del panel, no una prueba física MIDI/OSC ni su persistencia al guardar.

En el código de la versión 2.9.9.3, `Lua Sliders` aparece **debajo del editor Lua**
y se oculta cuando se cierra ese editor. Abrir un archivo `.lua`, expandir el
editor con su flecha lateral y ampliar la zona inferior arrastrando el separador
horizontal si quedó comprimida. Los controles A–E de ese panel son los sliders
de pantalla; las variables `slider_a`…`slider_e` leen sus valores. No hay que
instalar Lua ni tener un dispositivo conectado para moverlos.

Si un slider está animado por un modulador, quitar esa asignación para la prueba
manual. Los nombres exactos de menú y la visibilidad deben comprobarse en la
versión instalada; esta explicación se basa en `Source/PluginEditor.cpp`, no en
una interacción ya realizada con la app del usuario.

### Mapear el dispositivo

1. Conectar el controlador USB/MIDI y configurar los potenciómetros para enviar
   **CC absolutos** (0–127), no encoders relativos. Marca/modelo aún por confirmar.
2. En ajustes de audio/MIDI de osci-render, habilitar su entrada MIDI.
3. Abrir el estudio y localizar **Lua Sliders**. Probar A–E con el mouse primero;
   dejarlos en 0 para escuchar la versión de referencia.
4. Si la edición instalada ofrece **MIDI Learn**, usar el menú contextual del
   slider, iniciar aprendizaje y mover un solo potenciómetro. Repetir con A–E.
5. Guardar el proyecto y comprobar que conserva las asignaciones al reabrir.

Habilitar la entrada del dispositivo y activar notas MIDI del sintetizador son
cosas diferentes. Estas piezas tienen secuenciador propio: evitar disparar voces
adicionales con notas del teclado al mapear los CC.

Las [notas oficiales de versión](https://github.com/jameshball/osci-render/releases)
describen aprendizaje de CC desde el menú contextual dentro de las novedades
premium. Por eso **no se da por disponible en la instalación gratuita**. Si no
aparece, una alternativa es cargar el plugin en una DAW y mapear el controlador a
sus parámetros `Lua Slider A`…`E` usando el sistema de esa DAW. No se ha verificado
todavía el mapeo físico; no es necesario comprar nada
para probar los sliders con el mouse.

El contrato 0–1 y los nombres `slider_a`…`slider_e` se comprobaron en la copia local
2.9.9.3 (`LuaDocumentationComponent.cpp` y `PluginProcessor.cpp`), además de la
[wiki oficial](https://github.com/jameshball/osci-render/wiki).

### OSC y MIDI son rutas diferentes

- Controlador USB MIDI → MIDI CC → parámetro del host → slider Lua: ruta directa
  cuando la edición del host ofrece el aprendizaje correspondiente.
- Controlador OSC → receptor/puente OSC a MIDI → host → slider Lua: requiere un
  receptor adicional si no hay entrada OSC nativa comprobada. Una DAW también
  puede actuar como intermediaria si soporta el mapeo necesario.

No se encontró una entrada OSC de parámetros documentada en la revisión de
README/wiki y fuentes disponibles. La copia contiene módulos ausentes: no se
afirma que sea imposible, pero no se inventan direcciones como `/slider_a` ni un
puerto de escucha. Si el controlador ya envía MIDI, no necesita pasar por OSC.
No se instaló ningún puente ni se abrió un puerto.

### Por qué los estudios anteriores no resolvían la lentitud

En AIRE, A aumenta el tempo base de 38 a 54 BPM y C aumenta la rotación; esos
rangos no permiten ralentizar mucho ni detener la escena. La densidad aparente
proviene además de sumar voces con distintas frecuencias. No se corrige todo
bajando el tempo. El nuevo [contrato SDD](../specs/001-instrumento-superficies/spec.md)
separa escena y barrido, incluye pausa visual y prioriza una sola superficie
legible. Ese comportamiento está especificado, todavía no implementado.

## Si la figura casi no se ve

Falta aclarar si el problema es tamaño/brillo en el visualizador o exportación de
video. Como primera medida, los nuevos estudios mantienen un mínimo de amplitud
entre notas y tienen control D para reducir cuánto se achican. Los finales siguen
apagándose y terminan en silencio.

Probar sin efectos y con la visualización XY. La figura depende de los ajustes
de proyección, persistencia y ganancia de visualización del host. Si el problema
persiste, registrar versión, ajustes o mensaje exacto antes de cambiar más cosas.

## Videos de previsualización

Generamos MP4 de la señal estéreo calculada directamente por Lua, con dibujo XY
y audio. **No son capturas de osci-render**, ni reproducen su fósforo, efectos o
cámara adicional. Cada fotograma muestra 1/30 s de trayectoria real, sin inventar
una geometría distinta de la señal. El WAV mantiene el audio PCM sin compresión;
el AAC del MP4 es para mirar/escuchar, no para alimentar un osciloscopio físico.

Desde la raíz, con LuaJIT, Python/Pillow y ffmpeg ya disponibles en este Mac:

```sh
mkdir -p recordings
luajit scripts/check_live_studies.lua recordings
python3 scripts/preview_xy.py recordings/003-orbitas.wav recordings/003-orbitas.mp4
python3 scripts/preview_xy.py recordings/004-cristal.wav recordings/004-cristal.mp4
```

El renderizador no sobrescribe un video existente. Los archivos generados quedan
en `recordings/`, fuera de Git. Para repetir un estudio dentro del host, aumentar
`TAKE`; para repetirlo automáticamente, establecer `LOOP = true`.
