import re
import shutil


async def load_hwdata(hub):
    sysctl = shutil.which("sysctl")

    value = (await hub.exec.cmd.run([sysctl, "-n", "hw.model"])).stdout.strip()
    if not value.endswith(" is invalid"):
        hub.grains.GRAINS.productname = await hub.grains.init.clean_value(
            "productname", value
        )
