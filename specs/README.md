# Desarrollo guiado por especificaciones (SDD)

Este es el flujo de trabajo del proyecto desde el cambio de dirección del usuario:
**diseñar sonidos desde superficies algebraicas**, con control comprensible y
velocidades lentas. No implica instalar un framework ni una herramienta externa.

## Fuente de verdad

| Especificación | Estado | Alcance |
| --- | --- | --- |
| [001 — Instrumento de superficies](001-instrumento-superficies/spec.md) | Especificado; implementación pendiente | Geometría, sonido, velocidades y entrada de controles |
| [002 — Calidad del timbre](002-calidad-timbrica/spec.md) | Especificado; comparación auditiva pendiente | Suavidad, expresividad y evaluación del usuario |

Los estudios anteriores son antecedentes, no implementaciones conformes a estas
especificaciones. Las mallas de EXP-019 son una base geométrica ya verificada.

## Ciclo obligatorio

1. **Especificar:** problema, comportamiento observable, requisitos con ID,
   límites, controles, aceptación y dudas. Separar pedido de decisión propuesta.
2. **Planificar:** elegir la solución más pequeña que permita probar el requisito,
   identificar dependencias y riesgos concretos.
3. **Implementar:** tomar una tarea del plan; referenciar los IDs correspondientes.
   Si cambia el comportamiento deseado, actualizar primero el contrato.
4. **Verificar:** pruebas automatizadas pertinentes y comprobaciones perceptuales
   en el host. Registrar aprobado, fallido o pendiente, con evidencia.
5. **Entregar:** instrucciones de uso, limitaciones y commit atómico con código,
   pruebas y documentación que pertenezcan al mismo avance.

No se declara una especificación implementada porque exista un documento o un
render fuera del host. Tampoco se exige una ronda de permiso por cada cambio:
se avanza dentro del alcance autorizado y se pregunta solo por datos necesarios.

`docs/experimentos.md` registra pedidos y resultados; `specs/` define contratos;
`docs/bitacora.md` conserva evidencia y decisiones. Mantener enlaces entre ellos.

## Plantilla para nuevas especificaciones

```text
# NNN — Nombre
Estado / pedido relacionado / fecha
Problema y resultado esperado
Requisitos observables (NNN-R01...)
Controles y valores por defecto
Fuera de alcance
Criterios de aceptación (NNN-A01... → requisito)
Plan de tareas / evidencia / dudas pendientes
```
