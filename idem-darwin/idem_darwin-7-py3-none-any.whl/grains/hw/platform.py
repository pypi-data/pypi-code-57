async def load_profiler(hub):
    """
    Additional data for macOS systems
    Returns: A dictionary containing values for the following:
        - model_name
        - boot_rom_version
        - smc_version
        - serialnumber
    """
    hardware = (
        await hub.exec.cmd.run(["system_profiler", "SPHardwareDataType"])
    ).stdout.strip()
    for line in hardware.splitlines():
        field_name, _, field_val = line.partition(": ")
        if field_name.strip() == "Model Name":
            key = "model_name"
        elif field_name.strip() == "Boot ROM Version":
            key = "boot_rom_version"
        elif field_name.strip() == "SMC Version (system)":
            key = "smc_version"
        elif field_name.strip() == "Serial Number (system)":
            key = "serialnumber"
        else:
            key = None
        if key:
            hub.grains.GRAINS[key] = await hub.grains.init.clean_value(key, field_val)
