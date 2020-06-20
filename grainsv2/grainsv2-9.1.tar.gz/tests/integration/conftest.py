import pytest


@pytest.fixture
def hub(hub):
    hub.pop.sub.add(dyne_name="grains")
    yield hub
