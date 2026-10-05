# Bitácora

## 2026-10-04 — Preparación

- Repositorio de laboratorio inicialmente vacío, salvo `.git`.
- No existe `../osci-render-version`; la copia encontrada es
  `../osci-render-2.9.9.3`.
- Contiene `.jucer`, fuentes y declaración de submódulos; no contiene una app
  compilada en su raíz. `modules/osci_scripting` está vacío.
- No apareció osci-render entre las aplicaciones de `/Applications` ni en la
  búsqueda limitada a tres niveles de `~/Downloads` y `~/Applications`.
  Sí apareció `~/Downloads/Oscilloscope.app`, que es otra aplicación.
- Mac ARM64; disponibles `lua`, `luajit` y `python3` mediante Homebrew.
- No hay herramienta de consulta de cuota disponible en esta sesión.
- Documentados objetivos, responsabilidades de agentes y secuencia de pruebas.
- Creados tres ejemplos Lua originales para círculo, Lissajous y curva sobre toro.

### Estado al terminar la preparación inicial

- Verificación matemática: los tres archivos pasaron con Lua y LuaJIT, con 4097
  muestras cada uno. Se verificaron coordenadas finitas, amplitud, cierre, radio
  del círculo y ecuación implícita del toro.
- Descarga: la API oficial de GitHub confirmó que la release v2.9.9.3 tiene cero
  assets descargables. La web oficial enlaza a ReleasePlane. Se descargó el
  instalador macOS universal a `/tmp/osci-installer.dmg` y se montó en modo lectura
  en `/Volumes/osci-installer`.
- Instalador abierto: seleccionado `osci-render` → `Get osci-render free`.
  Ahora muestra `Before continuing`, con botones para Privacy Policy y Terms &
  Conditions. Aceptación de términos desmarcada; estadísticas anónimas marcadas
  por defecto; Continue deshabilitado. No se aceptaron acuerdos ni se continuó.
- Bloqueo concreto: falta confirmación explícita del usuario para aceptar los
  términos. La política de control de aplicaciones requiere esa confirmación.
  La instalación y el arranque del sintetizador aún no se completaron.
- El control de UI tardó varios minutos por llamada; conviene que el usuario
  complete ese diálogo directamente si desea evitar más espera.
- Imagen, escucha y edición en vivo dentro de osci-render: pendientes.

## Actualización posterior — primera ejecución confirmada por el usuario

- El usuario confirmó que completó la instalación y ejecutó los tres ejemplos.
  Esto supera el bloqueo de instalación de la entrada anterior.
- Considera los ejemplos demasiado simples y solicita explorar una composición
  más compleja, como las de los videos, idealmente con geometría algebraica.
- Pide buscar antecedentes y registrar todos los experimentos solicitados.
- No se infieren de esa confirmación la versión instalada, los ajustes de audio,
  una grabación ni una prueba de edición en vivo; siguen sin registrarse.
- Pedidos y propuestas organizados en [el registro de experimentos](experimentos.md).
- Investigación inicial: antecedentes de composición paramétrica y live coding
  de curvas sobre toros. No se verificó un puente Surfer Shuffle → osci-render
  ni una composición basada en superficies implícitas arbitrarias.

## EXP-002 — Primer prototipo de Estudio de un toro

- Propuesta aceptada por el usuario e implementada en
  `experiments/002-estudio-de-un-toro/estudio.lua`.
- 80 segundos a 96 BPM, 32 compases; presentación de 0–20 s, desarrollo de
  20–60 s y retorno de 60–80 s. Final en silencio, reinicio mediante `TAKE`.
- Secuencia menor con respuestas, cambios de raíz, acentos y silencios.
  Recorridos sobre un toro de radios variables; rotación 3D y envolvente común
  a imagen y sonido. No depende de MIDI ni de bibliotecas externas.
- `luajit scripts/check_torus_study.lua recordings/estudio-de-un-toro.wav`
  completó dos pasadas de 80 segundos por frecuencia (44.1 y 48 kHz): cotas,
  señal finita, actividad de las tres secciones, continuidad en cambios de nota,
  determinismo, silencio final y reinicio con TAKE. Picos: 0.409116 y 0.409109.
- WAV de preescucha generado a 48 kHz, estéreo de 16 bits; excluido de Git.
  Es la salida directa X/Y del script, no una grabación de osci-render.
- Pendiente: apertura y escucha del nuevo prototipo en osci-render, rendimiento
  en el host y valoración artística del usuario. No se verificó todavía la
  edición de controles durante la reproducción en el editor de la aplicación.
