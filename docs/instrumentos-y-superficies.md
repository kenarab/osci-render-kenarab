# Diseño: superficies, timbres e instrumentos

Diseño transversal actualizado en EXP-051. La biblioteca no pertenece a una pieza.

| Capa | Responsabilidad | Estado |
| --- | --- | --- |
| Definición de superficie | ID, ecuación, parámetros, dominio, fuente y versión | Catálogo y editor independientes |
| Vista geométrica | Render sombreado de F=0; cámara y recorte | WebGL directo, sin OBJ |
| Receta sonora | Convertir geometría en señal periódica, filtrado y nivel | Momentos de áreas, generación fuera del audio |
| Banco de timbre | Tablas precalculadas identificadas por superficie/receta | Cuatro bancos reutilizables |
| Asignación | Instrumento → banco; ganancia y expresión | Tres grupos en el prototipo de Oblivion; selección A/B/C |
| Pieza | Notas, tiempos, velocidades, pistas y procedencia | Fragmento de Oblivion; sin poseer ecuaciones |
| Salida XY | Proyección/barrido o suma audible | Dos ejercicios de cobertura y mezcla musical diferenciados |

Elegir el mismo banco para flauta y piano no fusiona sus notas ni su articulación.
Cambiar banco usa una mezcla suavizada que mantiene la fase y la reproducción.
En el prototipo los selectores son sliders por limitación de la interfaz Lua; una
interfaz propia podrá mostrar nombres y una miniatura por instrumento.

## Qué cambia en tiempo real

**Implementado:** ecuación/parámetro a en el editor visual; cámara; selección de
bancos de sonido ya calculados por instrumento; brillo y tempo. El control de
escena del ejercicio geométrico está separado de la frecuencia del barrido.

**Pendiente:** editar una ecuación y sustituir su banco sonoro durante el audio.
Se propone una cola de trabajos por superficie: conservar la última versión válida,
calcular el nuevo banco fuera del hilo de audio, descartar resultados obsoletos,
normalizar/comprobar cotas y sustituirlo con transición suave. Un cambio de slider
visual puede ser inmediato mientras el banco sonoro aún se calcula: la interfaz
debe mostrar esa diferencia, no fingir sincronía. Latencia objetivo por medir.

**Integración pendiente:** verificar TCP GPLA con la app instalada y decidir un
transporte para actualizar bancos. GPLA transporta trazos geométricos; por sí solo
no actualiza tablas Lua ni resuelve polinomios. Mantener ambos problemas separados.
No se modifica C++/JUCE ni se promete que la compra Pro resuelva este enlace.

## Probar con el usuario

1. [Esfera y elipsoide](../experiments/010-superficies-legibles/README.md): evaluar
   si la cobertura es reconocible en osci-render, ajustar ventana/persistencia.
2. [Oblivion](../experiments/011-oblivion-asignable/README.md): escuchar primero el
   preset; cambiar un instrumento por vez y anotar combinaciones preferidas.
3. En Pro, comprobar nombres/rangos de sliders, mapeo externo, cambios sostenidos
   y rendimiento. El usuario ya confirma Pro funcionando; mapeo físico y aceptación humana siguen pendientes.

La complejidad geométrica no garantiza buen timbre. Tampoco asignar una superficie
al instrumento hace que su forma sobreviva a la suma XY de todas las voces.

## Corrección de aceptación visual — 2026-10-07 (EXP-040)

El usuario observa que los poliedros resultan reconocibles en 3D, pero no las
superficies algebraicas de las pruebas. No considerar satisfecho el objetivo
visual por tener una malla o un render sombreado separado.

Hallazgos comprobados al revisar las rutas musicales:

- `experiments/008-bach-materias/engine.lua.in`, usado también por 009: cada
  banco sólo tiene X/Y y comienza con `gz=0`. Rotar ese plano no recupera la
  geometría original. El filtrado espectral y la mezcla tampoco la conservan.
- `library/algebraic_surfaces/player.lua.in`, prueba de Oblivion: retorna
  `{x*fade,y*fade,0}`. Es una salida plana y una suma de voces, no una superficie.
- 010 sí recorre puntos XYZ sobre esfera/elipsoide antes de proyectar; sigue
  siendo un barrido de franjas con legibilidad dependiente de ventana/persistencia.
  Su apariencia en el host aún no está aceptada por el usuario.
- El editor WebGL es una ruta distinta: busca raíces por cambios de signo. Puede
  perder raíces tangentes/hojas finas. Las mallas de récords además recortan dominios
  no compactos. No adjudicar a la síntesis un problema observado en ese editor.

Corrección propuesta: probar una sola superficie, conservando coordenadas XYZ
originales hasta la proyección; comparar con su referencia sombreada usando la
misma cámara y dominio, sin suma de voces ni transformación espectral. Evaluar
cobertura, uniones entre recorridos y persistencia antes de buscar un timbre musical.
No corregirlo agregando una Z arbitraria a los bancos: eso no reconstruye F=0.
La ruta tímbrica sigue siendo útil, pero no cuenta como representación geométrica.

Pendiente: localizar con el usuario si la comparación refiere al Lua del host,
a los videos o al editor; realizar la corrección en esa ruta y comprobarla allí.

## Identidades tímbricas intercambiables durante una interpretación

Requisito explícito del usuario (EXP-051 / INS-08…12): todos los proyectos con
partituras o MIDI deben permitir asignar y cambiar identidades tímbricas por voz
durante la ejecución. Alcance: Bach, Piazzolla, Daft Punk y repertorio futuro.
Esto complementa el instrumento de superficies sin partitura.

Flujo: **partitura/MIDI → voces estables → asignaciones → motores de timbre → salida**.
La pieza conserva eventos y procedencia. Un ID de voz identifica una parte musical,
no cada nota simultánea ni necesariamente cada pista MIDI. La agrupación de pistas
(por ejemplo, ambas manos del piano) es explícita y modificable en la sesión.
Los nombres originales «flauta», «piano» o programas GM son metadatos/importación;
no obligan a que esa voz conserve un sonido de flauta o piano.

| Objeto | Datos y responsabilidad |
| --- | --- |
| Identidad tímbrica de biblioteca | ID/version, motor, superficie y receta cuando corresponda, parámetros, articulación por defecto y calibración de nivel |
| Voz de la pieza | ID estable, pistas/canales de origen y eventos musicales; sin motor incrustado |
| Asignación de sesión | Voz → identidad/version; ajustes de expresión, ganancia y parámetros por voz |
| Escena de interpretación | Conjunto de asignaciones y ajustes recuperable durante la ejecución |
| Mapeo de controlador | Control físico → voz/parámetro/escena; independiente de los eventos de notas |

Una identidad puede usar barrido XYZ de superficie, banco derivado de geometría
o síntesis aditiva, por formantes u otra receta. Cada motor declara si conserva
F=0, produce sólo audio derivado o dispone de una vista geométrica de referencia.
No presentar el fundido entre dos geometrías como otra superficie algebraica
verificada. En escena visual, mantener objetos por voz; su mezcla sonora es aparte.

### Cambio durante notas sostenidas

La acción habitual será elegir otro timbre por nombre para una voz y escucharlo
mediante transición suave, sin reiniciar notas, transporte ni otras voces.
Conservar identidad de nota, altura, estado de pedal, tiempo de envolvente y
expresión. Cuando los motores no compartan fase, mantener dos instancias durante
el fundido, iniciar la entrante en el estado musical vigente y entregar futuros
note-off/pedal a ambas hasta retirar la saliente. No prometer continuidad de fase
entre motores incompatibles. Articulación nueva se aplica a notas nuevas; notas
sostenidas requieren adaptar su envolvente sin un nuevo ataque.

Propuesta inicial: fundido configurable de 20–500 ms (80 ms por defecto), con
cota de ganancia durante solapamiento y compensación de nivel por identidad.
Validar duración real de transición: el suavizado exponencial actual con constante
de 80 ms no equivale a terminar un fundido en 80 ms. La calibración evita saltos
bruscos de nivel, pero la equivalencia perceptual exige escucha.

### Preparación y operación en vivo

- Preparar antes de tocar una paleta de identidades y escenas; cálculo geométrico
  y construcción de bancos fuera del hilo de audio. Cambiar entre recursos listos.
- Mostrar voz, identidad actual, destino y estado «preparando/listo/error». Un
  recurso ausente o fallido conserva el último timbre válido.
- Cambios rápidos reemplazan el destino pendiente y usan un número acotado de
  motores; no acumular generaciones ni cortes al recibir muchos mensajes.
- Sliders/interfaz y MIDI CC apuntan al mismo modelo de asignación. Selectores
  discretos requieren estabilidad cerca de umbrales para evitar oscilaciones.
  El protocolo OSC y el mapeo real de Pro se verificarán antes de prometerlos.
- Guardar escenas con versiones y parámetros, sin duplicar la partitura ni
  modificar el preset de biblioteca al ajustar una voz. Recuperación de escena
  agrupa cambios para que las voces no queden temporalmente en escenas distintas.

### Estado y siguiente implementación

Oblivion 011 ya cambia cuatro bancos en tres grupos mediante A/B/C, con fase y
notas conservadas dentro del mismo motor. No cumple todavía el diseño general:
lista/grupos fijos, sin catálogo por nombre, escenas, adaptación entre motores
ni controles externos verificados. Bach y los solos XYZ no heredan esa capacidad.

Próximo incremento: extraer el modelo genérico de voces/asignaciones a partir de
011; elegir dos identidades precargadas para una voz; probar el intercambio con
nota sostenida y después reutilizarlo en Bach sin modificar sus eventos. Añadir
escenas y mapeo físico después de verificar ese contrato. No se implementa este
ruteo general con la presente actualización documental.
