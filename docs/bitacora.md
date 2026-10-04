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

### Estado

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
