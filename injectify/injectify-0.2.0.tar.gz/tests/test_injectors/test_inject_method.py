from injectify.api import inject
from injectify.injectors import (
    HeadInjector,
    TailInjector,
    ReturnInjector,
    FieldInjector,
    NestedInjector,
)


def test_head_injector_correctly_injects_method():
    class Target:
        def target(self, x):
            a = 10
            if x > a:
                a = x
            return a

    @inject(target=Target.target, injector=HeadInjector())
    def handler():
        x = 11

    target = Target()
    assert target.target(0) == 11
    assert target.target(10) == 11
    assert target.target(101) == 11


def test_tail_injector_correctly_injects_method():
    class Target:
        def target(self, x):
            if x > 100:
                return x

    @inject(target=Target.target, injector=TailInjector())
    def handler():
        return -1

    target = Target()
    assert target.target(13) == -1
    assert target.target(101) == 101


def test_return_injector_correctly_injects_method_all_returns():
    class Target:
        def target(self, x):
            if x > 100:
                y = x * 2
                return y
            else:
                y = x + 2
                return y

    @inject(target=Target.target, injector=ReturnInjector())
    def handler():
        return '{} :)'.format(y)

    target = Target()
    assert target.target(13) == '15 :)'
    assert target.target(101) == '202 :)'


def test_return_injector_correctly_injects_method_ordinal_returns():
    class Target:
        def target(self, x):
            if x > 100:
                y = x * 2
                return y
            else:
                y = x + 2
                return y

    @inject(target=Target.target, injector=ReturnInjector(ordinal=1))
    def handler():
        return '{} :)'.format(y)

    target = Target()
    assert target.target(13) == '15 :)'
    assert target.target(101) == 202


def test_field_injector_correctly_injects_method_before_all_fields():
    class Target:
        def target(self, x):
            if x > 100:
                y = x * 2
            else:
                y = x + 2
            return y

    @inject(target=Target.target, injector=FieldInjector('y', insert='before'))
    def handler():
        x += 1

    target = Target()
    assert target.target(13) == 16
    assert target.target(101) == 204


def test_field_injector_correctly_injects_method_after_all_fields():
    class Target:
        def target(self, x):
            if x > 100:
                y = x * 2
            else:
                y = x + 2
            return y

    @inject(target=Target.target, injector=FieldInjector('y', insert='after'))
    def handler():
        y -= 1

    target = Target()
    assert target.target(13) == 14
    assert target.target(101) == 201


def test_field_injector_correctly_injects_method_before_ordinal_field():
    class Target:
        def target(self, x):
            if x > 100:
                y = x * 2
            else:
                y = x + 2
            return y

    @inject(
        target=Target.target, injector=FieldInjector('y', ordinal=1, insert='before'),
    )
    def handler():
        x += 1

    target = Target()
    assert target.target(13) == 16
    assert target.target(101) == 202


def test_field_injector_correctly_injects_method_after_ordinal_field():
    class Target:
        def target(self, x):
            if x > 100:
                y = x * 2
            else:
                y = x + 2
            return y

    @inject(
        target=Target.target, injector=FieldInjector('y', ordinal=0, insert='after')
    )
    def handler():
        y -= 1

    target = Target()
    assert target.target(13) == 15
    assert target.target(101) == 201


def test_nested_injector_correctly_injects_method():
    class Target:
        def target(self, x):
            def nested(y):
                if y > 100:
                    return y

            if x < 200:
                return nested(x)

    @inject(target=Target.target, injector=NestedInjector('nested', TailInjector()))
    def handler():
        return -1

    target = Target()
    assert target.target(13) == -1
    assert target.target(101) == 101
    assert target.target(200) is None
