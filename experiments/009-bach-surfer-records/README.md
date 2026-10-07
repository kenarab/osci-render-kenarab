# AIRE — Seda y Cristal, superficies récord de SURFER

EXP-035 / REC-01–05. Dos orquestaciones del Adagio favorito, con las mismas 980
notas, rubato y tempo base de 26 BPM (aprox. 5:39). Este experimento conserva 005 y
008. Las pruebas numéricas no sustituyen la escucha ni la comprobación en osci-render.

## Escuchar y probar

1. [Comparación audiovisual de 60 s](../../recordings/009-comparacion.mp4):
   Adagio original → Seda → Cristal, mismo pasaje 30–50 s, RMS igualado a 0.13.
2. Obra completa: [Seda](../../recordings/009-seda.wav) y
   [Cristal](../../recordings/009-cristal.wav).
3. Abrir **un solo Lua** en osci-render, con volumen bajo: `aire-seda.lua` o
   `aire-cristal.lua`. Estos presets ignoran sliders residuales.
4. Para intervenir, abrir `aire-seda-control.lua` o `aire-cristal-control.lua`.

[Seda: voces aisladas](../../recordings/009-seda-voces.wav) y
[Cristal: voces aisladas](../../recordings/009-cristal-voces.wav): cuatro segundos
por voz, todas en C4 y con igual RMS. Permite comparar colores sin confundirlos
con altura, melodía ni volumen. Seda amortigua más los parciales; Cristal conserva
más energía superior. Son intenciones de diseño, no un juicio auditivo confirmado.

| Slider | Qué modifica | Referencia |
| --- | --- | --- |
| A | Tempo de la partitura, integrado y suavizado: 20–36 BPM | 0.375 = 26 BPM |
| B | Brillo, entre dos filtros del mismo material | 0.5 |
| C | Velocidad de rotación de la proyección sonora | 0; movimiento basal lento |
| D | Destaca voz I y reduce acompañamiento | 0 |
| E | Ancho Y de la proyección sonora | 0 |

C/E también afectan el sonido. Estos controles no modifican la ecuación ni la malla.
Mapeo MIDI/OSC y reproducción en el host: pendientes. No hace falta comprar ni
activar Pro para producir estos archivos; no se ha comprobado aquí qué funciones
premium están habilitadas. Para reiniciar, recargar con estado nuevo o incrementar
TAKE (401). El reinicio de step también reinicia la pieza.

## Material geométrico

Las fórmulas se extrajeron de la galería `record_*.jsurf` de
`/Applications/SURFER.app/Contents/Java/JFXSurfer.jar`. `sources.json` conserva las
expresiones, parámetros y hashes del recurso y del JAR. No se modifica la aplicación.

| Voz musical | Superficie | Grado | Récord bibliográfico de nodos |
| --- | --- | --- | --- |
| Violino I | Barth | 6 | 65 |
| Violino II | Togliatti | 5 | 31 |
| Viola | Endrass | 8 | 168 |
| Continuo | Kummer | 4 | 16 |

Referencia: Oliver Labs, [World record surfaces, IMAGINARY (2014)](https://www.imaginary.org/sites/default/files/imaginary-worldrecordsurfaces-oliver-labs.pdf).
Son cifras de la construcción algebraica de referencia, no nodos contados por
nuestro programa. En particular, no esperar ver los 65 nodos de Barth en este
recorte afín. No se afirma que todos los récords de la bibliografía sigan vigentes.

Los cuatro OBJ contienen **caras de superficies**, no curvas aisladas. Se pueden
abrir por separado en osci-render; su reproducción directa no es el timbre del Lua.
`superficies.png` muestra una vista sombreada de referencia. Tanto el PNG como el
video son visualizaciones propias de la malla, no capturas de SURFER/osci-render.

Se extrae F=0 con tetraedros sobre una grilla 32³ y bisección de aristas. Las cajas,
residuos y bordes están en `validacion.json`. Las superficies se recortan: quedan
bordes abiertos y no se agregan tapas falsas. El muestreo puede perder detalles o
conectividad cerca de singularidades; **no certifica la topología ni la totalidad
de la superficie algebraica**. El residuo pequeño sólo comprueba los vértices;
los interiores planos de los triángulos aproximan la superficie.

## Cómo interviene toda la malla en el sonido

Para cada triángulo se toman su área A y centro (x,y,z). Una proyección oblicua
u=x+0.31z+0.13y, v=y−0.27z+0.11x define θ=atan2(v,u) y r=√(u²+v²).
Para h=1…12 se acumula A(0.25+r)·exp(−i(hθ+profundidad)); la profundidad varía con
voz y canal. **Todas las caras contribuyen**, incluidas las partes interiores.
Es una cuadratura de momentos angulares de área, no modos físicos de una membrana.

Los momentos se normalizan, reciben una portadora fundamental explícita de 0.58
para sostener la altura musical aunque la simetría suprima h=1, y filtros de caída
exponencial por voz/estado. Las tablas periódicas resultantes tienen 2048 puntos.
El ataque abre el espectro y el sostenido lo relaja. La geometría se calcula fuera
del audio: Lua interpola tablas y conserva fraseo, vibrato tardío y jerarquía de voces.

El sonido depende de la caja, grilla, proyección y filtro elegidos. Es una decisión
compositiva reproducible, no «el sonido único» de una superficie. No se introduce
ruido aleatorio. La señal filtrada y la suma de voces no satisfacen F=0 y no dibujan
las mallas. La mayor parcial retenida es 12601.63 Hz para este registro; las tablas
con interpolación lineal no garantizan ausencia absoluta de imágenes espectrales.

## Reproducir

```sh
python3 scripts/build_bach_records.py
luajit scripts/check_bach_records.lua
luajit scripts/render_bach_air.lua recordings/009-seda experiments/009-bach-surfer-records/aire-seda.lua
luajit scripts/render_bach_air.lua recordings/009-cristal experiments/009-bach-surfer-records/aire-cristal.lua
python3 scripts/preview_bach_records.py
```

Python estándar y Pillow, LuaJIT y ffmpeg ya instalados. No se instala NumPy ni un
motor geométrico nuevo. El generador utiliza el motor expresivo versionado de 008.
El generador y renderizador reemplazan sus salidas: conservar tomas antes de repetir.
El video rechaza sobrescritura y requiere el WAV original `005-aire-adagio.wav`.

Fuente musical: [Mutopia 242, edición jeff covey, CC BY-SA 3.0](../005-aire-de-bach/SOURCE.md).
Los Lua derivados conservan esa atribución/licencia. No se copiaron imágenes de
la galería; las vistas se generan a partir de las ecuaciones registradas.

## Resultado comprobado

| Versión | Duración | Pico | RMS XY | Salto máximo por muestra |
| --- | --- | --- | --- | --- |
| Seda | 339.066 s | 0.61616 | 0.14789 | 0.07090 |
| Cristal | 339.066 s | 0.62377 | 0.13162 | 0.11091 |

Fin silencioso, reinicio TAKE/step y cambios de controles aprobados; controles
ensayados a 44.1/48 kHz. Residuos de vértices menores que 2.3e-8. No se verificó
rendimiento en el host ni se aprobó la calidad artística. [Métricas de audio](audio-validacion.json).
