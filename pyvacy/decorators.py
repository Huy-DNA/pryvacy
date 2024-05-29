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
        normal_methods = { name: method for name, method in inspect.getmembers(cls, inspect.ismethod) if not name.startswith("__") }
        cls.__dict__["@@original_methods"] = normal_methods

        for name, method in normal_methods.items():
            del cls.__dict__[name]

            match _get_access_policy(method):
                case AccessPolicy.PUBLIC:
                    def public_method(*args, **kwargs):
                        old_dict = cls.__dict__.copy()
                        cls.__dict__.update(cls.__dict__["@@original_methods"])
                        method(*args, **kwargs)
                        cls.__dict__ = old_dict
                    cls.__dict__[name] = public_method
                        
                case AccessPolicy.PRIVATE:
                    continue

                case AccessPolicy.PROTECTED:
                    continue

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

def _mangle_method_name(cls: Type, fn: Callable, access_policy: AccessPolicy) -> str:
    return f"@@_${cls.__name__}__${fn.__name__}__${access_policy}"
