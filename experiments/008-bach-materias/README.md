# AIRE — Cuárticas y Prisma

Dos orquestaciones nuevas del **Adagio favorito**, con las mismas 980 notas,
26 BPM de base, rubato y duración de aproximadamente **5:39**. No sustituyen
`005-aire-de-bach/aire-adagio.lua`. Estado: pruebas numéricas aprobadas; escucha
artística y reproducción en osci-render pendientes.

## Probar sin escribir Lua

Primero escuchar `recordings/008-comparacion.mp4`: tres fragmentos del mismo
pasaje (30–50 s), a volumen RMS comparable: Adagio anterior, Cuárticas y Prisma.
Después abrir en osci-render **un solo archivo**:

- `aire-cuarticas.lua`: cuatro timbres derivados de superficies polinómicas.
- `aire-prisma.lua`: cuatro timbres de modulación de fase, con evolución espectral.

Los presets ignoran sliders residuales. Comenzar con volumen bajo. Los WAV completos
son `recordings/008-cuarticas.wav` y `008-prisma.wav`. Para comparar los timbres sin
confundir altura con color, `008-cuarticas-voces.wav` y `008-prisma-voces.wav` tocan
C4 durante cuatro segundos por voz, en orden 1–4, igualados a RMS 0.13.

## Qué cambia en las voces

| Voz | Cuárticas: coeficientes (a,b,c) | Prisma: razón de modulación / índice máximo | Intención tímbrica, por escuchar |
| --- | --- | --- | --- |
| Violino I | (1,3,6), recorrido vertical a 2 ciclos | 2 / 1.25 | Cantabile con armónicos y vibrato tardío |
| Violino II | (5,1,2), recorrido a 3 ciclos | 3 / 0.65 | Contraste más hueco y contenido |
| Viola | (2,5,1), recorrido a 4 ciclos | 1 / 1.70 | Centro más denso, con evolución al sostener |
| Continuo | (1,1,4), recorrido a 2 ciclos | 2 / 0.38 | Base oscura, menos parciales altos |

Son instrumentos sintéticos, no emulaciones de cuerdas o bandoneón. El ataque
abre el espectro y el sostenido lo relaja, con distintas velocidades por voz.
Conservamos la respiración, las cadencias y la jerarquía del Adagio. No agregamos
ruido aleatorio, barridos de cientos de líneas ni reverberación que desfigure XY.

## Superficie completa y sonificación

Cada voz usa la superficie regular cerrada

```text
a*x^4 + b*y^4 + c*z^4 + k*(x^2+y^2+z^2) = 1
```

Los coeficientes positivos garantizan una intersección positiva por rayo. Para una
dirección unitaria d, q=a*dx^4+b*dy^4+c*dz^4 y
`r²=2/(k+sqrt(k²+4q))`. Esto construye la malla completa y permite comprobar F=0
sin un solver iterativo. No es un ejemplo singular ni un récord de SURFER.

`cuartica-1.obj`…`cuartica-4.obj` contienen caras, no sólo curvas. Cada una tiene
1106 vértices, 2208 triángulos, aristas compartidas por dos caras y Euler 2.
`superficies.png` es la vista sombreada de referencia, con k=0.05. Se pueden abrir
los OBJ por separado en osci-render para investigar el trazado, pero su reproducción
como OBJ **no es el mismo timbre** que la sonificación de los Lua.

La señal proviene de un recorrido periódico sobre cada superficie, proyección
XY, extracción de Fourier y amortiguación de parciales. Precalculamos dos estados,
k=0.8 y k=0.05, y conservamos 12 armónicos. El audio interpola tablas de 2048 puntos.
El filtrado, la mezcla de estados y la suma de voces **no siguen siendo puntos
exactos de F=0**. El slider de color interpola señales; no es aún un editor de
coeficientes con actualización de malla en vivo. Esta distinción mantiene pendiente
la integración SURFER completa (specs/006).

Prisma usa `phase=t+I*sin(ratio*t+0.18*sin(t))`, con dos índices por voz, seguida
de la misma extracción espectral. No atribuimos estas señales a una superficie.
La mayor componente retenida de la partitura, incluyendo margen de vibrato, es
12601.63 Hz, debajo de Nyquist a 44.1/48 kHz. La interpolación lineal de tablas
puede introducir imágenes débiles: no afirmamos eliminación absoluta de aliasing.
No se ofrece este banco para transponer arbitrariamente a registros más altos.

## Controles opcionales

Abrir la variante `-control.lua` sólo para manejar sliders A–E:

| Control | Acción | Valor de referencia |
| --- | --- | --- |
| A | Tempo integrado: 20–36 BPM | 0.375 = 26 BPM |
| B | Brillo: mezcla de estados espectrales | 0.5 |
| C | Velocidad de cámara | 0 |
| D | Destacar solista y reducir acompañamiento | 0 |
| E | Ancho de la proyección Y | 0 |

Los cambios se suavizan en 80 ms. C y E también modifican el sonido; no son
controles ópticos independientes. Mapeo MIDI/OSC en el host aún sin verificar.
Para reiniciar, recargar con estado nuevo o incrementar TAKE (301) si el host
conserva variables. Cambiar de familia o reiniciar step también reinicia la pieza.

## Reproducir y verificar

```sh
python3 scripts/build_bach_materials.py
luajit scripts/check_bach_materials.lua
luajit scripts/render_bach_air.lua recordings/008-cuarticas experiments/008-bach-materias/aire-cuarticas.lua
luajit scripts/render_bach_air.lua recordings/008-prisma experiments/008-bach-materias/aire-prisma.lua
python3 scripts/preview_bach_materials.py
```

La comparación requiere el WAV anterior `recordings/005-aire-adagio.wav`.
El generador de video conserva resultados existentes y rechaza sobrescribirlos.
El renderizador WAV sí escribe el prefijo elegido: elegir otro para conservar tomas.
No se instalan dependencias nuevas: Python/Pillow, LuaJIT y ffmpeg ya estaban.

Resultados de render a 48 kHz:

| Versión | Duración | Pico | RMS XY | Salto máximo |
| --- | --- | --- | --- | --- |
| Cuárticas | 339.066 s | 0.65084 | 0.14034 | 0.05410 |
| Prisma | 339.066 s | 0.60245 | 0.15805 | 0.08890 |

Fin silencioso, reinicio TAKE y cambios de controles aprobados. El ensayo específico
recorre 44.1/48 kHz con controles extremos y reinicio. No reemplaza una escucha ni
mide rendimiento dentro de osci-render. Fuente musical y atribución CC BY-SA 3.0:
[Mutopia 242 / edición jeff covey](../005-aire-de-bach/SOURCE.md). Los Lua contienen
notas derivadas de esa edición y conservan esa licencia.
