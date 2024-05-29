import pytest

from pyvacy import pyvacy, public, private, protected 

@pyvacy
class Base():
    @public
    def annotated_public_method(self):
        return "This is a public method annotated with @public"

    def bare_public_method(self):
        return "This is a public method not annotated with @public"

    @public
    def public_method_call_private_method(self):
        return self.annotated_private_method()
        
    @public
    def public_method_call_protected_method(self):
        return self.annotated_protected_method()

    @private
    def annotated_private_method(self):
        return "This is a private method annotated with @private"
        
    @protected
    def annotated_protected_method(self):
        return "This is a protected method annotated with @protected"

    @protected
    def protected_method_call_private_method(self):
        return self.annotated_private_method()
        
    @protected
    def protected_method_call_public_method(self):
        return self.annotated_public_method()

@pyvacy
class Derived(Base):
    @public
    def public_method_call_base_annotated_protected_method(self):
        return self.annotated_protected_method()

    @public
    def public_method_call_base_protected_method_call_private_method(self):
        return self.protected_method_call_private_method()

    @public
    def public_method_call_base_protected_method_call_public_method(self):
        return self.protected_method_call_public_method()

def test_public_methods():
    test = Base()
    assert test.annotated_public_method() == "This is a public method annotated with @public"
    assert test.bare_public_method() == "This is a public method not annotated with @public"
    assert test.public_method_call_private_method() == "This is a private method annotated with @private"
    assert test.public_method_call_protected_method() == "This is a protected method annotated with @protected"

def test_private_methods():
    test = Base()
    try:
        test.annotated_private_method()
    except Exception as e:
        assert f"{e}" == "'Base' object has no attribute 'annotated_private_method'"

def test_protected_methods():
    test = Base()
    try:
        test.annotated_protected_method()
    except Exception as e:
        assert f"{e}" == "'public_method_call_protected_method' method of Base is marked as protected"

def test_derived():
    test = Derived()
    assert test.public_method_call_base_annotated_protected_method() == "This is a protected method annotated with @protected"
