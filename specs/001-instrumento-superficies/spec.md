# 001 — Instrumento sonoro de superficies algebraicas

Estado: prototipo 007 implementado y verificado fuera del host; integración y escucha pendientes.
Pedidos: EXP-004/006/007/009/019/020/021/022. Dirección confirmada por el usuario.

## Problema

AIRE fue valorado positivamente como música, pero el dibujo se percibe aleatorio
y rápido. Mezclar cuatro voces cambia la trayectoria XY y dificulta reconocer la
superficie. El nuevo instrumento debe partir de una superficie y su recorrido,
sin necesitar una partitura MIDI. MIDI CC puede seguir siendo un control físico:
eliminar notas MIDI como fuente musical no obliga a descartar ese protocolo.

## Requisitos

- **SUP-R01 — Superficie:** conservar ecuación `F(x,y,z)=0`, dominio, parámetros
  y malla con caras. Curvas sueltas no satisfacen este requisito.
- **SUP-R02 — Correspondencia:** mostrar la superficie 3D y su representación
  XY, explicando qué se pierde al proyectar y barrer. Identificar la señal real
  después de filtrado; no presentar el render sombreado como salida del audio.
- **SUP-R03 — Sonido desde geometría:** generar el sonido mediante un recorrido
  determinista de la superficie, sin secuenciador de notas como fuente principal.
  Mantener partitura y referencias Bach/Piazzolla como otra línea del laboratorio.
- **SUP-R04 — Legibilidad:** ofrecer una posición y un barrido estables que
  permitan reconocer la forma. Una mezcla visualmente confusa no se acepta solo
  porque las muestras originales pertenecieran a una superficie.
- **SUP-R05 — Dos velocidades:** separar movimiento/deformación lenta de escena
  y rapidez del barrido sonoro. Pausar la primera debe mantener el sonido. Cambiar
  la segunda sí puede cambiar altura, timbre y calidad del trazado; explicarlo.
- **SUP-R06 — Control gradual:** cambios de velocidad integrados y suavizados,
  sin recalcular `ángulo=tiempo*velocidad_actual`, que produce saltos al moverla.
- **SUP-R07 — Interfaz:** controles utilizables con mouse antes de exigir hardware.
  Nombres, rangos, unidades y valores iniciales visibles en una guía breve.
- **SUP-R08 — Entradas:** MIDI CC directo si el host lo permite; OSC mediante un
  receptor/puente explícito si no hay entrada nativa verificada. No inventar puertos
  o direcciones OSC de osci-render. No leer sockets en el hilo de audio.
- **SUP-R09 — Rendimiento:** extracción de malla, planificación del recorrido y
  simplificación fuera del cálculo por muestra; límites de densidad y último estado
  válido al fallar una edición. No prometer live coding arbitrario aún.
- **SUP-R10 — Timbre:** cumplir la especificación [002](../002-calidad-timbrica/spec.md).

## Contrato inicial de controles para el nuevo instrumento

Propuesta de implementación concreta, revisable con evidencia. No modifica el
mapeo de los estudios existentes, que tienen sus propias guías.

| Control | Entrada normalizada | Salida propuesta | Inicial |
| --- | --- | --- | --- |
| Movimiento | A, 0–1 | 0–0.20 rad/s, curva cuadrática; 0 detiene cámara/deformación | 0.25 → 0.0125 rad/s |
| Barrido | B, 0–1 | 20–120 ciclos/s, rango logarítmico | 0.5 → ~49 ciclos/s |
| Forma | C, 0–1 | Un coeficiente con rango válido para la familia elegida | Centro del rango |
| Calidez | D, 0–1 | Reducción gradual de contenido agudo, vinculada a 002 | Variante suave |
| Nivel | E, 0–1 | Ganancia final; 0 silencia | 0.35 |

El tamaño del recorrido y la frecuencia de muestreo limitan el barrido viable.
Estos rangos deben ensayarse con un recorrido reducido, no aplicar 120 ciclos/s
a miles de aristas y asumir que se verá bien. Los valores iniciales se establecerán
explícitamente en un preset o guía; un slider existente en cero no significa ausente.

## Aceptación

| ID | Prueba | Estado |
| --- | --- | --- |
| SUP-A01 | Malla cerrada, no degenerada, ecuación/residuos y dominio documentados (R01) | Toro/Cassini en EXP-019 y toro paramétrico cerrado en 007 verificados |
| SUP-A02 | Reconocer la misma superficie en vista 3D y host XY, registrar comparación (R02/R04) | Video comparativo 007 revisado; host y reconocimiento por usuario pendientes |
| SUP-A03 | Sonido sostenido sin MIDI de notas ni partitura (R03) | Aprobado fuera del host: tres renders de 12 s, 007 |
| SUP-A04 | A=0 congela escena durante 10 s sin silenciar; valores bajos lentos y sin saltos (R05/R06) | Prueba de pausa 10 s y controles a 44.1/48 kHz aprobada fuera del host |
| SUP-A05 | B modifica barrido sin alterar velocidad de escena; medir legibilidad/aliasing (R05) | Independencia y espectro estático verificados; host pendiente |
| SUP-A06 | Mover controles con mouse y guardar/reabrir preset (R07) | Pendiente en host |
| SUP-A07 | Un potenciómetro mueve un parámetro identificado; registrar dispositivo y CC (R08) | Pendiente, hardware desconocido |
| SUP-A08 | Si se usa OSC, registrar receptor, puerto, dirección y conversión; probar desconexión (R08) | Pendiente; OSC no confirmado |
| SUP-A09 | Cambios no bloquean audio; dato inválido conserva geometría anterior (R09) | Controles inválidos conservan radio; geometría fuera de audio; performance en host y edición de ecuaciones pendientes |

## Evidencia técnica actual

En fuentes locales 2.9.9.3, `Source/PluginEditor.cpp` dispone `Lua Sliders` debajo
del editor y lo oculta si el editor Lua no está abierto. `LuaComponent.cpp` crea
ese panel y `LuaListComponent.cpp` conecta sus parámetros. Los sliders son 0–1.

No se halló un receptor OSC de parámetros en la búsqueda sobre `Source` ni una
interfaz documentada en README/wiki. La copia tiene submódulos incompletos: esto
**no demuestra ausencia absoluta**, pero impide prometer conexión OSC directa.
MIDI Learn figura como función premium en las notas de versión consultadas.

## Fuera de alcance de la primera entrega

Rehacer Bach, arreglar cinco obras de Piazzolla, instalar una DAW, comprar premium,
modificar C++/JUCE, aceptar cualquier polinomio o añadir una interfaz de red sin
definir sus límites. La primera entrega será una superficie y un recorrido legible.

## Primera implementación (EXP-020/021/023)

[007 — Toro sonoro](../../experiments/007-toro-sonoro/README.md) conserva malla con
caras y usa un barrido de 24 vueltas, continuo y de resolución finita. No rellena
todos los puntos de la superficie. El tratamiento tímbrico atenúa los armónicos
23/24/25 y equivale a reducir el radio menor: las vistas distinguen esa diferencia.
Presets autónomos para escuchar; `control.lua` para sliders sin editar código.
Valores iniciales y límites están en su guía. No hay MIDI físico ni OSC verificados.
