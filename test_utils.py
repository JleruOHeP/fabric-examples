import importlib.util
import sys
from pathlib import Path

def import_notebook(path: Path, runtime: dict, name: str = None):
    if name is None:
        name = path.stem.replace("-", "_")

    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module

    # 🔥 Inject Fabric globals BEFORE execution
    for k, v in runtime.items():
        setattr(module, k, v)

    spec.loader.exec_module(module)
    return module