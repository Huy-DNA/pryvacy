import inspect
from typing import Callable, Optional, Type


def _get_cls_ctx() -> Optional[Type]:
    try:
        return globals()["@@current_class"]
    except:
        return None

def _set_cls_ctx(cls: Optional[Type]):
    globals()["@@current_class"] = cls

def is_method(fn: Callable) -> bool:
    cls = _get_cls_ctx()
    return fn in [method for _, method in inspect.getmembers(cls, inspect.ismethod)]

def get_current_cls():
    return _get_cls_ctx()

class ClassContextManager():
    def __init__(self, cls: Type):
        self.cls = cls
        self.old_cls = None

    def __enter__(self):
        self.old_cls = _get_cls_ctx()        
        _set_cls_ctx(self.cls)
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.cls = self.old_cls 
        return True
