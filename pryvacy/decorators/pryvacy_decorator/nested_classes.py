import inspect
from typing import Type

from pryvacy.access_policy import AccessPolicy
from pryvacy.decorators.utils import get_access_policy 


def init(cls: Type):
    from pryvacy.decorators.pryvacy_decorator import pryvacy

    nested_classes = { name: obj for name, obj in cls.__dict__.items() if inspect.isclass(obj) and obj.__module__ == cls.__module__ }

    for name, nested_cls in nested_classes.items():
        match get_access_policy(nested_cls):
            case AccessPolicy.PUBLIC:
                pryvacy(nested_cls)
            case AccessPolicy.PRIVATE:
                raise NotImplemented("Can not annotate nested classes with @private yet")
            case AccessPolicy.PROTECTED:
                raise NotImplemented("Can not annotate nested classes with @protected yet")
