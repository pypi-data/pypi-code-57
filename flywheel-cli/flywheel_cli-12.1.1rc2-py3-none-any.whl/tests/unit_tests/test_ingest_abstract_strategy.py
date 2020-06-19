import pytest

from flywheel_cli.ingest.strategies import abstract
from flywheel_cli.ingest.template import StringMatchNode, TerminalNode


def test_add_template_node():
    strategy = DummyStrategy(config=None)
    node1 = StringMatchNode()
    strategy.add_template_node(node1)

    assert strategy.root_node == node1
    assert strategy._last_added_node == node1

    node2 = StringMatchNode()
    strategy.add_template_node(node2)

    assert strategy.root_node == node1
    assert strategy._last_added_node == node2


def test_add_template_node_raise():
    strategy = DummyStrategy(config=None)
    node1 = TerminalNode()
    strategy.add_template_node(node1)

    assert strategy.root_node == node1
    assert strategy._last_added_node == node1

    with pytest.raises(ValueError):
        strategy.add_template_node(StringMatchNode())


def test_initial_context_default(attr_dict):
    strategy = DummyStrategy(config=attr_dict({"group": None, "project": None,}))

    ctx = strategy.initial_context()
    assert ctx == {}


def test_initial_context_w_context(attr_dict):
    strategy = DummyStrategy(
        config=attr_dict({"group": None, "project": None,}),
        context={"key1": "value1", "key2": {"key21": "value21"}},
    )

    ctx = strategy.initial_context()
    assert ctx == {"key1": "value1", "key2": {"key21": "value21"}}


def test_initial_context_w_context_and_group_and_project(attr_dict):
    strategy = DummyStrategy(
        config=attr_dict({"group": "gid", "project": "pid",}),
        context={"key1": "value1",},
    )

    ctx = strategy.initial_context()
    assert ctx == {
        "key1": "value1",
        "group": {"_id": "gid"},
        "project": {"label": "pid"},
    }


class DummyStrategy(abstract.Strategy):
    def initialize(self):
        pass
