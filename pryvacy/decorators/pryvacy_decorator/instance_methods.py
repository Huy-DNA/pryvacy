import inspect
from typing import Type

from pryvacy.access_policy import AccessPolicy
from pryvacy.context import pop_cls_ctx, push_cls_ctx, get_current_class
from pryvacy.decorators.utils import get_access_policy 


def init(cls: Type):
    normal_methods = { name: method for name, method in inspect.getmembers(cls, inspect.isfunction) if not name.startswith("__") }
    for name, _method in normal_methods.items():
        match get_access_policy(_method):
            case AccessPolicy.PUBLIC:
                def _local_public():
                    method = _method
                    def public_method(self, *args, **kwargs):
                        try:
                            push_cls_ctx(cls)
                            return method(self, *args, **kwargs)
                        finally:
                            pop_cls_ctx()

                    return public_method

                setattr(cls, name, _local_public())

            case AccessPolicy.PRIVATE:
                def _local_public():
                    method = _method
                    def private_method(self, *args, **kwargs):
                        current_class = get_current_class()
                        if not current_class or not (current_class == cls or cls.__dict__.get(current_class.__name__, None) == current_class):
                            raise Exception(f"'{name}' method of {cls.__name__} is marked as private")

                        try:
                            push_cls_ctx(cls)
                            return method(self, *args, **kwargs)
                        finally:
                            pop_cls_ctx()

                    return private_method

                setattr(cls, name, _local_public())

            case AccessPolicy.PROTECTED:
                def _local_protected():
                    method = _method
                    def protected_method(self, *args, **kwargs):
                        current_class = get_current_class()
                        if not current_class or not (issubclass(current_class, cls) or cls.__dict__.get(current_class.__name__, None) == current_class):
                            raise Exception(f"'{name}' method of {cls.__name__} is marked as protected")

                        try:
                            push_cls_ctx(cls)
                            return method(self, *args, **kwargs)
                        finally:
                            pop_cls_ctx()

                    return protected_method

                setattr(cls, name, _local_protected())
