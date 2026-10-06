# 002 — Timbre cálido, suave y expresivo

Estado: tres variantes implementadas y renderizadas; aceptación auditiva pendiente.
Pedido relacionado: EXP-023. El usuario solicita un timbre más lindo que el actual.
Interpretación de diseño inicial: cálido y sostenido, menos áspero y menos parecido
a un pitido. Es una hipótesis que debe contrastarse con su escucha.

## Requisitos

- **TIM-R01:** fundamental reconocible y balance de armónicos controlable, sin
  ruido áspero añadido por saltos entre segmentos o muestreo insuficiente.
- **TIM-R02:** ataques, cambios de parámetros y liberaciones suaves; evitar clics,
  DC persistente, saturación y cambios bruscos de nivel.
- **TIM-R03:** obtener el timbre del recorrido y su tratamiento; no sustituirlo
  por una pista de audio ajena que rompa la relación explicable con la geometría.
- **TIM-R04:** si filtramos o modificamos la señal, mostrar la trayectoria XY
  posterior al tratamiento y distinguirla de la superficie geométrica original.
- **TIM-R05:** no confundir mayor volumen con mejor sonido. Comparaciones cortas
  con nivel RMS comparable, control de pico y mismas condiciones de escucha.
- **TIM-R06:** documentar compromisos: filtrar agudos suaviza esquinas y detalles;
  más densidad geométrica puede aumentar aspereza. La calidad visual y sonora se
  evalúan juntas, no maximizar una sin mostrar qué ocurre con la otra.

## Tres variantes iniciales propuestas

1. **Suave:** barrido continuo, poca energía aguda y transición sin saltos.
2. **Cuerpo:** algo más de armónicos bajos, manteniendo la fundamental y el nivel.
3. **Aire:** movimiento lento del color sonoro, sin ruido aleatorio por defecto.

Son nombres de trabajo; no prometer emulación de violín, bandoneón o instrumentos
acústicos sin diseñarla y escucharla. No alterar alturas mediante acordes prefijados
para ocultar un timbre que todavía no funciona.

## Aceptación

| ID | Evidencia requerida | Estado |
| --- | --- | --- |
| TIM-A01 | Tres muestras de 10–15 s de la misma superficie/registro, diferencia RMS ≤1 dB | Aprobado: 3 × 12 s, diferencia 0.395 dB |
| TIM-A02 | Señal finita, pico <0.95, medir DC y discontinuidades con umbrales justificados | Aprobado para clips: pico ≤0.21866, DC <0.001, delta <0.04; guía 007 |
| TIM-A03 | Revisar aliasing en el rango de barrido y densidad elegidos; no basta comprobar clipping | Espectro estático verificado a 44.1/48 kHz, armónicos hasta 3000 Hz; automatización arbitraria/host pendientes |
| TIM-A04 | Video comparativo XY antes/después y superficie 3D de referencia | Tres videos de 12 s y comparación de 36 s generados; fotograma revisado |
| TIM-A05 | Usuario elige variante o describe ajuste; registrar preferencia y contexto de escucha | Pendiente |

La definición de “más lindo” no se reemplaza por métricas: los controles técnicos
son condiciones de funcionamiento, la aceptación artística sigue siendo auditiva.

Evidencia y reproducción: [007 — Toro sonoro](../../experiments/007-toro-sonoro/README.md).
El tratamiento es una atenuación analítica de los términos del tubo; cambia la
superficie audible de r a r·g. La malla de referencia conserva el radio original.
No se afirma que esta primera síntesis sea ya el timbre preferido por el usuario.
