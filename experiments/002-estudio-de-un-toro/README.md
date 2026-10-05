# EXP-002 — Estudio de un toro

Primera composición original del laboratorio: **80 segundos**, 96 BPM, 32 compases
en 4/4. El mismo recorrido produce imagen y sonido; una secuencia de notas,
acentos, silencios y variaciones de la geometría reemplaza la figura estática.

## Probar en osci-render

1. Bajar el volumen y abrir `estudio.lua` con el selector de archivos.
2. Usar una sola voz, sin MIDI ni efectos para la primera comparación. La pieza
   lleva su propio reloj y afinación: el control de frecuencia del host no la afina.
3. Dejarla correr 80 segundos. Termina en silencio; no es un loop.
4. Para volver al principio, editar `local TAKE = 1` a `local TAKE = 2` en el
   editor integrado (incrementarlo en cada repetición). Esto reinicia el reloj
   aunque el editor conserve las variables globales de Lua.

| Tiempo | Sección | Qué buscar |
| --- | --- | --- |
| 0–20 s | Presentación | Entrada gradual, motivo de ocho notas y recorrido toroidal 2:3 |
| 20–60 s | Desarrollo | Respuestas más agudas, recorridos 2:5, 3:7, 2:7 y 3:8; tubo más grueso |
| 60–80 s | Retorno | Vuelve 2:3, disminuye la densidad, aparecen espacios y se apaga |

Los cambios de nota y recorrido ocurren con la envolvente en cero. La imagen
respira con cada nota y cambia de perspectiva lentamente. Es una estética
arpegiada y de síntesis geométrica; aún requiere tu evaluación musical.

## Geometría y controles

Antes de rotación y ganancia, el recorrido vive sobre
`(x²+y²+z²+R²−r²)²−4R²(x²+y²)=0`. Los radios varían en el tiempo manteniendo
`R > r > 0`. Después se rota en 3D y se escala con la envolvente musical; por eso
la señal final no satisface el polinomio original con los mismos radios y ejes.
No se representa una malla completa ni una superficie implícita arbitraria.

Controles en las primeras líneas del script:

- `BPM = 96`: tempo. La duración es `128*60/BPM` segundos. Cambiarlo y reiniciar
  TAKE para conservar una línea temporal coherente.
- `ROOT_HZ = 55`: frecuencia base del recorrido. Probar 41.203 o 65.406. El timbre
  contiene armónicos ligados a la geometría; esta frecuencia no garantiza que sea
  la altura percibida predominante.
- `LEVEL = 0.75`: ganancia, entre 0 y 1 para las cotas verificadas.
- `TAKE`: reinicio. No requiere instalar módulos Lua.

El reloj usa `step/sample_rate` relativo a la primera muestra. Si cambia la
frecuencia de muestreo o el contador retrocede, se reinicia la toma. Desactivar
MIDI evita varias voces reproduciendo secuencias distintas.

## Verificación y preescucha fuera del host

Desde la raíz:

```sh
luajit scripts/check_torus_study.lua
luajit scripts/check_torus_study.lua recordings/estudio-de-un-toro.wav
```

El segundo comando requiere crear antes `recordings/` y genera un WAV estéreo de
48 kHz/16 bits con X a la izquierda e Y a la derecha. Es la salida directa del
script, sin los efectos ni la proyección adicional que pueda aplicar osci-render.
El archivo generado no se incluye en Git.

La comprobación ejecuta los 80 segundos a 44.1 y 48 kHz: valores finitos, amplitud,
actividad en cada sección, continuidad local en cambios de nota y fin en silencio.
También comprueba determinismo y reinicio con TAKE. No sustituye medir el
rendimiento, escuchar y observar la pieza en osci-render.
