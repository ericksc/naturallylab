# Naturally Data Labs

Plataforma educativa estilo Katacoda: instrucciones a la izquierda y JupyterLab a la derecha.

## Implementación actual

- Frontend estático en `web/`.
- JupyterLab mediante JupyterLite, con Python/Pyodide en el navegador.
- Tres notebooks: fundamentos de Python, limpieza y análisis con pandas.
- Comprobaciones educativas que desbloquean pasos.
- Notebooks y progreso guardados en el navegador del estudiante.

Actualmente no hay JupyterHub, servidores Python por estudiante, Docker Compose,
PostgreSQL ni CLI Labs as Code. Las especificaciones para implementarlos están en
`docs/prompts/`. Las validaciones actuales son para práctica, no para calificación
resistente a manipulaciones.

## Ejecutar localmente

Requiere Python 3.12 y acceso a Internet para instalar dependencias y cargar el
runtime Python y sus paquetes en el navegador.

```sh
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements-build.txt
python scripts/build.py
python -m http.server 8000 --directory dist
```

Abrir http://localhost:8000. Ejecutar una celda con **Shift + Enter** y después
su celda de comprobación para completar el paso. Los archivos generados en
`dist/` se excluyen de Git y se reconstruyen con el script.

## Próxima implementación

- [Infraestructura Docker Compose](docs/prompts/docker-compose.md).
- [Laboratorios declarativos: Labs as Code](docs/prompts/labs-as-code.md).

Los prompts son requisitos de implementación para Codex; no son servicios ya desplegados.
