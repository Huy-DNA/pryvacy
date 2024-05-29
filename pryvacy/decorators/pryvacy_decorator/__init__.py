from typing import Type, TypeVar

from pryvacy.decorators.pryvacy_decorator import instance_methods
from pryvacy.decorators.pryvacy_decorator import nested_classes


T = TypeVar('T')
def pryvacy(cls: Type[T]) -> Type[T]:
    if "@@_pyvacified" in pryvacy.__dict__:
        return cls
    setattr(cls, "@@_pyvacified", ())

    instance_methods.init(cls)
    nested_classes.init(cls)
    
    old_init_subclass = cls.__init_subclass__
    @classmethod
    def init_subclass_wrapper(cls, **kwargs):
        pryvacy(cls)
        return old_init_subclass(**kwargs)

    setattr(cls, "__init_subclass__", init_subclass_wrapper)
        
    return cls


