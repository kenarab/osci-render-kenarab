# Laboratorio osci-render: instrucciones para agentes

## Propósito

Explorar música de osciloscopio, superficies algebraicas y live coding. El resultado
de cada etapa debe ser una prueba pequeña, reproducible y útil para experimentar.
Leer `docs/objetivos.md` y, cuando exista, `docs/bitacora.md` antes de iniciar otra etapa.

## Forma de trabajo

- Conversar y documentar en español.
- Mantener este repositorio como laboratorio; la copia externa de osci-render es
  una referencia. No modificarla sin una necesidad concreta autorizada.
- Preferir la aplicación oficial y Lua antes de compilar o modificar C++/JUCE.
- Separar resultados comprobados, hipótesis y pruebas pendientes. No declarar
  éxito de audio o interfaz a partir de una validación matemática solamente.
- Registrar ecuación, parámetros, semilla cuando corresponda, versión y resultado.
- Mantener la geometría costosa fuera del cálculo por muestra de audio.
- Empezar con volumen bajo; preservar la separación de los canales X/Y al grabar.
- No instalar dependencias grandes ni comprar software por anticipado.
- Ejecutar solamente verificaciones pertinentes a los cambios.
- Registrar cada experimento solicitado por el usuario en `docs/experimentos.md`,
  con estado, criterio de aceptación y evidencia. Distinguir pedidos del usuario
  de propuestas del agente; actualizar resultados sin perder los pendientes.

## Commits atómicos — preferencia explícita del usuario

- Hacer commit local de cada avance coherente cuando funcione. La atomicidad es
  completitud lógica, no una cantidad de líneas ni dividir artificialmente el trabajo.
- Cada commit debe tener un propósito claro y ser revisable de manera independiente.
  No mezclar refactorizaciones, cambios de comportamiento, dependencias o arreglos
  ajenos, salvo que sean inseparables para que el cambio funcione.
- Incluir las pruebas y la documentación necesarias junto con el cambio que explican.
  Cada commit debe dejar utilizable la funcionalidad afectada.
- Agregar rutas o fragmentos explícitos al staging; no usar `git add .` para
  incorporar cambios desconocidos. Preservar cambios y staging ajenos.
- Revisar el diff exacto del staging y ejecutar las verificaciones pertinentes
  antes de cada commit. Corregir fallos conocidos antes de confirmar.
- Usar mensajes descriptivos que indiquen el cambio concreto. Registrar su motivo
  y validación en el mensaje o en la entrega; distinguir controles bloqueados de
  controles aprobados.
- No incluir secretos, entornos, instaladores, grabaciones generadas ni archivos
  del usuario ajenos al cambio; no hacer commits incompletos solo para limpiar el árbol.
- Preservar el historial: corregir con un commit posterior o una reversión acordada.
  No reescribir commits ni descartar cambios del usuario sin autorización explícita.
- Los commits locales forman parte del trabajo autorizado; publicar mediante push
  requiere un remoto y alcance autorizados.

## Responsabilidades

Son roles de trabajo, no procesos activos ni agentes configurados en la aplicación.
Un solo agente puede cubrirlos. Delegar únicamente cuando el usuario lo solicite.

- Coordinación: objetivos, decisiones, bitácora y pruebas de aceptación.
- Entorno y audio: instalación, arranque, dispositivos y grabación estéreo.
- Geometría: ecuaciones, muestreo, contornos, mallas y recorridos continuos.
- Instrumento: Lua, controles musicales y live coding.

## Cuidado de cuota y productividad

- Antes de una tarea con varias etapas, consultar la cuota disponible si existe una herramienta para ello. Durante trabajo sostenido, volver a consultarla al terminar cada etapa sustancial o antes de otro ciclo de investigación, generación o verificación; evitar consultas repetitivas sin trabajo intermedio.
- Avisar antes de continuar cuando se acumulan llamadas, prompts, reintentos o verificaciones con poco progreso útil. Explicar brevemente qué se logró, qué falta y una alternativa de menor consumo. No esperar a agotar la cuota.
- Al detectar que queda 50% o menos de una ventana de cuota, detener el trabajo, informar el porcentaje y la ventana correspondiente, y preguntar si seguimos o lo dejamos para otro momento. Repetir la parada al detectar 25% o menos disponible. Aplicar a la ventana de cinco horas y a la semanal, cuando estén disponibles. Si la tarea empieza por debajo de un umbral sin autorización explícita para seguir en ese estado, avisar y detenerse antes del trabajo sustancial.
- Esperar una respuesta explícita antes de reanudar tras cada umbral. La aprobación para continuar en 50% no autoriza pasar silenciosamente el umbral de 25%. No repetir la misma parada si el usuario ya autorizó continuar en ese umbral y ventana.
- Estos controles se realizan entre operaciones: no prometer una alarma exacta en tiempo real ni un bloqueo automático del sistema. Si no se puede consultar la cuota, decirlo y no inventar porcentajes, tokens restantes o conversiones entre tokens y cuota.
- No presentar estimaciones de tokens como presupuestos fiables del consumo total. Priorizar el plazo del usuario, cambios concretos y una versión utilizable; evitar rehacer auditorías y revisar de nuevo material que no cambió.
- No consumir créditos de reinicio ni comprar saldo sin autorización explícita específica.
