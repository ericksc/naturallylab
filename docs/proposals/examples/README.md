# Paquete ilustrativo de publicación

`course.yaml` referencia `session.yaml` por ID y versión. La sesión contiene dos
lecturas locales y referencia el laboratorio incluido en `labs/pandas-cleaning/`.
El notebook es una copia del laboratorio de limpieza existente.

El manifiesto del laboratorio ilustra el contrato de la primera etapa con
JupyterLite. El formato para contenedores se describe en `docs/prompts/labs-as-code.md`.
No hay un cargador de estos manifiestos integrado en la plataforma todavía.

Validar referencias y estructura desde la raíz del repositorio:

```sh
python scripts/validate_publisher_examples.py
```

Las verificaciones son específicas de estos ejemplos y no sustituyen el esquema
completo, importador ZIP, control de acceso ni pipeline de publicación propuestos.
