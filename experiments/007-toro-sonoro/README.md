# Toro sonoro — tres timbres, una superficie

Primera implementación de SUP-R01–R07 y TIM-R01–R06. Prueba pequeña, sin partitura:
el recorrido de un toro produce todo el sonido. No es aún una composición larga.

**Resultado posterior:** el usuario escucha estática al abrir los Lua en osci-render.
El WAV le suena más limpio, pero **tampoco le gusta el timbre**. Esta dirección sonora
no fue aceptada. Las métricas de abajo son técnicas, no de calidad artística.
Se conserva la prueba como evidencia; la diferencia WAV/host sigue por diagnosticar.
[Revisión y ruta con IanniX](../../docs/iannix-superficies.md).

## Escuchar y comparar

Abrir **`recordings/007-comparacion.mp4`**: 36 segundos, Suave → Cuerpo → Aire.
Cada variante dura 12 segundos, con el mismo barrido, superficie inicial, cámara
y ganancia. Diferencia de RMS: **0.395 dB**, sin normalizar cada variante.

El video muestra tres paneles: superficie sombreada, barrido XY sin tratamiento
y señal XY audible tratada. La misma escala se usa para ambos trazados. Es un
render de los Lua, **no una captura de osci-render**. El sombreado no viene del audio.
Los MP4 usan AAC; conservar los WAV estéreo para la señal X/Y sin compresión.

| Variante | Lua para abrir directamente en osci-render | Audio / video en `recordings/` |
| --- | --- | --- |
| Suave | [suave.lua](suave.lua) | `007-suave.wav` / `007-suave.mp4` |
| Cuerpo | [cuerpo.lua](cuerpo.lua) | `007-cuerpo.wav` / `007-cuerpo.mp4` |
| Aire | [aire.lua](aire.lua) | `007-aire.wav` / `007-aire.mp4` |

Estos tres archivos son presets: suenan con valores internos, sin encontrar ni
configurar sliders. No reciben las perillas. Para eso abrir **[control.lua](control.lua)**.
No hace falta instalar Lua, conectar MIDI ni cargar el OBJ para probar el sonido.
Empezar con volumen bajo y sin efectos adicionales del host. El Lua suena de
forma continua; los clips incluyen un cierre de 0.4 s para terminar suavemente.

## Intervenir con los sliders de pantalla

Abrir `control.lua`. Expandir el editor Lua; `Lua Sliders` está debajo del código.
Si quedó comprimido, ampliar la zona inferior con el separador horizontal.
Ubicación comprobada en fuentes locales 2.9.9.3; interfaz instalada pendiente.
Poner **E en 0**, ajustar A–D y subir E lentamente a **0.35**:

| Slider | Función | Rango | Prueba inicial |
| --- | --- | --- | --- |
| A | Movimiento de escena | `0.20 A²` rad/s; 0 detiene tras suavizado | 0.25 |
| B | Barrido y altura del sonido | `20 × 6ᴮ` Hz; 20–120 Hz | 0.50 (~48.99 Hz) |
| C | Radio menor del toro | `0.18 + 0.12 C`; no cambia el radio mayor 0.62 | 0.50 |
| D | Calidez | Atenúa armónicos del tubo; 0 brillante, 1 suave | 0.90 |
| E | Nivel | Ganancia `0.75 E`; 0 silencia | 0.35 |

Mover A hasta cero: la escena se detiene, el recorrido que genera sonido continúa.
Mover B: cambia la altura y el barrido, no la velocidad de cámara.
Mover D: suaviza el sonido y adelgaza el tubo visible. Los controles tienen 80 ms
de suavizado; la parada no es instantánea. Datos numéricos inválidos conservan el
último valor válido. Incrementar `TAKE` para reiniciar; las fases siempre se integran.

**MIDI/OSC siguen sin prueba física.** MIDI CC requiere verificar MIDI Learn en
la edición instalada; OSC nativo no está confirmado. La prueba con mouse no
demuestra conexión de hardware. [Guía de conexión](../../docs/controlador-y-visuales.md).

## Superficie y sonido: relación exacta y límite de la representación

```text
F(x,y,z) = (x²+y²+z²+R²−r²)² − 4R²(x²+y²) = 0
R = 0.62; r = 0.18 + 0.12 C; dominio [-0.92,0.92]³
x = (R+r cos v) cos u; y = (R+r cos v) sin u; z = r sin v
u = θ; v = 24θ; dθ/dt = 2π × barrido
```

`toro.obj` conserva una **malla cerrada con caras**: 3072 vértices, 6144 triángulos,
Euler 0, residuo <1e-12, para C=0.5. Las geometrías se generan fuera del audio;
el callback solo evalúa la parametrización y controles. Sin aleatoriedad ni semilla.
La malla entregada es la referencia del preset; no se actualiza como archivo al mover C.

El audio recorre una curva cerrada con 24 vueltas poloidales: es una representación
de resolución finita de la superficie, **no un relleno continuo de todos sus puntos**.
La malla y la comparación sombreada evitan confundirla con toda la superficie.
Se ve toda la trama, incluso su parte posterior; no hay eliminación de líneas ocultas.
Para cualquier punto del toro, una vuelta del barrido pasa a una distancia como
máximo `(R+r)π/24` (≤0.121 para los radios admitidos): aún quedan huecos visibles.

El círculo central genera el armónico 1 y los términos del tubo, los armónicos
23, 24 y 25. Calidez multiplica esos tres por `g=1−0.75 D` antes de proyectar:
equivale exactamente a otro toro con **radio menor `r g`**, no a conservar la misma
superficie después de tratarla. La referencia izquierda mantiene r y el panel
derecho informa el radio audible. Suave usa D=0.90; Cuerpo, D=0.15; Aire, D=0.55
con modulación sinusoidal de ±0.20 ligada al movimiento de escena (~12.57 s/ciclo
en el preset). No se añade ruido ni un oscilador musical ajeno a la geometría.

Es una síntesis de pocos grupos de armónicos. La extensión a otras superficies
y timbres más complejos/profundos, incluido Bach, sigue pendiente.

## Reproducir y verificar

Desde la raíz del repositorio, con LuaJIT, Python/Pillow y ffmpeg ya disponibles:

```sh
python3 scripts/build_surface_instrument.py
luajit scripts/check_surface_instrument.lua recordings
python3 scripts/preview_surface_instrument.py
```

Editar `engine.lua.in` y regenerar: los cuatro `.lua` son entregables autónomos.
El render de video no sobrescribe videos existentes. Para otra toma, crear un
directorio y pasarlo a los dos últimos comandos. Audio, reportes e imágenes de
previsualización permanecen fuera de Git en `recordings/`.

| Variante | Pico XY | RMS XY | Delta máximo entre muestras |
| --- | --- | --- | --- |
| Suave | 0.18322 | 0.09465 | 0.00335 |
| Cuerpo | 0.21866 | 0.09905 | 0.00870 |
| Aire | 0.20796 | 0.09628 | 0.00726 |

Verificados: residuo del toro, señal finita, DC medio <0.001 en ambos canales,
clips con delta <0.04, pausa durante 10 s, barrido independiente, E=0, valores
inválidos y reinicio, a 44.1/48 kHz. Cambios extremos de controles: delta <0.16.
Son cotas numéricas para detectar saltos grandes, no pruebas de agrado auditivo.

Espectro estático verificado sobre muestras del Lua en los extremos 20/120 Hz:
solo armónicos 1/23/24/25, hasta 3000 Hz; residuo de energía relativa <1e-16.
Todos quedan por debajo de Nyquist a ambas tasas. Esto no certifica ausencia de
aliasing bajo cualquier automatización externa o efecto del host.
Prueba local LuaJIT: 48000 muestras en ~0.037 s de CPU; no mide el hilo de audio del host.

Pendientes: diagnóstico WAV frente a host, ajustes tímbricos, ejecución/performance
en osci-render, persistencia de sliders, MIDI físico, OSC y live coding de ecuaciones.
