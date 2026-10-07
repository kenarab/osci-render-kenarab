# 010 — Constructor visual por factores y Shuffle estructurado

Estado: proyecto pendiente, solicitado por el usuario (EXP-037). No implementado.
Propósito: acercar métodos de investigadores en geometría algebraica al público
mediante construcciones visibles y verificables. No usar lenguaje natural para
inventar superficies. El usuario desea compartir la línea de sonificación con
Surfer Invaders cuando esté preparada; no se ha enviado ni publicado nada.

## Requisitos propuestos a partir del pedido

- FAC-01: representar la expresión como árbol de factores y operaciones, con
  ecuación simbólica visible. Editor visual y fórmula comparten un estado.
- FAC-02: bloques para planos, cuádricas, productos, sumas, potencias y familias
  paramétricas. Mostrar grado formal/cota antes de simplificar y grado efectivo
  sólo cuando se calcule; un cambio paramétrico puede cancelar términos.
- FAC-03: preservar la factorización elegida y sus nombres sin expandir todo por
  defecto; permitir inspeccionar la contribución geométrica de cada factor.
- FAC-04: recetas atribuidas a fuentes primarias, con parámetros y restricciones
  explícitos. No atribuir nodos, récords o propiedades por apariencia de un render.
- FAC-05: Shuffle sobre una receta/gramática y restricciones elegidas; semilla,
  versión, límites y pasos de construcción guardados. Misma semilla y versión
  reproducen la expresión. No prometer que toda variante conserve singularidades.
- FAC-06: biblioteca común alimenta vista implícita y sonificación. Guardar árbol,
  fórmula, dominio, parámetros, fuente y semilla como formato abierto portable.

Ejemplos para un primer prototipo (propuestas del agente):

- Unión de dos superficies: P·Q=0, mostrando por separado P y Q.
- Familia P·Q−a=0 para explorar cómo se transforma esa unión.
- Familia P−a·Q²=0, con receta y atribución revisadas antes de presentarla como
  reproducción de una construcción de investigación.

Plan futuro: definir formato de árbol con nodos nombrados; una receta de dos
factores y slider; edición visual reversible con fórmula; vistas por factor;
Shuffle reproducible con restricciones; sumar recetas documentadas gradualmente.
Pruebas: ida/vuelta árbol↔formato, equivalencia de evaluación, semillas reproducibles,
conservación del último estado válido, render y escucha por separado.

Base actual: biblioteca `library/algebraic_surfaces` y editor matemático
`apps/surface-lab`. Su AST sintáctico es un punto de partida; todavía no conserva
nombres de factores, recetas de investigadores ni un historial de construcciones.
