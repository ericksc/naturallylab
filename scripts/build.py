"""Build the static site with the JupyterLite installed in this interpreter."""
from pathlib import Path
import shutil
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
out = root / 'dist'
out.mkdir(exist_ok=True)
for source in (root / 'web').iterdir():
    if source.is_file():
        shutil.copy2(source, out / source.name)
subprocess.run([
    sys.executable, '-m', 'jupyterlite_core', 'build',
    '--lite-dir', str(root / 'jupyter-build'),
    '--contents', str(root / 'notebooks'),
    '--output-dir', str(out / 'jupyter'), '--apps', 'lab',
    '--no-sourcemaps', '--no-unused-shared-packages',
    '--config', str(root / 'jupyter-build/jupyter_lite_config.py'),
], cwd=root, check=True)
