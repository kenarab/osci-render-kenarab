# Voz sintética, bajo y vocoder

Biblioteca independiente del repertorio. Los eventos de canciones los insertan
generadores de experimentos; no viven en estos módulos.

- `player.lua.in`: demostración de formantes.
- `song.lua.in`: reproductor con bancos de identidades y vocales sintéticas (018).
- `vocoder.lua`: biquads, vocoder de 12 bandas con envolventes, PolyBLEP,
  filtro de bajo y saturación suave. No lee archivos ni necesita dependencias.
- `bass.lua.in`: instrumento monofónico que consume eventos, modulador sintético
  precargado o `ext_x`, y una instancia propia del DSP. Controles por voz.
- `vocoder_effect.lua.in`: adaptador para Custom Lua Effect, X portadora / Y
  modulador. Usa la misma biblioteca sin partituras. No presupone entradas externas
  independientes dentro de la cadena de efectos.

Los archivos `.in` se expanden para osci-render, sin `require` del sistema de
archivos. El estado DSP es de cada consumidor y se prepara al inicializar. Las
bandas se fijan entonces; el pasabajos actualiza coeficientes cada 64 muestras
conservando memoria. Saturación suave acota salida; no sustituye dinámica completa
ni garantiza ausencia de aliasing. Salida sonora procesada no conserva F=0.

[Experimento 020, controles y límites](../../experiments/020-bajos-vocoder/README.md)
· [Investigación](../../docs/filtros-y-vocoder.md).
