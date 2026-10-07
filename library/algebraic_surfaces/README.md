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
