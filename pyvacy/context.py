from typing import Type

globals()["@@_current_class"] = []

def _push_cls_ctx(cls: Type):
    globals()["@@_current_class"].append(cls)

def _pop_cls_ctx() -> Type:
    return globals()["@@_current_class"].pop()

def get_current_class() -> Type:
    return globals()["@@_current_class"][-1]

class ClassContextManager():
    def __init__(self, cls: Type):
        self.cls = cls

    def __enter__(self):
        _push_cls_ctx(self.cls)
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        _pop_cls_ctx()
        return True
