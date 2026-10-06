# 003 — AIRE, versión lenta y expresiva

Pedido EXP-024: el usuario pide ralentizar el Air de Bach, darle más expresión
y, más adelante, usar superficies para timbres más complejos y profundos.

## Contrato y plan

- BAC-R01: conservar `aire.lua` y sus notas; entregar `aire-adagio.lua` autónomo.
- BAC-R02: bajar el tempo base de 38 a 26 BPM; A permite reducirlo hasta 18 BPM.
  Integrar el pulso sin alterar alturas ni saltar eventos.
- BAC-R03: arcos de intensidad por frase, acompañamiento contenido, ataques
  más suaves y cadencias con desaceleración y recuperación gradual.
- BAC-R04: cámara más lenta. No presentar la suma de voces como superficie.
- BAC-R05: generar audio completo y video; verificar duración, ausencia de
  clipping, final silencioso, controles y reinicio. Calidad expresiva: escucha pendiente.

Implementar un motor de interpretación separado reutilizando la misma partitura
y el importador. Conservar fuentes/licencia. La integración con el instrumento
de superficies queda en 001/002; no se promete que este arreglo la complete.

Aceptación: mismos 980 eventos; duración al menos 30% mayor que los 230.046 s
del original; amplitud <1 y delta <0.25; continuidad del reloj con CC; salida
silenciosa al final y reinicio correcto. Evaluación artística a cargo del usuario.
