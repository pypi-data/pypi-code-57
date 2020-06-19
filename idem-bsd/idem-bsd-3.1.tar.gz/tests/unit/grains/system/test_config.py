import pytest


@pytest.mark.asyncio
async def test_load_config(mock_hub, hub):
    mock_hub.grains.system.config.load_config = hub.grains.system.config.load_config
    await mock_hub.grains.system.config.load_config()
