# 014 — Referencias Daft Punk y voz robótica

EXP-044/045. Something About Us confirmado por el usuario. Propuestos además
Digital Love, Harder Better Faster Stronger y Get Lucky.
DP-01: descargar 2–3 arreglos accesibles, comprobar formato/legibilidad, registrar
URL, fecha, hash, instrumento, alcance y restricciones; no confundir PDF con HTML.
Elegir por utilidad comprobada, sin afirmar superioridad a arreglos no inspeccionados.
DP-02: prototipo Lua de vocales sintéticas secuenciadas con portadora armónica,
transiciones de formantes, articulación y parámetros suavizados. Sin muestras de
voces originales ni letras. No llamarlo vocoder analizador de voz real.
DP-03: salida XYZ finita con margen (<.3 por eje); WAV XY de escucha identificado
como tal, no evidencia de superficie algebraica. Conservar captura XYZ aparte.
DP-04: controles de articulación, formante y brillo separados del giro de escena;
armónicos por debajo de Nyquist y comprobaciones a 16/44.1/48 kHz.
Plan: fuentes y selección, síntesis aditiva de formantes fuera del cálculo costoso
por muestra, pequeño estudio original de 16 s, Lua/WAV y prueba de límites.
Pendientes: transcripción MIDI/MusicXML revisada y arreglos completos de temas;
vocoder con voz moduladora y portadora requiere otra prueba. El procesamiento
vocal altera el dibujo: no presentarlo como recorrido fiel de F=0.
