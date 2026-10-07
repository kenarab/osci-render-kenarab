# 012 — Superficies XYZ y una voz aislada

Corrección de EXP-040, requisitos XYZ-01…05. Son pruebas diagnósticas nuevas;
la calidad del sonido y la aceptación en osci-render siguen pendientes.

## Probar primero

Abrir `esfera.lua`, `elipsoide.lua` o `cuartica.lua` en osci-render, con volumen
bajo. Devuelven **tres coordenadas de la superficie**, sin banco plano ni OBJ.
Las versiones `-control.lua` usan A para giro de escena (0 = pausa), B para
barrido (12–36 Hz, centro 24), C para un parámetro de forma. No confundir barrido
con tempo. Son barridos densos sobre F=0; un osciloscopio traza líneas, no caras.
La cámara del host debe permitir apreciar profundidad; configuración y versión
instalada todavía no comprobadas en esta entrega.

Abrir `../../apps/xyz-stage/index.html` para inspeccionar las caras y el recorrido
XYZ real de estos tres ejercicios. Arrastrar para girar. Incluye mallas de Barth,
Togliatti, Endrass y Kummer de la biblioteca SURFER: son aproximaciones recortadas
al dominio del catálogo, no certificaciones de singularidades ni topología.
El visor conserva XYZ hasta la cámara final; no es una captura del host.

## Música: una voz primero

Resultados locales, fuera de Git:

- `../../recordings/012-bach-solo-xyz.lua`: Violino I, 34 notas.
- `../../recordings/012-oblivion-solo-xyz.lua`: flauta, 25 notas.
- Cada uno tiene una variante `-control.lua`: A tempo 0.5–1.5× (centro = original),
  B giro 0–0.2 rad/s (0 pausa), C coeficiente k de 0.1 a 0.9 (centro = 0.5).

Ambos duran 40 segundos al tempo original, correspondientes al fragmento 30–70 s.
Bach usa la partitura local de 005 y el Adagio a 26 BPM con rubato/cadencias;
Oblivion usa los eventos locales ScoreBase de la semilla, con su procedencia
registrada en `docs/proyecto-piazzolla`. Las notas derivadas no se versionan aquí.

La superficie es `X^4 + 3Y^4 + 6Z^4 + k*(X²+Y²+Z²) = 1`.
Cada nota barre la superficie con 12 vueltas longitudinales por período.
La envolvente escala uniformemente el objeto y el giro conserva distancias.
Los silencios retornan el origen. No se mezclan coordenadas de instrumentos.
No se aplica filtrado espectral: puede haber aliasing y aspereza; **no afirmamos
que el sonido sea mejor**. El propósito inmediato es reconocer una superficie
verdadera en la salida de una voz.

En modo musical, el visor muestra la superficie de referencia y la actividad
de esas notas, sin audio ni trazado de muestras musicales. No reproduce la
escala de la envolvente. Elegir otro modelo en el visor NO cambia el Lua:
asignación dinámica host↔visor y timbres de superficies récord quedan pendientes.

## Reproducir

Desde la raíz, con Python, LuaJIT y las fuentes musicales locales ya disponibles:

```sh
python3 scripts/build_xyz_exercises.py
luajit scripts/check_xyz_exercises.lua
python3 scripts/build_xyz_stage.py
python3 scripts/build_xyz_solos.py
luajit scripts/check_xyz_solos.lua
node scripts/check_xyz_stage.cjs
```

La biblioteca de ecuaciones, mallas y plantillas no contiene notas musicales.
Los generadores resuelven la cuártica radial de forma analítica, sin meshing ni
búsqueda de raíces por muestra. Las mallas se preparan fuera del audio.

Evidencia: `validacion.json` comprueba F=0 y covarianza de rango 3 de los ejercicios;
`solos.json` registra recortes. Test musical a 44.1/48 kHz: residuo máximo
2.45e-15 tras deshacer giro/escala, determinantes positivos >1.26e-6, fin,
reinicio y tempo aprobados. Esto no valida percepción ni configuración del host.
