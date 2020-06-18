import aiofiles
import os


async def load_cpuinfo(hub):
    num_cpus = 0
    cpu_model = "Unknown"
    cpu_flags = []

    cpuinfo = "/proc/cpuinfo"
    if os.path.isfile(cpuinfo):
        # Parse over the cpuinfo file
        async with aiofiles.open(cpuinfo, "r") as _fp:
            async for line in _fp:
                comps = line.split(":")
                if not len(comps) > 1:
                    continue
                key = comps[0].strip()
                val = comps[1].strip()
                if key == "processor":
                    num_cpus = int(val) + 1
                # head -2 /proc/cpuinfo
                # vendor_id       : IBM/S390
                # # processors    : 2
                elif key == "# processors":
                    num_cpus = int(val)
                elif key == "vendor_id":
                    cpu_model = val
                elif key == "model name":
                    cpu_model = val
                elif key == "flags":
                    cpu_flags = sorted(val.split())
                elif key == "Features":
                    cpu_flags = sorted(val.split())
                # ARM support - /proc/cpuinfo
                #
                # Processor       : ARMv6-compatible processor rev 7 (v6l)
                # BogoMIPS        : 697.95
                # Features        : swp half thumb fastmult vfp edsp java tls
                # CPU implementer : 0x41
                # CPU architecture: 7
                # CPU variant     : 0x0
                # CPU part        : 0xb76
                # CPU revision    : 7
                #
                # Hardware        : BCM2708
                # Revision        : 0002
                # Serial          : 00000000
                elif key == "Processor":
                    cpu_model = val.split("-")[0]
                    num_cpus = 1

        hub.grains.GRAINS.num_cpus = num_cpus
        hub.grains.GRAINS.cpu_model = cpu_model

    hub.grains.GRAINS.cpu_flags = sorted(cpu_flags)

    # Report if hardware virtualization is available under amd or intel
    hub.grains.GRAINS.hardware_virtualization = any(
        f in hub.grains.GRAINS.cpu_flags for f in ("svm", "vmx")
    )
