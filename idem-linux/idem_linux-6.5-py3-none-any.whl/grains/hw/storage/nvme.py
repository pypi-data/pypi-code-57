# -*- coding: utf-8 -*-
"""
Grains for NVMe Qualified Names (NQN).
"""
import aiofiles
import errno

import os


async def load_nvme_nqn(hub):
    """
    Return NVMe NQN from a Linux host.
    """
    nvme_nqn = []

    initiator = "/etc/nvme/hostnqn"
    if os.path.exists(initiator):
        try:
            async with aiofiles.open(initiator, "r") as _nvme:
                async for line in _nvme:
                    line = line.strip()
                    if line.startswith("nqn."):
                        nvme_nqn.append(line)
        except IOError as ex:
            if ex.errno != errno.ENOENT:
                hub.log.debug(f"Error while accessing '{initiator}': {ex}")

    if nvme_nqn:
        hub.grains.GRAINS.nvme_nqn = nvme_nqn
