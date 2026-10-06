# Registro de experimentos

Este registro reúne los pedidos de la conversación. Las propuestas concretas del
agente se identifican aparte: todavía no son resultados ni decisiones del usuario.
Actualizar este archivo cada vez que se solicite o se pruebe un experimento.

## Pedidos del usuario

| ID | Experimento o investigación | Estado | Criterio de aceptación / evidencia |
| --- | --- | --- | --- |
| EXP-001 | Instalar osci-render y ejecutar pruebas mínimas | Ejecutado por el usuario | Confirmó instalación y ejecución de círculo, Lissajous y recorrido sobre toro. Los considera demasiado simples. Validación matemática previa en Lua y LuaJIT; ajustes y grabación aún no registrados. |
| EXP-002 | Composición más compleja, como las de los videos, idealmente con geometría algebraica | Primer prototipo implementado; evaluación en osci-render pendiente | [Estudio de un toro](../experiments/002-estudio-de-un-toro/README.md): 80 s, tres secciones, secuenciador y geometría animada. Falta evaluación del usuario sobre imagen y sonido. |
| EXP-003 | Investigar quién compuso música de osciloscopio usando esta clase de geometría | Primera búsqueda realizada | Referencias primarias abajo; distinguir composición paramétrica de superficies implícitas generales. No se afirma una búsqueda exhaustiva. |
| EXP-004 | Usar superficies algebraicas elegidas, más allá de la generación aleatoria | Pendiente | Partir de una ecuación registrada, producir curvas o malla y comprobar la visualización en osci-render. Conservar ecuación, dominio, parámetros y método de recorrido. |
| EXP-005 | Recuperar o adaptar el generador aleatorio de superficies de Surfer Shuffle | Pendiente; código original por localizar | Reproducir una superficie con la misma semilla y parámetros y evaluar su uso musical. El enlace del proyecto está disponible; su código no se importó. |
| EXP-006 | Live coding de superficies | Pendiente | Editar una ecuación o sus parámetros durante la ejecución y observar/escuchar cambios. Registrar latencia y comportamiento ante errores. Ejecutar archivos existentes no verifica este punto. |
| EXP-007 | Integración directa del renderizador de superficies con osci-render | Pendiente de prototipo | Demostrar un flujo ecuación → geometría recorrible → osci-render. Precisar si usa Lua, archivos o streaming, sin presumir una API inexistente. |
| EXP-008 | Pruebas de temas para disfrutar y desarrollar el proyecto de arte y ciencia | Objetivo continuo | Guardar piezas o sesiones reproducibles y notas sobre qué funciona musical y visualmente. Aún no hay temas específicos seleccionados. |
| EXP-009 | Controlar parámetros clave con potenciómetros | Sliders A–E implementados en los dos nuevos estudios; hardware pendiente | Tempo, forma, rotación, presencia y registro. Falta marca/modelo, edición instalada y prueba de mapeo MIDI CC. |
| EXP-010 | Crear dos estudios más, similares al toro | Implementados; escucha en host pendiente | Órbitas (elipsoide, 60 s) y Cristal (cuártica, 71.11 s), con WAV y previsualizaciones XY. |
| EXP-011 | Mejorar/aclarar la salida visual, casi invisible según el usuario | Pendiente de aclaración; primera mejora preparada | Nuevos estudios con mayor presencia entre notas, slider D y videos directos XY. Falta distinguir problema del visualizador frente a exportación. |
| EXP-012 | Crear una obra especialmente elaborada basada en el Air de Bach | Adaptación implementada; valoración en host pendiente | AIRE, 3:50, cuatro voces de Mutopia 242, repeticiones AABB, fraseo, toros por voz y cinco controles. Video y audio reproducibles; fuente/licencia documentadas. |
| EXP-013 | Explicar qué hace el código y cómo intervenir, aclarando controlador directo frente a software adicional | Guía preparada; conexión física pendiente | Explicación del audio como recorrido XY, ejercicio con cinco perillas y rutas MIDI Learn/DAW según edición. Falta controlador y versión instalada. |
| EXP-014 | Incorporar Libertango de Piazzolla como referencia | Catalogado; versión y análisis pendientes | Fuente editorial/discográfica y siguiente paso en referencias-piazzolla.md. |
| EXP-015 | Incorporar Oblivion de Piazzolla como referencia | Catalogado; versión y análisis pendientes | Fuente editorial localizada; no se importó un arreglo. |
| EXP-016 | Incorporar Violentango de Piazzolla como referencia | Catalogado; versión y análisis pendientes | Fuente editorial/discográfica localizada. |
| EXP-017 | Incorporar Meditango de Piazzolla como referencia | Catalogado; versión y análisis pendientes | Fuente editorial/discográfica localizada. |
| EXP-018 | Incorporar Solitude de Piazzolla como referencia | Identidad exacta por confirmar | Candidato: Solitude de Suite Lumière; no confundir con Années de solitude. |

Las cinco referencias se desarrollan en [Repertorio Piazzolla](referencias-piazzolla.md).

El usuario indicó que le gusta mucho EXP-002; la evaluación sonora es positiva,
pero reportó dificultades para ver lo visual. Conservar el original como referencia.

## Antecedentes verificados

### Jerobeam Fenderson y Hansi3D — Oscilloscope Music / N-SPHERES

La [presentación del proyecto](https://oscilloscopemusic.com/info/about/) explica
que la misma señal estéreo alimenta los altavoces y los ejes X/Y del osciloscopio.
Es un antecedente directo de composición audiovisual mediante sonido.

[N-SPHERES](https://www.oscilloscopemusic.com/watch/n-spheres) es especialmente
relevante: sus autores describen una construcción basada casi enteramente en
funciones paramétricas y cinco piezas: Function, Intersect, Attractor, Flux y Core.
La publicación vincula el desarrollo a OsciStudio 7 y su live coding. Sirve como
referencia artística y técnica; no demuestra una implementación equivalente en
osci-render ni la evaluación directa de polinomios implícitos arbitrarios.

En [esta explicación de Hansi](https://forum.oscilloscopemusic.com/t/compiling-oscilloscope-paths-to-floppy/624)
se aclara que N-SPHERES utiliza un proyecto propio de C/C++ con elementos muy
específicos. No asumir que sus ejecutables o composiciones están disponibles como
proyectos editables de osci-render. No se compró ni descargó material de pago.

### Live coding de un recorrido toroidal

Un participante publicó [I made a twisted torus!](https://forum.oscilloscopemusic.com/t/i-made-a-twisted-torus/545),
con código y controles de radio, anchura y frecuencias de recorrido en OsciStudio.
La fórmula describe una curva sobre un toro: es un antecedente cercano a nuestro
tercer ejemplo, no una composición compleja terminada ni un barrido de toda la
superficie. Aunque el texto menciona Möbius, no adoptamos esa clasificación para
la fórmula publicada.

### osci-render y Surfer Shuffle

El [repositorio oficial de osci-render](https://github.com/jameshball/osci-render)
incluye demostraciones de Lua, animación desde Blender y automatización en una DAW;
enlaza los proyectos `square_spiral.osci` y `square_spiral.rpp`. Son candidatos
para estudiar estructura y automatización; no los ejecutamos en esta investigación.

[Surfer Shuffle](https://www.imaginary.org/program/surfer-shuffle) documenta la
generación aleatoria de superficies algebraicas basada en jsurf. Queda por
construir y verificar su puente hacia recorridos de audio.

**Límite de la búsqueda:** encontramos precedentes sólidos de composición con
funciones paramétricas y geometría 3D. No encontramos en esta búsqueda breve un
ejemplo verificado de composición que tome superficies implícitas arbitrarias
de Surfer Shuffle y las convierta directamente en música de osciloscopio. Esto
no demuestra que no exista.

## Propuesta aceptada para EXP-002: Estudio de un toro

El usuario aceptó comenzar con esta propuesta. Primer prototipo implementado en
[estudio.lua](../experiments/002-estudio-de-un-toro/estudio.lua): 80 segundos, 96 BPM,
32 compases y tres secciones. Su secuenciador funciona sin MIDI ni dependencias.
La guía del experimento explica reinicio, controles y verificación fuera del host.

1. **Presentación:** un recorrido cerrado sobre el toro, con motivo rítmico y
   rotación lenta que permita reconocer la forma.
2. **Desarrollo:** alternar recorridos y variar radios, orientación y densidad
   según una secuencia musical; evaluar cada cambio tanto por sonido como por imagen.
3. **Retorno:** recuperar el motivo inicial y reducir gradualmente la complejidad.

Base algebraica:

```text
(x² + y² + z² + R² − r²)² − 4R²(x² + y²) = 0, con R > r > 0
```

Podemos recorrer puntos de esta superficie con una parametrización conocida,
sin resolver el polinomio por cada muestra de audio. La rotación cambia su
proyección; modificar los radios cambia la superficie. Hay que distinguir ambos
efectos al documentar la pieza.

La complejidad buscada es también musical: secciones, motivos, tensión, pausas
y transiciones. Añadir líneas por sí solo no satisface el pedido. Sumar señales
XY superpone sus coordenadas y no equivale a dibujar objetos independientes;
evaluar recorridos secuenciales y transiciones antes de añadir capas.

Validación prevista: coordenadas finitas y acotadas, continuidad en cambios de
sección, cierre cuando corresponda, ausencia de saturación y escucha/visualización
en osci-render. Guardar parámetros y versión de la aplicación; no confundir una
prueba matemática aprobada con una composición musical lograda.

## Otras propuestas, todavía no solicitadas por nombre

- **Cortes de una superficie implícita:** pasar de esfera/toro a una superficie
  polinómica menos trivial y comparar secciones planas con aristas de una malla.
- **Variaciones con semilla:** convertir un pequeño conjunto reproducible de
  superficies aleatorias en motivos de una misma pieza, evitando cambios arbitrarios.
- **Estudio de una referencia:** elegir un video concreto y analizar su estructura
  temporal, relación entre sonido e imagen y técnicas que podamos reproducir.

## Datos a guardar al ejecutar cada prueba

ID, archivos/commit, ecuación y dominio, parámetros/semilla, versión de osci-render,
salida y frecuencia de muestreo, procedimiento, resultado observado, apreciación
musical del usuario y próximo cambio. Marcar explícitamente los datos desconocidos.
