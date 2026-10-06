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

## Dos estudios controlables y previsualización XY

- El usuario evaluó positivamente el estudio del toro, informó escasa visibilidad
  y pidió control por potenciómetros y dos estudios similares. Registrados como
  EXP-009, EXP-010 y EXP-011. Marca/modelo y naturaleza del problema visual todavía
  pendientes de aclaración.
- Creados Órbitas (elipsoide cuadrático, 60 s a 72 BPM, 3/4) y Cristal (superficie
  cuártica, 71.11 s a 108 BPM, 4/4). A–E controlan tempo, forma, rotación, presencia
  y registro. Todos en cero producen la versión de referencia.
- Controles suavizados 35 ms; reloj y rotación integrados. La envolvente conserva
  presencia entre notas, con apagado al principio y al final. El original se conserva.
- Prueba completa con LuaJIT a 48 kHz para ambos: polinomio antes de cámara,
  coordenadas finitas/acotadas, actividad, final silencioso, reinicio y repetición
  determinista. Barridos extremos de A–E a 44.1 y 48 kHz aprobados.
  Picos de referencia: Órbitas 0.4674, Cristal 0.4983.
- WAV PCM y MP4 XY con audio generados localmente en `recordings/` (fuera de Git).
  Videos nuevos verificados con ffprobe: H.264 640×640 y AAC, duración 60.00 y
  71.11 s; revisados fotogramas de desarrollo. Son renders directos de la señal,
  no capturas del host. También se generó la previsualización del toro original:
  `recordings/estudio-de-un-toro.mp4`, 80 s, H.264 con audio AAC verificado.
- Guía de CC absolutos y sliders documentada. Las notas oficiales ubican MIDI
  Learn entre funciones premium; mapeo desde DAW como alternativa por verificar.
- Pendiente: prueba de los nuevos Lua en osci-render, controlador físico,
  persistencia de asignaciones y evaluación artística del usuario.
