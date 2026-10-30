# Propuesta: NaturallyLab Publisher

Estado: propuesta para revisión; no implementada.
Fecha: 2026-10-30.

## Decisión recomendada

Crear un módulo de publicación llamado **NaturallyLab Publisher**, con Git como
fuente de verdad y una plantilla de archivos compartida por CLI y panel web.
Publicar contenido debe ser independiente de construir los entornos de ejecución.

Un docente podrá duplicar una sesión, editar instrucciones y notebooks, previsualizar
y publicar una versión. Un autor técnico podrá hacer lo mismo mediante Git y
`labctl`. Ambos caminos deben producir el mismo paquete validado.

La primera entrega debe integrar publicación desde Git con el sitio estático actual.
El panel de importación y publicación se agrega después de incorporar un backend
autenticado. No hace falta esperar a JupyterHub para organizar y publicar contenido.

## Situación actual y alcance

El repositorio contiene un frontend estático y tres notebooks ejecutados con
JupyterLite. El catálogo y las instrucciones están definidos en `web/app.js`.
No existen todavía API, PostgreSQL, JupyterHub, CLI ni publicación declarativa.

En esta propuesta, una **sesión** es una unidad didáctica: objetivos, explicación,
actividades y una secuencia de laboratorios. No representa una videollamada ni una
instancia del kernel. Un **laboratorio** es un ejercicio reutilizable con notebook,
datos, pasos, entorno y comprobaciones.

Objetivo: agregar sesiones y laboratorios mediante archivos, sin editar JavaScript.
Para el sitio estático esto requiere regenerar y desplegar los archivos de contenido;
no implica disponibilidad de una API ni actualización instantánea sin despliegue.

## Alternativas consideradas

| Alternativa | Ventaja | Limitación | Decisión |
|---|---|---|---|
| Carpetas Git + YAML + Markdown + notebooks | Revisión, historial y automatización; aprovecha el repositorio actual | El autor necesita Git o una interfaz que lo abstraiga | Base recomendada |
| ZIP cargado desde un panel | Ágil para docentes sin experiencia en Git | Requiere backend, identidad, límites y control de versiones | Segundo canal sobre el mismo formato |
| CMS generalista | Editor visual de textos | Notebooks, imágenes de ejecución y validaciones requieren adaptación | No incorporarlo en el MVP |
| Repositorio distinto por cada laboratorio | Permisos independientes | Mayor mantenimiento y coordinación de versiones | Posponer hasta necesitar autores externos |

## Estructura propuesta

- `courses/<id>/course.yaml`: recorrido y orden de sesiones.
- `sessions/<id>/session.yaml`: objetivos, actividades y referencias a laboratorios.
- `sessions/<id>/content/*.md`: explicación, preparación y cierre.
- `labs/<id>/lab.yaml`: manifiesto compatible con la especificación existente.
- `labs/<id>/steps/*.md`: instrucciones por paso.
- `labs/<id>/notebooks/`: material inicial.
- `labs/<id>/data/`: datos pequeños de práctica.
- `labs/<id>/checks/`: comprobaciones.
- `labs/<id>/solutions/`: soluciones reservadas para docentes.
- `environments/`: imágenes y dependencias administradas de forma separada.

Los manifiestos deben validar `schema_version`, identificador, versión semántica,
referencias, tiempos y campos desconocidos. En una sesión, cada referencia debe
fijar la versión del laboratorio: cambiar un laboratorio no debe cambiar
silenciosamente una sesión ya publicada. Los ejemplos adjuntos son ilustrativos,
no manifiestos que el frontend actual ya pueda interpretar.

## Flujo del docente

1. **Crear o duplicar** una plantilla de sesión o laboratorio.
2. **Editar** YAML, Markdown y notebooks; en el panel futuro, usar un formulario.
3. **Validar**: recibir mensajes como `session.yaml → activities[1].lab: versión inexistente`.
4. **Previsualizar** instrucciones y notebook sin activar la versión para estudiantes.
5. **Publicar** un paquete validado y una referencia a su commit de origen.
6. **Verificar** que el catálogo entrega la versión correcta.
7. **Revertir** la referencia activa a una publicación anterior si es necesario.

Las versiones publicadas serán inmutables. Corregir contenido genera otra versión.
Los borradores se pueden modificar libremente. No se sobrescribe el notebook
personal de un estudiante al publicar una corrección.

## CLI propuesta

Los siguientes comandos son contratos a implementar, no comandos disponibles hoy:

```sh
labctl session init pandas-sesion-01
labctl lab init pandas-cleaning
labctl validate .
labctl preview sessions/pandas-sesion-01
labctl package sessions/pandas-sesion-01 --output build/session.zip
labctl publish build/session.zip --target staging
labctl promote <release-id> --target production
labctl rollback <release-id> --target production
```

`package` debe incluir solo material entregable y todas las versiones de laboratorios
referenciadas, además de un índice, checksums y commit de origen. Las soluciones y
secretos no entran en el paquete público. Las comprobaciones destinadas al entorno
del estudiante son visibles para él y no deben confundirse con pruebas privadas.

`publish` debe ser idempotente para la combinación de ID, versión y checksum.
Misma versión y contenido diferente: rechazar. Mismo contenido: reutilizar la
publicación. Nunca construir imágenes Docker por subir una sesión de texto.

## Arquitectura de publicación

La entrada Git y la entrada ZIP convergen en un único validador y empaquetador.
El resultado es una publicación con estados: borrador, validando, listo,
publicando, publicado o fallido. Cada intento conserva diagnósticos.

**Primera etapa, compatible con el sitio actual:**

- Extraer catálogo e instrucciones de `web/app.js` a archivos declarativos.
- Generar JSON público y notebooks a partir del contenido validado.
- Usar GitHub Actions para validar pull requests y preparar publicaciones.
- Crear vista previa como artefacto descargable; una URL de staging requiere un
  alojamiento configurado y no se considera automática por usar Actions.
- Publicar mediante un adaptador de despliegue. El sitio actual usa Sites y no
  dispone aún de un mecanismo de despliegue desatendido desde GitHub Actions:
  resolver esa integración explícitamente o usar otro destino aprobado.
- Reutilizar el entorno JupyterLite para contenido compatible.

**Segunda etapa, plataforma con Docker Compose:**

- FastAPI incorpora importaciones, publicaciones, historial y auditoría.
- PostgreSQL almacena metadatos, versiones y referencias activas.
- Un directorio persistente o almacenamiento de objetos conserva paquetes inmutables.
- Un worker procesa importaciones y validaciones con límites de recursos y timeout.
- El frontend obtiene catálogo y contenido desde la API.
- JupyterHub/DockerSpawner crea entornos a partir de imágenes aprobadas.
- Cada sesión de estudiante fija una versión y un entorno; nuevas publicaciones
  afectan nuevas instancias y no migran trabajo existente automáticamente.

Para el MVP no es necesario incorporar Redis o un broker: una cola de trabajos
persistente en PostgreSQL y un worker son suficientes como diseño inicial. La
implementación deberá resolver exclusión, reintentos y recuperación de trabajos.

## Panel de publicación propuesto

Ruta `/admin/content`, disponible para autores y publicadores autenticados:

- Crear desde plantilla o importar ZIP.
- Mostrar contenido detectado, versión, laboratorios y entorno requerido.
- Editar metadatos e instrucciones.
- Ver errores y advertencias por archivo.
- Abrir vista previa.
- Publicar y consultar estado del trabajo.
- Ver historial, autor, commit, checksum y publicación activa.
- Revertir sin borrar el historial.

La interfaz debe mostrar “requiere construir entorno” cuando cambien dependencias.
La construcción será una acción independiente del administrador. El docente podrá
seleccionar una imagen aprobada, evitando reconstrucciones para cambios de texto.
El panel podrá crear un pull request con una GitHub App de alcance limitado; los
borradores aún no sincronizados deben indicarse y tener reintentos sin duplicación.
No se deben almacenar tokens de GitHub en el navegador.

## Validación y controles

- YAML con carga segura, esquema estricto y rechazo de campos desconocidos.
- Validar notebooks sin ejecutar código durante la importación.
- Revisar referencias, archivos, IDs, versiones y dependencias.
- Sanitizar Markdown/HTML antes de renderizarlo.
- Límite inicial propuesto: ZIP de 25 MiB y 100 MiB extraídos; configurable.
- Rechazar rutas absolutas, recorrido `..`, enlaces simbólicos, archivos duplicados
  y expansión desproporcionada del ZIP. No usar extracción sin controles.
- Autores editan borradores; publicadores activan versiones; administradores
  aprueban entornos. Una persona puede reunir esos roles en una instalación pequeña.
- No ejecutar tests o Dockerfiles no revisados con secretos ni socket Docker.
- Tests de práctica en entornos del estudiante no equivalen a evaluación segura.
- El rollback del catálogo no elimina progreso, notebooks ni datos de estudiantes.
- Rechazar publicaciones concurrentes si cambió la versión activa esperada.

## Plan y criterios de aceptación

| Entrega | Resultado verificable |
|---|---|
| 1. Contrato y migración | Tres laboratorios actuales y una sesión en formato declarativo; ningún contenido didáctico hardcodeado en JavaScript |
| 2. Autoría y validación | Plantillas, esquema, CLI inicial y errores por archivo; un cuarto laboratorio se incorpora sin editar la aplicación |
| 3. Publicación desde Git | Validación en PR, paquete reproducible, staging configurable y activación explícita; historial y rollback |
| 4. Panel de docentes | Importar ZIP, previsualizar, publicar y ver errores sobre el mismo pipeline |
| 5. Integración de entornos | Imágenes aprobadas, versiones fijadas y apertura del notebook correcto en JupyterHub |

Objetivos propuestos de agilidad, a medir en el piloto: crear un borrador a partir
de plantilla en menos de cinco minutos y activar contenido ya escrito en menos de
dos minutos si no cambia el entorno. Son objetivos, no tiempos garantizados de CI.

Pruebas de aceptación: importar paquete válido; rechazar ruta peligrosa; detectar
versión ausente; excluir soluciones; impedir publicar una versión con contenido
diferente; reintentar sin duplicados; preservar notebooks tras una corrección;
revertir el catálogo; comprobar que la vista previa coincide con lo publicado.

## Recomendación de arranque

Comenzar por entregas 1 y 2 y una publicación manual de un paquete validado.
Después automatizar staging y promoción con GitHub Actions. Construir el panel ZIP
cuando exista el backend. Así se mejora la publicación sin bloquearla por la
migración completa a Docker Compose ni mantener dos formatos de autoría.

## Referencias oficiales

- GitHub Actions, workflows y disparadores:
  https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows
- Ejecución manual de workflows:
  https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow
- Pydantic, validación estricta:
  https://github.com/pydantic/pydantic/blob/main/docs/concepts/strict_mode.md

Las decisiones arquitectónicas y los objetivos de tiempos de este documento son
propuestas para NaturallyLab; no son garantías de las herramientas citadas.
