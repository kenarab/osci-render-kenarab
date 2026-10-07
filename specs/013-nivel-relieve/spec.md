# 013 — Nivel sin recorte y profundidad reconocible

Pedido EXP-043: tras reiniciar, imagen cuadrada, saturación y superficies poco 3D.
NIV-01: registrar ganancia y Threshold antes/después; conservar archivos Bach.
NIV-02: ejercicios XYZ con orientación inicial oblicua y giro lento predeterminado;
A=0 detiene sólo escena. Ecuación y distancias se conservan tras deshacer rotación.
NIV-03: contrastar esfera simétrica y elipsoide/cuártica anisótropos, sin prometer
que más curvas o más volumen mejoren la profundidad. No filtrar coordenadas.
Aceptación: no recorte visual en host tras ajustar nivel; Lua mantiene F=0/rango 3
con giro y parámetros. Escucha y percepción de volumen geométrico: usuario.
Plan: ganancia 2.1787→0.30, Threshold .2947→1; corregir orientación en plantilla,
regenerar ejercicios y evidencia; probar elipsoide en host, documentar límites.
