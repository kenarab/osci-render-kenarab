# Objetivos y decisiones iniciales

## Intención artística

Crear un instrumento para ver y escuchar geometría, disfrutar piezas musicales y
experimentar con la relación entre forma, recorrido, timbre y movimiento. Recuperar
las ideas de Surfer Shuffle sin limitar el instrumento a superficies aleatorias.

## Objetivos

1. Arrancar osci-render en este Mac y establecer una sesión reproducible.
2. Ver y escuchar círculo, Lissajous y un recorrido sobre un toro algebraico.
3. Explorar superficies escritas a mano como `F(x,y,z; parámetros)=0`, además de
   parametrizaciones explícitas cuando existan.
4. Incorporar generación aleatoria con semilla, grado y complejidad acotados;
   recuperar el generador anterior cuando dispongamos de su código.
5. Hacer live coding: editar ecuaciones y parámetros y percibir el cambio visual
   y sonoro durante la ejecución.
6. Componer pequeñas piezas: presets, transiciones, tempo y controles MIDI/DAW.
7. Guardar ecuaciones, parámetros, semillas, proyectos y grabaciones para repetir
   y comparar los experimentos.
8. Explorar integración directa de geometría con osci-render; modificar el motor
   solo si las interfaces existentes no alcanzan.

## Distinción fundamental

Una superficie implícita es un conjunto bidimensional en el espacio. El audio
estéreo describe un recorrido temporal `(X(t), Y(t))`. Necesitamos elegir curvas
sobre la superficie, contornos o aristas, ordenarlas y proyectarlas. Esa elección
afecta tanto la imagen como el sonido: más detalle no garantiza mejor resultado.
No basta con enviar a osci-render la imagen sombreada que produce SURFER.

## Herramientas y arquitectura propuestas

| Herramienta | Función | Momento |
| --- | --- | --- |
| osci-render standalone oficial | Síntesis y osciloscopio integrado | Primero |
| Lua dentro de osci-render | Recorridos paramétricos y edición en vivo | Primero |
| Git + este repositorio | Versionar experimentos y decisiones | Desde ahora |
| Python + NumPy/SymPy | Ecuaciones, evaluación y generación con semilla | Al abordar implícitas |
| scikit-image | Extracción de isosuperficies con marching cubes | Prototipo de mallas |
| Exportación OBJ | Puente de geometría estática hacia osci-render | Tras el arranque |
| Blender + integración oficial | Cámara, animación y líneas de escenas | Si aporta al experimento |
| DAW existente (por elegir) | MIDI, automatización y piezas | Tras validar audio |
| C++/JUCE + clon upstream | Cambios en el motor | Solo ante una limitación medida |

Ya hay Blender, SURFER, REAPER, Ableton y otras herramientas en `/Applications`;
su presencia no implica compatibilidad ni funcionamiento verificados. No hace
falta instalar todo ni añadir un dispositivo virtual para la primera prueba.

Dos rutas complementarias:

```text
parametrización -> Lua -> osci-render -> audio estéreo / visualización XY
F(x,y,z)=0 -> geometría fuera del audio -> curvas o malla -> OBJ / puente futuro
                                                     -> osci-render
```

Empezaremos el live coding con el editor integrado. La recarga desde editores
externos y un eventual protocolo de streaming todavía deben comprobarse; no
suponemos que exista una API para recibir ecuaciones implícitas directamente.
Para implícitas, conservar el último resultado válido si una edición falla y
limitar resolución/tiempo de cálculo son requisitos del futuro puente.

## Etapas y aceptación

- **0 — Arranque:** aplicación abierta, versión registrada, dispositivo de salida
  confirmado y círculo visible. Confirmar escucha con el usuario.
- **1 — Pruebas mínimas:** abrir los tres Lua, registrar imagen/sonido y comprobar
  que editar un parámetro en el editor integrado produce el cambio esperado.
- **2 — Superficies:** esfera y toro como casos conocidos; obtener geometría de
  una ecuación implícita, exportarla y verla en osci-render. Medir complejidad y
  discontinuidades; no empezar con mallas densas.
- **3 — Generación:** guardar y repetir al menos una superficie por semilla;
  manejar resultados vacíos, singularidades y componentes desconectadas.
- **4 — Instrumento en vivo:** cambiar parámetros sin bloquear audio, conservar
  el último estado válido y medir latencia y comportamiento ante errores.
- **5 — Piezas:** guardar una sesión y una grabación estéreo reproducibles con
  las superficies y automatizaciones usadas.

## Decisiones pendientes

- Localizar el código original de Surfer Shuffle y elegir qué partes recuperar.
- Elegir la primera familia de superficies y la DAW, después de escuchar ejemplos.
- Definir más adelante si usaremos un osciloscopio físico además del virtual.
- Evaluar funciones gratuitas/premium según la versión instalada, sin compras
  ni activaciones automáticas.

## Referencias

- [Surfer Shuffle, IMAGINARY](https://www.imaginary.org/program/surfer-shuffle):
  generador basado en jsurf, con controles de semilla y grado.
- [osci-render, repositorio oficial](https://github.com/jameshball/osci-render)
- [Distribución oficial](https://osci-render.com/)
- [Versión correspondiente al ZIP local](https://github.com/jameshball/osci-render/releases/tag/v2.9.9.3)

Las herramientas geométricas son propuestas de arquitectura, todavía no
dependencias instaladas ni una integración implementada.
