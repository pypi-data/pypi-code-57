import pytest


@pytest.fixture(scope="function")
def hub(hub):
    """
    provides a full hub that is used as a reference for mock_hub
    """
    hub.pop.sub.add(dyne_name="grains")
    hub.pop.sub.add(dyne_name="exec")

    yield hub


@pytest.fixture(scope="function")
def mock_hub(hub, mock_hub):
    """
    A hub specific to grains unit testing
    Scope is function so that grains values are clean with every run
    """
    mock_hub.grains.init.clean_value = hub.grains.init.clean_value
    mock_hub.grains.GRAINS = hub.pop.data.omap()

    yield mock_hub

    del mock_hub.grains.GRAINS
