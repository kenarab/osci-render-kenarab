# Daft Punk — selección inicial para el laboratorio

Pedido EXP-044/045, 2026-10-07. «Something About Us» confirmado por el usuario.
Dos arreglos descargados y revisados por muestreo, seleccionados por legibilidad,
atribución y separación de partes. No afirmamos que sean los mejores existentes:
no hubo comparación auditiva nota por nota con los originales.

## Prioridad actual del usuario

| Tema | Dirección del trabajo | Estado |
| --- | --- | --- |
| Something About Us | Fraseo cálido y sostenido | PDF disponible; interpretación pendiente |
| Giorgio by Moroder | Desarrollo por capas y arco narrativo | Nueva preferencia; fuente/transcripción pendiente |
| Instant Crush (Julian Casablancas) | Línea vocal expresiva y tratamiento robótico | Nueva preferencia; fuente/transcripción pendiente |
| Lose Yourself to Dance | Bajo sincopado, pulso de baile y articulación | Groove original inspirado, no transcripción |

El tema con Julian Casablancas es [Instant Crush, según Sony Music](https://www.sonymusic.es/lanzamientos/daft-punk-lanza-el-video-de-su-single-instant-crush-junto-julian-casablancas-lider-de-strokes/).
La selección anterior (Digital Love, Harder Better Faster Stronger y Get Lucky)
se conserva en el medley descargado como material secundario, sin priorizarla.
Daft Punk está iniciado: fuentes y estudios tímbricos; **ningún tema completo
interpretado todavía**. No dar por cumplidos arreglos con una demo de vocales.

[Groove original de 24 s](../../recordings/013-groove-disco.wav), 100 BPM,
bombo a negras, bajo y vocales sincopados. Elección de tempo del estudio, no
transcripción del original. No contiene grabaciones ni riff copiado. El nombre
Lose Yourself to Dance es la referencia de intención; semejanza y calidad están
pendientes de escucha. [Lua](../../experiments/013-voz-robotica/groove-disco.lua).

## Descargas elegidas

1. [Something About Us — William Bishop](../../downloads/daft-punk/originals/something-about-us-v2.pdf).
   [Fuente pública](https://www.superpartituras.com.br/daft-punk/something-about-us-v-2).
   PDF vectorial, pentagramas nítidos y dos partes que permiten separar acompañamiento
   y línea principal. Páginas 1 y 6 inspeccionadas, cierre presente. No fija un BPM
   numérico en su apertura. Prioridad: transcribir y cotejar una voz, no inventar un MIDI.
2. [Daft Punk Medley — Tom Wallace](../../downloads/daft-punk/originals/medley-colorado-mesa.pdf).
   [Fuente: Colorado Mesa University](https://www.coloradomesa.edu/marching-band/documents/daft-punk-medley5.pdf).
   Paquete de partes de banda, 16 hojas escaneadas, dos páginas musicales por hoja;
   edición Arrangers' Publishing Company, percusión atribuida a Tony McCutchen.
   Hojas 1, 8 y 16 inspeccionadas: legibles y con articulaciones/dinámicas. Incluye
   también Technologic y One More Time. Es un medley a 136 BPM, **no cuatro arreglos
   completos**. Habrá que deshacer transposiciones instrumentales antes de combinar
   voces; la digitalización/OCR requiere revisión. No es una partitura general.

El manifiesto [fuentes.json](fuentes.json) conserva URL, fecha, tamaño y SHA-256.
Los originales quedan en downloads (fuera de Git). Acceso público no equivale a
licencia abierta; no hay licencia de redistribución verificada. Las otras fuentes
intentadas y sus obstáculos están registradas. No se compró ni instaló software.

## Vocoder y primera aproximación

Un vocoder analiza bandas de una señal moduladora para controlar el espectro de
una portadora. La referencia técnica es el
[manual oficial de Ableton, Vocoder](https://www.ableton.com/en/live-manual/12/live-audio-effect-reference/#vocoder).
Esta primera prueba utiliza envolventes espectrales sintéticas de vocales, no voz
analizada. Explora un carácter robótico sin samples ni imitación de una voz concreta.

[Prueba reproducible](../../experiments/013-voz-robotica/README.md): Lua autónomo,
controles y WAV de 16 s. El filtrado o reconstrucción vocal cambia el dibujo;
no se etiqueta como superficie algebraica fiel. Geometría y sonificación siguen
siendo componentes separados. Un vocoder real con voz moduladora y una portadora
procedente de superficies es el siguiente experimento, no un resultado ya obtenido.
