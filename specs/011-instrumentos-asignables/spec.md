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
