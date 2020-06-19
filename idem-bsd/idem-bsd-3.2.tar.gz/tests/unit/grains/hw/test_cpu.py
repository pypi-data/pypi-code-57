from dict_tools import data
import io
import pytest
import mock

CPUTIL_DATA = """
cpu0: features FOO<SVM,3DNOWPREFETCH,WDT>
cpu1: features1 BAR<VME,VMMCALL,TACO>
"""

DMESG_BOOT_DATA = """
---<<BOOT>>---
Copyright (c) 1992-2020 The FreeBSD Project.
Copyright (c) 1979, 1980, 1983, 1986, 1988, 1989, 1991, 1992, 1993, 1994
        The Regents of the University of California. All rights reserved.
FreeBSD is a registered trademark of The FreeBSD Foundation.
FreeBSD 12.1-STABLE GENERIC amd64
FreeBSD clang version 9.0.1 (git@github.com:llvm/llvm-project.git c1a0a213378a458fbea1a5c77b315c7dce08fd05) (based on LLVM 9.0.1)
VT(vga): text 80x25
CPU: AMD Ryzen 7 2700X Eight-Core Processor          (3700.09-MHz K8-class CPU)
  Origin="AuthenticAMD"  Id=0x800f82  Family=0x17  Model=0x8  Stepping=2
  Features=0x1783fbff<SVM,3DNOWPREFETCH,WDT>
  Features2=0x5ed82203<VME,VMMCALL>
  AMD Features=0x2a500800<TACO,SALAD>
  AMD Features2=0x1f3<ONE,TWO,THREE>
  Structured Extended Features=0x840021<FOUR,FIVE,SIX>
  TSC: P-state invariant
real memory  = 9126805504 (8704 MB)
avail memory = 8276000768 (7892 MB)
random: unblocking device.
arc4random: no preloaded entropy cache
arc4random: no preloaded entropy cache
arc4random: no preloaded entropy cache
arc4random: no preloaded entropy cache
arc4random: no preloaded entropy cache
Cuse v0.1.36 @ /dev/cuse
lo0: link state changed to UP
uhub0: 12 ports with 12 removable, self powered
em0: link state changed to UP
"""


@pytest.mark.asyncio
async def test_load_cpu_arch_sysctl(mock_hub, hub):
    mock_hub.exec.cmd.run.return_value = data.NamespaceDict(
        {"stdout": "testarch", "retcode": 0}
    )

    with mock.patch("shutil.which", side_effect=[True, False]):
        mock_hub.grains.hw.cpu.load_cpu_arch = hub.grains.hw.cpu.load_cpu_arch
        await mock_hub.grains.hw.cpu.load_cpu_arch()

    assert mock_hub.grains.GRAINS.cpuarch == "testarch"


@pytest.mark.asyncio
async def test_load_cpu_arch_arch(mock_hub, hub):
    mock_hub.exec.cmd.run.return_value = data.NamespaceDict(
        {"stdout": "testarch", "retcode": 0}
    )

    with mock.patch("shutil.which", side_effect=[False, True]):
        mock_hub.grains.hw.cpu.load_cpu_arch = hub.grains.hw.cpu.load_cpu_arch
        await mock_hub.grains.hw.cpu.load_cpu_arch()

    assert mock_hub.grains.GRAINS.cpuarch == "testarch"


@pytest.mark.asyncio
async def test_load_cpu_arch(mock_hub, hub):
    mock_hub.grains.GRAINS.osarch = "testarch"

    with mock.patch("shutil.which", side_effect=[False, False]):
        mock_hub.grains.hw.cpu.load_cpu_arch = hub.grains.hw.cpu.load_cpu_arch
        await mock_hub.grains.hw.cpu.load_cpu_arch()

    assert mock_hub.grains.GRAINS.cpuarch == "testarch"


@pytest.mark.asyncio
async def test_load_cpu_flags_cputil(mock_hub, hub):
    mock_hub.exec.cmd.run.return_value = data.NamespaceDict({"stdout": CPUTIL_DATA})

    with mock.patch("shutil.which", return_value=True):
        with mock.patch("os.path.isfile", return_value=False):
            mock_hub.grains.hw.cpu.load_cpu_flags = hub.grains.hw.cpu.load_cpu_flags
            await mock_hub.grains.hw.cpu.load_cpu_flags()

    assert mock_hub.grains.GRAINS.cpu_flags == (
        "3dnowprefetch",
        "svm",
        "taco",
        "vme",
        "vmmcall",
        "wdt",
    )
    assert mock_hub.grains.GRAINS.hardware_virtualization is True


@pytest.mark.asyncio
async def test_load_cpu_flags_dmesg(mock_hub, hub):
    with mock.patch("shutil.which", return_value=False):
        with mock.patch("os.path.exists", return_value=True):
            with mock.patch(
                "aiofiles.threadpool.sync_open",
                return_value=io.StringIO(DMESG_BOOT_DATA),
            ):
                mock_hub.grains.hw.cpu.load_cpu_flags = hub.grains.hw.cpu.load_cpu_flags
                await mock_hub.grains.hw.cpu.load_cpu_flags()

    assert mock_hub.grains.GRAINS.cpu_flags == (
        "3dnowprefetch",
        "five",
        "four",
        "one",
        "salad",
        "six",
        "svm",
        "taco",
        "three",
        "two",
        "vme",
        "vmmcall",
        "wdt",
    )
    assert mock_hub.grains.GRAINS.hardware_virtualization is True


@pytest.mark.asyncio
async def test_load_cpu_flags(mock_hub, hub):
    with mock.patch("shutil.which", return_value=False):
        with mock.patch("os.path.exists", return_value=False):
            mock_hub.grains.hw.cpu.load_cpu_flags = hub.grains.hw.cpu.load_cpu_flags
            await mock_hub.grains.hw.cpu.load_cpu_flags()

    assert mock_hub.grains.GRAINS.cpu_flags == tuple()
    assert mock_hub.grains.GRAINS.hardware_virtualization is False


@pytest.mark.asyncio
async def test_load_cpu_model(mock_hub, hub):
    mock_hub.exec.cmd.run.return_value = data.NamespaceDict(
        {"stdout": "test_model", "retcode": 0}
    )

    with mock.patch("shutil.which", return_value=True):
        mock_hub.grains.hw.cpu.load_cpu_model = hub.grains.hw.cpu.load_cpu_model
        await mock_hub.grains.hw.cpu.load_cpu_model()

    assert mock_hub.grains.GRAINS.cpu_model == "test_model"


@pytest.mark.asyncio
async def test_load_num_cpus(mock_hub, hub):
    mock_hub.exec.cmd.run.return_value = data.NamespaceDict(
        {"stdout": "234", "retcode": 0}
    )

    with mock.patch("shutil.which", return_value=True):
        mock_hub.grains.hw.cpu.load_num_cpus = hub.grains.hw.cpu.load_num_cpus
        await mock_hub.grains.hw.cpu.load_num_cpus()

    assert mock_hub.grains.GRAINS.num_cpus == 234


@pytest.mark.asyncio
async def test_load_num_cpus_default(mock_hub, hub):
    with mock.patch("shutil.which", return_value=False):
        mock_hub.grains.hw.cpu.load_num_cpus = hub.grains.hw.cpu.load_num_cpus
        await mock_hub.grains.hw.cpu.load_num_cpus()

    assert mock_hub.grains.GRAINS.num_cpus == 1
