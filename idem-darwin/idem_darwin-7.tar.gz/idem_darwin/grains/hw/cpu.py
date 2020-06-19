import shutil


async def load_num_cpus(hub):
    sysctl = shutil.which("sysctl")
    if sysctl:
        hub.grains.GRAINS.num_cpus = int(
            (await hub.exec.cmd.run([sysctl, "-n", "hw.ncpu"])).stdout.strip()
        )


async def load_cpu_arch(hub):
    sysctl = shutil.which("sysctl")
    if sysctl:
        hub.grains.GRAINS.cpuarch = (
            await hub.exec.cmd.run([sysctl, "-n", "hw.machine"])
        ).stdout.strip()


async def load_cpu_model(hub):
    sysctl = shutil.which("sysctl")
    if sysctl:
        hub.grains.GRAINS.cpu_model = (
            await hub.exec.cmd.run([sysctl, "-n", "machdep.cpu.brand_string"])
        ).stdout


async def load_cpu_flags(hub):
    sysctl = shutil.which("sysctl")
    if sysctl:
        hub.grains.GRAINS.cpu_flags = sorted(
            (await hub.exec.cmd.run([sysctl, "-n", "machdep.cpu.features"]))
            .stdout.strip()
            .lower()
            .split(" ")
        )

        # Report if hardware visualization is available under amd or intel
        hub.grains.GRAINS.hardware_virtualization = bool(
            {"svm", "vmx"} - set(hub.grains.GRAINS.cpu_flags)
        )
