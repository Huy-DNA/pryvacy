from typing import Type

globals = globals()
globals["@@_current_class"] = None

last_cls = None

def set_cls_ctx(cls: Type, override = False):
    if override and get_current_class():
        return
    
    global last_cls
    last_cls = get_current_class()
    globals["@@_current_class"] = cls

def reset_cls_ctx():
    globals["@@_current_class"] = last_cls

def get_current_class() -> Type:
    return globals["@@_current_class"]

