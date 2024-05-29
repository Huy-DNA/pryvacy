from typing import Type, TypeVar

from pyvacy.decorators.pyvacy_decorator import instance_methods


T = TypeVar('T')
def pyvacy(cls: Type[T]) -> Type[T]:
    if "@@_pyvacified" in pyvacy.__dict__:
        return cls
    setattr(cls, "@@_pyvacified", ())

    instance_methods.init(cls)

    old_init_subclass = cls.__init_subclass__
    @classmethod
    def init_subclass_wrapper(cls, **kwargs):
        pyvacy(cls)
        return old_init_subclass(**kwargs)

    setattr(cls, "__init_subclass__", init_subclass_wrapper)
        
    return cls


