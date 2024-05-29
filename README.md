# pryvacy - a set of access control decorators for python

## Philosophy

* Incur as least overhead as possible when using the access control decorators
* Only classes that use the decorators need to be changed, other related classes do not need to -> Can be opted-in easily

## Installation

```bash
pip install pryvacy
```

## Usage

The package provides 3 access control decorators: `@private`, `@public`, `@protected` that can be used on methods and nested classes (currently only `@private` can be used on nested classes)

```python
from pryvacy import pryvacy, private, public, protected

@pryvacy
class Foo():
  @public
  def public_method(self):
    pass

  @protected
  def protected_method(self):
    pass

  @privaye
  def private_method(self):
    pass
```

Access control rules:
* Methods inside `Foo` are able to access `public_method`, `protected_method`, `private_method`.
* Code outside `Foo` and not inside any `Foo`'s subclass methods can only access `public_method`.
* Methods inside `Foo`'s subclasses (either decorated with `@pryvacy` or not) can access `public_method` and `protected_method`.
* Nested classes methods can access `public_method`, `protected_method`, `private_method`.

## Pitfalls & Bugs

Disclaimer: The package has not been tested thoroughly! Use with caution! Any contributions are appreciated~

Currently, class-level code cannot access `protected_method` and `private_method`.

Example:
```python
  class Foo():
    ...
    class Bar(Foo):
      Foo().public_method() # OK!
      Foo().protected_method() # Exception!
      Foo().private_method() # Exception!
```

## Current limitations

* `@private` and `@protected` are not supported on nested classes yet.

* No way to enforce access policy on class and instance attributes.

## Roadmap

* Benchmark decorated classes

* Test comprehensively the decorators interaction with the whole ecosystem

* Implement @private and @protected on nested classes

