import re
import shutil


async def load_gpudata(hub):
    gpus = []

    lshw = shutil.which("lshw")
    if lshw:
        ret = await hub.exec.cmd.run([lshw, "-class", "display"])
        match = re.findall("product:\s+(.*)\s+vendor:\s+(.*)", ret.stdout)
        for m in match:
            gpus.append({"model": m[0], "vendor": m[1]})

    hub.grains.GRAINS.gpus = gpus
    hub.grains.GRAINS.num_gpus = len(hub.grains.GRAINS.gpus)
