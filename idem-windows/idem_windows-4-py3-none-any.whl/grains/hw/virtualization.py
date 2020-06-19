async def load_hw_virt_enabled(hub):
    """
    Find out if hardware virtualization is enabled for the CPU
    """
    hub.grains.GRAINS.hardware_virtualization = await hub.exec.wmi.get(
        "Win32_Processor", 0, "VirtualizationFirmwareEnabled"
    )
