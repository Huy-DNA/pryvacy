import inspect
from enum import Enum

from typing import Callable, TypeVar, Type

from pyvacy.context import is_method

T = TypeVar('T')

class AccessPolicy(Enum):
    PUBLIC = 0
    PROTECTED = 1
    PRIVATE = 2

def pyvacy(cls: Type[T]) -> Type[T]:
    normal_methods = [method for name, method in inspect.getmembers(cls, inspect.ismethod) if not name.startswith("__")]

    for method in normal_methods:
        match _get_access_policy(method):
            case AccessPolicy.PUBLIC:
                continue
            case AccessPolicy.PRIVATE:
                pass
            case AccessPolicy.PROTECTED:
                pass

    return cls

def private(fn: Callable) -> Callable:
    if not is_method(fn):
        raise Exception("Can not mark a non-method as private") 
    
    _set_access_policy(fn, AccessPolicy.PRIVATE)

    return fn

def public(fn: Callable) -> Callable:
    if not is_method(fn):
        raise Exception("Can not mark a non-method as public")

    _set_access_policy(fn, AccessPolicy.PUBLIC)

    return fn

def protected(fn: Callable) -> Callable:
    if not is_method(fn):
        raise Exception("Can not mark a non-method as protected")

    _set_access_policy(fn, AccessPolicy.PROTECTED)

    return fn

def _get_access_policy(fn: Callable) -> AccessPolicy:
    return fn.__dict__.get("@@_access_control", AccessPolicy.PUBLIC)

def _set_access_policy(fn: Callable, access_policy: AccessPolicy):
    fn.__dict__["@@_access_control"] = access_policy

def _mangle_method_name(cls: Type, fn: Callable) -> str:
    return f"@@_${cls.__name__}__${fn.__name__}"
