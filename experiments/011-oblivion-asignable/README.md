# Oblivion — timbres asignables por instrumento

EXP-039 / INS-02–05. Fragmento **30–70 s** del arreglo ScoreBase 38762 reunido en
la semilla. Fuente: [ficha](https://scorebase.org/scores/38762), crédito del PDF:
José Bragato; XML: flauta, fagot y piano. Atribución/licencia abierta no verificadas.
No se publican notas/MIDI/Lua musical: permanecen en `recordings`/`downloads`, fuera de Git.

[Escuchar/ver prueba](../../recordings/011-oblivion.mp4) ·
[WAV](../../recordings/011-oblivion.wav) ·
[Lua preset](../../recordings/011-oblivion.lua) ·
[Lua con controles](../../recordings/011-oblivion-control.lua).

Abrir un solo Lua, volumen bajo. El preset ignora sliders; la variante controlable
permite cambiar **independientemente** la superficie que provee timbre a cada instrumento:

| Slider | Función | Referencia |
| --- | --- | --- |
| A | Superficie de flauta | 0: Barth |
| B | Superficie de fagot | 0.33: Togliatti |
| C | Superficie del piano (ambas manos) | 1: Kummer |
| D | Velocidad temporal 0.5–1.5; mantiene alturas | 0.5: tempo original |
| E | Brillo de los tres instrumentos | 0.4 |

Selección A/B/C: [0,0.25) Barth; [0.25,0.5) Togliatti; [0.5,0.75) Endrass;
[0.75,1] Kummer. Al cruzar un umbral se mezclan bancos durante una transición
exponencial de 80 ms, sin reiniciar fase ni notas. Son bancos precalculados:
no se modifica aún la ecuación durante el audio. TAKE=501 y reinicio de step reinician.

`config.json` identifica instrumentos, pistas de origen, asignación inicial,
procedencia y recorte. Las dos pistas de piano comparten selector pero conservan
sus notas simultáneas. La prueba usa 312 eventos; los que cruzan límites del fragmento
se recortan y registran, sin inventar duración para eventos nulos.

Los timbres vienen de `library/algebraic_surfaces/timbres.lua`, registrados en
`timbres.json`. Todos los instrumentos pueden usar cualquier banco. El reproductor
`player.lua.in` recibe bancos y eventos; ni la ecuación ni su malla pertenecen a esta
pieza. Este primer reproductor tiene tres grupos de instrumento; no es aún un
editor general de ruteo para un número arbitrario de pistas.

El video muestra **la suma XY del audio**, con etiquetas de asignación. No conserva
los dibujos de las tres superficies: asignar timbre a una voz no dibuja la malla.
Para experimentar con forma visible, usar los ejercicios 010 y el editor implícito.

## Reproducir

```sh
python3 scripts/build_assignable_study.py
luajit scripts/render_small_studies.lua
python3 scripts/preview_small_studies.py
```

Requiere el MIDI ya importado de la semilla y recursos de la biblioteca. El generador
reemplaza sus salidas. No se inicia audio en el host automáticamente.
Pruebas: polifonía (hasta siete notas activas), señal acotada, fin silencioso,
reinicio y selección de bancos a 44.1/48 kHz. Prueba auditiva, mapeo externo y
rendimiento en la versión Pro quedan pendientes con el usuario.
