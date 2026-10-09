# Superficies que suenan

Laboratorio de arte y ciencia: superficies algebraicas, música de osciloscopio y
live coding con osci-render. Surfer Shuffle es un antecedente del proyecto; queremos
trabajar tanto con superficies elegidas como con generación aleatoria reproducible.

- [Editor de ecuaciones en vivo, sin OBJ](apps/surface-lab/index.html) · [Instrucciones](apps/surface-lab/README.md)
- [Biblioteca reutilizable de superficies](library/algebraic_surfaces/README.md)
- [Constructor visual por factores — proyecto pendiente](specs/010-constructor-algebraico/spec.md)
- [Diseño de timbres por instrumento y pruebas pequeñas](docs/instrumentos-y-superficies.md)
- [Objetivos, etapas y herramientas](docs/objetivos.md)
- [Primera sesión con osci-render](docs/primer-arranque.md)
- [Estudio de un toro — composición de 80 segundos](experiments/002-estudio-de-un-toro/README.md)
- [Órbitas — elipsoide con controles en vivo](experiments/003-orbitas/README.md)
- [Cristal — superficie de cuarto grado](experiments/004-cristal/README.md)
- [AIRE — cuatro voces de Bach en el espacio](experiments/005-aire-de-bach/README.md)
- [Superficies implícitas: mallas y vista sombreada](experiments/006-superficies-implicitas/README.md)
- [Piazzolla: las cinco obras de referencia](docs/referencias-piazzolla.md)
- [Potenciómetros MIDI y previsualizaciones en video](docs/controlador-y-visuales.md)
- [Registro de experimentos solicitados](docs/experimentos.md)
- [Toro sonoro: tres timbres y controles de movimiento](experiments/007-toro-sonoro/README.md)
- [Bach: tempo controlable, expresión y cuatro timbres](experiments/005-aire-de-bach/README.md#nueva-versión-controlable-aire-expresivo)
- [SDD: especificaciones y plan del instrumento de superficies](specs/README.md)
- [IanniX, OSC y superficies completas: hallazgos y próxima prueba](docs/iannix-superficies.md)
- [Hallazgos y estado de las pruebas](docs/bitacora.md)
- [Instrucciones para agentes](AGENTS.md)

Los ejemplos de `experiments/001-primeras-curvas/` se abren como archivos Lua en
osci-render. Se pueden comprobar sin audio usando:

```sh
lua scripts/check_curves.lua
```

Este repositorio contiene nuestros experimentos, no el código fuente de osci-render.

## Nuevos experimentos — 2026-10-08

Los estudios anteriores permanecen intactos. Empezar por:

- [015 — Bach con timbres por voz](experiments/015-bach-voces-vivas/README.md):
  Lua completo, A–D para identidades, E tempo, F expresión, G giro; solos XYZ aparte.
- [016 — Superficies diversas](experiments/016-superficies-diversas/README.md):
  toro, Roman, doble cono y Cassini; Lua y galería con caras.
- [017 — Oblivion con Lua en la carpeta](experiments/017-oblivion-voces-vivas/README.md):
  preset, controles y vistas XYZ por instrumento. Archivos musicales sólo locales.

Mezcla sonora derivada y geometría por voz son salidas distintas; comparar con
la galería antes de evaluar la configuración del visualizador de osci-render.

- [018 — Daft Punk: arreglos largos](experiments/018-daft-repertorio/README.md):
  cuatro pares de Lua preset/control y WAV íntegros de los archivos fuente; Giorgio
  es un arreglo reducido, no la versión original completa.

- [019 — Cuárticas vivas](experiments/019-cuarticas-vivas/README.md): familias
  de seis/ocho lóbulos, deformación por coeficiente en Lua y visor 3D sin audio.

- [020 — Bajos de sintetizador y vocoder](experiments/020-bajos-vocoder/README.md):
  Lose Yourself to Dance/Giorgio, subgrave, filtro resonante y vocoder de 12 bandas.
