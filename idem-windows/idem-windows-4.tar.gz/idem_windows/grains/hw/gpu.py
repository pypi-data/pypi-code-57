async def load_gpu_data(hub):
    gpus = []
    for gpuinfo in await hub.exec.wmi.get("Win32_VideoController"):
        gpus.append({"model": gpuinfo.Name, "vendor": gpuinfo.AdapterCompatibility})

    hub.grains.GRAINS.gpus = gpus
    hub.grains.GRAINS.num_gpus = len(gpus)
