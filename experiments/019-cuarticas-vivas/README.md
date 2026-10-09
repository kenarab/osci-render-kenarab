# Cuárticas vivas: seis y ocho lóbulos

EXP-056 / LOB-01…05. Ejercicio pequeño, independiente del repertorio.
Las dos familias permiten cambiar **el coeficiente de la ecuación en vivo**,
con coordenadas XYZ y sin archivos OBJ intermedios.

Primero abrir el [visor 3D sin audio](index.html): elegir una familia, mover
Deformación y arrastrar para girar la cámara. Las caras permiten reconocer la
superficie; el barrido de referencia se activa aparte. El visor no controla Pro.

| Familia | Ecuación | Inicio / rango de a | Lua preset | Lua controlable |
| --- | --- | --- | --- | --- |
| Seis lóbulos | `(x²+y²+z²)²-a(x⁴+y⁴+z⁴)=1` | .92 / 0–.96 | [seis-lobulos.lua](seis-lobulos.lua) | [seis-lobulos-control.lua](seis-lobulos-control.lua) |
| Ocho lóbulos | `x⁴+y⁴+z⁴-a(x²y²+y²z²+z²x²)=1` | .88 / 0–.94 | [ocho-lobulos.lua](ocho-lobulos.lua) | [ocho-lobulos-control.lua](ocho-lobulos-control.lua) |

Son familias suaves y compactas construidas para este estudio. La primera tiene
prolongaciones sobre los seis semiejes; la segunda sobre las ocho diagonales.
En a=0, la primera es una esfera y la segunda una cuártica redondeada.
Los rangos elegidos mantienen positivo el denominador radial. No se les atribuyen
récords de singularidades: las superficies de SURFER siguen en la biblioteca
existente y su barrido musical completo es otro pendiente.

## Controles en osci-render

Abrir primero el preset, luego la variante `-control.lua`, con sliders en Static
para comparar. Para esta prueba visual conviene empezar con volumen bajo. La
ruta XYZ conserva la forma y no tiene limitación espectral; su sonido puede
resultar áspero. La prueba de timbres musicales intercambiables está en 015–018.

| Slider | Función | Valor inicial normalizado |
| --- | --- | --- |
| A | Deformación: `a=max*A` | Seis: .958333; ocho: .936170 |
| B | Giro de escena 0–.2 rad/s; 0 congela orientación | .5 |
| C | Portadora longitudinal 55–165 Hz | .5 → 110 Hz |
| D | Cobertura latitudinal 3–11 Hz | .5 → 7 Hz |
| E | Radio máximo de salida .4–.8 | .75 → .7 |

A/C/D/E se suavizan con constante temporal de 80 ms; no se reinician fases al
cambiar. B=0 conserva el barrido y el audio. Al subir A se estrechan los cuellos
y sobresalen los lóbulos. La escala uniforme se adapta para que el radio máximo
permanezca constante: comparar la forma, no sólo el tamaño. E es escala de XYZ,
y por tanto también modifica nivel de audio; brillo/color se ajustan en el host.

La parametrización evalúa la ecuación en cada muestra, con solución radial
cerrada. No se filtran coordenadas ni se suman voces. La salida incluye rotación
3D y escala uniforme; F=0 se verifica al deshacer esas transformaciones.

El visor usa las mismas fórmulas, cámara con profundidad y 9024 triángulos por
familia. Sólo reconstruye la malla al editar a. Su trazo es una ventana de 144 ms
a 110/7 Hz, no una captura del host ni seguimiento de los sliders de Pro.

## Evidencia y prueba humana pendiente

- [Validación Lua](validacion-lua.json): tres tasas, residuo <2.2e-14, salida
  acotada por .8, energía en XYZ, 512/512 celdas angulares en un segundo,
  pausa, deformación sostenida y reinicio. Cobertura discreta, no prueba de
  relleno continuo en un visualizador.
- JS: mallas/recorridos sobre F=0, sin caras degeneradas, cota radial y contraste
  entre lóbulos y cuellos. WebGL: selección, deformación, restauración y cámara.
- [Seis lóbulos](../../recordings/019-seis-lobulos.png) y
  [ocho lóbulos](../../recordings/019-ocho-lobulos.png): capturas del visor local,
  no de osci-render.
- Pendiente: que se distingan en Pro con tu configuración; respuesta al MIDI
  físico y evaluación del sonido. Las pruebas numéricas no resuelven esa aceptación.

Para tu prueba: comparar primero las caras del visor con el preset en Pro,
pausar giro con B=0 y mover A. Después variar C y D por separado. Si el aspecto
no coincide, registrar archivo, valores A–E y configuración del visualizador.

Reproducir sin activar audio:

```sh
python3 scripts/build_lobed_surfaces.py
luajit scripts/check_lobed_surfaces.lua
node scripts/check_lobed_gallery.cjs --math-only
node scripts/check_lobed_gallery.cjs
```

`lobed.lua`, `lobed.js` y la plantilla son biblioteca independiente. El generador
escribe sólo 019; mantiene intactos los estudios anteriores y los proyectos .osci.
