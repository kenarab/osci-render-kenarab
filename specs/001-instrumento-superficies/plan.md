# Plan incremental y evidencia

1. **Identificar controles del host.** Abrir un `.lua`, expandir editor y panel
   inferior; comprobar mouse y rango. Registrar versión/edición. No hace falta
   controlador para esta tarea. Corresponde a SUP-A06.
2. **Elegir un primer instrumento.** Toro de EXP-019; ensayar malla reducida o
   barrido por secciones que cubra la superficie y preserve continuidad. Comparar
   contra su vista sombreada. No sumar cuatro voces durante esta validación.
3. **Separar relojes.** Movimiento lento y barrido sonoro con estado independiente;
   implementar A=0 como congelación visual. Probar extremos y cambios en vivo.
4. **Diseñar timbre.** Generar las tres variantes de 002 con igual nivel percibido
   aproximado; elegir con el usuario antes de componer otra pieza larga.
5. **Conectar hardware.** Probar un solo CC. Si el controlador ya habla MIDI,
   no convertirlo a OSC sin necesidad. Si solo habla OSC, elegir puente/receptor
   tras conocer el dispositivo y la edición del host.
6. **Validar y cerrar.** Audio, vista de superficie, representación XY, instrucciones
   y resultados; commit con IDs de requisitos y limitaciones.

Cada paso se implementa y verifica como incremento utilizable. La existencia de
este plan no marca ninguna tarea como completada.

## Dudas que afectan a integración

- Marca/modelo del controlador y si envía CC MIDI, OSC o ambos.
- Versión y edición de osci-render; disponibilidad efectiva de MIDI Learn.
- Qué velocidad molestó más en AIRE: recorrido XY, movimiento de cámara o tempo.
  Se separan las tres nociones aunque todavía no haya respuesta.

## Decisiones vigentes

- SDD local con Markdown y pruebas del repositorio; sin framework adicional.
- Motor musical nuevo desde geometría; conservar AIRE como referencia histórica.
- No imponer un puente OSC antes de saber si hace falta.
- Evaluación perceptual del usuario obligatoria para declarar logrado el timbre;
  no introduce un permiso extra para implementar o renderizar pruebas autorizadas.
