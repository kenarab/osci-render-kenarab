# 012 — Geometría XYZ conservada

EXP-040/041. Corrección explícita: no aplanar superficies, no Z artificial ni
proyección XY precalculada como representación del objeto. El sonido anterior
no está aceptado. Conservar entregas anteriores sólo como antecedentes.

- XYZ-01: nuevos ejercicios retornan coordenadas XYZ reales de la superficie.
  Cámara/proyección final del dispositivo no forma parte del banco geométrico.
- XYZ-02: verificar ecuación y rango tridimensional (covarianza de rango 3),
  no sólo existencia de un tercer número. Rotaciones deben ser ortogonales.
- XYZ-03: referencia 3D interactiva con caras y recorrido sobre la misma geometría;
  guardar muestras XYZ, no descartar Z al preparar evidencia visual.
- XYZ-04: para música, mostrar superficies por instrumento sin sumar coordenadas.
  Las notas y mezcla audible son otra salida. Identificar cualquier audio reutilizado
  y no atribuirle fidelidad geométrica ni nueva aceptación tímbrica.
- XYZ-05: ecuaciones y geometría reutilizables fuera de las piezas; sin OBJ como
  transporte hacia osci-render. Prueba en host por parte del usuario, pendiente.

Plan: rehacer esfera/elipsoide/cuártica como generadores XYZ; medir soporte 3D;
preparar visor de las coordenadas y caras, después escenas de repertorio con
objetos separados y asignación visible. No sustituir la coordenada Z por un adorno.

Decisión del usuario: **una voz aislada primero**. XYZ-04 se implementa inicialmente
con Violino I de Bach y flauta de Oblivion, por separado, sin mezcla. La cuártica
analítica es el primer instrumento verificable. Superficies récord: referencia
visual con caras; recorridos musicales y asignación dinámica quedan pendientes.

Aceptación automatizada: check_xyz_exercises.lua (XYZ-01/02/03),
check_xyz_solos.lua (XYZ-01/02/04: ecuación del retorno, rango 3, controles,
fin/reinicio a 44.1 y 48 kHz), check_xyz_stage.cjs (XYZ-03: WebGL, profundidad,
cambio de escena y cámara). Aceptación humana de forma y sonido en host: pendiente.
