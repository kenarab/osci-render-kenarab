# Primera sesión

## Qué tenemos

`../osci-render-2.9.9.3` contiene código fuente extraído de un ZIP. No es una
instalación ejecutable. Por ejemplo, `modules/osci_scripting` está vacío. Este Mac
es ARM64. Para empezar, obtener el ejecutable macOS oficial desde
[osci-render.com](https://osci-render.com/). La
[release v2.9.9.3](https://github.com/jameshball/osci-render/releases/tag/v2.9.9.3)
no tiene ejecutables adjuntos, según la consulta registrada en la bitácora.

El ZIP «Source code» de GitHub no sustituye la aplicación. Un clon con submódulos
es conveniente para desarrollar el motor, pero además requiere su entorno de
compilación. No necesitamos compilar para probar nuestras curvas.

Se obtuvo el instalador mediante el [enlace macOS del servicio oficial](https://jameshball.releaseplane.org/download?platform=mac-universal),
referenciado por la web de osci-render. Está abierto desde
`/Volumes/osci-installer/osci-installer.app`, detenido en el diálogo de términos.
El DMG en `/tmp/osci-installer.dmg` es temporal. La versión del sintetizador que
instale este servicio debe registrarse al abrirlo: no se presupone que coincida
con la versión 2.9.9.3 del código fuente local.

## Prueba manual mínima

1. Abrir `osci-render.app`. Empezar con volumen bajo.
2. Seleccionar la salida de audio en los ajustes de la aplicación. Para esta
   prueba no hace falta entrada de micrófono ni un dispositivo virtual.
3. Confirmar que el osciloscopio integrado muestra actividad. Registrar versión,
   salida, frecuencia de muestreo y cualquier mensaje de error.
4. Abrir `experiments/001-primeras-curvas/01-circle.lua` desde el selector de
   archivos. Debe verse un círculo. Mantener desactivados los efectos al comparar.
5. Abrir `02-lissajous.lua`. Debe verse una figura cerrada de relación 3:2.
6. Abrir `03-torus-path.lua`. Es una curva cerrada sobre un toro, no la superficie
   completa. Usar la rotación 3D del programa para explorar su proyección.
7. En el editor integrado cambiar `p = 3` a `p = 5` en la segunda prueba y
   comprobar el cambio en vivo; guardar la variante con otro nombre.
8. Guardar el proyecto desde osci-render. Registrar resultados en la bitácora.

Si no hay sonido, revisar salida, ganancia y si el modo MIDI espera notas.
Si falla la apertura, guardar el mensaje exacto antes de cambiar el sistema.
No retirar cuarentena ni desactivar protecciones de macOS automáticamente.

## Qué comprueba el script

`lua scripts/check_curves.lua` ejecuta los archivos reales con una fase simulada;
comprueba coordenadas finitas, amplitud acotada, cierre y pertenencia del recorrido
al toro algebraico. No comprueba el motor de audio, su editor ni el dispositivo.

El contrato `phase` y `return {x,y,z}` se basa en los ejemplos Lua incluidos en
la copia 2.9.9.3. La ejecución dentro de la aplicación se registra por separado.
