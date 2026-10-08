# Cuatro formas distintas: XYZ y referencia con caras

Nuevo experimento VIV-03. [Galería 3D interactiva](index.html) sin audio ·
[Comparación con caras](../../recordings/016-superficies-diversas.png).

| Superficie | Lua autónomo | Lua con controles | Rasgo visible |
| --- | --- | --- | --- |
| Toro | [toro.lua](toro.lua) | [toro-control.lua](toro-control.lua) | Abertura central |
| Roman | [roman.lua](roman.lua) | [roman-control.lua](roman-control.lua) | Autointersecciones y hojas |
| Doble cono | [cono.lua](cono.lua) | [cono-control.lua](cono-control.lua) | Dos conos unidos por el vértice |
| Cassini | [cassini.lua](cassini.lua) | [cassini-control.lua](cassini-control.lua) | Dos lóbulos con cuello estrecho |

A giro 0–.2 rad/s (0 pausa sin parar audio); B portadora 80–160 Hz (centro
recomendado .375=110 Hz); C cobertura 4–12 Hz (.375=7 Hz). El preset autónomo
ignora sliders/LFO de controles. Tamaño de objeto acotado con normalización
uniforme; la ganancia de audio global y Image Scale siguen perteneciendo al host.

Cada Lua devuelve puntos XYZ de su ecuación, sin OBJ ni aplanar Z. La galería
muestra caras y un recorrido de referencia de 143 ms; arrastrar para cambiar cámara.
No es captura del host ni controla el Lua. El ruido percibido depende del recorrido:
estas muestras geométricas **no están filtradas**. Para inspeccionar sin ruido usar
la galería; para comparar timbres usar la mezcla 015/017 derivada de estas formas.

Ecuaciones y constantes en validacion.json y library/performance/identities.json.
Roman representa su parte compacta parametrizada; la ecuación también incluye
extensiones de los ejes no mostradas. Cono recortado en |z|<=.7. Toro/Cassini son
superficies cerradas. No se afirma recuento de singularidades ni topología a partir
de estas mallas. Ninguno es la cuártica radial de los experimentos anteriores.

Pruebas de F=0 sobre retorno Lua, invirtiendo rotación/escala, a 16/44.1/48 kHz:
residuo <1.1e-15; energía XYZ y señal finita comprobadas. Las mallas usan las mismas
constantes. Percepción en Pro y calidad sonora todavía no aceptadas.

Reproducir: `python3 scripts/build_diverse_surfaces.py`.
Verificar Lua: `luajit scripts/check_live_voices.lua`.
Verificar galería: `node scripts/check_diverse_gallery.cjs` (Chrome headless).
