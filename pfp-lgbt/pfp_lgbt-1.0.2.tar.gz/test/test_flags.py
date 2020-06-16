import pytest
from unittest import IsolatedAsyncioTestCase
import pfp_lgbt

class Flag(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.client = pfp_lgbt.Client()
        self.flags = await self.client.flags()

    async def asyncTearDown(self):
        await self.client.close()

class TestFlag(Flag):
    async def test_flag_count(self):
        assert len(self.flags) > 10, 'Flag count is not higher than 10'
    async def test_flag_present(self):
        presentCount = 0
        for flag in self.flags:
            if (flag.name == 'nb') or (flag.name == 'pride') or (flag.name == 'trans'):
                presentCount += 1
        assert presentCount == 3, 'NB, Pride and Trans flags are not present'
    async def test_flag_none_present(self):
        nonePresent = False
        for flag in self.flags:
            if (flag.name is None) or (flag.default_alpha is None) or (flag.tooltip is None) or (flag.image is None):
                nonePresent = True
        assert nonePresent == False, 'A flag object contains an empty property'