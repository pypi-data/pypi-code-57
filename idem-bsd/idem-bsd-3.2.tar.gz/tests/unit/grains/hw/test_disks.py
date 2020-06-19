from dict_tools import data
import pytest
import mock

GEOM_DATA = """
Geom name: ada0
Providers:
1. Name: ada0
   Mediasize: 8001563222016 (7.3T)
   Sectorsize: 512
   Stripesize: 4096
   Stripeoffset: 0
   Mode: r0w0e0
   descr: ST8000DM004-2CX188
   lunid: 5000c500bf190722
   ident: WCT1BC9M
   rotationrate: 5425
   fwsectors: 63
   fwheads: 16

Geom name: ada1
Providers:
1. Name: ada1
   Mediasize: 8001563222016 (7.3T)
   Sectorsize: 512
   Stripesize: 4096
   Stripeoffset: 0
   Mode: r0w0e0
   descr: ST8000DM004-2CX188
   lunid: 5000c500b47391c8
   ident: ZCT0LDX1
   rotationrate: 5425
   fwsectors: 63
   fwheads: 16

Geom name: ada2
Providers:
1. Name: ada2
   Mediasize: 1000204886016 (932G)
   Sectorsize: 512
   Mode: r0w0e0
   descr: WDC WD10EACS-00D6B0
   lunid: 50014ee201badced
   ident: WD-WCAU41052079
   rotationrate: unknown
   fwsectors: 63
   fwheads: 16

Geom name: ada3
Providers:
1. Name: ada3
   Mediasize: 1000204886016 (932G)
   Sectorsize: 512
   Mode: r0w0e0
   descr: ST31000528AS
   lunid: 5000c5003ecd83c1
   ident: 9VPDXRPV
   rotationrate: 7200
   fwsectors: 63
   fwheads: 16

Geom name: ada4
Providers:
1. Name: ada4 (Boot drive)
   Mediasize: 160041885696 (149G)
   Sectorsize: 512
   Mode: r1w1e2
   descr: ST3160815AS
   ident: 5RA9Y4HX
   rotationrate: unknown
   fwsectors: 63
   fwheads: 16
"""


@pytest.mark.asyncio
async def test_load_disks(mock_hub, hub):
    mock_hub.exec.cmd.run.return_value = data.NamespaceDict({"stdout": GEOM_DATA})

    with mock.patch("shutil.which", return_value=True):
        mock_hub.grains.hw.disks.load_disks = hub.grains.hw.disks.load_disks
        await mock_hub.grains.hw.disks.load_disks()

    assert mock_hub.grains.GRAINS.disks == ("ada0", "ada1", "ada3")
    assert mock_hub.grains.GRAINS.SSDs == ("ada2", "ada4")
