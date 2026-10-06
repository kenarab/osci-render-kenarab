# IanniX, superficies completas y osci-render

Investigación inicial para EXP-028/029. No hay conexión implementada ni probada.

## Resultado de la escucha

El usuario escuchó estática al abrir los Lua 007 en osci-render. Comparó después
el WAV: es distinto y más limpio, **pero tampoco le gusta su carácter sonoro**.
Aclaró que “suena como estática” expresa esa valoración, no solo un posible fallo.
**TIM-A05 no está aceptado artísticamente**, y además hay una diferencia de
reproducción entre WAV y host por diagnosticar. Son dos cuestiones distintas.

Las pruebas de ecuaciones, continuidad y espectro estático pasan, pero no prueban
un timbre agradable. No se atribuye aún la diferencia del host a clipping,
aliasing o configuración. Añadir complejidad geométrica no asegura resolver el timbre.
Para el siguiente diseño, elegir una muestra corta agradable antes de una obra larga;
para el host, comparar configuración/efectos y una grabación de la salida real.

Lectura de la app: abierta en `aire-adagio.lua`, lista de sliders desplazada a
H–O y última edición visible de M. Nuestros estudios usan A–E; M no los controla.
Desplazar esa lista hacia arriba. El panel Lua sí está presente. La versión
instalada, según `/Applications/osci-render.app/Contents/Info.plist`, es **2.9.9.10**;
la copia de fuentes usada como referencia es 2.9.9.3. No se verificaron efectos,
escucha o grabación de la salida real. La consulta de UI tardó 240 s; se evitó
repetir operaciones lentas sin evidencia adicional.

## Qué significa dibujar la superficie completa

El usuario aclara que su referencia es **[SURFER](https://www.imaginary.org/program/surfer)**,
no una demo concreta de osci-render: quiere superficies implícitas y ejemplos
con singularidades. SURFER documenta el conjunto de ceros de polinomios y su
galería interactiva. Este es el objetivo, precisado en [006](../specs/006-superficies-surfer/spec.md).
No se reduce a elegir otro toro ni a aumentar el número de vueltas de una curva.

El modelo matemático puede ser una superficie con caras y coeficientes editables.
Su proyección XY de audio es un recorrido temporal: la apariencia de área requiere
barridos, trama o persistencia. Se puede mejorar mucho la representación mediante
selección de aristas/contornos y ocultación, pero no equiparar automáticamente
esa salida con una superficie sombreada de un renderizador 3D.

La [documentación actual del proyecto](https://github.com/jameshball/osci-render)
confirma importación OBJ e integración con Blender mediante Line Art. La
[wiki antigua](https://github.com/jameshball/osci-render/wiki) describe mallas
wireframe y ocultación de aristas; advierte que corresponde a la versión legacy,
por lo que no se prometen menús o rendimiento equivalentes en la app instalada.

Propuesta: editar coeficientes sobre una malla sombreada en Blender y escoger
su representación hacia osci-render. Mantener a la vista superficie y XY real;
un control modifica el modelo y el sonido, sin fingir que el sombreado sale del WAV.
El prototipo 007 aún no implementa ese editor ni actualiza su OBJ al mover C.

Como antecedente cercano, [OSCI-VISION del Melt Museum](https://meltmuseum.com/en/museum-map/)
declara TouchDesigner, Blender, osci-render y Leap Motion para geometría interactiva.
Es un ejemplo de interacción 3D con osci-render, no una integración con IanniX.

## OSC: conexiones diferentes

El nombre osci-render alude a su uso con osciloscopios; no prueba soporte del
protocolo Open Sound Control. No se encontró una entrada nativa documentada para
controlar sliders por OSC en las fuentes revisadas. La copia local tiene módulos
incompletos, así que la búsqueda no demuestra ausencia universal.

El [conector oficial de Blender](https://github.com/jameshball/osci-render/blob/main/blender/osci_render/__init__.py)
usa socket TCP y su formato GPLA para trazos. La copia 2.9.9.3 coincide: `SOCK_STREAM`
y datos binarios en base64. No es OSC ni una dirección a la que enviar `/slider_a`.

## IanniX: tiene sentido como partitura gráfica

[IanniX](https://www.iannix.org/en/whatisiannix/) documenta secuenciación gráfica
en tiempo real, curvas/eventos por OSC y programación de partituras con JavaScript.
Puede organizar duración de escenas, trayectorias de controles y respuestas para
la [narración propuesta](../specs/005-narracion-audiovisual/spec.md).

No se encontró un ejemplo específico y verificable de **IanniX + osci-render**
en esta búsqueda web (términos exactos y búsquedas relacionadas con osciloscopios).
No equivale a afirmar que nunca se hizo. El sitio oficial, README y documentación
de osci-render no presentan un conector IanniX. No se inventa un antecedente.

La ruta más concreta para probar con herramientas ya mencionadas en el proyecto:

```text
IanniX → OSC → REAPER (aprendizaje de parámetro FX)
                     → osci-render como plugin → slider Lua → geometría/sonido
```

[REAPER documenta](https://www.reaper.fm/sdk/osc/osc.php) recepción OSC y asignación
de mensajes a parámetros de efectos con FX Learn. Por eso este esquema es una
inferencia técnica fundada, no una conexión ya validada. Hay que verificar que
el plugin instalado exponga el slider elegido y que IanniX envíe el dato esperado.
No requiere presumir OSC nativo en osci-render. Tampoco envía muestras de audio
por OSC: envía controles lentos, que Lua suaviza y usa al generar audio.

## Primera prueba futura, criterio de aceptación

1. Confirmar versiones de IanniX, REAPER y plugin osci-render; verificar un slider
   con mouse en el host antes de conectar redes.
2. Configurar un cursor de IanniX con un valor normalizado 0–1 y una salida OSC
   local. Elegir y documentar puerto/dirección en el receptor; no son valores
   predeterminados de osci-render.
3. Aprender ese mensaje en REAPER para un solo parámetro: radio/forma. Ver el
   slider moverse y comprobar los extremos contra la malla y el XY audible.
4. Detener IanniX y verificar que se conserva el último valor válido, sin saltos
   ni corte del audio. Guardar y reabrir el proyecto para comprobar persistencia.

Aceptación: captura de un cursor cambiando un coeficiente identificado, superficie
coherente, audio continuo y mapeo reproducible. Solo después añadir escenas,
controles de expresión y hardware. No se instalaron puentes ni se abrieron puertos.
