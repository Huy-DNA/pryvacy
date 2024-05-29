import pytest

from pryvacy import private, public, pryvacy

def test():
    global Foo

    @pryvacy
    class Foo():
        @public
        def annotated_public_method(self):
            Bar().call_private()

        @private
        def annotated_private_method(self):
            print("private")

    global Bar

    class Bar():
        def call_public(self):
            Foo().annotated_public_method()

        def call_private(self):
            Foo().annotated_private_method()

def test_back_and_forth():
    try:
        Bar().call_public()
        assert False
    except Exception as e:
        assert f"{e}" == ""
