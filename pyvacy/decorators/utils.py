from typing import Callable, Type, Union

from pyvacy.access_policy import AccessPolicy


def get_access_policy(obj: Union[Callable, Type]) -> AccessPolicy:
    return obj.__dict__.get("@@_access_control", AccessPolicy.PUBLIC)

def set_access_policy(obj: Union[Callable, Type], access_policy: AccessPolicy):
    setattr(obj, "@@_access_control", access_policy)


