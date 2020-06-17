import idem_linux.grains.hw.proc.mem
import io
import os.path
import pytest
import mock

PROC_DATA = """
MemTotal:       32516664 kB
MemFree:        22083944 kB
MemAvailable:   26204512 kB
Buffers:          521160 kB
Cached:          4902056 kB
SwapCached:            0 kB
Active:          5863208 kB
Inactive:        2799936 kB
Active(anon):    4147624 kB
Inactive(anon):   408408 kB
Active(file):    1715584 kB
Inactive(file):  2391528 kB
Unevictable:      939552 kB
Mlocked:              64 kB
SwapTotal:    9999999999 kB
SwapFree:              0 kB
Dirty:             50944 kB
Writeback:             0 kB
AnonPages:       4179584 kB
Mapped:          1381124 kB
Shmem:           1384168 kB
KReclaimable:     482260 kB
Slab:             640464 kB
SReclaimable:     482260 kB
SUnreclaim:       158204 kB
KernelStack:       15280 kB
PageTables:        35588 kB
NFS_Unstable:          0 kB
Bounce:                0 kB
WritebackTmp:          0 kB
CommitLimit:    16258332 kB
Committed_AS:   10456304 kB
VmallocTotal:   34359738367 kB
VmallocUsed:       36660 kB
VmallocChunk:          0 kB
Percpu:            10176 kB
HardwareCorrupted:     0 kB
AnonHugePages:     86016 kB
ShmemHugePages:        0 kB
ShmemPmdMapped:        0 kB
FileHugePages:         0 kB
FilePmdMapped:         0 kB
HugePages_Total:       0
HugePages_Free:        0
HugePages_Rsvd:        0
HugePages_Surp:        0
Hugepagesize:       2048 kB
Hugetlb:               0 kB
DirectMap4k:      281992 kB
DirectMap2M:     7733248 kB
DirectMap1G:    25165824 kB
"""


@pytest.mark.asyncio
async def test_load_meminfo(mock_hub):
    with mock.patch.object(os.path, "isfile", return_value=True) and mock.patch(
        "aiofiles.threadpool.sync_open", return_value=io.StringIO(PROC_DATA)
    ):
        await idem_linux.grains.hw.proc.mem.load_meminfo(mock_hub)

    assert mock_hub.grains.GRAINS.mem_total == 31754
    assert mock_hub.grains.GRAINS.swap_total == 9765624
