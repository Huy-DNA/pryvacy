import inspect
from typing import Type

from pryvacy.access_policy import AccessPolicy
from pryvacy.context import reset_cls_ctx, set_cls_ctx, get_current_class
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
                            set_cls_ctx(cls)
                            return method(self, *args, **kwargs)
                        finally:
                            reset_cls_ctx()

                    return public_method

                setattr(cls, name, _local_public())

            case AccessPolicy.PRIVATE:
                def _local_public():
                    method = _method
                    def private_method(self, *args, **kwargs):
                        try:
                            current_class = get_current_class()
                            assert current_class and (current_class == cls or cls.__dict__[current_class.__name__] == current_class)
                        except Exception:
                            raise Exception(f"'{name}' method of {cls.__name__} is marked as private")

                        try:
                            set_cls_ctx(cls)
                            return method(self, *args, **kwargs)
                        finally:
                            reset_cls_ctx()

                    return private_method

                setattr(cls, name, _local_public())

            case AccessPolicy.PROTECTED:
                def _local_protected():
                    method = _method
                    def protected_method(self, *args, **kwargs):
                        try:
                            current_class = get_current_class()
                            assert current_class and (issubclass(current_class, cls) or cls.__dict__[current_class.__name__] == current_class)
                        except Exception:
                            raise Exception(f"'{name}' method of {cls.__name__} is marked as protected")

                        try:
                            set_cls_ctx(cls)
                            return method(self, *args, **kwargs)
                        finally:
                            reset_cls_ctx()

                    return protected_method

                setattr(cls, name, _local_protected())
