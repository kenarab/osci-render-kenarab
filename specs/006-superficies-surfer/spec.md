# 006 — Superficies implícitas como en SURFER

Estado: biblioteca y editor implícito implementados; sonificación en vivo e integración con host pendientes.

## Incremento EXP-036: biblioteca y editor independientes (2026-10-07)

- ALG-R07: ecuaciones, procedencia, geometría y herramientas reutilizables viven
  fuera de Bach; proyectos musicales consumen la biblioteca sin apropiarse de ella.
- ALG-R08: campo de ecuación con parámetros, galería, cámara y render implícito
  directo en GPU, sin OBJ. Actualización al editar; conservar última vista válida.
  «Inmediato» es objetivo interactivo, no garantía de latencia en cualquier equipo.
- ALG-R09: parser matemático acotado sin ejecutar JavaScript del usuario; errores
  visibles. Guardar/cargar estado JSON portable; no depender de servicios externos.
- ALG-R10: documentar protocolo real de osci-render antes de prometer enlace.
  Vista sombreada local y trazado de audio son salidas diferentes. El enlace al
  host debe ser explícito, limitado a loopback y permanecer pendiente si no se prueba.

Plan: extraer biblioteca conservando bancos Bach; implementar editor local WebGL
con ray casting de F=0; probar parser, fallos de edición y render en navegador.
Investigar el servidor de objetos del código local como transporte sin archivos.
EXP-004/005/006/028. Referencia explícita: [SURFER](https://www.imaginary.org/program/surfer).
El usuario desarrolló un generador aleatorio y quiere explorar también ejemplos
con singularidades, incluidos los de las galerías de investigación. Un toro o
una curva enrollada no satisfacen por sí solos este objetivo.

- ALG-R01: tomar `F(x,y,z; parámetros)=0` como modelo principal; conservar ecuación,
  dominio, parámetros, fuente y semilla cuando corresponda. Permitir editar un
  coeficiente y ver la superficie sombreada completa en el dominio elegido.
- ALG-R02: seleccionar un ejemplo singular de la galería y verificar su ecuación
  y procedencia antes de atribuirle un récord o número de singularidades. No inferir
  singularidades de píxeles brillantes: estudiar `F=0` y `∇F=0`.
- ALG-R03: tratar singularidades y cambios de topología explícitamente. No exigir
  una malla regular/manifold a todo ejemplo ni suavizar una singularidad sin informarlo.
  Las pruebas de Euler y gradiente no nulo usadas para toros no son universales.
- ALG-R04: calcular geometría/render fuera del audio, con límites de resolución
  y tiempo y conservación del último estado válido ante una edición inválida.
- ALG-R05: mostrar superficie y XY audible por separado. Elegir un barrido o
  sonificación y evaluar su timbre antes de aumentar la densidad geométrica.
- ALG-R06: un control modifica un coeficiente y ambas representaciones lo siguen.
  IanniX puede secuenciar ese control; no sustituye el renderizador implícito.

Siguiente incremento: enlazar un ejemplo verificado, un coeficiente, una vista
sombreada interactiva y su sonificación controlada. Comparar con SURFER y guardar
un estado reproducible. Recuperar el código/distribución de Surfer Shuffle sin
suponer que el ZIP enlazado contenga ya todo el código fuente utilizable.

Base existente: extracción de toro/Cassini en 006 del directorio `experiments`.
La especificación 001 describe el primer instrumento regular; esta amplía su
alcance a superficies implícitas singulares. Ya hay un editor matemático local (`apps/surface-lab`); ALG-R06 sigue pendiente.
