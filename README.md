# Superficies que suenan

Laboratorio de arte y ciencia: superficies algebraicas, música de osciloscopio y
live coding con osci-render. Surfer Shuffle es un antecedente del proyecto; queremos
trabajar tanto con superficies elegidas como con generación aleatoria reproducible.

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
- [Hallazgos y estado de las pruebas](docs/bitacora.md)
- [Instrucciones para agentes](AGENTS.md)

Los ejemplos de `experiments/001-primeras-curvas/` se abren como archivos Lua en
osci-render. Se pueden comprobar sin audio usando:

```sh
lua scripts/check_curves.lua
```

Este repositorio contiene nuestros experimentos, no el código fuente de osci-render.
