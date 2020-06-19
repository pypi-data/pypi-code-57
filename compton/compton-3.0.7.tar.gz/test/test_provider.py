import pytest
from compton import (
    Provider,
    Orchestrator
)

from .types import (
    SimpleReducer
)


def test_check():
    class A:
        pass

    with pytest.raises(
        ValueError,
        match='must be an instance of Provider'
    ):
        Orchestrator([
            SimpleReducer()
        ]).connect(A())


def test_str():
    class InvalidProvider(Provider):
        @property
        def vector(self):
            return 1

        def init():
            pass

        def remove():
            pass

        def when_update():
            pass

    assert str(InvalidProvider()) == 'provider<invalid>'

    with pytest.raises(
        ValueError,
        match='vector of provider<invalid> must be a tuple, but got `1`'
    ):
        Orchestrator([
            SimpleReducer()
        ]).connect(InvalidProvider())

    class ValidVectorProvider(Provider):
        @property
        def vector(self):
            return (1, 2)

        def init():
            pass

        def remove():
            pass

        def when_update():
            pass

    assert str(ValidVectorProvider()) == 'provider<1,2>'


def test_vector_not_hashable():
    class VectorNotHashableProvider(Provider):
        @property
        def vector(self):
            return ({},)

        def init():
            pass

        def remove():
            pass

        def when_update():
            pass

    with pytest.raises(
        ValueError,
        match='vector of provider<{}>'
    ):
        Orchestrator([
            SimpleReducer()
        ]).connect(VectorNotHashableProvider())
