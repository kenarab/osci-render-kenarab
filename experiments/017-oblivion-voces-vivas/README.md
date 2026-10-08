# Oblivion: Lua locales dentro del experimento

Nuevo experimento VIV-02/06. **Los Lua están en esta misma carpeta**, no hay que
buscar en recordings. Los experimentos 011/012 no se modifican.

- [oblivion.lua](oblivion.lua): mezcla con tres identidades fijas; ignora sliders.
- [oblivion-control.lua](oblivion-control.lua): A flauta, B fagot, C piano;
  D sin función; E tempo, F expresión, G giro. Tabla de valores en
  [Bach 015](../015-bach-voces-vivas/README.md).
- [Flauta XYZ](oblivion-voz-1-xyz-control.lua), [Fagot XYZ](oblivion-voz-2-xyz-control.lua),
  [Piano XYZ](oblivion-voz-3-xyz-control.lua): una voz/superficie, no mezcla geométrica.
- [WAV de 20 segundos](../../recordings/017-oblivion-voces-vivas.wav).

Asignación inicial: flauta/toro, fagot/Roman, piano/doble cono. Las tres admiten
cualquiera de las cuatro identidades. El piano conserva ambas manos en la mezcla;
su vista aislada elige la nota activa más aguda. La mezcla usa bancos espectrales,
los solos XYZ usan el recorrido geométrico y pueden sonar más ásperos. No comparar
sus formas como si fueran la misma señal. F=0 silencia; preset ignora controles.

Fuente: arreglo ScoreBase 38762, atribuido a José Bragato en el PDF de la semilla;
procedencia completa en manifest.json. Fragmento 41.4892–70 s; flauta entra a .25 s,
duración 28.5108 s y loop con fundidos. No se verificó licencia abierta para
redistribuir las notas; los Lua derivados están disponibles localmente y quedan
ignorados por Git. En otro checkout se generan con las fuentes de la semilla:
`python3 scripts/build_live_voices.py`. El generador no descarga repertorio.

Verificado fuera del host a 16/44.1/48 kHz: señal, transiciones entre bancos,
transporte y superficies de solos. Pendientes escucha y prueba Pro/controlador.
