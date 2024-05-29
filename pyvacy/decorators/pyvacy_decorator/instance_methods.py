import inspect
from typing import Type

from pyvacy.access_policy import AccessPolicy
from pyvacy.context import reset_cls_ctx, set_cls_ctx, get_current_class
from pyvacy.decorators.utils import get_access_policy 


def init(cls: Type):
    normal_methods = { name: method for name, method in inspect.getmembers(cls, inspect.isfunction) if not name.startswith("__") }
    
    for name, _method in normal_methods.items():
        match get_access_policy(_method):
            case AccessPolicy.PUBLIC:
                continue

            case AccessPolicy.PRIVATE:
                def _local_private():
                    method = _method
                    def protected_method(self, *args, **kwargs):
                        try:
                            assert get_current_class() == cls 
                        except Exception:
                            raise Exception(f"'{name}' method of {cls.__name__} is marked as private")

                        try:
                            set_cls_ctx(cls)
                            return method(self, *args, **kwargs)
                        finally:
                            reset_cls_ctx()

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

                        try:
                            set_cls_ctx(cls)
                            return method(self, *args, **kwargs)
                        finally:
                            reset_cls_ctx()

                    return protected_method

                setattr(cls, name, _local_protected())
