# Editor de ecuaciones — Superficies en vivo

Abrir [index.html](index.html) en Chrome/Firefox moderno con WebGL 2.
Funciona como archivo local: no instalar dependencias, iniciar servidor ni trasladar
OBJ. No envía datos a Internet. La aplicación comienza con una esfera.

Escribir `x^4+y^4+z^4=a` y mover el slider a. También se puede seleccionar esfera,
toro, Barth, Togliatti, Endrass o Kummer. Arrastrar gira la cámara; rueda acerca.
Guardar/cargar estado conserva ecuación, parámetro, dominio y cámara como JSON.
El prompt es matemático, según preferencia explícita del usuario; no lenguaje natural.

La escritura recompila el shader después de 280 ms sin teclear; el slider cambia
un uniforme sin recompilar. El coste real depende de GPU, navegador y ecuación.
No se prometió ni midió un límite universal de latencia. La última vista válida se
conserva ante errores de sintaxis o parámetros no finitos.

Sintaxis: `x y z a`, números, `pi`, `+ - * /`, paréntesis, exponentes enteros 0–12 y
una igualdad opcional. Escribir multiplicaciones explícitas. `sqrt`, `sin`, `cos`
sólo aceptan constantes numéricas (permiten las fórmulas de SURFER). No se admite
variable espacial en denominador ni ejecución de JavaScript. a recorre 0–2; otros
coeficientes se pueden editar en la ecuación en este primer incremento.

El render busca el primer cambio de signo de F sobre cada rayo dentro del cubo
[−L,L]³, refina por bisección y estima normales. Dibuja una superficie sombreada
directamente, sin generar malla. Es un prototipo de muestreo: puede perder hojas
muy finas, raíces tangentes/múltiples y detalles singulares; no certifica topología.
Una pantalla vacía puede significar que no hay intersección detectable en la caja.

## Integración con osci-render: comprobado y pendiente

Comprobado en la copia local `../osci-render-2.9.9.3`:

- `blender/osci_render/__init__.py`, `osci_render_connect` y `send_scene_to_osci_render`:
  conexión TCP a localhost, puerto configurable 51600–51699, defecto 51677.
- Cada mensaje contiene un documento GPLA binario v2.0.0 codificado en base64 y
  terminado por salto de línea. `CLOSE\n` cierra la conexión.
- `get_frame_info_binary` describe cámara, matriz, objetos y trazos con vértices 3D.
  `Source/PluginProcessor.cpp` entrega los frames al controlador del sintetizador.

Esto ofrece una vía **sin OBJ en disco**. No es OSC ni un receptor de ecuaciones.
El navegador no puede abrir TCP arbitrario: hará falta un puente local pequeño y
trazos calculados fuera del audio, derivados del mismo estado de ecuación/parámetros.
La vista sombreada permanecería separada del barrido XY audible.

**No implementado/conectado aún:** puente TCP, barridos, sonificación sincronizada,
automación externa y control de calidad del timbre. No se probó compatibilidad con
el binario instalado 2.9.9.10 ni se infirió acceso premium a partir de la copia fuente.
No se modificó el repositorio externo, no se abrió audio y no se activó software.

Siguiente incremento acotado: puente loopback con envío explícito, límites de
puntos/frecuencia, sustitución del frame anterior y desconexión; probar esfera y
un control antes de las superficies récord. Una fuente de estado alimentará vista,
trazos y futuros bancos sonoros. ALG-R06 continúa pendiente hasta esa prueba.

## Verificación reproducible

`node scripts/check_surface_expression.cjs` prueba catálogo, precedencia, evaluación
y entradas inválidas. `node scripts/check_surface_editor.cjs` abre Chrome headless
con perfil temporal y SwiftShader, comprueba los seis shaders y conservación de
píxeles al introducir un error; guarda una captura en el directorio temporal.
Se puede indicar otra ruta de Chrome con `CHROME_PATH`. Requiere permiso para
iniciar ese proceso local. Estas pruebas no miden rendimiento de la GPU física.

Resultado de esta entrega: ambos ensayos aprobados, captura inspeccionada y sin
errores WebGL. Render y parser funcionan; la conexión sonora sigue pendiente.
