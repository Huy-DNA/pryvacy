# pyvacy - a set of access control decorators for python

## Philosophy

* Incur as least overhead as possible when using the access control decorators 

## Current limitation

* Still very slow - a lot is going on when calling the decorated methods
* Still not handle metaprogramming correctly - for example, if a method modify a `<class>.__dict__`
* Still not support class methods, static methods, class attributes and instance attributes
