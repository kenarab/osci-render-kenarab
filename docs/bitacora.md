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

## 2026-10-06 — AIRE / Cuatro voces en el espacio

- El usuario solicita una obra de mayor elaboración sobre el Air de Bach y una
  explicación comprensible de cómo intervenir con controlador. EXP-012/013.
- Obtenida edición Mutopia 242 de jeff covey, CC BY-SA 3.0, con fuentes LilyPond
  y MIDI orquestal. Conservados originales, procedencia y SHA-256; no samples.
- Importadas cuatro voces: 149/105/112/150 notas de origen. Desplegadas las
  repeticiones y casillas según la partitura: 282/200/215/283 eventos, 980 total,
  144 negras. Re mayor original, no transcripción literal de Wilhelmj.
- Adaptación: tempo base 38 BPM, respiración, cadencias y ralentización final;
  cuatro recorridos toroidales sumados, cinco controles suavizados, cuatro episodios.
- Render de 230.046 s a 48 kHz; pico 0.75060, RMS XY 0.16765, delta máximo 0.05527.
  Validaciones de notas iniciales, duración, monofonía por voz, final en silencio,
  reinicio TAKE, controles extremos a 44.1 kHz y tamaño íntegro del WAV aprobadas.
- Generador de video XY de concierto con persistencia óptica, capítulos y crédito
  en imagen. Solo la señal produce el trazo; color y composición gráfica editoriales.
- Video completo verificado: 230.046 s, H.264 960×960 y audio AAC; revisados
  fotogramas de Hilo (25 s) y Luz (180 s). Entrega en `recordings/005-aire.mp4`.
- Guía explica controles sin programar y condiciones de conexión MIDI directa.
  La apreciación sonora y la ejecución dentro de osci-render quedan pendientes.

## Corrección de alcance — superficies y repertorio Piazzolla

- El usuario solicitó Libertango, Oblivion, Violentango, Meditango y Solitude como
  referencias; registradas individualmente, con fuentes editoriales/discográficas.
  No se importaron partituras ni grabaciones ni se hicieron arreglos de Piazzolla.
- El usuario aclaró que las curvas anteriores no cumplen su pedido de visualizar
  superficies. Se corrigió el criterio en objetivos, instrucciones y experimentos.
- EXP-019: extracción implícita de toro y Cassini mediante tetraedros, con caras,
  exportación OBJ y vista sombreada. Mallas cerradas por incidencia de aristas,
  Euler 0/2 y residuos de vértices por debajo de 1e-9. Vista inspeccionada.
- Pendiente: importar y evaluar las mallas en osci-render, reducir/ordenar su
  barrido si hace falta y relacionar deformaciones con música. El render sombreado
  es una referencia geométrica, no una captura de audio.

## Dirección nueva y SDD

- El usuario valora AIRE, pero percibe su dibujo aleatorio y rápido; pide diseñar
  sonidos desde superficies, sliders lentos y aclarar MIDI/OSC. Añade prioridad
  de mejorar el timbre. No se interpreta como rechazo del control MIDI CC.
- Implementado el flujo SDD local: requisitos identificados, plan incremental y
  matrices de aceptación en specs/001 y specs/002. El nuevo motor no se declara
  implementado; la comparación de timbres sigue pendiente.
- Localización de Lua Sliders comprobada en fuentes 2.9.9.3: bajo el editor,
  visible solo al abrirlo. No se verificó todavía la interfaz instalada.
- OSC de parámetros no encontrado en fuentes/documentación revisadas; revisión
  limitada por módulos ausentes. Ruta directa MIDI o puente OSC según hardware.
- Completado el commit interrumpido de superficies: 34582b2. El usuario autoriza
  volver a solicitar el commit que rechazó por error.

## EXP-024 — AIRE Adagio

- El usuario pide ralentizar Bach y darle más expresión, manteniendo la dirección
  de superficies para el desarrollo tímbrico posterior. Se conserva el original.
- Nueva interpretación autónoma: base 26 BPM; A reduce hasta 18 BPM; cadencias
  con recuperación gradual, arcos de frase, acompañamiento contenido y cámara lenta.
- Render completo: 339.066 s, pico 0.73115, RMS XY 0.15147, delta 0.05119.
  Misma partitura de 980 eventos; sin clipping, final silencioso, TAKE y CC probados.
- Audio y video son renders fuera del host. Calidad artística y ejecución en
  osci-render siguen pendientes. No se presenta esta mezcla como superficie.

## EXP-020/021/023 — Toro sonoro

- Implementados tres presets autónomos y un Lua de control A–E sin partitura.
  Malla cerrada con caras, R=0.62 y r=0.24; parametrización para barrido continuo
  de 24 vueltas, representación finita que deja huecos, no relleno total de la superficie.
- Calidez atenúa armónicos 23/24/25 conservando el 1; equivale a un toro con radio
  menor reducido. Videos muestran superficie de referencia, XY crudo y XY tratado.
- Suave/Cuerpo/Aire: 12 s por variante, pico máximo 0.21866, RMS entre 0.09465 y
  0.09905, diferencia 0.395 dB. DC <0.001 y delta <0.04 en los clips.
- Comprobados a 44.1/48 kHz: pausa 10 s sin cortar audio, independencia de barrido,
  controles extremos, inválidos, silencio y reinicio. Espectro estático 20/120 Hz:
  armónicos hasta 3000 Hz; residuo relativo fuera de 1/23/24/25 <1e-16.
- Videos H.264/AAC, 1440×600, tres de 12 s y montaje de 36 s; fotograma de Cuerpo
  inspeccionado. Audio PCM X/Y sin compresión preservado en WAV. No son capturas del host.
- LuaJIT externo procesó 48000 muestras de control.lua en ~0.037 s CPU; no es una
  medición del hilo de audio de osci-render. No se instalaron dependencias.
- El usuario pregunta por MIDI/OSC: se confirmó expresamente que no hay prueba
  física; se solicitaron modelo de controlador y versión/edición, todavía sin respuesta.
  OSC nativo, hardware, escucha y performance en host continúan pendientes.

## EXP-025/026 — Ajuste tras escuchar el Adagio

- El usuario informa que 26 BPM resultó demasiado lento y pide tempo/expresión
  controlables y voces con timbres diferentes, menos robóticas.
- AIRE EXPRESIVO: preset 32 BPM y entregable para sliders A–E; rango 20–52 BPM,
  fraseo, articulación, color y balance. Cuatro perfiles de recorrido/filtro,
  vibratos propios y microdesfases de ataque deterministas. Se conservan versiones anteriores.
- Audio completo 274.567 s: pico 0.54046, RMS 0.13769, delta 0.04398, fin y TAKE
  aprobados. Prueba del Lua controlable a 44.1/48 kHz: tempo extremo, polinomios,
  continuidad y controles inválidos aprobados. No equivale a una prueba MIDI física.
- Muestra XY de 60 s y cuatro timbres aislados de 6 s al mismo RMS 0.13.
  Los timbres y la expresividad aún requieren escucha; no son cuerdas acústicas.

## Rechazo tímbrico e investigación de IanniX

- El usuario describe los toroides como estática, insiste en modificar superficies
  completas con controles y pregunta por demos e integración con IanniX, que ya usó.
  TIM-A05 y EXP-023 se marcan no aceptados; sin atribuir todavía una causa técnica.
- Se solicitaron contexto WAV/video frente a Lua/host y una demo de referencia.
  No se recibió respuesta al registrar esta entrada. La API Lua local documenta
  `step` por muestra, `sample_rate` y 26 sliders A–Z; no apareció un desajuste evidente
  con el modelo usado por las pruebas, pero eso no verifica el sonido en la app.
- No se encontró un antecedente exacto IanniX–osci-render en la búsqueda limitada.
  IanniX documenta OSC; REAPER documenta OSC y FX Learn. Se propone esa ruta para
  controlar el plugin, pendiente de una prueba de un solo parámetro.
- El conector oficial Blender/osci-render usa TCP/GPLA, no OSC. Blender es candidato
  para editar/ver la malla completa y obtener su representación de líneas hacia el host.
  Se conserva como pendiente el editor de superficies dinámicas; más densidad de
  trazado no garantiza mejor sonido. Fuentes y límites en docs/iannix-superficies.md.
- Registrada propuesta narrativa Respirar la materia (EXP-027), sin componer aún
  una obra larga; IanniX podría organizar escenas y curvas de control.

### Aclaraciones y lectura del host

- El usuario confirma: estática **con los Lua en osci-render**. Se solicita ahora
  comparación con `007-suave.wav`; no se atribuye el rechazo al WAV sin escucharlo.
- Referencia aportada: SURFER y sus galerías, incluidas superficies con singularidades;
  el usuario reafirma la autoría de su generador. Especificación 006 precisa el
  modelo implícito, editor de coeficientes y tratamiento explícito de singularidades.
- La UI leída muestra `aire-adagio.lua` y los sliders H–O; M fue editado. Los Lua
  entregados usan A–E. Se informó cómo desplazarse a esos controles. No se manipuló
  la app ni se obtuvo una grabación. La consulta tardó 240 s: no se repitieron
  llamadas lentas para adivinar una causa de ruido.
- Info.plist de la app: **2.9.9.10**, frente a fuentes de referencia 2.9.9.3.
  Se confirma presencia del panel; MIDI Learn, efectos y audio real siguen pendientes.

### Resultado de la comparación WAV/host

- El usuario confirma que `007-suave.wav` es distinto y más limpio que el Lua en
  osci-render. Aclara después que tampoco le gusta ese timbre: “suena como estática”
  es su descripción perceptual. El rechazo artístico no se reduce a un fallo técnico.
- TIM-A05 sigue no aceptado. Quedan separados el rediseño sonoro y el diagnóstico
  de la diferencia con el host; no se atribuye causa sin una grabación/configuración.
- Antes de otra generación larga, priorizar una superficie implícita de referencia
  y una muestra breve que permita elegir dirección tímbrica. Bach controlable y
  la comparación de cuatro voces ya están disponibles como entregas independientes.

## 2026-10-06 — MIDI, premium y host; preferencia por Adagio

- EXP-030: comparación documentada en `docs/midi-premium-live-reaper.md`, con
  fuentes oficiales, precios comprobables y protocolo de aceptación. REAPER
  ofrece recepción OSC/FX Learn; propuesta para alojar osci-render e integrar IanniX.
- Inventario de Info.plist: REAPER 5.04 y Live 9.1 ya instalados; osci-render
  2.9.9.10 en app, AU y VST3. No confundir instalación con compatibilidad o licencia.
- Recomendación: evaluar REAPER actual antes de comprar premium sólo por MIDI.
  La automatización de sliders del plugin gratuito necesita prueba en el host;
  la referencia fuente 2.9.9.3 no basta para validar el binario instalado.
- Última preferencia del usuario: Adagio es su Bach favorito; se actualizan registro
  y especificación sin modificar música ni borrar variantes.
- Verificación de esta etapa: documentación y enlaces locales; sin cambios de código,
  instalación, compra, prueba física o nueva renderización de audio.

## 2026-10-06 — Nuevas materias para el Adagio (EXP-031)

- El interés por premium incluye explorar el instrumento y su interfaz, no sólo MIDI.
  El usuario considera instalar DAW actual; no se instala en esta etapa.
- 008 conserva la interpretación Adagio con dos orquestaciones: superficies cuárticas
  y modulación de fase precalculada. Cada voz tiene espectro y evolución diferentes.
- Cuatro mallas cerradas completas y vista sombreada; la señal audible es sonificación
  filtrada de recorridos, no una visualización completa de las superficies. Editor
  SURFER, singularidades y actualización conjunta de coeficientes siguen pendientes.
- Dos WAV completos de 339.066 s, picos 0.65084/0.60245; continuidad, fin y reinicio
  aprobados. Ocho timbres aislados a igual RMS, controles a 44.1/48 kHz y comparación
  audiovisual con el Adagio original. Falta escucha del usuario y prueba en host.

## 2026-10-06 — Ingreso de repertorio Piazzolla (EXP-032)

- Localizadas ofertas MIDI específicas: Libertango de GEERDES y Oblivion, arreglo
  de Play The Piano en Pianosolo. Procedencia, alcance, precios consultados y enlaces
  en `docs/referencias-piazzolla.md`. No se compraron ni descargaron archivos.
- Importador SMF 0/1 preparado: notas polifónicas, velocidad, pistas, canales,
  tempo/segundos, CC, programas y SHA-256/procedencia. Salida privada en recordings.
- Prueba sintética de dos tempos, acordes y running status, rechazo de entradas
  inválidas y lectura de las 516 notas del MIDI fuente de Bach: aprobadas.
- Falta el archivo elegido para producir arreglos musicales; aún no hay Piazzolla
  sonando en Lua. Se pidió enlace al usuario y aclaración de Solitude. No se
  presenta infraestructura ni una propuesta de orquestación como obra terminada.

## 2026-10-06 — Atlas Piazzolla, planificación para otro repositorio (EXP-033)

- Pedido: reunir tantos arreglos como podamos y construir un archivo amplio de
  Piazzolla. El usuario decide planificar aquí y ejecutar después en otro repositorio.
- Entregados `docs/proyecto-piazzolla/README.md` y `fuentes.json`: alcance, entidades,
  ATL-01–09, etapas, semillas, transferencia del importador y prompt de arranque.
- Recolección interrumpida: un HTML público de Oblivion/Songparts descargado y
  registrado por hash; ningún MIDI/PDF/MusicXML musical confirmado. No se creó repo.
- Diagnóstico observado: curl falló por DNS en sandbox y funcionó al autorizar red.
  No se observó evidencia de bloqueo por User-Agent. Registrar la causa específica
  y usar navegador cuando el flujo público lo requiera; sin asumir éxito tras aborto.
- Verificación de esta entrega: JSON válido, enlaces locales, hash del HTML y diff.

## 2026-10-06/07 — Colección semilla del Atlas (EXP-034)

- Usuario precisa: colección amplia futura en otro repositorio; aquí lote semilla.
  Incluir PDF, MIDI, notación abierta, fotos y escaneos; conservar variaciones para
  estudiar interpretación y convertirlas sin perder originales (ATL-10/11).
- Obtenidos 19 archivos válidos: 10 MIDI, 3 MXL, 5 PDF, una página WebP. Dos
  respuestas vacías no cuentan como partituras. Guardadas 90 fichas de catálogo.
- Derivados: diez JSON de eventos y tres MusicXML extraídos; PDF/imagen pendientes
  de OMR/transcripción. Originales y derivados fuera de Git; manifiestos con hash.
- SEM-06: importación tolerante opcional de duración cero; conserva 2 eventos en
  Oblivion y 32 en Libertango piano de ScoreBase. Modo estricto sin cambios.
- Corrección del hallazgo inicial: las variantes de Oblivion difieren en uno en el
  conteo de notas, pero muchas intensidades. 1863 eventos temporales comunes; sólo
  130 coinciden también en velocidad. No se fusionan ni se eligió un mejor arreglo.
- Validación: parsers MIDI/XML, firmas PDF/imagen, inspección de primera/última
  página de los cinco PDF; casos de cero duración y compatibilidad del parser.
- Reintentado curl tras rechazo accidental indicado por usuario. ScoreBase funciona;
  SheetMusicGiant devuelve HTTP 200 vacío aun con Referer. Chrome/IAB no disponibles.
  No se adjudica causa anti-bot sin evidencia ni se declara búsqueda exhaustiva.

## 2026-10-07 — Soledad de Suite Lumière: identidad confirmada

- El usuario precisa Soledad/Solitude de Suite Lumière (años 70), no la otra obra
  homónima. Se actualizan referencias, traspaso, manifiesto de fuentes y semilla.
- Búsqueda dirigida encuentra candidato de partitura completa identificado como
  Suite Lumiere, ficha de Melos y arreglo en MuseScore. El enlace de PDFCoffee
  y el recurso de su visor devolvieron HTML: no se cuentan como PDF descargado.
- Estado: identificación resuelta, archivo musical pendiente; siguen 19 originales
  válidos. Validación de JSON y diff; no hubo cambios de código ni nuevas pruebas de audio.

## 2026-10-07 — Referencias audibles de Solitude / Suite Lumière (EXP-034)

- Descargadas dos demos públicas de BackingtracksMusic 0239, trío en si menor:
  flauta de referencia y acompañamiento. La fuente identifica Suite Lumière (1975).
- SEM-07 agrega MP3 al catálogo con codec, duración, canales, frecuencia y
  decodificación completa. No hay conversión audio→notas ni juicio de calidad.
- Lote actualizado: 21 originales válidos, 13 derivados, 2 fallos vacíos y 90 fichas.
  Las muestras del mismo arreglo no se cuentan como arreglos independientes.
- La partitura completa/MIDI de Solitude sigue pendiente. MuseScore: HTTP 403;
  PDFCoffee: HTML en lugar de PDF. Se dejó de reiterar esas solicitudes.
- Verificación: catálogo regenerado; ambas demos decodificadas sin errores;
  rechazo de HTML falsamente etiquetado MP3 y de formato desconocido comprobado.

## 2026-10-07 — Regreso a Bach: superficies récord de SURFER (EXP-035)

- Usuario da por suficiente Piazzolla aquí; Atlas se retomará en otro repositorio.
  Pide timbres complejos por voz del Bach favorito con superficies récord de SURFER.
  Considera comprar Pro; no se compra/activa software ni se depende de esa compra.
- REC-01–05: ecuaciones y parámetros extraídos del JAR del SURFER instalado, con
  hashes. Barth/Togliatti/Endrass/Kummer, una por voz. Mallas con caras en cajas
  finitas, vista sombreada y OBJ; singularidades/topología no certificadas por grid.
- Toda cara participa en momentos angulares ponderados por área para síntesis.
  Portadora tonal explícita, 12 armónicos, dos estados de brillo y filtros por voz;
  tablas precalculadas. No se interpreta la señal filtrada como puntos de F=0.
- Seda y Cristal: dos Lua preset y dos controlables; mantienen las 980 notas,
  rubato y 339.066 s del Adagio. WAV completos, voces aisladas y comparación A/B/C.
- Render 48 kHz: picos 0.61616/0.62377, saltos máximos 0.07090/0.11091. Fin
  silencioso, TAKE, reinicio step y controles a 44.1/48 kHz aprobados. Geometría:
  residuo <2.3e-8 en vértices; 32³ es una aproximación, no recuento de nodos.
- Escucha artística, MIDI/OSC, rendimiento/visibilidad de OBJ dentro del host y
  modificación conjunta de ecuación/timbre siguen pendientes. No se instaló nada.

## 2026-10-07 — Biblioteca geométrica independiente de Bach

- Corrección explícita del usuario: superficies reutilizables para distintos
  proyectos. Catálogo, mallas opcionales, render y momentos pasan a
  `library/algebraic_surfaces`; Bach importa la biblioteca.
- Generador independiente probado sin partitura. Ecuaciones y OBJ conservados;
  imagen de biblioteca ya no etiqueta las superficies como voces musicales.
- Regeneración tras extracción conservó los cuatro Lua de Bach byte por byte.
  No se repitieron renders de audio porque los bancos/engine no cambiaron.

## 2026-10-07 — Editor implícito y futuro constructor visual (EXP-036/037)

- Usuario elige ecuaciones y parámetros. Editor WebGL 2 local sin OBJ, servidor
  ni servicios externos; galería de seis ejemplos, slider a, cámara y estado JSON.
- Parser restringido/AST compartido, ray casting de F=0 y última vista válida
  conservada ante error. No certifica tangencias, topología ni latencia universal.
- Chrome headless con SwiftShader: seis shaders compilados, slider actualizado,
  edición inválida conserva los píxeles y gl.getError()=0; captura inspeccionada.
  Node: evaluación, precedencia, catálogo y rechazo de entradas inválidas aprobados.
- Código fuente local: integración Blender usa TCP localhost con GPLA v2 base64
  por línea; es una ruta sin OBJ, no OSC ni recepción directa de polinomios.
  Puente/audio en vivo no implementados; compatibilidad con binario pendiente.
- Usuario propone constructor visual por factores para acercar métodos de
  investigadores al público y Shuffle estructurado. Especificación 010 pendiente;
  no confundir AST del parser con interfaz visual o recetas ya implementadas.
- Se preserva sonificación por momentos de área para otros proyectos. Usuario
  quiere compartirla con Surfer Invaders cuando esté lista; no se envió nada.

## 2026-10-07 — Superficies legibles y Oblivion asignable (EXP-038/039)

- Pedido: ejercicios XY pequeños y Piazzolla con elección de timbre por instrumento.
  Usuario hará pruebas humanas con Pro. No se cuenta como host/MIDI ya verificado.
- Dos Lua preset + controlables: esfera/elipsoide, barrido 24 Hz y escena lenta.
  Videos 10 s dibujan XY real con ventana 50 ms; captura inspeccionada. Son franjas
  sobre F=0, no relleno continuo. A pausa escena sin parar barrido; B barrido; C ancho.
- Oblivion: 30–70 s del arreglo ScoreBase ya obtenido, 312 eventos; flauta/fagot/piano,
  dos pistas de piano agrupadas para timbre pero notas simultáneas preservadas.
  Notas y Lua musical permanecen fuera de Git; configuración/procedencia versionadas.
- Biblioteca de cuatro bancos sin partitura, generador independiente y reproductor
  con selección por instrumento: A/B/C. Transición 80 ms, tempo D, brillo E.
- Render Oblivion: pico 0.30021, RMS 0.06416, salto máximo 0.03273, hasta siete
  notas simultáneas, fin/reinicio aprobados. Cambios de bancos a 44.1/48 kHz aprobados.
  Esfera/elipsoide: F=0 antes de proyección, continuidad y límites aprobados.
- Separación vigente: geometría editable, receta de sonificación, bancos versionados,
  asignación por instrumento y pieza. Coeficientes→audio en vivo y puente host pendientes.

## 2026-10-07 — Pérdida de forma en la salida visual (EXP-040)

- Usuario detecta peor reconocimiento 3D de superficies que de poliedros.
- Inspección confirma bancos planos en Bach (`gz=0`) y salida Z=0 en Oblivion;
  sus transformaciones espectrales y mezcla no representan las superficies fuente.
- Se registra incumplimiento del objetivo visual en esas rutas, sin adjudicar
  todavía un fallo específico al editor WebGL o al meshing. Se pidió localizar
  dónde observa la diferencia antes de cambiar la ruta equivocada.
- No se cambió sonido ni geometría; verificación pertinente: lectura de las rutas
  de generación/proyección y revisión del diff documental.

## 2026-10-07 — Ejercicios XYZ y voz aislada (EXP-041)

- Pedido: repetir ejercicios sin aplanar Z; usuario elige una voz aislada primero.
- Nuevos esfera/elipsoide/cuártica retornan XYZ, rotación ortogonal y parámetros.
  F=0 y covarianza de rango 3 comprobados sobre el retorno, no sólo el generador.
- Bach Violino I y Oblivion flauta, recortes 30–70 s: nuevos Lua con cuártica radial,
  sin suma de voces ni filtrado de coordenadas. Tempo, giro y coeficiente separados.
  Prueba a 44.1/48 kHz: residuo <2.45e-15, rango 3, límites, fin/reinicio y tempo OK.
- Biblioteca reutilizable, visor WebGL con caras y muestras XYZ de los ejercicios;
  superficies récord disponibles como referencia 3D. En música, el visor sólo
  muestra referencia/actividad; elegir malla allí no reasigna el timbre del host.
- XYZ-01…05: evidencia y reproducción en experiments/012-superficies-xyz/README.md.
  Sonido todavía no aceptado; host, timbres récord y puente de asignación pendientes.

## 2026-10-07 — Diagnóstico de silencio común en el host (EXP-042)

- Usuario informa que ni XYZ ni los Bach anteriores producen imagen/sonido.
- En osci-render abierto (registro: 2.9.9.10 Free, standalone) se cargó
  `012-superficies-xyz/esfera.lua`: se observa punto fijo, sin error Lua visible.
- El efecto global contiene `return { x, y, z }`. Desactivarlo no recuperó la
  imagen; se restauró su estado activo y el editor del archivo. No se tocaron Lua.
- El registro del host contiene repetidos `prepareToPlay: sampleRate=16000
  samplesPerBlock=512`. Es una pista de dispositivo/reinicialización, no prueba
  suficiente de causa. No se pudo leer el menú Audio mediante automatización.
- Esfera y aire-seda producen salida finita y no nula en LuaJIT a 16 kHz durante
  un segundo. Eso descarta silencio intrínseco en ese ensayo, no valida el host.
- Pendiente: identificar dispositivo de salida/entrada y frecuencia en Audio,
  comprobar recuperación visual y escucha con el usuario. Se dejó esfera cargada.
- Usuario confirma conexión y desconexión de auriculares antes del fallo.
  Próxima prueba: Audio > Settings, reseleccionar salida disponible, comprobar
  canales y frecuencia; reiniciar aplicación si no recupera el procesamiento.

## 2026-10-07 — Nivel, brillo y orientación (EXP-043)

- Usuario confirma que reiniciar recuperó audio/imagen (EXP-042), pero señala
  saturación, recorte cuadrado y poco relieve.
- Lectura y prueba en host: Volume 2.1787→.30, Threshold .2947→1.00. Desaparece
  el contorno cuadrado observado en aire-seda. Bach permanece sin cambios.
- Line Intensity 5→1, Persistence .5→.15 y Glow .3→.1 permiten distinguir
  barridos. Smoothing=0. Ganancia menor implica figura más pequeña, no usarla
  como zoom. A/C aún tienen LFO: presets autónomos evitan esa interferencia.
- NIV-02: plantilla TAKE 602, orientación oblicua, inclinación y giro lento .1 rad/s.
  Lua de esfera/elipsoide/cuártica regenerados; F=0 <1.9e-15 y covarianza de rango 3.
  Evidencia XYZ en marco del objeto tras invertir rotación, sin aplanar.
- Elipsoide cargado y visible en host 2.9.9.10 Free. Mejora perceptual de profundidad
  y ausencia de distorsión audible todavía deben confirmarse por el usuario.

## 2026-10-07 — Daft Punk y ensayo de formantes (EXP-044/045)

- Usuario confirma Something About Us. Cuatro propuestas: ese tema, Digital Love,
  Harder Better Faster Stronger y Get Lucky. Selección documentada en
  docs/repertorio-daft-punk con manifiesto de fuentes, hashes y obstáculos.
- Descargados dos arreglos: William Bishop (6 páginas, dos partes de piano) y
  medley de Tom Wallace alojado en Colorado Mesa (16 hojas de partes de banda).
  Revisión visual por muestreo, no comparación nota por nota. Medley contiene
  fragmentos de los otros tres temas; no son tres arreglos completos adicionales.
- DP-02…04: generador independiente de repertorio, vocales/formantes sintéticos,
  estudio original de 32 sílabas/16 s. Lua autónomo y controlable A–D, WAV XY y
  captura XYZ separada. No es vocoder de voz real ni superficie algebraica.
- Pruebas a 16/44.1/48 kHz, preset y controles: pico .20, señal finita, energía
  en tres ejes y reinicio aprobados. Sonido/calidad artística pendientes de escucha;
  armónicos acotados no implican ausencia completa de aliasing de modulación.
- Sin compras ni instalaciones. Originales y grabaciones fuera de Git.
- Usuario informa imagen demasiado pequeña y ruido fatigante; vuelve a Bach.
  Se aclara que Volume .30 es ajuste diagnóstico provisional, no configuración
  definitiva. Se detienen pruebas sonoras de superficies en host; queda pendiente
  tamaño visual independiente del nivel de audio y timbre aceptable. No se carga
  la nueva prueba vocal automáticamente (herramienta UI no disponible al intentarlo).

## 2026-10-07 — Groove solicitado y política de niveles (EXP-046/047)

- Preferencias actualizadas: Something About Us, Giorgio by Moroder, Instant Crush
  (Julian Casablancas) y Lose Yourself to Dance. Daft iniciado, arreglos pendientes.
- GRV-01/02: variante original de ensayo vocal con bajo sincopado y bombo, 100 BPM,
  WAV 24 s. Pico máximo medido .144373; salida/reinicio comprobados a tres tasas.
  Lua y WAV disponibles sin modificar sesión de Bach ni cargar sonidos en host.
- GRV-03: limitación final de escucha y calibración por instrumento propuestas;
  no se confirmó compresor nativo ni se instaló DAW. No atribuir a compresión
  corrección de aliasing, saltos o fidelidad de superficie. Aceptación auditiva pendiente.

## 2026-10-07 — Revisión del tamaño visual (EXP-048)

- Se reconoce que reducir Volume dejó pendiente el tamaño del dibujo.
- En la copia actual `../osci-render`, Visualiser Settings incluye Image Scale
  bajo OSCI_PREMIUM. No confundir con Scale de la cadena general de efectos.
- Interfaz inaccesible por fallo de arranque de herramienta; no se cambió nada
  en la sesión. Rango, valor actual, disponibilidad instalada y separación efectiva
  del audio pendientes de comprobación. Se documentó la prueba manual.
