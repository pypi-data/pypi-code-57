# -*- coding: utf-8 -*-
"""
    tests.unit.conftest
    ~~~~~~~~~~~~~~
    Provide mock_hub fixture for all unit tests.
"""
import pytest


@pytest.fixture(scope="function")
def hub(hub):
    hub.pop.sub.add(dyne_name="grains")
    yield hub
