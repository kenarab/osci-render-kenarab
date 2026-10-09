# 021 — Posición, pausa y reinicio de reproductores Lua

2026-10-09 / EXP-058. Usuario no encuentra FF/rewind y percibe poca actividad/bajo.
Confirmado 020; ventana observada con el preset vocoder de Lose. Mantener 001–020 intactos.

- TRN-01: variantes nuevas de los bajos 020 y temas 018; notas incorporadas al
  generar, sin leer MIDI en tiempo real. Documentar diferencia fuente/host.
- TRN-02: J solicita posición normalizada, K=0 reproduce/K=1 pausa, L dispara
  retorno al comienzo al pasar de 0 a 1. La posición avanza internamente; J no
  la congela ni se actualiza automáticamente. Jitter pequeño no repite seeks.
- TRN-03: reposicionar hacia delante/atrás, reconstruyendo notas sostenidas e
  índice correcto. Índice binario y candidatos precalculados por segundo, sin
  recorrer toda la partitura por muestra ni por seek. Limpiar estado DSP al salto.
- TRN-04: fundido de 20 ms antes del salto y 20 ms al continuar. Última petición
  gana durante movimiento. Pausa congela reloj y silencia con fundido; resume
  desde ahí. Salto estando pausado o después del fin debe funcionar.
- TRN-05: variantes con sonido fijo que sólo leen J/K/L para aislar sliders
  heredados; variantes de controles mantienen los timbres previos. Calibración
  Mi2 (82.4069 Hz), ciclos de 8 s continuos, sin MIDI ni sliders para comparar
  salida/registro grave sin que termine mientras el usuario busca controles.
  No cambiar timbre de los estudios previos ni declarar diagnóstico de host.
- TRN-06: pruebas a 16/44.1/48 kHz de saltos, notas cruzando destino, índice,
  pausa/reanudación, jitter, último destino, inicio/fin y cota de audio. Compilar
  todas las variantes. Medir sonido del primer segundo y tono de calibración.
  Escucha y UI/controlador físicos pendientes.

Plan: transporte reusable, adaptadores a los dos motores existentes, generación
en 021, Lua de calibración y guía breve de controles. No añadir dependencia ni
control OSC/DAW automático; el reloj DAW queda como extensión separada.
