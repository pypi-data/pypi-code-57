from flywheel_cli.ingest import config
from flywheel_cli.ingest.strategies.dicom import DicomStrategy
from flywheel_cli.ingest.template import ScannerNode


def test_instantiate():
    cfg = config.DicomConfig(group="group", project="project")
    strategy = DicomStrategy(cfg)

    assert isinstance(strategy, DicomStrategy)
    assert strategy.config == cfg


def test_config():
    cfg = config.DicomConfig(
        group="group", project="project", subject="subject", session="session"
    )
    strategy = DicomStrategy(cfg)

    assert strategy.context == {
        "subject": {"label": "subject"},
        "session": {"label": "session"},
    }


def test_initialize():
    cfg = config.DicomConfig(group="group", project="project")
    strategy = DicomStrategy(cfg)
    strategy.initialize()

    assert isinstance(strategy.root_node, ScannerNode)
    assert strategy.root_node == strategy._last_added_node
    assert strategy.root_node.scanner_type == "dicom"
    assert strategy.root_node.opts == {}
