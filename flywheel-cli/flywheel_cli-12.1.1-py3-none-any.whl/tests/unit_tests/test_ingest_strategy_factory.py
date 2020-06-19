import pytest

from flywheel_cli.ingest import config
from flywheel_cli.ingest.strategies import dicom, factory, folder, template


def test_factory_raise(attr_dict):
    cfg = attr_dict({"strategy_name": "Unknwon"})
    with pytest.raises(ValueError):
        factory.create_strategy(cfg)


def test_factory_dicom():
    cfg = config.DicomConfig(group="gid", project="pid")

    strategy = factory.create_strategy(cfg)

    assert isinstance(strategy, dicom.DicomStrategy)


def test_factory_folder():
    cfg = config.FolderConfig()

    strategy = factory.create_strategy(cfg)

    assert isinstance(strategy, folder.FolderStrategy)


def test_factory_template():
    cfg = config.TemplateConfig(template=[])

    strategy = factory.create_strategy(cfg)

    assert isinstance(strategy, template.TemplateStrategy)
