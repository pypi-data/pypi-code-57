import pytest
from repofinder.config import Config


def test_config_loader_raise_error():
    with pytest.raises(FileNotFoundError):
        Config("tests/data/not_exists.yml")


def test_config_loader_ok():
    Config('tests/data/test_params.yml')


def test_config_loader_content():
    config = Config('tests/data/test_params.yml')
    assert config.language == "<NAME>"

    assert type(config.created) == dict
    assert config.created['gt'] == "<DATE>"
    assert config.created['lt'] == "<DATE>"

    assert type(config.pushed) == dict
    assert config.pushed['gt'] == "<DATE>"
    assert config.pushed['lt'] == "<DATE>"

    assert type(config.stars) == dict
    assert config.stars['gt'] == "<NUMBER>"
    assert config.stars['lt'] == "<NUMBER>"

    assert type(config.forks) == dict
    assert config.forks['gt'] == "<NUMBER>"
    assert config.forks['lt'] == "<NUMBER>"
