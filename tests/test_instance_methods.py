import pytest

from pryvacy import private, protected, public, pryvacy

def test():
    global Base

    @pryvacy
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
    
    global PyvacifiedDerived
    
    @pryvacy
    class PyvacifiedDerived(Base):
        @public
        def public_method_call_base_annotated_protected_method(self):
            return self.annotated_protected_method()

        @public
        def public_method_call_base_protected_method_call_private_method(self):
            return self.protected_method_call_private_method()

        @public
        def public_method_call_base_protected_method_call_public_method(self):
            return self.protected_method_call_public_method()

    global BareDerived
    
    class BareDerived(Base):
        def public_method_call_base_annotated_protected_method(self):
            return self.annotated_protected_method()

        def public_method_call_base_protected_method_call_private_method(self):
            return self.protected_method_call_private_method()

        def public_method_call_base_protected_method_call_public_method(self):
            return self.protected_method_call_public_method()
    
    global Underived

    @pryvacy
    class Underived():
        def public_method_call_protected_method(self):
            return Base().annotated_protected_method()

    global Outer

    @pryvacy
    class Outer():
        @private
        def foo(self):
            return "private outer foo"

        class Inner1():
            def foo(self):
                return f"{Outer().foo()} public inner1 foo"

        @pryvacy
        class Inner2():
            @public
            def foo(self):
                return f"{Outer().foo()} public inner2 foo"

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
        assert False
    except Exception as e:
        assert f"{e}" == "'protected_method_call_public_method' method of Base is marked as private"

def test_protected_methods():
    test = Base()
    try:
        test.annotated_protected_method()
        assert False
    except Exception as e:
        assert f"{e}" == "'protected_method_call_public_method' method of Base is marked as protected"

def test_pivacified_derived():
    test = PyvacifiedDerived()
    assert test.public_method_call_base_annotated_protected_method() == "This is a protected method annotated with @protected"
    assert test.public_method_call_protected_method() == "This is a protected method annotated with @protected"
    assert test.public_method_call_base_protected_method_call_private_method() == "This is a private method annotated with @private"
    assert test.public_method_call_base_protected_method_call_public_method() == "This is a public method annotated with @public"

def test_bare_derived():
    test = BareDerived()
    assert test.public_method_call_base_annotated_protected_method() == "This is a protected method annotated with @protected"
    assert test.public_method_call_protected_method() == "This is a protected method annotated with @protected"
    assert test.public_method_call_base_protected_method_call_private_method() == "This is a private method annotated with @private"
    assert test.public_method_call_base_protected_method_call_public_method() == "This is a public method annotated with @public"

def test_underived():
    test = Underived()
    try:
        test.public_method_call_protected_method()
        assert False
    except Exception as e:
        assert f"{e}" == "'protected_method_call_public_method' method of Base is marked as protected"

def test_nested_classes():
    assert Outer.Inner1().foo() == "private outer foo public inner1 foo"
    assert Outer.Inner2().foo() == "private outer foo public inner2 foo"
