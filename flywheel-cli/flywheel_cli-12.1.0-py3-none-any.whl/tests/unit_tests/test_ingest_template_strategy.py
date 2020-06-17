import re

import pytest

from flywheel_cli.ingest import config
from flywheel_cli.ingest.strategies.template import TemplateStrategy
from flywheel_cli.ingest.template import StringMatchNode, TerminalNode


def test_instantiate():
    cfg = config.TemplateConfig(template="template")
    strategy = TemplateStrategy(cfg)

    assert isinstance(strategy, TemplateStrategy)
    assert strategy.config == cfg

def test_initialize_template_raise():
    cfg = config.TemplateConfig(template=[])
    strategy = TemplateStrategy(cfg)

    with pytest.raises(ValueError) as execinfo:
        strategy.initialize()

    assert "template" in str(execinfo.value).lower()

def test_initialize_template_no_group_raise():
    cfg = config.TemplateConfig(template="template")
    strategy = TemplateStrategy(cfg)

    with pytest.raises(ValueError) as execinfo:
        strategy.initialize()

    assert "group" in str(execinfo.value).lower()

def test_initialize_template_str_invalid_raise():
    cfg = config.TemplateConfig(
        group="group_id",
        template="["
    )
    strategy = TemplateStrategy(cfg)

    with pytest.raises(ValueError) as execinfo:
        strategy.initialize()

    assert "invalid" in str(execinfo.value).lower()

def test_initialize_template_str():
    cfg = config.TemplateConfig(
        group="group_id",
        template=".*"
    )
    strategy = TemplateStrategy(cfg)
    strategy.initialize()

    assert isinstance(strategy.root_node, StringMatchNode)
    assert strategy.root_node.template == re.compile(".*")

def test_initialize_template_list():
    cfg = config.TemplateConfig(
        group="group_id",
        template=[
            {"pattern": "{project}"},
            {"pattern": "{subject}"},
            {"pattern": "{session}"}
        ]
    )

    strategy = TemplateStrategy(cfg)
    strategy.initialize()

    node = strategy.root_node
    #project
    assert isinstance(node, StringMatchNode)
    assert node.template == re.compile("(?P<project>.+)")
    #subject
    node = node.next_node
    assert isinstance(node, StringMatchNode)
    assert node.template == re.compile("(?P<subject>.+)")
    #session
    node = node.next_node
    assert isinstance(node, StringMatchNode)
    assert node.template == re.compile("(?P<session>.+)")

    node = node.next_node
    assert isinstance(node, TerminalNode)

def test_check_group_reference_node_raise():
    cfg = config.TemplateConfig(template=[])

    strategy = TemplateStrategy(cfg)
    node = StringMatchNode(re.compile("(?P<random>.+)"))
    node.set_next(StringMatchNode(re.compile("(?P<random1>.+)")))
    strategy.root_node = node

    with pytest.raises(ValueError):
        strategy.check_group_reference()
