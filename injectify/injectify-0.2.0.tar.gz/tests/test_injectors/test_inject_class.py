from injectify.api import inject
from injectify.injectors import (
    HeadInjector,
    TailInjector,
    FieldInjector,
)


class cls11:
    x = 10


def test_head_injector_correctly_injects_class():
    @inject(target=cls11, injector=HeadInjector())
    def handler():
        x = 11

    assert cls11.x == 10
    assert cls11().x == 10


class cls24:
    x = 10


def test_tail_injector_correctly_injects_class():
    @inject(target=cls24, injector=TailInjector())
    def handler():
        x = 11

    assert cls24.x == 11
    assert cls24().x == 11


class cls37:
    x = 10
    y = 20
    z = 30


def test_field_injector_correctly_injects_class_before_field():
    @inject(target=cls37, injector=FieldInjector('y', insert='before'))
    def handler():
        x = 15

    assert cls37.x == 15
    assert cls37().x == 15
    assert cls37.y == 20
    assert cls37().y == 20
    assert cls37.z == 30
    assert cls37().z == 30


class cls54:
    x = 10
    y = 20
    z = 30


def test_field_injector_correctly_injects_class_after_field():
    @inject(target=cls54, injector=FieldInjector('y', insert='after'))
    def handler():
        y = 25

    assert cls54.x == 10
    assert cls54().x == 10
    assert cls54.y == 25
    assert cls54().y == 25
    assert cls54.z == 30
    assert cls54().z == 30
