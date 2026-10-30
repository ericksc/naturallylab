# Prompt: infraestructura Docker Compose

Actúa como arquitecto de software y DevOps senior. Implementa en este repositorio
la infraestructura de Naturally Data Labs, una plataforma educativa estilo Katacoda.
Crea archivos y prueba la solución; no te limites a proponer una arquitectura.

## Experiencia

Conserva la interfaz de instrucciones a la izquierda y JupyterLab a la derecha.
Interfaz y contenido en español, diseño claro y adaptable, sin emojis. Reutiliza
el frontend existente y sustituye JupyterLite/Pyodide por JupyterLab en contenedores.
Permite seleccionar laboratorios, ejecutar notebooks, conservar archivos, validar
pasos, consultar progreso, iniciar y detener entornos. Reiniciar el kernel no debe
borrar archivos; restaurar archivos iniciales debe ser una operación separada.

## Servicios

- Docker Compose para orquestación.
- Nginx como punto de entrada, con WebSockets y rutas de JupyterHub.
- JupyterHub y DockerSpawner: un servidor JupyterLab independiente por estudiante.
- Imagen de laboratorio con Python, pandas, NumPy, matplotlib, seaborn y scikit-learn.
- FastAPI para catálogo, instrucciones y progreso.
- PostgreSQL con migraciones y persistencia.
- Volúmenes por estudiante para notebooks y volumen de PostgreSQL.

Integra JupyterLab bajo el mismo origen. Configura iframe, autenticación y cookies
sin desactivar globalmente protecciones de seguridad. Incluye opción para abrir
JupyterLab en otra pestaña. Abrir un laboratorio no sobrescribe trabajo existente.

## Operación y seguridad

Configura la red utilizada por los contenedores dinámicos de DockerSpawner.
Define límites de CPU, memoria y procesos y apagado por inactividad configurable.
Los notebooks se ejecutan sin privilegios y sin socket Docker. Restringe el socket
al servicio de gestión que realmente lo necesite y documenta su acceso equivalente
a administración del host. No lo expongas por HTTP. Mantén servicios internos sin
puertos públicos innecesarios y secretos fuera del repositorio.

Incluye autenticación local de desarrollo para dos estudiantes, claramente
identificada, con credenciales configurables. Prepara autenticación OAuth/OIDC.
El progreso se asocia a la identidad autenticada, no a un usuario arbitrario enviado
por el navegador. Documenta HTTPS y las limitaciones de Docker Compose para ejecutar
código hostil en un servicio público.

## Contenido y entregables

Implementa también la especificación de `labs-as-code.md`: tres laboratorios
funcionales de Python, limpieza con pandas y análisis con pandas. Incluye
instrucciones, notebooks iniciales, datos, comprobaciones y soluciones separadas.

Entrega compose.yaml, Dockerfiles, configuraciones, backend, migraciones,
frontend integrado, .env.example sin secretos, healthchecks, scripts de diagnóstico
y README con instalación, respaldos y resolución de problemas.

Arranque: `docker compose up --build -d`. Automatiza o documenta cualquier paso previo.

## Verificación

Valida Compose, construcción, arranque, login, proxy, WebSockets, ejecución real
Python/pandas, aislamiento de dos estudiantes, persistencia de notebooks y progreso,
y apagado por inactividad. No elimines volúmenes ni datos existentes para probar.
Describe qué validaciones son de práctica y sus límites. No simules resultados.

Trabaja hasta una versión ejecutable. Informa archivos, comandos, URL local,
pruebas realizadas y limitaciones pendientes. No declares exitosas pruebas que
no se pudieron ejecutar.
