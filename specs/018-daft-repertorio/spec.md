# 018 — Daft Punk: arreglos largos y nuevas interpretaciones

EXP-055. Pedido: más estudios y completar los cuatro temas prioritarios sin
modificar los anteriores. Usuario acepta positivamente ensayos 013.

- DFT-01: adquirir y verificar archivos MIDI reales, conservar URL/hash/duración,
  pistas y procedencia. No confundir un arreglo acortado con el original completo.
- DFT-02: reproducir de inicio a fin todos los eventos positivos del archivo elegido,
  con tempo fuente, polifonía y velocidades; declarar pedal/bend no interpretados.
  Fin silencioso explícito, nueva carga/step reinicia. Sin loop que finja longitud.
- DFT-03: usar voz sintética por formantes y acompañamiento/bajo de identidades
  algebraicas, percusión sintetizada según canal 10. Sin muestras vocales ni letras.
  Es síntesis vocal, no vocoder de análisis ni imitación de una persona.
- DFT-04: preset y controlable por pieza, A/B/C identidad de melodía/acompañamiento/
  bajo; D percusión, E tempo, F expresión, G vocal, H brillo robot. Agrupación de
  pistas explícita en manifiesto; conserva notas de cada pista, no asegura timbre GM.
- DFT-05: validar todos los eventos hasta fin, picos/no NaN a 48 kHz; controles y
  tasa 16 kHz en muestra breve. Reportar notas procesadas/fin; escucha/host pendientes.
- DFT-06: originales/notas/Lua musical y WAV locales fuera de Git; versionar motor,
  manifiestos y pruebas. No comprar créditos ni acceder a enlaces premium cerrados.

Plan: cuatro adaptadores de fuentes descargadas, banco vocal independiente,
reproductor polifónico y render íntegro offline. Giorgio encontrado en arreglo
5:49; versión original completa sigue pendiente de fuente/cotejo. Los demás
arreglos tampoco se certifican idénticos a la grabación por su duración.
