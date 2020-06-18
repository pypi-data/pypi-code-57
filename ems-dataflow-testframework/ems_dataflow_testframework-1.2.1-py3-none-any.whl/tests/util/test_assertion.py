import pytest

from testframework.util import assertion
from tests.util.module_for_assert_has_decorator import DecoratorDummy
from tests.util import module_for_assert_has_decorator


def test_undecoratedModule_delegatesUndecoratedAndRestoresModule():
    assert 2 == module_for_assert_has_decorator.DecoratorDummy.return_one()

    with assertion.undecorated_module(module_for_assert_has_decorator,
                                      'tests.util.dummy_decorator.dummydec') as module_without_decorator:
        assert 1 == module_for_assert_has_decorator.DecoratorDummy.return_one()
        assert 1 == module_without_decorator.DecoratorDummy.return_one()

    assert 2 == module_for_assert_has_decorator.DecoratorDummy.return_one()


@assertion.undecorated_module(module_for_assert_has_decorator, 'tests.util.dummy_decorator.dummydec')
def test_undecoratedModuleAsDecorator_delegatesUndecoratedAndRestoresModule():
    with assertion.undecorated_module(module_for_assert_has_decorator,
                                      'tests.util.dummy_decorator.dummydec'):
        assert 1 == module_for_assert_has_decorator.DecoratorDummy.return_one()


def test_assertHasDecorator_failIfMethodDoesNotHaveDecorator():
    with pytest.raises(AssertionError):
        assertion.assert_has_decorator(DecoratorDummy.method_without_decorator, 'tests.util.dummy_decorator.dummydec')


def test_assertHasDecorator_passesIfMethodHasDecoratorWithCorrectParameters():
    assertion.assert_has_decorator(DecoratorDummy.method_with_decorator, 'tests.util.dummy_decorator.dummydec', 103,
                                   stop_max_delay=10000, wait_fixed=1000)


def test_assertHasDecorator_failIfMethodDoesnotHaveDecoratorWithIncorrectParameters():
    assertion.assert_has_decorator(DecoratorDummy.method_with_decorator_3, 'tests.util.dummy_decorator.dummydec',
                                   stop_max_delay=10001)


def test_assertHasDecorator_failIfMethodDoesNotHaveThatDecorator():
    with pytest.raises(AssertionError):
        assertion.assert_has_decorator(DecoratorDummy.method_without_decorator, 'tests.util.dummy_decorator.dummydec')


def test_assertHasDecorator_restoresOriginalModule():
    assertion.assert_has_decorator(DecoratorDummy.return_one, 'tests.util.dummy_decorator.dummydec', multiple_by=2)

    from tests.util.module_for_assert_has_decorator import DecoratorDummy as OriginalDecoratorDummy

    assert 2 == OriginalDecoratorDummy.return_one()
