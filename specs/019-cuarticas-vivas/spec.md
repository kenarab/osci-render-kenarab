# 019 — Cuárticas deformables con lóbulos

2026-10-09 / EXP-056. Continúa el pedido de diversidad, superficies XYZ y
parámetros en vivo. Propuesta acotada: seis y ocho lóbulos; no son superficies
récord ni reemplazan la integración implícita general pendiente.

- LOB-01: experimento nuevo 019; preservar 001–018 y proyectos del usuario.
- LOB-02: dos familias F(x,y,z;a)=0, parametrización radial exacta con tres
  coordenadas. Seis: (x²+y²+z²)²-a(x⁴+y⁴+z⁴)=1, a∈[0,.96].
  Ocho: x⁴+y⁴+z⁴-a(x²y²+y²z²+z²x²)=1, a∈[0,.94].
  El denominador positivo evita raíces vacías y singularidades en este rango.
- LOB-03: Lua preset/control por familia; A deformación, B giro de escena
  (0 pausa sin cortar audio), C portadora 55–165 Hz, D cobertura 3–11 Hz,
  E escala .4–.8. Suavizar cambios de parámetros conservando fases.
  Retornar XYZ sin filtro ni proyección previa. No proclamar calidad sonora.
- LOB-04: visor local sin audio, caras, cámara y barrido de referencia; cambiar
  a reconstruye directamente la malla sin OBJ. Controles de caras/recorrido,
  ecuación y valor de a visibles. Este visor no controla el host.
- LOB-05: verificar residuo antes/después de invertir rotación/escala, finitud,
  cotas y energía XYZ a 16/44.1/48 kHz; cobertura angular, pausa y cambios
  sostenidos. Navegador: ambos modelos, deformación, cámara y sin errores WebGL.
  Escucha, reconocimiento en Pro y MIDI físico pendientes.

Plan: biblioteca de ecuaciones Lua/JS independiente, cuatro Lua nuevos, visor
que reutiliza el renderizador existente sin modificarlo, pruebas geométricas
y captura visual. No convertir este avance en otra colección de partituras.
