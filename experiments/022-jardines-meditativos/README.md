# Jardines meditativos — tres instrumentos continuos

EXP-059 / MED-01…06. Música original sin partitura, sin final silencioso. No se
modificaron los estudios anteriores ni tu sesión. Esta serie recupera el registro
grave, voces sostenidas y superficies legibles, sin el vocoder de 020.

## Empezá por escuchar

Con volumen bajo, abrir un **sonido fijo**: ignora los sliders heredados y entra
en 1.5 s. No depende de archivos MIDI ni de notas entrantes.

| Estudio | Sonido fijo | Con controlador | Superficie XYZ fija | XYZ con controlador | Extracto directo |
| --- | --- | --- | --- | --- | --- |
| Claustro de luz | [Lua](claustro-sonido.lua) | [Lua](claustro-sonido-control.lua) | [Lua](claustro-xyz.lua) | [Lua](claustro-xyz-control.lua) | [36 s WAV](../../recordings/022-claustro.wav) |
| Jardín suspendido | [Lua](jardin-sonido.lua) | [Lua](jardin-sonido-control.lua) | [Lua](jardin-xyz.lua) | [Lua](jardin-xyz-control.lua) | [36 s WAV](../../recordings/022-jardin.wav) |
| Memoria de agua | [Lua](memoria-sonido.lua) | [Lua](memoria-sonido-control.lua) | [Lua](memoria-xyz.lua) | [Lua](memoria-xyz-control.lua) | [36 s WAV](../../recordings/022-memoria.wav) |

- **Claustro:** cuártica de seis lóbulos, fundamental Do2, quinta estable y voces
  que se desplazan entre colores menores y mayores. Un bordón para explorar despacio.
- **Jardín:** cuártica de ocho lóbulos, Re2, tercera y séptima más luminosas. Las
  voces tienen respiraciones distintas y el acorde cambia sin reataques.
- **Memoria:** superficie de Roman, La1, quinta y voces medias, espacio estéreo
  amortiguado. Sus autointersecciones son parte de la forma, no errores de dibujo.

El WAV no incluye Polygonizer, Delay ni demás efectos de tu sesión. Para comparar
el Lua, usá una copia de proyecto con esos efectos desactivados. El motor ya tiene
espacio estéreo; el Delay del host se suma a él. No se cambió ninguna configuración.

## Ocho perillas, el mismo mapa

En los archivos `-control`, poner los sliders en Static y mapear cada uno a un
CC de tu controlador mediante el aprendizaje MIDI de tu Pro. Los CC 20–27 son
una propuesta; se pueden elegir otros. Esto no instala ni configura el hardware.

| Slider / CC propuesto | Qué hacés | Valor inicial normalizado |
| --- | --- | --- |
| A / 20 | Deformar la superficie; en sonido interpola su banco tímbrico | .91 / .86 / .50 según estudio |
| B / 21 | Giro de escena: 0 congela la orientación sin cortar sonido ni barrido | .40 |
| C / 22 | Registro continuo La1–La2; conserva relaciones entre voces | .25 / .417 / 0 |
| D / 23 | Cobertura XYZ, 4.3–9.7 vueltas/s; no cambia tempo musical | .50 |
| E / 24 | Expresión: 0 silencio, 1 máximo del motor | .65 |
| F / 25 | Brillo sonoro: parciales suaves a más presentes | .28 |
| G / 26 | Espacio estéreo: seco a mayor resonancia | .35 |
| H / 27 | Profundidad de respiración y duración de evolución armónica | .40 |

A/E/C actúan en ambas versiones. B/D sólo cambian XYZ. F/G/H sólo cambian sonido.
En XYZ no se filtran las coordenadas. No hay un mando único llamado velocidad:
giro, barrido y ritmo armónico son independientes. CC suavizados en 150 ms,
salvo B=0, que congela la escena inmediatamente. C cambia altura de forma continua,
sin cuantización: para notas estables usá los valores iniciales.

Los controles heredados del host sí afectan `-control`: **E=0 silencia**. Por eso
primero escuchar el preset fijo. Los presets ignoran A–H; el volumen y los efectos
globales del host siguen actuando sobre ellos.
Se puede reiniciar la escena con Reset Step Counter; no hace falta buscar una
sección con bajo porque estos instrumentos son continuos.

## Una pequeña performance

1. **Llegada:** Claustro, F=.15/G=.25/H=.30. Sostener el registro; subir E lentamente.
2. **Apertura:** mover A despacio y abrir F hasta .6; G=.6 deja mayor espacio.
3. **Suspensión:** en XYZ llevar B a cero: forma inmóvil con barrido activo. Explorar A.
4. **Regreso:** volver al sonido, F=.15, H=.25; bajar E para cerrar a mano.

Cambiar de archivo reinicia ese instrumento: no es una transición entre motores
sin corte. Estas acciones son propuestas artísticas, no presets aceptados por escucha.

## Geometría y timbre: dos rutas honestas

[Referencia 3D con caras](index.html): selección de las tres formas iniciales,
cámara y barrido de 200 ms. Es una referencia local sin audio, MIDI ni sincronización
con Pro; no sigue cambios de A. No requiere exportar OBJ.

En los Lua XYZ cada muestra es un punto real 3D, con cobertura angular, rotación
y escala uniformes. En sonido se mezclan cuatro voces y dos resonadores: **esa
salida es audio estéreo con z=0; su dibujo no es la superficie**. El audio geométrico
XYZ puede ser áspero. Abrir un Lua sonoro y pretender ver la cuártica no funciona.
Todavía no hay una ruta comprobada que produzca ambas salidas independientes
simultáneamente en un único archivo/host; las versiones se prueban por separado.

Ecuaciones antes de escala/rotación, con A normalizado:

- Claustro: `(x²+y²+z²)² − a(x⁴+y⁴+z⁴) = 1`, `a=.5+.46A`.
- Jardín: `x⁴+y⁴+z⁴ − a(x²y²+y²z²+z²x²) = 1`, `a=.5+.44A`.
- Memoria: `X²y²+X²z²+y²z²−Xyz=0`, `X=x/(.7+.6A)`; parte compacta parametrizada.
  No incluye las extensiones de los ejes del conjunto implícito de Roman.

Banco: ocho estados de forma, momentos ponderados por área de **todas las caras**,
fase de profundidad, fundamental explícita y cuatro bandas (2/4/8/12 parciales).
Dos brillos y canales, interpolación entre estados sin recálculo por muestra.
No son frecuencias propias físicas ni superficies récord de SURFER. La selección
de banda limita parciales bajo .4*sample_rate; interpolación/modulación pueden
introducir imágenes residuales. No se promete ausencia absoluta de aliasing.

## Evidencia y reproducción

[Manifiesto](manifest.json), [validación](validacion.json). Pruebas geométricas y DSP
aprobadas a 16/44.1/48 kHz, incluidos controles, silencio, reinicio y presets.
La calidad artística, profundidad percibida, brillo en Pro y MIDI físico quedan
pendientes del usuario. No se deducen de cotas ni de ecuaciones correctas.

```sh
python3 scripts/build_meditative_gardens.py
luajit scripts/check_meditative_gardens.lua
node scripts/check_meditative_gallery.cjs
```

Sin dependencias nuevas. Lua/bancos y mallas regenerables locales; biblioteca,
generador, especificación y pruebas versionados. WAV/capturas fuera de Git.
