from jupyter_core.paths import jupyter_path
from pathlib import Path
c.LiteBuildConfig.federated_extensions = [str(Path(p) / '@jupyterlite/pyodide-kernel-extension') for p in jupyter_path('labextensions') if (Path(p) / '@jupyterlite/pyodide-kernel-extension').exists()]
