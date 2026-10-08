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
| EXP-004 | Usar superficies algebraicas elegidas, más allá de la generación aleatoria | Mallas 006 y prototipo sonoro 007; host pendiente | Partir de una ecuación registrada, producir curvas o malla y comprobar la visualización en osci-render. Conservar ecuación, dominio, parámetros y método de recorrido. |
| EXP-005 | Recuperar o adaptar el generador aleatorio de superficies de Surfer Shuffle | Pendiente; código original por localizar | Reproducir una superficie con la misma semilla y parámetros y evaluar su uso musical. El enlace del proyecto está disponible; su código no se importó. |
| EXP-006 | Live coding de superficies | Pendiente | Editar una ecuación o sus parámetros durante la ejecución y observar/escuchar cambios. Registrar latencia y comportamiento ante errores. Ejecutar archivos existentes no verifica este punto. |
| EXP-007 | Integración directa del renderizador de superficies con osci-render | Lua autónomo 007 preparado; integración en host pendiente | Demostrar un flujo ecuación → geometría recorrible → osci-render. Precisar si usa Lua, archivos o streaming, sin presumir una API inexistente. |
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
| EXP-018 | Incorporar Solitude de Piazzolla como referencia | Suite Lumière confirmada por usuario; dos demos de audio obtenidas | [Semilla](proyecto-piazzolla/semilla.md): faltan partitura completa/MIDI; no confundir con Années de solitude. |
| EXP-019 | Corregir el enfoque: visualizar superficies algebraicas completas, no solo curvas | Prototipo geométrico implementado; host pendiente | Mallas implícitas de toro/Cassini con caras, OBJ y vista sombreada; falta verificar legibilidad y rendimiento en osci-render. |
| EXP-020 | Diseñar sonidos desde superficies, en vez de notas MIDI como motor | Prototipo 007 implementado; host pendiente | Malla de toro con caras, raster de 24 vueltas y comparación 3D/XY; no relleno continuo. SUP-R01–R04. |
| EXP-021 | Controlar lentitud y pausa con slider, separando velocidades | Implementado y probado fuera del host | 007: A movimiento/pausa, B barrido; pausa de 10 s con audio a 44.1/48 kHz. Mouse/hardware pendientes. |
| EXP-022 | Implementar SDD y aclarar acceso a sliders/ruta OSC | Flujo SDD y guía implementados; conexión pendiente | specs/README.md; localización del panel verificada en fuentes; OSC nativo no confirmado. |
| EXP-023 | Conseguir un timbre más lindo | Variantes 007 no aceptadas: suenan como estática y no gustan | Suave/Cuerpo/Aire, WAV y videos; métricas aprobadas no equivalen a calidad. WAV más limpio que Lua/host, pero tampoco gusta. Rediseño tímbrico y diferencia de reproducción pendientes. |
| EXP-024 | Air de Bach más lento y expresivo; superficies para futuros timbres profundos | Adagio implementado; última preferencia del usuario: su versión favorita | BAC-R01–R05: base 26 BPM y 5:39. Antes se pidió más velocidad (EXP-025); el 2026-10-06 se elige Adagio como referencia; superficies y timbre siguen en EXP-020/023. |
| EXP-025 | Controlar tempo y expresión de Bach: el Adagio resultó demasiado lento | Implementado; nueva escucha pendiente | AIRE EXPRESIVO, preset 32 BPM, controles 20–52 BPM, expresión/articulación/color/balance; audio de 4:35 y muestra de 60 s. |
| EXP-026 | Timbres distintos por voz y ejecución menos robótica | Cuatro perfiles implementados; aceptación auditiva pendiente | Recorridos/filtros por voz, fraseo/vibrato y microdesfases deterministas; comparación de cuatro notas C4 de 6 s a igual RMS. |
| EXP-027 | Explorar narraciones visuales y sonoras que relaten una historia | Storyboard propuesto; obra pendiente | specs/005: aparición, encuentro, tensión y transformación; cada gesto visual debe tener consecuencia audible identificable. |
| EXP-028 | Modificar superficies con controles y representarlas completas, como en demos | Investigación inicial; editor/malla dinámica pendientes | Distinguir malla sombreada de barrido XY. Referencia aclarada: SURFER y superficies singulares (specs/006). Editor implícito/coeficientes y puente al host pendientes. |
| EXP-029 | Investigar antecedentes y sentido de integrar IanniX con osci-render | Investigación documentada; integración pendiente | No se encontró antecedente exacto. Ruta propuesta IanniX → OSC → REAPER → parámetros de osci-render; verificar un cursor y un coeficiente. |
| EXP-030 | Comparar premium, Live y REAPER para MIDI y conexión futura con IanniX | Investigación completada; prueba física pendiente | [Comparativa y protocolo](midi-premium-live-reaper.md). Verificar un CC → Lua Slider A, guardar/reabrir y luego un mensaje OSC; no comprar antes de comprobar parámetros expuestos. |
| EXP-031 | Nuevas versiones del Bach favorito con timbres por voz basados en superficies u otras síntesis complejas | Cuárticas y Prisma implementados; escucha y host pendientes | [008](../experiments/008-bach-materias/README.md): dos Lua/presets y controles, WAV de 5:39, ocho voces aisladas, comparación de 60 s; mallas completas y análisis espectral. |
| EXP-032 | Avanzar con la música de Piazzolla | Fuentes MIDI concretas localizadas e importador preparado; archivos/arreglos pendientes | [Repertorio](referencias-piazzolla.md): Libertango y Oblivion; importación probada con tempo/polifonía, sin atribuir notas inventadas a Piazzolla. |
| EXP-033 | Reunir arreglos públicos y planificar la mayor base de datos posible de Piazzolla en otro repositorio | Plan y traspaso preparados; ejecución diferida por el usuario | [Atlas Piazzolla](proyecto-piazzolla/README.md): ATL-01–09, modelo, fases y semillas. Un HTML obtenido; ningún arreglo musical descargado aún. |
| EXP-034 | Experimento semilla: coleccionar variantes y formatos de Piazzolla y preparar lengua franca | 21 originales válidos, 13 derivados y catálogo local; escucha/OMR pendientes | [Semilla](proyecto-piazzolla/semilla.md): 10 MIDI, 3 MXL, 5 PDF, 1 imagen, 2 demos MP3; dos fallos vacíos, 90 fichas candidatas. SEM-01–07. |
| EXP-035 | Bach con timbres complejos derivados de superficies récord de SURFER/IMAGINARY | Seda y Cristal implementados; escucha y host pendientes | [009](../experiments/009-bach-surfer-records/README.md): cuatro mallas SURFER, WAV completos, voces aisladas y comparación. REC-01–05. |
| EXP-036 | Separar superficies de Bach y editar ecuaciones/parámetros con visualización inmediata, sin OBJ | Biblioteca y editor WebGL implementados; enlace sonoro pendiente | [Editor](../apps/surface-lab/README.md): seis ejemplos, slider a, estado JSON; probar integración TCP real. ALG-R07–10. |
| EXP-037 | Constructor visual por factores para divulgar métodos de geometría algebraica y un Shuffle estructurado | Proyecto pendiente, especificado; no implementado | [Constructor](../specs/010-constructor-algebraico/spec.md): árbol/factores, recetas atribuidas, restricciones y semilla; sin lenguaje natural. |
| EXP-038 | Ejercicios pequeños donde se reconozcan superficies en el XY real | Esfera/elipsoide implementados; aceptación visual en host pendiente | [010](../experiments/010-superficies-legibles/README.md): barrido de cobertura y videos de 10 s, sin reemplazar XY por malla. |
| EXP-039 | Prueba sencilla de Piazzolla con timbres elegibles dinámicamente por instrumento | Oblivion 30–70 s implementado; escucha/Pro pendientes | [011](../experiments/011-oblivion-asignable/README.md): flauta/fagot/piano, bancos independientes, transición 80 ms. INS-02–05. |
| EXP-040 | Corregir pérdida de forma 3D de superficies frente a poliedros | Causas identificadas en Lua musicales; localización con usuario pendiente | [Diagnóstico](instrumentos-y-superficies.md#corrección-de-aceptación-visual--2026-10-07-exp-040): bancos planos y suma de voces no conservan geometría; aceptación requiere probar la misma superficie en la salida real. |

**Criterio corregido:** EXP-001/002/010/012 son estudios de recorridos y música;
no completan por sí solos EXP-004 ni el requisito de visualizar superficies.

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

## EXP-041 — Repetir ejercicios con XYZ conservado

**Pedido del usuario; prototipo verificado, aceptación humana pendiente.**
Una voz aislada primero: violín de Bach y flauta de Oblivion en pruebas separadas.
Esfera, elipsoide y cuártica como ejercicios pequeños; mallas SURFER como referencia.
Criterio: puntos XYZ sobre F=0, soporte tridimensional, caras reconocibles y controles
separados de tempo/barrido/giro; comprobar forma y sonido dentro del host.
Evidencia: `experiments/012-superficies-xyz/README.md`, especificación XYZ-01…05 y
pruebas Lua a 44.1/48 kHz. Pendiente: escucha, host, timbres de superficies récord
y asignación dinámica. El sonido anterior y el nuevo no tienen aceptación artística.

## EXP-042 — Recuperar salida del host para XYZ y Bach

**Incidencia reportada por el usuario; diagnóstico abierto.** Ambos dejan de
producir salida percibida. Criterio: recuperar dibujo y audio de esfera y de un
Bach previamente funcional, identificando el ajuste o fallo responsable.
Evidencia inicial: punto fijo en esfera, sin error Lua visible; efecto identidad
no explica el fallo al probar bypass; registro con reinicios a 16 kHz. Dispositivo
real y causa sin confirmar. LuaJIT produce señal a esa frecuencia; no equivale a
prueba en host. No modificar geometría para corregir una causa aún desconocida.

## EXP-043 — Recorte cuadrado, saturación y poca profundidad

Pedido del usuario. Reiniciar resolvió EXP-042 según escucha del usuario. En host,
ganancia 2.1787 y Threshold .2947; al pasar a .30 y 1 desaparece el contorno cuadrado
observado. Escucha pendiente. Corregir orientación/giro de XYZ sin aplanar ni filtrar.
Criterios NIV-01…03 en specs/013-nivel-relieve.

## EXP-044 — Partituras Daft Punk

Pedido: descargar y elegir 2–3 arreglos de buena calidad; proponer cuatro temas.
Something About Us confirmado; propuestas Digital Love, Harder Better Faster
Stronger y Get Lucky. Criterio DP-01: procedencia, formato real, legibilidad y
alcance comprobados. Conversiones revisadas a MIDI/MusicXML pendientes.

## EXP-045 — Efecto vocal robótico en osciloscopio

Pedido del usuario de explorar vocoder. Primera propuesta: vocales sintéticas
con formantes y articulación, ensayo original sin voz grabada ni letra de temas.
Criterios DP-02…04: parámetros útiles, margen, XYZ y WAV diferenciados; aceptación
artística en host pendiente. Vocoder de análisis de voz real no implementado aquí.

Resultado inicial EXP-044: dos arreglos descargados y revisados por muestreo;
ver docs/repertorio-daft-punk/README.md. EXP-045: prototipo y WAV disponibles en
experiments/013-voz-robotica; pico .20 y pruebas de controles a tres frecuencias
aprobadas. No hay transcripción completa de Daft Punk ni aceptación artística aún.

## EXP-046 — Groove y selección Daft Punk actualizada

Pedido del usuario: priorizar Giorgio by Moroder, Instant Crush y groove de Lose
Yourself to Dance, conservando Something About Us. Fuentes de los nuevos títulos
y arreglos completos pendientes. Ensayo original `013-voz-robotica/groove-disco.lua`
y WAV 24 s, bombo/bajo/vocales; GRV-01/02. Picos <.145 a 16/44.1/48 kHz, reinicio
aprobado. No es transcripción. Aceptación de groove y escucha pendientes.

## EXP-047 — Control de nivel general para Lua

Consulta/pedido de diseño: compresor o limitador común frente a calibración por
archivo. Investigación registrada en docs/niveles-y-dinamica.md (GRV-03).
Propuesta: ganancia calibrada por instrumento + limitador final sólo en escucha,
referencia geométrica separada. Compresor nativo no confirmado; sin instalación.
Criterio pendiente: controlar picos sin recorte previo ni cambios XY desiguales,
comparar audición y geometría. Ningún procesador garantiza buen timbre de todo Lua.

## EXP-048 — Recuperar tamaño visual sin subir audio

Pedido explícito: revisar la configuración porque las imágenes quedaron pequeñas.
Image Scale localizado en Visualiser Settings del código local, condicionado a
Premium; distinto del efecto general Scale. Criterio: ampliar ambos ejes igual,
sin recorte ni aumento audible, conservando Bach como referencia. Prueba en host
pendiente: la herramienta UI falló al iniciar. No se modificó la sesión.
Detalles y procedimiento en docs/niveles-y-dinamica.md.

## EXP-049 — Oblivion en Pro: entrada y transporte

Pedido: revisar Oblivion que no funciona. Comprobado: el solo tenía 11.7392 s
sin notas y ambas variantes finalizaban en silencio; no se confirmó la causa
del fallo en host. INS-06/07: solo recortado con entrada a 250 ms, variantes loop
y de una pasada, cambio de modo reinicia. Dos vueltas a 16/44.1/48 kHz aprobadas;
solo conserva F=0. Pro registrado a 16 kHz: riesgo de aliasing del banco.
No se alteró la sesión ni se reprodujo audio durante el curso. Host/escucha pendientes.

## EXP-050 — Cuártica con portadora y cobertura separadas

Pedido: continuar superficies algebraicas. Propuesta del agente: ensayo sin
partitura con portadora 110 Hz, cobertura 7 Hz y giro independiente; A–D en Lua.
CUA-01…04: XYZ sobre F=0, biblioteca separada, referencia con caras y captura
del barrido real, WAV 6 s sin normalizar. Residuo <2.7e-15 y 128/128 celdas
angulares en un segundo a 16/44.1/48 kHz; pico <.400. Sonido y Pro pendientes.
No se afirma que una superficie más compleja garantice timbre más agradable.
Ver experiments/014-cuartica-tonal/README.md.

## EXP-051 — Identidades tímbricas por voz, intercambiables en vivo

Pedido explícito: diseño común a los proyectos con partituras/MIDI para elegir
y cambiar fácilmente identidades por voz durante una interpretación. INS-08…12
registran separación de pieza/biblioteca/asignación, notas sostenidas, escenas,
precarga, niveles y controles. Diseño documentado; implementación general pendiente.
Aceptación: reutilizar identidades en Bach y Oblivion, cambiarlas sin reiniciar
notas/tempo/otras voces, sin notas colgadas, con escenas recuperables y prueba Pro.
El selector de cuatro bancos/tres grupos de 011 es antecedente, no cumplimiento
general ni mapeo de controlador comprobado.

## EXP-052 — Bach y Oblivion con identidades por voz, en carpetas nuevas

Pedido: implementar Bach asignable, entregar Lua accesible de Oblivion y preservar
los estudios ya usados. VIV-01/02/04/05/06: nuevos 015 y 017, mismo motor con
asignación A–D, tempo E, expresión F, giro G. Preset y archivos controlables;
mezcla sonora derivada separada de solos XYZ. Oblivion Lua en su propia carpeta,
ignorado por Git por procedencia musical, con manifest y generador reproducible.
Verificado a 16/44.1/48 kHz: cambios sostenidos sin reiniciar fases/eventos/tempo,
histéresis, reinicio/loop y F=0 en solos. WAV de 20 s de ambos. Cota de mezcla
para todo el repertorio a expresión máxima: Bach .270, Oblivion .351. Escucha,
controlador y host pendientes. No se modificaron experimentos 001–014 ni .osci.

## EXP-053 — Diversidad geométrica más allá de esfera/elipsoide

Pedido explícito: formas más diversas y visibles; cuárticas anteriores no convencen.
Propuesta implementada en 016: toro, Roman (parte compacta), doble cono recortado
y Cassini de dos lóbulos. Cuatro presets XYZ y cuatro controlables, galería 3D
con caras y captura de referencia; no OBJ ni proyección anterior al retorno Lua.
VIV-03: residuo F=0 <1.1e-15; galerías y cámara verificadas en Chrome WebGL2.
No son superficies récord SURFER ni timbre aceptado; pendiente validación Pro.

## EXP-054 — Riqueza visual como configuración separada

Pedido: revisar colores tenues/oscuridad; tamaño ya ampliado por el usuario en Pro.
Controles localizados en código: Line Colour, Screen Colour, Light Effects e
Image Scale. Procedimiento en docs/niveles-y-dinamica.md; aplicación y comparación
pendientes. Aceptación: mismo Lua/cámara con mejor legibilidad y audio sin cambios.
La configuración no sustituye diversidad de superficies ni densidad del barrido.
