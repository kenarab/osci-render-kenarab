# 017 — Voces intercambiables y superficies distinguibles

2026-10-08, EXP-052/053. Pedido: implementar Bach con superficies por timbre,
Lua accesible de Oblivion y más diversidad geométrica; conservar estudios anteriores.

- VIV-01: escribir sólo experimentos nuevos (015/016/017), biblioteca nueva y
  generadores nuevos. No regenerar ni modificar 001–014 ni proyectos .osci del usuario.
- VIV-02: Bach completo con cuatro voces estables, A/B/C/D asignan identidades
  independientemente, E tempo .5–1.5x, F expresión y G giro de escena. Oblivion
  consume el mismo motor con tres grupos. Paleta precargada y suavizado de 80 ms
  de constante temporal; conservar fases, notas y tiempo al cambiar timbre.
- VIV-03: cuatro identidades con ecuación y receta reproducible: toro, Roman,
  doble cono y Cassini de dos lóbulos. Lua XYZ autónomo por superficie y mallas
  con caras de referencia, sin OBJ ni reducción previa a z=0. Validar F=0.
- VIV-04: mezcla musical usa timbres espectrales derivados de las superficies;
  declarar que no conserva su geometría. Archivos de voz aislada devuelven XYZ
  de la identidad asignada; no sumar coordenadas de voces. En transición mantener
  dos identidades sonoras, pero seleccionar una geometría exacta (cambio discreto).
  Sólo el modo aislado sirve para inspección de superficie, no como mezcla total.
- VIV-05: timbres de escucha con bancos limitados a armónicos compatibles con
  tasa/altura; envolventes y margen de nivel. La interpolación de tabla puede dejar
  imágenes espectrales residuales; no afirmar ausencia total de aliasing. La ruta
  geométrica no está limitada espectralmente. Calidad subjetiva pendiente.
- VIV-06: acceso directo a Lua dentro de cada experimento nuevo. Notas de Oblivion
  locales e ignoradas por Git; fuente/recorte manifestados. No reproducir audio ni
  reemplazar sesión del usuario para verificar offline.

Plan: geometría y paleta independientes; reproductor parametrizado por eventos y
voces; dos adaptadores de repertorio; pruebas sostenidas, MIDI CC simulados,
reinicio/fin/loop y niveles a 16/44.1/48 kHz; comparación visual fuera del host.
Prueba en Pro/controlador y percepción de profundidad siguen pendientes.
