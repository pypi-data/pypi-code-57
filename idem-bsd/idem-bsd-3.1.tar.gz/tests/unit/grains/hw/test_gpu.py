from dict_tools import data
import pytest
import mock

PCICONF_DATA = """
atapci0@pci0:0:1:1:     class=0x01018a card=0x00000000 chip=0x71118086 rev=0x01 hdr=0x00
    vendor     = 'Intel Corporation'
    device     = '82371AB/EB/MB PIIX4 IDE'
    class      = mass storage
    subclass   = ATA
vgapci0@pci0:0:2:0:     class=0x030000 card=0x040515ad chip=0x040515ad rev=0x00 hdr=0x00
    vendor     = 'VMware'
    device     = 'SVGA II Adapter'
    class      = display
    subclass   = VGA
em0@pci0:0:3:0: class=0x020000 card=0x001e8086 chip=0x100e8086 rev=0x02 hdr=0x00
    vendor     = 'Intel Corporation'
    device     = '82540EM Gigabit Ethernet Controller'
    class      = network
    subclass   = ethernet
"""

GLXINFO_DATA = """
name of display: :0
display: :0  screen: 0
direct rendering: Yes
Extended renderer info (GLX_MESA_query_renderer):
    Vendor: VMware, Inc. (0xffffffff)
    Device: llvmpipe (LLVM 8.0, 128 bits) (0xffffffff)
    Version: 18.3.2
    Accelerated: no
    Video memory: 8704MB
    Unified memory: no
    Preferred profile: core (0x1)
    Max core profile version: 3.3
    Max compat profile version: 3.1
    Max GLES1 profile version: 1.1
    Max GLES[23] profile version: 3.0
OpenGL vendor string: VMware, Inc.
OpenGL renderer string: llvmpipe (LLVM 8.0, 128 bits)
OpenGL core profile version string: 3.3 (Core Profile) Mesa 18.3.2
OpenGL core profile shading language version string: 3.30
OpenGL core profile context flags: (none)
OpenGL core profile profile mask: core profile

OpenGL version string: 3.1 Mesa 18.3.2
OpenGL shading language version string: 1.40
OpenGL context flags: (none)

OpenGL ES profile version string: OpenGL ES 3.0 Mesa 18.3.2
OpenGL ES profile shading language version string: OpenGL ES GLSL ES 3.00
"""

PCICTL_DATA = """
000:00:0: Intel Xeon E3-1200 v3 Host Bridge, DRAM (host bridge, revision 0x06)
000:01:0: Intel Haswell PCI-E x16 Controller (PCI bridge, revision 0x06)
000:01:1: Intel Haswell PCI-E x8 Controller (PCI bridge, revision 0x06)
000:20:0: Intel 8 Series USB xHCI (USB serial bus, xHCI, revision 0x05)
000:26:0: Intel 8 Series USB EHCI (USB serial bus, EHCI, revision 0x05)
000:28:0: Intel 8 Series PCIE (PCI bridge, revision 0xd5)
000:28:1: Intel 8 Series PCIE (PCI bridge, revision 0xd5)
000:28:2: Intel 8 Series PCIE (PCI bridge, revision 0xd5)
000:28:4: Intel 8 Series PCIE (PCI bridge, revision 0xd5)
000:29:0: Intel 8 Series USB EHCI (USB serial bus, EHCI, revision 0x05)
000:31:0: Intel C222 LPC (ISA bridge, revision 0x05)
000:31:2: Intel 8 Series (desktop) SATA Controller (AHCI) (SATA mass storage, AHCI 1.0, revision 0x05)
000:31:3: Intel 8 Series SMBus Controller (SMBus serial bus, revision 0x05)
000:31:6: Intel 8 Series Thermal (miscellaneous DASP, revision 0x05)
001:00:0: Intel 82599 (SFI/SFP+) 10 GbE Controller (ethernet network, revision 0x01)
002:00:0: Intel 6700PXH PCI Express-to-PCI Bridge #0 (PCI bridge, revision 0x09)
002:00:2: Intel 6700PXH PCI Express-to-PCI Bridge #1 (PCI bridge, revision 0x09)
005:00:0: ASPEED Technology AST1150 PCIe-to-PCI bridge (PCI bridge, revision 0x03)
006:00:0: ASPEED Technology ASPEED Graphics Family (VGA display, revision 0x30)
007:00:0: Intel I210-T1 Ethernet Server Adapter (ethernet network, revision 0x03)
008:00:0: Intel I210-T1 Ethernet Server Adapter (ethernet network, revision 0x03)
009:00:0: Intel PCIe NVMe SSD (Flash mass storage, NVMe, revision 0x01)
"""


@pytest.mark.asyncio
async def test_load_gpudata_pciconf(mock_hub, hub):
    mock_hub.exec.cmd.run.return_value = data.NamespaceDict(
        {"stdout": PCICONF_DATA, "retcode": 0}
    )

    with mock.patch("shutil.which", side_effect=[True, False, False]):
        mock_hub.grains.hw.gpu.load_gpudata = hub.grains.hw.gpu.load_gpudata
        await mock_hub.grains.hw.gpu.load_gpudata()

    assert mock_hub.grains.GRAINS.gpus == (
        {"model": "SVGA II Adapter", "vendor": "VMware"},
    )
    assert mock_hub.grains.GRAINS.num_gpus == 1


@pytest.mark.asyncio
async def test_load_gpudata_pciutil(mock_hub, hub):
    mock_hub.exec.cmd.run.return_value = data.NamespaceDict(
        {"stdout": PCICTL_DATA, "retcode": 0}
    )

    with mock.patch("shutil.which", side_effect=[False, True, False]):
        mock_hub.grains.hw.gpu.load_gpudata = hub.grains.hw.gpu.load_gpudata
        await mock_hub.grains.hw.gpu.load_gpudata()

    assert mock_hub.grains.GRAINS.gpus == (
        {"model": "Technology ASPEED Graphics Family", "vendor": "ASPEED"},
    )
    assert mock_hub.grains.GRAINS.num_gpus == 1


@pytest.mark.asyncio
async def test_load_gpudata_glxinfo(mock_hub, hub):
    mock_hub.exec.cmd.run.return_value = data.NamespaceDict(
        {"stdout": GLXINFO_DATA, "retcode": 0}
    )

    with mock.patch("shutil.which", side_effect=[False, False, True]):
        mock_hub.grains.hw.gpu.load_gpudata = hub.grains.hw.gpu.load_gpudata
        await mock_hub.grains.hw.gpu.load_gpudata()

    assert mock_hub.grains.GRAINS.gpus == (
        {"model": " llvmpipe (LLVM 8.0, 128 bits)", "vendor": " VMware, Inc."},
    )
    assert mock_hub.grains.GRAINS.num_gpus == 1


@pytest.mark.asyncio
async def test_load_gpudata(mock_hub, hub):
    with mock.patch("shutil.which", side_effect=[False, False, False]):
        mock_hub.grains.hw.gpu.load_gpudata = hub.grains.hw.gpu.load_gpudata
        await mock_hub.grains.hw.gpu.load_gpudata()

    assert mock_hub.grains.GRAINS.gpus == ()
    assert mock_hub.grains.GRAINS.num_gpus == 0
