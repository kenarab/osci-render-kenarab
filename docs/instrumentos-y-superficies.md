# Diseño: superficies, timbres e instrumentos

Estado después de EXP-038/039. La biblioteca no pertenece a Bach ni a Piazzolla.

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
   y rendimiento. La instalación/activación y aceptación humana siguen pendientes.

La complejidad geométrica no garantiza buen timbre. Tampoco asignar una superficie
al instrumento hace que su forma sobreviva a la suma XY de todas las voces.
