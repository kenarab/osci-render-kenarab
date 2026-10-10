# 022 — Jardines meditativos para controlador

2026-10-10 / EXP-059. Pedido: reunir los mejores hallazgos en una serie nueva,
con impacto visual, sonido profundo y cuasi meditativo, manejable con MIDI CC.

- MED-01: tres instrumentos originales continuos, sin MIDI de notas, sin final
  silencioso ni introducción larga. Preservar 001–021 y sesiones del usuario.
- MED-02: seis lóbulos, ocho lóbulos y superficie de Roman; conservar XYZ con
  rotación y escala uniformes, cobertura angular completa y referencia con caras.
  Ecuaciones y rangos explícitos; no atribuir singularidades récord a estas formas.
- MED-03: separar archivo XYZ de archivo sonoro. Sonido con fundamental grave,
  voces sostenidas, respiración lenta, bancos derivados de todas las caras de la
  superficie y espacio estéreo. La mezcla no conserva F=0 ni representa una superficie.
  El sonido XYZ queda geométrico y puede resultar áspero: no prometer lo contrario.
- MED-04: mapa común A forma, B giro (0 congela sólo escena), C registro,
  D cobertura, E expresión (0 silencio), F brillo, G espacio, H respiración.
  Suavizar CC durante 150 ms; separar giro/cobertura/ritmo musical. Presets ignoran
  sliders heredados; archivos controlables requieren valores iniciales publicados.
- MED-05: interpolar bancos precalculados de ocho formas; ningún mallado ni
  análisis espectral por muestra. Limitar parciales según sample_rate y pitch.
- MED-06: validar ecuación después de invertir rotación/escala, cobertura,
  niveles, silencio, reinicio y controles a 16/44.1/48 kHz. Renderizar extractos
  estéreo para escuchar sin efectos de host. Calidad artística y MIDI físico pendientes.

Plan: biblioteca de geometría/bancos y motor autónomo, generador sólo 022, nueve
Lua (XYZ fijo/control y sonido control), tres presets sonoros adicionales para
comparación sin CC heredados, visor de referencia y guía de ocho controles.
No cambiar host, instalar software ni integrar audio/visor por un protocolo nuevo.
