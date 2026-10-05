# Superficies que suenan

Laboratorio de arte y ciencia: superficies algebraicas, música de osciloscopio y
live coding con osci-render. Surfer Shuffle es un antecedente del proyecto; queremos
trabajar tanto con superficies elegidas como con generación aleatoria reproducible.

- [Objetivos, etapas y herramientas](docs/objetivos.md)
- [Primera sesión con osci-render](docs/primer-arranque.md)
- [Estudio de un toro — composición de 80 segundos](experiments/002-estudio-de-un-toro/README.md)
- [Registro de experimentos solicitados](docs/experimentos.md)
- [Hallazgos y estado de las pruebas](docs/bitacora.md)
- [Instrucciones para agentes](AGENTS.md)

Los ejemplos de `experiments/001-primeras-curvas/` se abren como archivos Lua en
osci-render. Se pueden comprobar sin audio usando:

```sh
lua scripts/check_curves.lua
```

Este repositorio contiene nuestros experimentos, no el código fuente de osci-render.
