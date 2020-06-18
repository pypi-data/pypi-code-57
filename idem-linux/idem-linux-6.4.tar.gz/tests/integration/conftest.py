import pytest


@pytest.fixture(scope="session")
def hub(hub):
    hub.pop.sub.add(dyne_name="grains")
    hub.pop.sub.add(dyne_name="exec")
    hub.pop.sub.add(dyne_name="states")

    hub.grains.init.standalone()

    yield hub
