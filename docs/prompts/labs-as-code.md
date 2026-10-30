# Prompt: Labs as Code

Implementa laboratorios declarativos versionados en Git. Crear un laboratorio
no debe requerir cambios en el frontend ni en la lógica del backend.

## Estructura

Cada carpeta `labs/<id>/` contiene:

- `lab.yaml`: manifiesto.
- `README.md`: documentación del autor.
- `environment/Dockerfile` y `requirements.txt`: entorno.
- `steps/*.md`: instrucciones.
- `notebooks/*.ipynb`: notebooks iniciales.
- `data/`: datos de ejemplo.
- `checks/test_*.py`: comprobaciones.
- `solutions/`: soluciones, excluidas de la imagen y archivos del estudiante.

Ejemplo de manifiesto que debes implementar y documentar:

```yaml
schema_version: 1
id: pandas-cleaning
version: "1.0.0"
title: Limpieza de datos con pandas
description: Inspeccionar y limpiar un conjunto de datos.
language: es
difficulty: beginner
estimated_minutes: 20
tags: [python, pandas]
environment:
  dockerfile: environment/Dockerfile
  requirements: environment/requirements.txt
  resources:
    cpu: 1
    memory: 1GiB
    pids: 128
workspace:
  notebook: notebooks/practice.ipynb
  seed: [notebooks/, data/]
  persistence: per-user
steps:
  - id: inspect
    title: Inspeccionar los datos
    instructions: steps/01-inspect.md
    validation:
      file: checks/test_inspect.py
  - id: missing-values
    title: Tratar valores faltantes
    instructions: steps/02-missing-values.md
    validation:
      file: checks/test_missing_values.py
  - id: duplicates
    title: Eliminar duplicados
    instructions: steps/03-duplicates.md
    validation:
      file: checks/test_duplicates.py
```

## Requisitos

Descubre automáticamente los laboratorios y valida sus manifiestos con Pydantic o
JSON Schema. Rechaza IDs duplicados, archivos ausentes y rutas que escapen de la
carpeta, incluidos enlaces simbólicos. Genera catálogo e instrucciones desde el YAML.

Construye imágenes únicamente mediante una operación explícita del administrador.
No construyas Dockerfiles solicitados por estudiantes. Aplica límites máximos de
recursos configurados por la plataforma, aunque el manifiesto solicite más.

Copia archivos iniciales sin sobrescribir el trabajo. Guarda progreso por identidad
autenticada, laboratorio, versión y paso. Define el comportamiento ante versiones nuevas.

Define un contrato verificable para resultados del notebook: ejecutar una copia
guardada o inspeccionar archivos de salida. Un proceso de tests separado no puede
leer directamente las variables del kernel activo. Aplica timeouts, captura errores,
y documenta que las comprobaciones en un entorno controlado por el estudiante son
para práctica y no constituyen calificación resistente a manipulaciones.

## CLI y CI

Implementa realmente estos comandos y documenta instalación y uso:

```sh
labctl init nombre-del-lab
labctl validate labs/
labctl build pandas-cleaning
labctl check pandas-cleaning
```

Incluye plantilla de autoría y CI que valide manifiestos, notebooks y comprobaciones.
La CI no debe ejecutar código de contribuciones no confiables con credenciales ni
acceso privilegiado al host. Entrega Python básico, limpieza con pandas y análisis
con pandas usando este formato. Agregar un cuarto laboratorio debe requerir solo
su carpeta, validación, construcción y actualización del catálogo.
