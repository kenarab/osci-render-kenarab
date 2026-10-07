# Biblioteca de superficies algebraicas

Independiente de Bach y de cualquier partitura. Las ecuaciones son la fuente de
verdad; los OBJ son recursos opcionales conservados del experimento anterior.
La biblioteca no requiere ni abre osci-render.

- `catalog.json`: ecuaciones y parámetros de SURFER, procedencia y hashes.
- `catalog.js`: distribución del catálogo para clientes de navegador sin servidor.
- `core.py`: extracción opcional con tetraedros, vista de mallas y momentos de área.
  Su evaluador Python sólo admite fórmulas locales de confianza del catálogo;
  no utilizarlo para texto arbitrario ni como parser de un editor público.
- `build.py`: genera recursos sin música. Desde la raíz:
  `PYTHONPATH=library python3 -m algebraic_surfaces.build`.
- `assets/`: OBJ, imagen y métricas geométricas; aproximaciones en dominio finito.

Bach importa esta biblioteca. Los bancos Lua se conservaron idénticos byte por
byte al separarla. La asignación de timbres/alturas, filtros y partitura pertenece
al proyecto musical, no al catálogo.

Para agregar una superficie, editar `catalog.json`, registrar ecuación, parámetros,
dominio y fuente; regenerar recursos. No atribuir un récord por la apariencia ni
considerar completa una superficie no compacta recortada en una caja.

## Editor directo

Abrir [Superficies en vivo](../../apps/surface-lab/index.html): ecuaciones, parámetro
a y render implícito WebGL sin OBJ. `expression.js` ofrece AST, evaluación y GLSL
sin ejecutar código del usuario. [Uso y límites](../../apps/surface-lab/README.md).

## Bancos e instrumentos independientes

`timbres.json` registra cuatro bancos por ID de superficie, hash de malla y receta;
`timbres.lua` contiene sólo tablas sonoras, sin partitura. Se generan mediante
`PYTHONPATH=library python3 -m algebraic_surfaces.timbres`, sin repertorio.
La prueba de Oblivion consume este generador desde un script separado. El primer consumidor es `player.lua.in`: tres grupos de instrumento,
selección independiente y transición suave entre bancos, conservando la polifonía.
Los bancos pueden incorporarse a cualquier pieza; editar ecuaciones en vivo requiere
un generador asíncrono y un puente aún pendientes.

## Ruta XYZ (012)

`xyz.lua.in` y `solo_xyz.lua.in` conservan coordenadas de una superficie verdadera.
`geometry3d.js` contiene mallas reutilizables y recorridos de diagnóstico, sin notas.
Los bancos espectrales anteriores no equivalen a esta geometría. Ver
[ejercicios y límites](../../experiments/012-superficies-xyz/README.md).
