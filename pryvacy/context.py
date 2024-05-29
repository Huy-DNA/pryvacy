from typing import Optional, Type

globals = globals()
globals["@@_current_class"] = []

last_cls = None

def push_cls_ctx(cls: Type):
    globals["@@_current_class"].append(cls)

def pop_cls_ctx():
    globals["@@_current_class"].pop()

def get_current_class() -> Optional[Type]:
    if globals["@@_current_class"]:
        return globals["@@_current_class"][-1]
    return None

