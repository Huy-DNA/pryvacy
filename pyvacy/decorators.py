import inspect
from enum import Enum

from typing import Callable, TypeVar, Type

from pyvacy.context import get_current_class, reset_cls_ctx, set_cls_ctx

class AccessPolicy(Enum):
    PUBLIC = 0
    PROTECTED = 1
    PRIVATE = 2

T = TypeVar('T')
def pyvacy(cls: Type[T]) -> Type[T]:
    if "@@_pyvacified" in pyvacy.__dict__:
        return cls
    setattr(cls, "@@_pyvacified", ())

    normal_methods = { name: method for name, method in inspect.getmembers(cls, inspect.isfunction) if not name.startswith("__") }
    
    for name, _method in normal_methods.items():
        def _local():
            method = _method
            def wrapped_method(*args, **kwargs):
                try:
                    set_cls_ctx(cls, override = False)
                    return method(*args, **kwargs)
                finally:
                    reset_cls_ctx() 
            _set_access_policy(wrapped_method, _get_access_policy(method))
            return wrapped_method
        normal_methods[name] = _local()
        setattr(cls, name, normal_methods[name])

    origin_dict = cls.__dict__.copy()

    for name, _method in normal_methods.items():
        match _get_access_policy(_method):
            case AccessPolicy.PUBLIC:
                def _local_public():
                    method = _method
                    def public_method(*args, **kwargs):
                        _switch_dict(cls, exposed_dict, origin_dict)
                        result = method(*args, **kwargs)
                        _switch_dict(cls, origin_dict, exposed_dict)
                        return result
                    return public_method

                setattr(cls, name, _local_public())
                        
            case AccessPolicy.PRIVATE:
                def _local_private():
                    method = _method
                    def protected_method(self, *args, **kwargs):
                        try:
                            assert get_current_class() == cls 
                        except Exception:
                            raise Exception(f"'{name}' method of {cls.__name__} is marked as private")

                        _switch_dict(cls, exposed_dict, origin_dict)
                        result = method(self, *args, **kwargs)
                        _switch_dict(cls, origin_dict, exposed_dict)
                        return result

                    return protected_method

                setattr(cls, name, _local_private())

            case AccessPolicy.PROTECTED:
                def _local_protected():
                    method = _method
                    def protected_method(self, *args, **kwargs):
                        try:
                            assert issubclass(get_current_class(), cls) 
                        except Exception:
                            raise Exception(f"'{name}' method of {cls.__name__} is marked as protected")

                        _switch_dict(cls, exposed_dict, origin_dict)
                        result = method(self, *args, **kwargs)
                        _switch_dict(cls, origin_dict, exposed_dict)
                        return result

                    return protected_method

                setattr(cls, name, _local_protected())

    exposed_dict = cls.__dict__.copy()

    old_init_subclass = cls.__init_subclass__
    @classmethod
    def init_subclass_wrapper(cls, **kwargs):
        pyvacy(cls)
        return old_init_subclass(**kwargs)

    setattr(cls, "__init_subclass__", init_subclass_wrapper)
        
    return cls

def private(fn: Callable) -> Callable:
    _set_access_policy(fn, AccessPolicy.PRIVATE)

    return fn

def public(fn: Callable) -> Callable:
    _set_access_policy(fn, AccessPolicy.PUBLIC)

    return fn

def protected(fn: Callable) -> Callable:
    _set_access_policy(fn, AccessPolicy.PROTECTED)

    return fn

def _get_access_policy(fn: Callable) -> AccessPolicy:
    return fn.__dict__.get("@@_access_control", AccessPolicy.PUBLIC)

def _set_access_policy(fn: Callable, access_policy: AccessPolicy):
    fn.__dict__["@@_access_control"] = access_policy

def _switch_dict(obj: object, rem_dict: dict, add_dict: dict):
    for name in rem_dict:
        try:
            delattr(obj, name)
        except:
            pass
    for name, method in add_dict.items():
        try:
            setattr(obj, name, method)
        except:
            pass
