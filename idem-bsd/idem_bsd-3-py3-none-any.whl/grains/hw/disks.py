import logging
import re
import shutil
from typing import Any, Dict, List, Tuple

log = logging.getLogger(__name__)


class GEOM:
    GEOMNAME = "Geom name"
    MEDIASIZE = "Mediasize"
    SECTORSIZE = "Sectorsize"
    STRIPESIZE = "Stripesize"
    STRIPEOFFSET = "Stripeoffset"
    DESCR = "descr"  # model
    LUNID = "lunid"
    LUNNAME = "lunname"
    IDENT = "ident"  # serial
    ROTATIONRATE = "rotationrate"  # RPM or 0 for non-rotating

    # Preserve the API where possible with Salt < 2016.3
    _aliases = {
        DESCR: "device_model",
        IDENT: "serial_number",
        ROTATIONRATE: "media_RPM",
        LUNID: "WWN",
    }

    _datatypes = {
        MEDIASIZE: ("re_int", r"(\d+)"),
        SECTORSIZE: "try_int",
        STRIPESIZE: "try_int",
        STRIPEOFFSET: "try_int",
        ROTATIONRATE: "try_int",
    }


_geom_attribs = [GEOM.__dict__[key] for key in GEOM.__dict__ if not key.startswith("_")]


def _datavalue(datatype, data):
    if datatype == "try_int":
        try:
            return int(data)
        except ValueError:
            return None
    elif datatype is tuple and datatype[0] == "re_int":
        search = re.search(datatype[1], data)
        if search:
            try:
                return int(search.group(1))
            except ValueError:
                return None
        return None
    else:
        return data


async def _parse_geom_attribs(device: str) -> Tuple[Dict[str, Any], List[str]]:
    disks = {}
    ssds = []
    tmp = {}
    for line in device.split("\n"):
        for attrib in _geom_attribs:
            search = re.search(fr"{attrib}:\s(.*)", line)
            if search:
                value = _datavalue(GEOM._datatypes.get(attrib), search.group(1))
                tmp[attrib] = value
                if attrib in GEOM._aliases:
                    tmp[GEOM._aliases[attrib]] = value

    name = tmp.pop(GEOM.GEOMNAME)
    if not name.startswith("cd"):
        disks[name] = tmp
        if not tmp.get(GEOM.ROTATIONRATE):
            log.debug("Device %s reports itself as an SSD", device)
            ssds.append(name)

    return disks, ssds


async def load_disks(hub):
    """
    Return list of disk devices and work out if they are SSD or HDD.
    """
    ssds = []
    disks = {}

    geom = shutil.which("geom")
    if geom:
        devices = (
            (await hub.exec.cmd.run([geom, "disk", "list"]))
            .stdout.strip()
            .split("\n\n")
        )
        for device in devices:
            d, s = await _parse_geom_attribs(device)
            disks.update(d)
            ssds.extend(s)

    if ssds:
        hub.grains.GRAINS.SSDs = sorted(ssds)
    if disks:
        # This should be a list like it is on every other OS
        # It should also only contain rotational disks like every other OS
        hub.grains.GRAINS.disks = sorted(set(disks) - set(ssds))
