import pytest

from examples.index import (
    vdom,
    render,
    split,
    scope,
    props,
    expressions,
    escaping,
    prevent_escaping,
    conditional,
    looping,
    components,
    callable,
    context,
)


@pytest.mark.parametrize(
    'target',
    [
        vdom,
        render,
        split,
        scope,
        props,
        expressions,
        escaping,
        prevent_escaping,
        conditional,
        looping,
        components,
        callable,
        context
    ]
)
def test_docs_index(target):
    assert target.expected == target.result
