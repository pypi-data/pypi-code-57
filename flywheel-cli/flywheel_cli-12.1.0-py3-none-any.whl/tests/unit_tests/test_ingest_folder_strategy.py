import re

from flywheel_cli.ingest import config
from flywheel_cli.ingest.strategies.folder import FolderStrategy
from flywheel_cli.ingest.template import StringMatchNode, TerminalNode


def test_instantiate():
    cfg = config.FolderConfig()
    strategy = FolderStrategy(cfg)

    assert isinstance(strategy, FolderStrategy)
    assert strategy.config == cfg

def test_initialize_default():
    cfg = config.FolderConfig()
    strategy = FolderStrategy(cfg)
    strategy.initialize()

    node = strategy.root_node
    # default group
    assert isinstance(node, StringMatchNode)
    assert node.template == "group"
    # default project
    node = node.next_node
    assert isinstance(node, StringMatchNode)
    assert node.template == "project"
    # default subject
    node = node.next_node
    assert isinstance(node, StringMatchNode)
    assert node.template == "subject"
    # default session
    node = node.next_node
    assert isinstance(node, StringMatchNode)
    assert node.template == "session"
    # default acquisition
    node = node.next_node
    assert isinstance(node, StringMatchNode)
    assert node.template == "acquisition"
    node = node.next_node
    assert isinstance(node, StringMatchNode)
    assert node.template == re.compile(cfg.dicom)
    assert node.packfile_type == "dicom"

    node = node.next_node
    assert isinstance(node, TerminalNode)

def test_initialize_root_dirs():
    cfg = config.FolderConfig(
        root_dirs=2
    )
    strategy = FolderStrategy(cfg)
    strategy.initialize()

    node = strategy.root_node
    assert isinstance(node, StringMatchNode)
    assert node.template == re.compile(".*")

    node = node.next_node
    assert isinstance(node, StringMatchNode)
    assert node.template == re.compile(".*")

    node = node.next_node
    assert isinstance(node, StringMatchNode)
    assert node.template == "group"

def test_initialize_custom():
    cfg = config.FolderConfig(
        group="gid",
        project="pid",
        no_subjects=True,
        no_sessions=True,
        pack_acquisitions=True
    )
    strategy = FolderStrategy(cfg)
    strategy.initialize()

    node = strategy.root_node
    assert isinstance(node, StringMatchNode)
    assert node.template == "acquisition"
    assert node.packfile_type == cfg.pack_acquisitions
