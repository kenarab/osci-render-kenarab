# AIRE — Cuatro voces en el espacio

Una interpretación electrónica y geométrica del Air de la Suite n.º 3 de Bach,
BWV 1068/II. **3:50**, cuatro voces, 36 compases con repeticiones AABB, Re mayor.
Es una adaptación del original orquestal, no la transcripción exacta de Wilhelmj
para la cuerda de Sol. [Fuente, transformaciones y licencia](SOURCE.md).

## Primero, disfrutarla

### Nueva versión controlable: AIRE EXPRESIVO

El Adagio resultó demasiado lento para el usuario. El nuevo preset empieza en
**32 BPM** y dura **4:35**; los controles permiten elegir entre 20 y 52 BPM.
No se considera definitivo ese tempo ni se declara resuelta la sensación robótica.

- Escucha directa: abrir **[aire-expresivo.lua](aire-expresivo.lua)**. Usa valores
  internos; no necesita configurar sliders y no responde a ellos.
- Para intervenir: abrir **[aire-control.lua](aire-control.lua)** y ajustar los
  sliders según la tabla. No hace falta editar código.
- Audio completo: `recordings/005-aire-expresivo.wav`.
- Video de preescucha, primer minuto: `recordings/005-expresivo-muestra.mp4`.
- Comparación de voces: `recordings/005-voces.wav`, cuatro notas C4 de 6 s,
  en orden I–IV, igualadas a RMS 0.13 para comparar color y no volumen.

| Slider | Control | Valor inicial recomendado |
| --- | --- | --- |
| A | Tempo base `20 + 32 A` BPM, antes del rubato | **0.375 = 32 BPM**; 0.50 = 36 BPM |
| B | Expresión: fraseo, cadencias, vibrato y pequeños desfases entre voces | 0.65 |
| C | Color: grosor y filtro, con respuesta diferente en cada voz | 0.45 |
| D | Articulación: 0 más separada, 1 más ligada | 0.70 |
| E | Balance solista: 0 conjunto, 1 melodía al frente | 0.20 |

Los sliders están debajo del editor Lua; ver [guía](../../docs/controlador-y-visuales.md).
En el archivo controlable, A=0 significa 20 BPM: **configurar A primero**.
E es balance, no volumen. Usar el volumen general del host para escuchar bajo.
Suavizado de 80 ms, reloj integrado y conservación de controles ante NaN/infinito.
Cambiar `TAKE = 201` a `202` para reiniciar.

Los cuatro timbres tienen recorridos y filtros distintos: I, tubo fino y sonido
contenido; II, más armónicos pares; III, armónicos impares 3/5 y más cuerpo;
IV, tubo grueso con filtro más oscuro. Nombres descriptivos, no emulación acústica.
La expresión añade arcos de intensidad, vibrato gradual de distinta velocidad
por voz y desfases de ataque reproducibles de hasta 14 ms en el acompañamiento.
No se agregan notas aleatorias. Mover C no equivale a elegir un instrumento
acústico por voz: esa interfaz más amplia aún no existe.

Sigue siendo una suma de señales: **no muestra cuatro superficies completas**.
El filtro por voz cambia su trayectoria XY. Para ver la comparación entre malla
y sonido está [Toro sonoro](../007-toro-sonoro/README.md), cuya primera versión
el usuario describió como estática; su timbre no fue aceptado.

```sh
python3 scripts/build_bach_air.py
luajit scripts/render_bach_air.lua recordings/005-aire-expresivo experiments/005-aire-de-bach/aire-expresivo.lua
luajit scripts/check_bach_expression.lua
ffmpeg -i recordings/005-aire-expresivo.wav -t 60 -af afade=t=out:st=59:d=1 -c:a pcm_s16le recordings/005-expresivo-muestra.wav
python3 scripts/preview_xy.py recordings/005-expresivo-muestra.wav recordings/005-expresivo-muestra.mp4
```

Motor editable: `engine-expresivo.lua.in`. Misma fuente/licencia y 980 eventos.
Render completo: 274.567 s; pico 0.54046, RMS XY 0.13769, delta 0.04398, fin
silencioso y reinicio. Prueba de `aire-control.lua` a 44.1/48 kHz: extremos 20/52 BPM,
continuidad, polinomios y controles inválidos aprobados; delta máximo 0.04190.
La prueba de controles simula sliders en Lua; **no certifica MIDI/OSC físico**.
Escucha expresiva y ejecución dentro del host pendientes.

### Nueva versión: AIRE ADAGIO

Pedido EXP-024: más lento y expresivo. Abrir **`aire-adagio.lua`** o escuchar
`recordings/005-aire-adagio.wav` / `recordings/005-aire-adagio.mp4`.
Duración de referencia **5:39**, frente a 3:50 del original: tempo base 26 BPM,
arcos de intensidad de ocho negras, acompañamiento más contenido, ataques suaves
y respiración gradual en cadencias. Conserva las mismas 980 notas/eventos.
La cámara gira más lentamente. Esto sigue siendo la mezcla de cuatro recorridos,
no una visualización de superficies completas ni el nuevo instrumento de timbres.

Empezar con A–E en **0**, sin efectos añadidos y volumen bajo.
**A ahora significa Lentitud: 0 = 26 BPM, 1 = 18 BPM**, antes del rubato.
B, D y E mantienen sus funciones; C aumenta la cámara de 0.006 a 0.041 rad/s.
Para reiniciar cambiar `TAKE = 101` a `102`; usa otra serie para aislar el estado
del original al cambiar de archivo. La expresividad sigue pendiente de tu escucha.

```sh
python3 scripts/build_bach_air.py
luajit scripts/render_bach_air.lua recordings/005-aire-adagio experiments/005-aire-de-bach/aire-adagio.lua
python3 scripts/preview_bach_air.py recordings/005-aire-adagio
```

Motor editable: `engine-adagio.lua.in`. Fuente y licencia: [SOURCE.md](SOURCE.md).
Render completo a 48 kHz: 339.066 s, pico 0.73115, RMS XY 0.15147 y delta
máximo 0.05119. Verificados final silencioso, reinicio y CC a 44.1 kHz.

### Original conservado

- Video con audio: `recordings/005-aire.mp4`.
- Audio sin compresión: `recordings/005-aire.wav`.
- Para tocarla en osci-render: abrir **`aire.lua`**, no `engine.lua.in`.

Empezar con volumen bajo, los sliders Lua A–E en **0**, sin efectos añadidos ni
disparo de notas MIDI. El Lua contiene toda la partitura: no requiere cargar el
MIDI, instalar bibliotecas o conectar una DAW para reproducirlo.
Termina en silencio; cambiar `local TAKE = 1` por `local TAKE = 2` para reiniciar.
Si conservó ajustes de otra prueba, volver A–E a cero antes de reiniciar.

| Tiempo de referencia | Episodio | Desarrollo |
| --- | --- | --- |
| 0:00–0:38 | Hilo | Melodía al frente y acompañamiento más contenido |
| 0:38–1:16 | Bóveda | Repetición A con mayor profundidad y apertura |
| 1:16–2:32 | Penumbra | Sección B: contrapunto y cambio de perspectiva |
| 2:32–3:50 | Luz | Repetición B, mayor riqueza armónica y cadencia ralentizada |

Hay respiración leve de compás, relajación de cadencias, vibrato discreto en la
melodía, ataques según duración y una fermata temporal por ralentización final.
Los títulos son nuestra lectura artística; no movimientos adicionales de Bach.

## Qué estás viendo y oyendo

Pensá el audio como un lápiz: el canal izquierdo indica dónde está horizontalmente
y el derecho dónde está verticalmente. Al recorrer una figura cientos de veces
por segundo escuchamos una nota. Cambiar esa rapidez cambia la altura musical;
cambiar la forma cambia el timbre.

Esta obra tiene cuatro lápices matemáticos: violín I, violín II, viola y continuo,
cuyas notas vienen de la edición de Mutopia. Cada voz recorre un toro algebraico.
Sumamos las cuatro señales para escuchar el contrapunto; en la pantalla aparece
**una trayectoria resultante**, no cuatro instrumentos dibujados por separado.
Los acordes estables y las disonancias producen texturas diferentes.

El instrumento es sintético: no intenta simular fielmente una orquesta de cuerdas.
La base toroidal favorece un sonido sostenido, con armónicos moderados. No hay
samples comerciales, base musical independiente ni figuras desconectadas del WAV.
En el video, color, persistencia luminosa, títulos y capítulos son decisiones
gráficas. El trazo proviene de las muestras X/Y, sin sustituirlas por una animación.

## Cómo intervenir sin programar

Durante la reproducción, mové **un solo slider Lua** lentamente y escuchá:

| Slider / perilla | Tu gesto | Qué cambia |
| --- | --- | --- |
| A — Pulso | Acelerar la interpretación | Tempo base de 38 a 54 BPM, conservando las notas |
| B — Materia | Dar más cuerpo al sonido | Grosor del toro y riqueza armónica |
| C — Mirada | Girar el espacio | Velocidad de cámara, también cambia la mezcla XY audible |
| D — Solista | Acercar la melodía | Reduce acompañamiento y realza ligeramente violín I |
| E — Apertura | Abrir la figura | Escala vertical y balance entre canales |

Todos los controles se suavizan durante 80 ms. No hace falta moverlos: la obra
ya tiene un desarrollo programado. Las duraciones de la tabla corresponden a A=0.
Estos cinco nombres corresponden a **AIRE**, no al mapeo de los estudios anteriores.

Primera intervención sugerida: escuchar Hilo sin tocar nada; en Bóveda llevar B
a 0.3; en Penumbra llevar D a 0.5 para reconocer la melodía; en Luz devolver D a
cero y aumentar E lentamente. El volumen general se controla en el host.

## ¿Controlador directo o software adicional?

Un controlador que envía MIDI CC puede conectarse directamente a osci-render
**si tu edición ofrece MIDI Learn**. Habilitar la entrada MIDI, abrir el menú
contextual de Lua Slider A, activar aprendizaje y girar una perilla. Repetir
con B–E. Usar CC absolutos 0–127. Guardar el proyecto y verificar el mapeo al reabrir.

Las notas oficiales sitúan MIDI Learn entre funciones premium: no suponemos que
esté en tu edición gratuita. Si falta, se puede mapear desde una DAW al plugin;
ya hay DAWs instaladas en este Mac, aunque ese flujo aún no se probó. No instalamos
ni compramos nada. [Guía general y referencias](../../docs/controlador-y-visuales.md).
Falta conocer marca/modelo de tu controlador y confirmar edición de osci-render.

## Geometría, reproducción y comprobaciones

Cada voz usa `u=θ`, `v=2θ+desfase` y
`x=(R+r cos v) cos u`, `y=(R+r cos v) sin u`, `z=r sin v`.
Cumple `(x²+y²+z²+R²−r²)²−4R²(x²+y²)=0` antes de rotación, envolvente y mezcla.
La suma de voces no está restringida a un único toro. Mantener ese detalle evita
confundir música polifónica con renderizado de una superficie implícita completa.

```sh
python3 scripts/build_bach_air.py
luajit scripts/render_bach_air.lua
python3 scripts/preview_bach_air.py
```

El importador verifica cuatro voces, alturas iniciales, longitud de 76 negras
escritas y ausencia de solapamientos en cada voz; despliega casillas y repeticiones
a 144 negras y 980 eventos. `score.json` conserva notas, fuente y hash del MIDI.
`aire.lua` es generado y autónomo; editar `engine.lua.in` para cambios permanentes.

El render completo a 48 kHz verificó salida finita, pico **0.75060**, RMS XY
**0.16765**, diferencia máxima entre muestras **0.05527** y final silencioso.
También se comprobaron reinicio TAKE y movimientos extremos de controles a
44.1 kHz. El WAV guarda la señal PCM estéreo de 16 bits; el MP4 utiliza AAC y no
reemplaza ese WAV para alimentar un osciloscopio físico.

Pendientes: valoración auditiva del usuario, reproducción y rendimiento dentro
de osci-render, controles físicos y comparación con la captura del host. Las
verificaciones numéricas no certifican por sí solas la calidad musical.
