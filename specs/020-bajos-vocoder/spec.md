# 020 — Bajo de sintetizador y vocoder

2026-10-09 / EXP-057. Pedido: bajos potentes y vocoderizados, usando Daft Punk
como ejemplo; investigar extensión de filtros. Se preservan 001–019 y .osci.

- BVC-01: dos estudios aislados de 24 s con notas de bajo de los MIDI ya obtenidos
  de Lose Yourself to Dance y Giorgio by Moroder. Fuente, recorte, pista y hash
  registrados; no presentarlos como temas completos ni reproducción del disco.
- BVC-02: portadora con dientes de sierra PolyBLEP, filtro resonante de cuatro
  polos, seno grave paralelo y saturación suave con cota de salida. Potencia
  perceptual pendiente; no afirmar ausencia de aliasing tras no linealidades.
- BVC-03: vocoder real de 12 bandas: filtrar modulador, seguir envolventes y
  modular las bandas correspondientes de la portadora. Demostración autónoma
  con vocales sintéticas; opción de modulador externo ext_x/ext_y. Las vocales
  no contienen letras ni una voz del disco. Sin modulador, el vocoder debe callar.
- BVC-04: preset seco, preset vocoder y controlable por estudio. A corte, B drive,
  C mezcla vocoder, D vocal sintética, E tempo, F expresión, G seno grave, H mezcla
  de entrada externa, I resonancia. Mantener fases al mover controles. Parada
  al fin de una pasada con cola/fundido, step reinicia; no instalar ni abrir host.
- BVC-05: biblioteca DSP separada de temas, efecto Lua reutilizable con entrada
  de dos canales: X portadora, Y modulador. Esta disposición es mono y exige
  ruteo explícito. Efecto personalizado no comparte automáticamente ext_x/ext_y.
- BVC-06: prueba de transferencia espectral del modulador (400 vs 2400 Hz),
  silencio en ausencia de una de las señales, estabilidad/niveles/reset y
  controles a 16/44.1/48 kHz. WAV secos/procesados para comparar. No declarar
  calidad artística, realismo vocal ni aceptación en host desde métricas.
- BVC-07: documentar Custom Lua Effect y ruta VST/AU en DAW, con fuentes primarias
  y evidencia local. Sidechain de amplitud no sustituye análisis multibanda.

Plan: DSP y efecto independiente; dos adaptadores de bajos locales; seis Lua,
comparaciones WAV y tests DSP. Salida de audio procesado XY: estos filtros no
preservan F=0. Geometría XYZ conserva su ruta aparte. Ruteo físico pendiente.
