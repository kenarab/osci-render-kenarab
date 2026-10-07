# 011 — Pruebas pequeñas y asignación dinámica de timbres

EXP-038/039. Pedido: ver superficies en ejercicios pequeños y probar Piazzolla
con instrumentos vinculados a superficies, independientemente de la partitura.

- INS-01: ejercicios de esfera y elipsoide con barrido de cobertura, coordenadas
  sobre F=0 y video del XY real. Etiquetar persistencia/limitación del osciloscopio;
  no sustituir el XY por un render sombreado ni prometer relleno continuo.
- INS-02: bancos de timbres reutilizables identificados por superficie, con ecuación,
  receta y hash. La pieza refiere IDs y asignaciones, sin poseer la geometría.
- INS-03: fragmento de 40 s de Oblivion de la semilla, flauta/fagot/piano, preservando
  simultaneidad, tiempos y velocidades. Las dos pistas de piano son un instrumento.
- INS-04: elegir banco por instrumento durante ejecución, transición suavizada sin
  reiniciar notas. Tempo separado de timbre y de cámara; límites de señal comprobados.
- INS-05: mostrar qué superficie provee el timbre; distinguir asignación sonora,
  geometría sombreada y mezcla XY. No prometer que la suma dibuje los objetos.

Plan: biblioteca de bancos independiente; reproductor Lua genérico con asignación
por instrumento; importación local del fragmento (notas fuera de Git); dos barridos
Lua y videos breves. Pruebas de polifonía, cambios en notas sostenidas, fin y reinicio.
Aceptación musical/visibilidad dentro de osci-render y mapeo físico requieren al usuario.

Configuración en vivo: bancos precalculados y mezcla disponibles en este incremento.
Editar una ecuación arbitraria y regenerar banco de forma asíncrona/versionada queda
pendiente; tampoco se implementa aquí el puente TCP GPLA. No depende de activar Pro.

## INS-06 — Repetición explícita para diagnóstico de silencio

Pedido: Oblivion no funciona en Pro (2026-10-07). La causa en host no está
confirmada. Los reproductores locales terminan en silencio tras 40 s.
Agregar variantes `-loop` y `-loop-control`, conservando las de una pasada.
Repetir sin reconstruir bancos, con fundidos en los extremos; cambiar de variante
reinicia el estado aunque step siga aumentando. Aplicar al reproductor asignable
y al solo XYZ. Verificar actividad antes/después de dos vueltas, fin de la variante
original, reinicio, cambios de modo y salida finita a 16/44.1/48 kHz.
No declarar reparación del host por pasar esta prueba offline.

INS-07: en el solo de Oblivion se comprobó entrada de flauta a 11.7392 s.
Recortar únicamente silencio inicial dejando 250 ms antes de la primera nota;
preservar duraciones y alturas y registrar offset/duración reales. El asignable
con todos los instrumentos conserva sus 40 s. No atribuir al recorte una solución
a fallos de dispositivo. Las verificaciones usan la duración declarada.

## Contrato transversal de interpretación en vivo — EXP-051

Pedido explícito: identidades tímbricas por voz fácilmente intercambiables en
todos los proyectos basados en partituras o MIDI, incluso durante una actuación.
Diseño en docs/instrumentos-y-superficies.md; implementación general pendiente.

- INS-08: separar eventos, voz estable, identidad de biblioteca y asignación de
  sesión. Reutilizar una identidad en distintas piezas y cambiarla sin editar notas
  ni el preset global; agrupación de pistas explícita, sin límite fijo de tres voces.
- INS-09: sustituir timbre en nota sostenida sin reiniciar transporte, altura,
  pedal ni otras voces; transición acotada y sin reataque forzado. Si el motor cambia,
  transferir estado musical, no asumir compatibilidad de fase. Comprobar note-off
  durante el fundido y cambios rápidos; no dejar notas colgadas.
- INS-10: identidad versionada con parámetros, articulación y nivel calibrado;
  admitir superficies XYZ, bancos derivados y otros motores. Declarar qué salida
  conserva geometría; audio mezclado/fundido no certifica una superficie F=0.
- INS-11: paletas precargadas y escenas de asignaciones recuperables sin cargar
  geometría en el hilo de audio. Error o recurso ausente mantiene el timbre válido.
  Acotar instancias/colas y mostrar estado real, sin confirmar éxito anticipado.
- INS-12: interfaz y entradas de control comparten el modelo de asignación;
  nombrar voz e identidad, permitir cambiar una voz o escena completa. Verificar
  MIDI CC/OSC en host antes de declararlos disponibles.

Aceptación pendiente: misma secuencia en Bach y Oblivion con dos asignaciones
intercambiables; eventos/tempo intactos; cambios sostenidos y rápidos sin notas
colgadas; recuperación de escena/versiones; error de carga conservador; cotas de
nivel y coste medidas. Ausencia perceptual de clics y facilidad de uso requieren
escucha y prueba en Pro/controlador. El prototipo 011 sólo cubre una parte de INS-09
entre bancos del mismo motor, con tres grupos fijos.
