import re
import shutil
from typing import Dict, List


KNOWN_VENDORS = [
    "nvidia",
    "amd",
    "ati",
    "intel",
    "cirrus logic",
    "vmware",
    "matrox",
    "aspeed",
]


async def _load_lspci(hub) -> List[Dict[str, str]]:
    gpus = []

    lspci = shutil.which("lspci")
    if lspci:
        # dominant gpu vendors to search for (MUST be lowercase for matching below)
        gpu_classes = ("vga compatible controller", "3d controller")

        devs = []
        try:
            lspci_out = (await hub.exec.cmd.run(f"{lspci} -vmm")).stdout

            cur_dev = {}
            error = False
            # Add a blank element to the lspci_out.splitlines() list,
            # otherwise the last device is not evaluated as a cur_dev and ignored.
            lspci_list = lspci_out.splitlines()
            lspci_list.append("")
            for line in lspci_list:
                # check for record-separating empty lines
                if line == "":
                    if cur_dev.get("Class", "").lower() in gpu_classes:
                        devs.append(cur_dev)
                    cur_dev = {}
                    continue
                if re.match(r"^\w+:\s+.*", line):
                    key, val = line.split(":", 1)
                    cur_dev[key.strip()] = val.strip()
                else:
                    error = True
                    hub.log.debug("Unexpected lspci output: '%s'", line)

            if error:
                hub.log.warning(
                    "Error loading grains, unexpected linux_gpu_data output, "
                    "check that you have a valid shell configured and "
                    "permissions to run lspci command"
                )
        except OSError:
            pass

        for gpu in devs:
            vendor_strings = gpu["Vendor"].lower().split()
            # default vendor to 'unknown', overwrite if we match a known one
            vendor = "unknown"
            for name in KNOWN_VENDORS:
                # search for an 'expected' vendor name in the list of strings
                if name in vendor_strings:
                    vendor = name
                    break
            gpus.append({"model": gpu["Device"], "vendor": vendor})

    return gpus


async def _load_glxinfo(hub) -> List[Dict[str, str]]:
    """Mesa library for detecting gpu info"""
    gpus = []
    glxinfo = shutil.which("glxinfo")
    if glxinfo:
        ret = await hub.exec.cmd.run([glxinfo, "-B"])
        if not ret.retcode:
            for line in ret.stdout.splitlines():
                if "Device:" in line:
                    gpus.append(
                        {
                            "model": line.split(":")[1].split("(")[0].strip(),
                            "vendor": "unknown",
                        }
                    )
    return gpus


async def load_gpudata(hub):
    hub.grains.GRAINS.gpus = await _load_lspci(hub) or await _load_glxinfo(hub)
    hub.grains.GRAINS.num_gpus = len(hub.grains.GRAINS.gpus)
