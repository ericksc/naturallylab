# Validación local de la propuesta de publicación

Fecha: 2026-10-30.

## Resultados

- PASS: `python scripts/validate_publisher_examples.py`.
- PASS: referencias curso → sesión → laboratorio con versión explícita.
- PASS: suma de duraciones, IDs únicos, rutas e instrucciones existentes.
- PASS: notebook inicial JSON válido, sin salidas ni contadores de ejecución.
- PASS: rechazo de rutas absolutas, recorrido `..` y archivos ausentes.
- PASS: `node --check web/app.js` y `node --check web/worker.js`.
- PASS: instalación de dependencias y `python scripts/build.py`.
- PASS: respuestas HTTP 200 locales para la portada, JS, CSS, worker, JupyterLab,
  configuración de JupyterLite y los tres notebooks publicados.
- PASS: extensión del kernel Pyodide registrada en la configuración generada.
- PASS: `git diff --check` antes de registrar los cambios.

## Correcciones realizadas

Los ejemplos iniciales referenciaban lecturas y un laboratorio que no estaban
incluidos. Se agregó un paquete autocontenido con esas lecturas, un manifiesto de
laboratorio, tres instrucciones y una copia del notebook de limpieza existente.
Se incorporó un verificador reproducible y se declaró PyYAML como dependencia.

## Alcance

Estas comprobaciones validan la propuesta, sus ejemplos y la construcción estática
existente. No equivalen a probar un publicador integrado: no se han implementado
importación ZIP, API de publicación, autenticación del panel, promoción, rollback,
JupyterHub ni Docker Compose. Tampoco se repitieron pruebas de interacción gráfica
ni de ejecución del kernel en navegador en esta validación. El servidor HTTP de
prueba se detuvo al terminar y no se modificó el sitio alojado.
