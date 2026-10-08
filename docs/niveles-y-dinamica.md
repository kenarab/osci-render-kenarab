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

## Tamaño visual: control localizado, prueba pendiente

Revisión del código disponible en `../osci-render/Source/visualiser/`:
`VisualiserSettings.h:177` define **Image Scale** con dos controles de escala
y `VisualiserSettings.cpp:71` lo muestra bajo `OSCI_PREMIUM`. Es un control del
visualizador distinto del efecto general Scale de `PluginProcessor.cpp:77`.
La presencia en esta copia no verifica su disponibilidad en la versión instalada.

Prueba propuesta: en Visualiser Settings, si aparece Image Scale, aumentar ambos
ejes por el mismo factor, conservando Volume .30 y Threshold 1; empezar por
duplicar la escala y detenerse antes de cortar el dibujo contra los bordes.
Confirmar tamaño mayor, proporciones conservadas y audio sin cambio. No se conoce
aún el rango ni el valor actual del control en la aplicación.

La automatización de la interfaz falló al iniciar (`native pipe startup failed`).
No se aplicó el ajuste ni se comprobó la ruta completa de render/audio. El problema
de tamaño sigue abierto; no aumentar Volume para compensarlo sin esa separación.

## Preset visual independiente — EXP-054

El usuario ya amplió Image Scale en Pro, pero percibe poco brillo/color/riqueza.
Controles confirmados en `../osci-render/Source/visualiser/VisualiserSettings.h`:
Line Colour (Hue, Saturation, Intensity), Screen Colour (color/ambientación de
fondo), Light Effects (Persistence, Focus, Glow, Afterglow, Overexposure).
Image Scale y posición son del visualizador; el efecto Scale de audio es distinto.

Propuesta de ajuste, todavía no aplicada: conservar escala elegida; subir primero
Intensity del trazo y saturación; mantener fondo oscuro con contraste; ajustar
Focus observando grosor/nitidez, y sólo después un Glow moderado. Subir Persistence
lo suficiente para reconocer el barrido, sin acumular vueltas en una mancha.
Reservar Afterglow/Overexposure para una variante expresiva posterior. No proponer
valores universales sin ver el rango ni el resultado de la versión instalada.

Guardar una COPIA de proyecto como preset visual para comparar; el proyecto puede
incluir audio además de visuales, por lo que no se debe cargar indiscriminadamente
sobre otra sesión. Anotar ajustes visuales por separado. No se editó ni guardó
ningún .osci del usuario. No usar Volume/Threshold para cambiar brillo o tamaño.

Aceptar esta prueba al comparar el mismo Lua y cámara antes/después: mayor contraste
y color, trazos distinguibles y sin recorte; audio sin variación. Un preset visual
no agrega hojas, singularidades ni cobertura: éstas dependen de geometría/barrido.
