import inspect
from typing import Type

from pyvacy.access_policy import AccessPolicy
from pyvacy.decorators.utils import get_access_policy 


def init(cls: Type):
    from pyvacy.decorators.pyvacy_decorator import pyvacy

    nested_classes = { name: obj for name, obj in inspect.getmembers(cls, inspect.isclass) if obj.__module__ == cls.__module__ }

    for name, nested_cls in nested_classes.items():
        match get_access_policy(nested_cls):
            case AccessPolicy.PUBLIC:
                pyvacy(nested_cls)
            case AccessPolicy.PRIVATE:
                raise NotImplemented("Can not annotate nested classes with @private yet")
            case AccessPolicy.PROTECTED:
                raise NotImplemented("Can not annotate nested classes with @protected yet")
