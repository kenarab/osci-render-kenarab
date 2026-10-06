# MIDI, premium, Live y REAPER

Investigación del 2026-10-06. EXP-030. Recomendación: probar una versión actual de
**REAPER como host de osci-render**, antes de comprar premium exclusivamente por
el mapeo MIDI. Encaja con la futura integración con IanniX. Si ya se trabaja con
un Live moderno compatible, usar Live también es una buena solución; no hace falta
encadenar ambas DAW para mover unos controles.

## Qué resuelve cada opción

| Opción | Ventaja para este laboratorio | Coste o límite |
| --- | --- | --- |
| osci-render premium autónomo | Controlador → MIDI Learn interno → controles, con menos aplicaciones abiertas | Conviene si la prioridad es tocar directamente en osci-render; precio actual no verificado |
| osci-render como plugin en Live | Mapeo del host, automatización y composición en una sesión musical | Aprovechar una licencia compatible existente; no recomiendo comprar Live sólo para mapear potenciómetros |
| osci-render como plugin en REAPER | Mapeo, grabación y recepción OSC para conectar IanniX | Configuración inicial del host; evaluación completa de 60 días y licencia posterior |

El usuario confirma que la interfaz le exige premium para MIDI Learn directo.
Las [notas oficiales](https://github.com/jameshball/osci-render/releases) separan
funciones premium de las gratuitas. No pude recuperar un precio fiable de la
[tienda oficial](https://jameshball.gumroad.com/l/osci-render); comprobar allí el
importe y las condiciones aplicables antes de comprar. No se puede concluir que
premium sea más barato o más caro que REAPER con esta evidencia.

REAPER cuesta **USD 60** con licencia descontada para uso personal, educativo o
comercial con ingresos brutos anuales de hasta USD 20.000; la comercial cuesta
**USD 225**. Ambas tienen las mismas funciones. Impuestos aparte. La evaluación
es de 60 días, no una licencia gratuita permanente.
Fuente: [compra y evaluación de REAPER](https://www.reaper.fm/purchase.php).

## Lo que ya está instalado

Lectura de `Contents/Info.plist` en `/Applications` y
`/Library/Audio/Plug-Ins`, sin ejecutar ni modificar las aplicaciones:

| Componente | Versión encontrada |
| --- | --- |
| osci-render autónomo, VST3 y AU; plugin normal e instrument | 2.9.9.10 |
| REAPER64.app | 5.04 |
| Ableton Live 9 Suite.app | 9.1 |
| Copia oculta .Ableton Live 9 Suite_updated.app | 9.1.1 |
| IanniX.app | 0.9.20 |

**REAPER ya está instalado**, pero conviene evaluar una versión actual compatible
antes de preparar una sesión nueva. La descarga actual ofrece macOS Universal
Intel/ARM64: [descargas oficiales](https://www.reaper.fm/download.php).
La presencia de archivos no acredita licencia, arranque ni compatibilidad efectiva.

Live 9 tiene soporte oficial para Mac Intel con OS X 10.7–macOS 10.13.
Además, VST3 llegó en Live 10.1: el Live 9 encontrado no puede cargar nuestro
VST3. Hay AU instalado, pero eso no resuelve por sí solo la compatibilidad del
programa antiguo con el sistema actual. Fuentes:
[requisitos de Live 9](https://help.ableton.com/hc/en-us/articles/209772425-Live-1-9-Minimum-System-Requirements)
y [novedades de Live 10.1](https://www.ableton.com/en/release-notes/live-10/).

## MIDI Learn interno y automatización del host

Son mecanismos diferentes. En la segunda ruta el host recibe el CC del
potenciómetro y cambia un parámetro automatizable del plugin:

```text
Controlador USB MIDI → REAPER / Live → parámetro Lua Slider A → slider_a
IanniX → OSC → REAPER (FX Learn) → parámetro del plugin → Lua
```

Enviar un CC directamente al plugin no habilita su MIDI Learn premium.
La alternativa usa la automatización que el plugin expone al host. Ableton
explica el procedimiento con Configure y MIDI Mapping:
[Using MIDI CC in Live](https://help.ableton.com/hc/en-us/articles/360010389480-Using-MIDI-CC-in-Live).
Para controles remotos se habilita Remote en la entrada MIDI; Track y Sync tienen
otras funciones: [ajustes MIDI de Live](https://help.ableton.com/hc/en-us/articles/209774205-Live-s-MIDI-Settings).

En la referencia local `../osci-render-2.9.9.3/Source/PluginProcessor.cpp`,
`addLuaSlider()` crea parámetros `Lua Slider A`…`Z`, identificadores `luaA`…`Z`,
rango 0–1; la creación e incorporación de estos efectos no está dentro de una
condición premium. Es evidencia favorable, **no una prueba del binario 2.9.9.10**:
falta comprobar que el host enumera, modifica y restaura esos parámetros en la
edición instalada. No se declara resuelto el mapeo físico.

## REAPER como centro de conexión

Tiene sentido usarlo como **host y centro de ruteo**: aloja VST3/AU, recibe
controles y graba la salida. No requiere montar un servidor aparte. En la ruta
OSC, REAPER sí actúa como receptor de mensajes de IanniX.

Su documentación permite agregar una superficie OSC y habilitar la vinculación
de mensajes con acciones y FX Learn. Por eso es un candidato concreto para el
puente con IanniX, sin convertir necesariamente OSC a MIDI.
Fuente: [OSC en REAPER](https://www.reaper.fm/sdk/osc/osc.php).
La integración completa todavía no fue ensayada; ver
[investigación de IanniX y superficies](iannix-superficies.md).

No hacen falta cables virtuales de audio ni un bus MIDI entre aplicaciones cuando
osci-render está cargado dentro de REAPER. Empezar con un host, una pista y un
plugin. Conservar X/Y como estéreo y evitar sumarlo a mono; cualquier procesamiento
que altere los canales también altera el dibujo. Empezar con volumen bajo.

## Prueba mínima pendiente y criterio de aceptación

1. Usar un REAPER compatible y cargar el plugin de osci-render. Registrar versión,
   formato y configuración; no actualizar ni reemplazar las instalaciones antiguas
   como parte de esta investigación.
2. Abrir `experiments/005-aire-de-bach/aire-adagio.lua`. Es la interpretación
   **preferida por el usuario** según su última escucha; conservarla como referencia.
3. Comprobar primero con el mouse el parámetro `Lua Slider A` del host. En este
   archivo, A=0 corresponde a 26 BPM y A=1 a 18 BPM: subir A ralentiza la pieza.
   El tempo de la DAW no sustituye este control del secuenciador Lua.
4. Habilitar el controlador para mensajes de control en REAPER. Elegir el parámetro
   A en la lista de parámetros del FX y usar Learn del host con un CC absoluto.
   Verificar ambos extremos, cambios continuos, ausencia de notas extra y escucha.
5. Guardar y reabrir la sesión: deben conservarse archivo y asignación. Grabar
   una muestra estéreo breve y verificar imagen y sonido, sin atribuir aceptación
   musical al mero movimiento del slider.
6. Después, probar un único mensaje OSC de IanniX hacia FX Learn, con valor
   normalizado 0–1; documentar dirección, puerto y escala realmente configurados.
   Pausar IanniX debe mantener el último valor. Evitar dos fuentes simultáneas
   sobre el mismo parámetro durante la prueba.

Aceptación: potenciómetro → parámetro → cambio audible/visible, persistencia de
sesión y control OSC comprobados por separado. Si el plugin gratuito no expone
el parámetro o impide cambiarlo, registrar ese resultado antes de decidir premium.
No hace falta comprar primero para investigar esa condición.

## Decisión artística y límites

El Adagio pasa a ser la referencia musical preferida; el comentario anterior de
que era lento se conserva como historia, no como preferencia vigente. La variante
controlable sigue disponible como comparación, sin reemplazar el Adagio.

Comprar premium o cambiar de DAW no garantiza resolver el timbre descrito como
“estática”, ni implementa el editor de superficies implícitas tipo SURFER. Esos
pendientes siguen en EXP-023/028. Los controles servirán para explorar el diseño
sonoro, pero su calidad exige nuevas pruebas de escucha.

Resultado de esta etapa: investigación y procedimiento reproducible documentados.
No se instalaron aplicaciones, compraron licencias ni probaron conexiones físicas.
