import pytest


@pytest.mark.skip_if_not_root
@pytest.mark.asyncio
async def test_get(hub):
    await hub.exec.smbios.get("bios-version")


@pytest.mark.skip_if_not_root
@pytest.mark.asyncio
async def test_records(hub):
    await hub.exec.smbios.records(0)
