# Identidades y reproductor de voces — VIV-01…06

Biblioteca independiente de las piezas. `geometry.py` y `geometry.lua` comparten
cuatro parametrizaciones; `identities.json` registra ecuación, dominio y receta.
`player.lua.in` recibe notas, voces y asignaciones del adaptador de repertorio.
No depende de un canal MIDI fijo ni posee las notas de Bach/Piazzolla.

Cada identidad sonora se deriva de un recorrido XYZ, incluida su profundidad,
mediante coeficientes de Fourier, fundamental explícita y nivel calibrado. Se
precargan cuatro bandas (2/4/8/12 armónicos, 512 muestras). Se elige la banda más
rica cuyo último parcial está por debajo de .42*sample_rate para esa nota.
La interpolación puede introducir imágenes residuales: no es garantía de ausencia
absoluta de aliasing. Timbres perceptualmente distintos/agradables: pendientes.

Los selectores por voz mezclan bancos con constante temporal de 80 ms, preservando
fases y eventos. La histéresis .012 alrededor de umbrales evita jitter MIDI; usar
los centros .125/.375/.625/.875 (aproximadamente CC 16/48/79/111). No hay cola de
recálculo: paleta precargada. Escenas persistentes y cambio entre motores arbitrarios
siguen pendientes. Son asignaciones intercambiables dentro de un motor común.

Modo mezcla: devuelve XY de todas las voces y z=0; **no representa superficies**.
Modo voz XYZ: devuelve puntos de la identidad seleccionada, con rotación y escala
uniforme de expresión/envolvente. Durante cambio de identidad la geometría cambia
sin interpolarla: un fundido de coordenadas no conservaría F=0. Ese cambio puede
ser audible; la transición sonora suave se garantiza por diseño sólo en la ruta
de bancos, pendiente de escucha. Una parte polifónica muestra su nota activa más
aguda; los demás eventos se conservan en la mezcla pero no se suman visualmente.

Roman muestra la parte compacta parametrizada; la ecuación también se anula sobre
extensiones de los ejes que no se incluyen. Cono recortado a |z|<=.7. Son referencias
matemáticas discretizadas, no certificaciones topológicas. No son las superficies
récord de la biblioteca SURFER: ésta permanece intacta para siguientes pruebas.

Generadores: `scripts/build_live_voices.py`, `scripts/build_diverse_surfaces.py`.
Sólo escriben los nuevos experimentos 015/016/017 y recursos de esta biblioteca.
Pruebas: `check_live_voices.lua`, `check_diverse_gallery.cjs` y renders offline con
`render_live_voices.lua`. No se alteran 001–014 ni archivos .osci del usuario.

`transport.lua` añade un transporte independiente de la síntesis: posición J,
pausa K y reinicio L, con fundidos de 20 ms. El generador precalcula índices de
notas por segundo; la búsqueda reconstruye las notas sostenidas sin recorrer
toda la partitura por muestra. J manda una posición y no indica el avance actual.
La historia de filtros no se reconstruye. Integración y límites en
[experimento 021](../../experiments/021-transporte-lua/README.md).

`meditative.lua.in` es el motor autónomo del [022](../../experiments/022-jardines-meditativos/README.md):
sin partitura, con cuatro voces sostenidas y ocho controles comunes. Su variante
XYZ preserva geometría; su variante sonora interpola momentos de todas las caras,
añade fundamental y espacio estéreo, sin conservar la ecuación en la mezcla.
Bancos/geometría se generan fuera del audio; no modela vibración física de membranas.
