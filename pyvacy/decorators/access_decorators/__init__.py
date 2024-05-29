from typing import Callable

from pyvacy.access_policy import AccessPolicy
from pyvacy.decorators.utils import set_access_policy


def private(fn: Callable) -> Callable:
    set_access_policy(fn, AccessPolicy.PRIVATE)

    return fn

def public(fn: Callable) -> Callable:
    set_access_policy(fn, AccessPolicy.PUBLIC)

    return fn

def protected(fn: Callable) -> Callable:
    set_access_policy(fn, AccessPolicy.PROTECTED)

    return fn


