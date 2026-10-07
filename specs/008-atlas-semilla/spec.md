# 008 — Semilla local de Atlas Piazzolla

Pedido EXP-034, ampliación del usuario: fuentes musicales de cualquier formato,
variantes para estudiar interpretaciones y conversión a una lengua franca. Este
repositorio ejecuta un lote pequeño; el archivo exhaustivo continúa en otro.

- SEM-01: conservar originales descargados fuera de Git, con fuente, formato real,
  fecha UTC, hash, tamaño, estado y relación entre formatos del mismo arreglo.
- SEM-02: preservar variantes; agrupar duplicados exactos por hash y registrar
  similitudes sin fusionarlas ni declarar que una variante es mejor sin escuchar.
- SEM-03: extraer MusicXML de MXL y eventos JSON de MIDI, manteniendo originales y
  advertencias de pérdida. No simular conversión de PDF/foto mediante OCR de texto.
- SEM-04: catalogar PDF e imágenes, distinguir muestra/página/partes/obra completa;
  OMR y revisión musical pendientes. HTTP 200 con cero bytes es descarga fallida.
- SEM-05: representar el lote mediante manifiesto y tabla navegable, con faltantes
  explícitos para las cinco obras. Inventario de fuentes no equivale a descarga.
- SEM-06: ante notas MIDI de duración cero, importación tolerante opcional conserva
  el evento y lo advierte; comportamiento estricto anterior permanece por defecto.

Aceptación: firmas y parsers reales, controles de hashes, notas/tempos y extracción
XML. Validación artística y transcripción de PDFs/escaneos no forman parte del lote.
