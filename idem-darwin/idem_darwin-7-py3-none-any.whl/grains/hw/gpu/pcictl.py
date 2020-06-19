import shutil


async def load_data(hub):
    """
    num_gpus: int
    gpus:
      - vendor: nvidia|amd|ati|...
        model: string
    """
    gpus = []

    system_profiler = shutil.which("system_profiler")
    if system_profiler:
        try:
            pcictl_out = (
                await hub.exec.cmd.run([system_profiler, "SPDisplaysDataType"])
            ).stdout.strip()
            for line in pcictl_out.splitlines():
                fieldname, _, fieldval = line.partition(": ")
                if fieldname.strip() == "Chipset Model":
                    vendor, _, model = fieldval.partition(" ")
                    gpus.append({"model": model, "vendor": vendor.lower()})
        except OSError:
            pass

    hub.grains.GRAINS.gpus = gpus
    hub.grains.GRAINS.num_gpus = len(gpus)
