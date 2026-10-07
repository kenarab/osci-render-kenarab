# 009 — Bach desde superficies récord de SURFER

Pedido EXP-035. Piazzolla queda cerrado en este laboratorio; Atlas se retomará
aparte. Conservar el Adagio favorito y probar timbres derivados de superficies
de la galería récord de IMAGINARY/SURFER, distintos por voz.

- REC-01: conservar ecuaciones y parámetros exactos de la instalación SURFER,
  procedencia y hash; distinguir récord bibliográfico de singularidades resueltas.
- REC-02: producir mallas con caras de las cuatro superficies dentro de una caja
  documentada, OBJ y vista sombreada. No afirmar completitud de superficies
  no compactas ni topología exacta en los nodos a resolución finita.
- REC-03: cada timbre incorpora áreas de todas las caras de su malla; describir
  transformación, filtrado y portadora tonal. Sin solver por muestra de audio.
- REC-04: dos tratamientos comparables del mismo Adagio, cuatro voces, tempo
  controlable y expresión heredada. Preservar versiones anteriores.
- REC-05: entregar Lua, WAV completo, comparación audiovisual y voces aisladas;
  comprobar continuidad, fin, reinicio, límites y controles a 44.1/48 kHz.
  Calidad auditiva y funcionamiento dentro del host quedan pendientes de prueba.

Plan: extraer fórmulas locales; muestrear F=0 con tetraedros y bisección de aristas;
convertir momentos angulares ponderados por área en bancos periódicos limitados
en armónicos; reutilizar motor expresivo de 008; renderizar y documentar.

Aceptación: residuo de vértices, caras no degeneradas, geometría finita, bancos
distintos, señal acotada y sin saltos grandes. Video rotulado separa superficie
sombreada y XY audible. Los recortes y la cuadratura no prueban el conteo de nodos.
