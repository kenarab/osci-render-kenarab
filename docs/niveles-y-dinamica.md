# Nivel, compresión y geometría

EXP-047 / GRV-03. No hay una calibración universal que haga agradable cualquier
Lua: nivel, contenido espectral, saltos y aliasing son problemas distintos.

## Qué se comprobó en osci-render

Volume=2.1787 y Threshold=.2947 producían bordes cuadrados; con Volume=.30 y
Threshold=1 desaparecieron. Threshold no se debe confundir con el umbral de un
compresor transparente. No se confirmó un compresor/limitador nativo en la versión
instalada; la copia local tiene módulos externos ausentes, por lo que una búsqueda
sin resultados no demuestra que no exista. No se instaló ni configuró otro host.

## Diseño propuesto

1. Cada instrumento tendrá una ganancia fija conservadora y picos medidos en sus
   parámetros útiles. Puede calibrarse al generar el preset: no hace falta ajustar
   cada nota. Cambios arbitrarios de ecuación/mezcla requieren nueva medición.
2. En una DAW, un limitador al final del bus de escucha contiene picos inesperados;
   compresor opcional para dinámica, sin intentar arreglar timbres desagradables.
   Punto de partida propuesto: techo -1 dBTP si permite true peak, poca reducción
   habitual; si trabaja continuamente, bajar entrada. No es un preset ya instalado.
3. Separar la referencia XYZ y su escala visual del bus procesado para escuchar.
   Si se comprime X/Y por separado se alteran proporciones; enlazar canales reduce
   ese problema, pero una ganancia que varía durante el recorrido tampoco conserva
   exactamente la superficie. El limitador no recupera señal ya recortada antes.

El [manual oficial de Ableton](https://www.ableton.com/en/manual/live-audio-effect-reference/)
explica Compressor y Limiter y recomienda el limitador al final de la cadena para
controlar clipping. Esto describe una ruta posible, no confirma compatibilidad
ni funcionamiento de la instalación local de Live. Mantener Threshold 1 en host;
Volume .30 sigue siendo diagnóstico provisional y achica la imagen.

Pendiente: control de escala visual independiente, ruteo de escucha y prueba con
un limitador real. Prioridad perceptual: Bach como referencia agradable; no pedir
al usuario que soporte barridos ruidosos para validar geometría.

## Persistencia de la sesión

Comprobado en este Mac: `~/Library/Application Support/osci-render.settings`
contiene `filterState` (estado del proyecto serializado), ventana y audioSetup.
`osci-render_globals.settings` guarda otras preferencias y directorio reciente.
El código `getStateInformation` guarda efectos y parámetros en el proyecto y
`setStateInformation` los restaura. No son ajustes individuales de cada `.lua`:
cambiar de archivo mantiene la ganancia/Threshold de la sesión. Guardar/cargar
un proyecto puede restaurar ese estado. El instante exacto de escritura automática
no se comprobó; no asumir que cada movimiento de slider ya está persistido.
No editar ni borrar estos archivos mientras la aplicación está abierta. Para
reproducibilidad conviene guardar un proyecto de escucha con nombre propio y
anotar ganancias por instrumento; esta propuesta no crea ese proyecto todavía.
