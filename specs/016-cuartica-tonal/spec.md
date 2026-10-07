# 016 — Cuártica con portadora y cobertura separadas

Pedido: continuar superficies algebraicas 3D; EXP-050. Propuesta del agente:
ensayo pequeño sin partitura, antes de volver a superficies singulares.

- CUA-01: devolver XYZ sobre X⁴+3Y⁴+6Z⁴+k(X²+Y²+Z²)=1, escala uniforme .42,
  sin filtrado, mezcla de voces ni OBJ. Referencia con caras en xyz-stage.
- CUA-02: separar portadora longitudinal (80–160 Hz, 110 por defecto), cobertura
  latitudinal (4–12 Hz, 7 por defecto) y giro de escena (0–.2 rad/s).
  A giro (0 pausa); B portadora; C k (.1–.9); D cobertura. Preset ignora sliders.
- CUA-03: verificar F=0 tras invertir giro, cobertura de direcciones, energía XYZ
  y señal acotada a 16/44.1/48 kHz. Render WAV estéreo del retorno XY sin normalizar.
  La cobertura requiere persistencia aproximada de 1/7 s; no es relleno simultáneo.
- CUA-04: no declarar sonido agradable ni ausencia de aliasing por una cota de picos.
  Prueba de escucha y comparación del visualizador Pro pendientes.

Plan: plantilla de biblioteca, generador de dos variantes, comprobación geométrica
y render offline; reutilizar visor con caras de la misma cuártica k=.5.
