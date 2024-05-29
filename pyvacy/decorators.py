import inspect
from enum import Enum

from typing import Callable, TypeVar, Type

from pyvacy.context import ClassContextManager

T = TypeVar('T')

class AccessPolicy(Enum):
    PUBLIC = 0
    PROTECTED = 1
    PRIVATE = 2

def pyvacy(cls: Type[T]) -> Type[T]:
    with ClassContextManager(cls):
        normal_methods = { name: method for name, method in inspect.getmembers(cls, inspect.isfunction) if not name.startswith("__") }
        origin_dict = cls.__dict__.copy() 
        
        for _name, _method in normal_methods.items():
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
                    setattr(cls, _name, _local_public())
                        
                case AccessPolicy.PRIVATE:
                    delattr(cls, _name)
                
                case AccessPolicy.PROTECTED:
                    def _local_protected():
                        method = _method
                        __class__ = cls
                        def protected_method(self, *args, **kwargs):
                            try:
                                super()
                                assert isinstance(self, cls)
                            except Exception as e:
                                raise Exception(f"'{_name}' method of {cls.__name__} is marked as protected")
                            _switch_dict(cls, exposed_dict, origin_dict)
                            result = method(self, *args, **kwargs)
                            _switch_dict(cls, origin_dict, exposed_dict)
                            return result

                        return protected_method
                    setattr(cls, _name, _local_protected())
        
        exposed_dict = cls.__dict__.copy()
        
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
