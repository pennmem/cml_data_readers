from typing import Dict, Type


def _import_readers() -> Dict[str, Type]:
    import importlib
    import pkgutil
    import sys

    pkg = sys.modules[__name__]
    classes = {}

    for module_finder, name, ispkg in pkgutil.iter_modules(pkg.__path__):
        module_name = ".".join([pkg.__name__, name])
        module = importlib.import_module(module_name)
        classes.update({
            cls: getattr(module, cls)
            for cls in dir(module)
            if cls.endswith("Reader")
        })

    return classes


_types = _import_readers()
globals().update(_types)
__all__ = list(_types.keys())
