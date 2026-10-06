# 005 — Narración visual y sonora

Estado: propuesta inicial, sin obra implementada. EXP-027.
El usuario pregunta por historias contadas con osci-render. El sistema permite
organizar escenas con estados de geometría, recorridos, timbre, ritmo y transiciones.
La limitación es que la proyección XY audible no equivale a una imagen sombreada libre.

## Propuesta del agente: Respirar la materia

| Escena | Cambio visual | Consecuencia sonora |
| --- | --- | --- |
| Aparición | Surge una superficie estable, con trama suave | Ataque lento, fundamental y pocos armónicos |
| Encuentro | Dos gestos se alternan y responden | Pregunta/respuesta de registros y timbres, sin sumar dibujos indiscriminadamente |
| Tensión | Se deforma la superficie y se densifica su barrido | Mayor contenido armónico y pulsación; conservar continuidad |
| Transformación | La forma recupera estabilidad con otras proporciones | El motivo vuelve con otro color y respiración más amplia |

No exige voz hablada: el relato puede surgir de recurrencias, contrastes y memoria
de una forma/motivo. Es un arco original propuesto, no una interpretación atribuida a Bach.

## Requisitos para el siguiente prototipo

- NAR-R01: storyboard temporal que relacione cada gesto geométrico con un gesto audible.
- NAR-R02: conservar mallas/ecuaciones y mostrar XY real; transiciones suaves y reproducibles.
- NAR-R03: una previsualización corta antes de una obra larga; distinguir referencia sombreada
  y salida audible, con capítulos que permitan describir qué cambió.
- NAR-R04: escuchar/evaluar si se perciben aparición, tensión y transformación.
  Un título no demuestra que la historia se entienda.

Pendiente: elegir duración, familia de superficies y motivo. No se inicia una
producción larga mientras todavía se elige el timbre del instrumento 007.

IanniX es candidato para ordenar escenas y curvas de control. La
[ruta de integración](../../docs/iannix-superficies.md) está investigada, no implementada.
