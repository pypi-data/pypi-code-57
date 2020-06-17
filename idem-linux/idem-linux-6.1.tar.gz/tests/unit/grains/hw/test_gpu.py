import idem_linux.grains.hw.gpu
import pytest
import shutil
import mock
from dict_tools import data

LSPCI_DATA = """
Slot:	00:00.0
Class:	Host bridge
Vendor:	Intel Corporation
Device:	8th Gen Core Processor Host Bridge/DRAM Registers
SVendor:	Dell
SDevice:	8th Gen Core Processor Host Bridge/DRAM Registers
Rev:	07

Slot:	00:01.0
Class:	PCI bridge
Vendor:	Intel Corporation
Device:	Xeon E3-1200 v5/E3-1500 v5/6th Gen Core Processor PCIe Controller (x16)
Rev:	07

Slot:	00:02.0
Class:	VGA compatible controller
Vendor:	Intel Corporation
Device:	UHD Graphics 630 (Mobile)
SVendor:	Dell
SDevice:	UHD Graphics 630 (Mobile)

Slot:	00:04.0
Class:	Signal processing controller
Vendor:	Intel Corporation
Device:	Xeon E3-1200 v5/E3-1500 v5/6th Gen Core Processor Thermal Subsystem
SVendor:	Dell
SDevice:	Xeon E3-1200 v5/E3-1500 v5/6th Gen Core Processor Thermal Subsystem
Rev:	07

Slot:	00:08.0
Class:	System peripheral
Vendor:	Intel Corporation
Device:	Xeon E3-1200 v5/v6 / E3-1500 v5 / 6th/7th/8th Gen Core Processor Gaussian Mixture Model
SVendor:	Dell
SDevice:	Xeon E3-1200 v5/v6 / E3-1500 v5 / 6th/7th/8th Gen Core Processor Gaussian Mixture Model

Slot:	00:12.0
Class:	Signal processing controller
Vendor:	Intel Corporation
Device:	Cannon Lake PCH Thermal Controller
SVendor:	Dell
SDevice:	Cannon Lake PCH Thermal Controller
Rev:	10

Slot:	00:14.0
Class:	USB controller
Vendor:	Intel Corporation
Device:	Cannon Lake PCH USB 3.1 xHCI Host Controller
SVendor:	Dell
SDevice:	Cannon Lake PCH USB 3.1 xHCI Host Controller
Rev:	10
ProgIf:	30

Slot:	00:14.2
Class:	RAM memory
Vendor:	Intel Corporation
Device:	Cannon Lake PCH Shared SRAM
SVendor:	Dell
SDevice:	Cannon Lake PCH Shared SRAM
Rev:	10

Slot:	00:15.0
Class:	Serial bus controller [0c80]
Vendor:	Intel Corporation
Device:	Cannon Lake PCH Serial IO I2C Controller #0
SVendor:	Dell
SDevice:	Cannon Lake PCH Serial IO I2C Controller
Rev:	10

Slot:	00:15.1
Class:	Serial bus controller [0c80]
Vendor:	Intel Corporation
Device:	Cannon Lake PCH Serial IO I2C Controller #1
SVendor:	Dell
SDevice:	Cannon Lake PCH Serial IO I2C Controller
Rev:	10

Slot:	00:16.0
Class:	Communication controller
Vendor:	Intel Corporation
Device:	Cannon Lake PCH HECI Controller
SVendor:	Dell
SDevice:	Cannon Lake PCH HECI Controller
Rev:	10

Slot:	00:17.0
Class:	SATA controller
Vendor:	Intel Corporation
Device:	Cannon Lake Mobile PCH SATA AHCI Controller
SVendor:	Dell
SDevice:	Cannon Lake Mobile PCH SATA AHCI Controller
Rev:	10
ProgIf:	01

Slot:	00:1b.0
Class:	PCI bridge
Vendor:	Intel Corporation
Device:	Cannon Lake PCH PCI Express Root Port #17
Rev:	f0

Slot:	00:1c.0
Class:	PCI bridge
Vendor:	Intel Corporation
Device:	Cannon Lake PCH PCI Express Root Port #1
Rev:	f0

Slot:	00:1c.4
Class:	PCI bridge
Vendor:	Intel Corporation
Device:	Cannon Lake PCH PCI Express Root Port #5
Rev:	f0

Slot:	00:1d.0
Class:	PCI bridge
Vendor:	Intel Corporation
Device:	Cannon Lake PCH PCI Express Root Port #9
Rev:	f0

Slot:	00:1f.0
Class:	ISA bridge
Vendor:	Intel Corporation
Device:	Device a30e
SVendor:	Dell
SDevice:	Device 087c
Rev:	10

Slot:	00:1f.3
Class:	Audio device
Vendor:	Intel Corporation
Device:	Cannon Lake PCH cAVS
SVendor:	Dell
SDevice:	Cannon Lake PCH cAVS
Rev:	10
ProgIf:	80

Slot:	00:1f.4
Class:	SMBus
Vendor:	Intel Corporation
Device:	Cannon Lake PCH SMBus Controller
SVendor:	Dell
SDevice:	Cannon Lake PCH SMBus Controller
Rev:	10

Slot:	00:1f.5
Class:	Serial bus controller [0c80]
Vendor:	Intel Corporation
Device:	Cannon Lake PCH SPI Controller
SVendor:	Dell
SDevice:	Cannon Lake PCH SPI Controller
Rev:	10

Slot:	01:00.0
Class:	3D controller
Vendor:	NVIDIA Corporation
Device:	GP107M [GeForce GTX 1050 Ti Mobile]
Rev:	ff
ProgIf:	ff

Slot:	3b:00.0
Class:	Network controller
Vendor:	Qualcomm Atheros
Device:	QCA6174 802.11ac Wireless Network Adapter
SVendor:	Bigfoot Networks, Inc.
SDevice:	QCA6174 802.11ac Wireless Network Adapter
Rev:	32

Slot:	3c:00.0
Class:	Unassigned class [ff00]
Vendor:	Realtek Semiconductor Co., Ltd.
Device:	RTS525A PCI Express Card Reader
SVendor:	Dell
SDevice:	RTS525A PCI Express Card Reader
Rev:	01

Slot:	3d:00.0
Class:	Non-Volatile memory controller
Vendor:	Toshiba Corporation
Device:	Device 011a
SVendor:	Toshiba Corporation
SDevice:	Device 0001
ProgIf:	02
NUMANode:	0
"""


@pytest.mark.asyncio
async def test_load_lspci(mock_hub):
    mock_hub.exec.cmd.run.return_value = data.NamespaceDict({"stdout": LSPCI_DATA})

    with mock.patch.object(shutil, "which", return_value=True):
        await idem_linux.grains.hw.gpu.load_gpudata(mock_hub)

    assert mock_hub.grains.GRAINS.gpus == (
        {"model": "UHD Graphics 630 (Mobile)", "vendor": "intel"},
        {"model": "GP107M [GeForce GTX 1050 Ti Mobile]", "vendor": "nvidia"},
    )
    assert mock_hub.grains.GRAINS.num_gpus == 2
