# 004 — Bach controlable y voces con identidad

Estado: implementado fuera del host; escucha pendiente. EXP-025/026.
El usuario encuentra rápido el original y demasiado lento el Adagio. Pide tempo
ajustable, expresión y timbres diferenciados que reduzcan la sensación robótica.

- VIV-R01: nuevo preset a 32 BPM y archivo controlable, rango 20–52 BPM continuo;
  conservar original/Adagio y las 980 notas. Cambiar tempo no cambia alturas.
- VIV-R02: cinco controles: tempo, expresión, color, articulación y balance solista.
  Preset audible sin configurar sliders; versión de control con valores explícitos.
- VIV-R03: cuatro perfiles tímbricos definidos por recorridos toroidales distintos
  y tratamiento espectral por voz. No llamarlos emulaciones de cuerdas acústicas.
- VIV-R04: expresión controla fraseo, rubato, vibrato gradual, intensidad y pequeños
  desfases deterministas entre voces; sin aleatoriedad irreproducible ni desafinación grande.
- VIV-R05: validar controles extremos y reloj, continuidad, final, reinicio y cotas;
  generar audio completo y muestra breve para escuchar timbres. Espectro/host/percepción
  pendientes donde no se midan. La mezcla no representa superficies independientes.

Plan: ampliar el generador existente, implementar motor separado, renderizar
audio y una preescucha breve; documentar valores iniciales y límites. El nuevo
instrumento de superficies 007 queda disponible para su evaluación, sin fingir
que el arreglo de Bach resuelva la visualización de esas superficies.

Aceptación: preset 32 BPM, A=0/1 implica 20/52 BPM antes de rubato; mismo score;
audio completo entre las duraciones del original y Adagio; señales finitas <1,
delta <0.25 y fin silencioso; cuatro perfiles distinguibles matemáticamente y
comparación auditiva pendiente. MIDI/OSC físico continúa pendiente.

Evidencia: audio completo de 274.567 s, pico 0.54046, delta 0.04398, final
silencioso y reinicio; controles reales del entregable simulados a 44.1/48 kHz,
extremos 20/52 BPM, polinomios, datos inválidos y continuidad aprobados. Muestra
de video de 60 s y cuatro timbres aislados, 6 s por voz, RMS 0.13. Ver guía de 005.
