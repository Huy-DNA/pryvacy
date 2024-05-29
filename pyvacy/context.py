from typing import Type

setattr(globals(), "@@_current_class", None)

def set_cls_ctx(cls: Type, override = False):
    if override and get_current_class():
        return
    setattr(globals(), "@@_current_class", cls)

def unset_cls_ctx():
    setattr(globals(), "@@_current_class", None)

def get_current_class() -> Type:
    return getattr(globals(), "@@_current_class")

