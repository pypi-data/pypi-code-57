# This is going to be a monster, if you are running a vm you can test this
# grain with please submit patches!
# Provides:
#   virtual
#   virtual_subtype
import aiofiles
import enum
import re
import shutil
import os


class XenFeatures(enum.IntEnum):
    """
    Try to read and decode the supported feature set of the hypervisor
    Based on https://github.com/brendangregg/Misc/blob/master/xen/xen-features.py
    Table data from include/xen/interface/features.h
    """

    writable_page_tables = 0
    writable_descriptor_tables = 1
    auto_translated_physmap = 2
    supervisor_mode_kernel = 3
    pae_pgdir_above_4gb = 4
    mmu_pt_update_preserve_ad = 5

    gnttab_map_avail_bits = 7
    hvm_callback_vector = 8
    hvm_safe_pvclock = 9
    hvm_pirqs = 10
    dom0 = 11
    grant_map_identity = 12
    memory_op_vnode_supported = 13
    ARM_SMCCC_supported = 14


async def _load_virtual_hypervisor_version(hub):
    """
    Returns detailed hypervisor information from sysfs
    Currently this seems to be used only by Xen
    """
    # Try to get the exact hypervisor version from sysfs
    try:
        version = {}
        for fn in ("major", "minor", "extra"):
            version_path = f"/sys/hypervisor/version/{fn}"
            if os.path.exists(version_path):
                async with aiofiles.open(version_path, "r") as fhr:
                    version[fn] = (await fhr.read()).strip()
        hub.grains.GRAINS.virtual_hv_version = (
            f"{version['major']}.{version['minor']}{version['extra']}"
        )
        hub.grains.GRAINS.virtual_hv_version_info = [
            version["major"],
            version["minor"],
            version["extra"],
        ]
    except (IOError, OSError, KeyError):
        pass


async def _load_virtual_hypervisor_features(hub):
    features_path = "/sys/hypervisor/properties/features"
    if os.path.exists(features_path):
        try:
            enabled_features = []
            async with aiofiles.open(features_path, "r") as fhr:
                features = (await fhr.read()).strip()
                hub.grains.GRAINS.virtual_hv_features = features
                for feature in XenFeatures:
                    if int(features, 16) & (1 << feature.value):
                        enabled_features.append(feature.name)
            hub.grains.GRAINS.virtual_hv_features_list = enabled_features
        except (IOError, OSError, KeyError):
            pass


async def _virt_dmidecode(hub) -> str:
    command = shutil.which("dmidecode")
    if command:
        ret = await hub.exec.cmd.run([command])
        if ret.retcode:
            hub.log.info(
                "Although '%s' was found in path, the current user "
                "cannot execute it. Grains output might not be "
                "accurate.",
                command,
            )
        elif "Vendor: QEMU" in ret.stdout:
            # Product Name: VirtualBox
            # FIXME: Make this detect between kvm or qemu
            return "kvm"
        elif "Manufacturer: QEMU" in ret.stdout:
            return "kvm"
        elif "Vendor: Bochs" in ret.stdout:
            return "kvm"
        elif "Manufacturer: Bochs" in ret.stdout:
            return "kvm"
        elif "BHYVE" in ret.stdout:
            return "bhyve"
        elif "Manufacturer: oVirt" in ret.stdout:
            # Product Name: (oVirt) www.ovirt.org
            # Red Hat Community virtualization Project based on kvm
            hub.grains.GRAINS.virtual_subtype = "ovirt"
            return "kvm"
        elif "Product Name: RHEV Hypervisor" in ret.stdout:
            # Red Hat Enterprise Virtualization
            hub.grains.GRAINS.virtual_subtype = "rhev"
            return "kvm"
        elif "VirtualBox" in ret.stdout:
            return "VirtualBox"
        elif "VMware" in ret.stdout:
            # Product Name: VMware Virtual Platform
            return "VMware"
        elif ": Microsoft" in ret.stdout and "Virtual Machine" in ret.stdout:
            # Manufacturer: Microsoft Corporation
            # Product Name: Virtual Machine
            return "VirtualPC"
        elif "Parallels Software" in ret.stdout:
            # Manufacturer: Parallels Software International Inc.
            return "Parallels"
        elif "Manufacturer: Google" in ret.stdout:
            return "kvm"
        elif "Vendor: SeaBIOS" in ret.stdout:
            # Proxmox KVM
            return "kvm"


async def _virt_lspci(hub) -> str:
    # Check if enable_lspci is True or False
    # TODO add this to the right place in opts, where is that?
    if hub.OPT.get("enable_lspci") is True and os.path.exists("/proc/bus/pci"):
        # /proc/bus/pci does not exists, lspci will fail
        command = shutil.which("lspci")
        if command:
            ret = await hub.exec.cmd.run([command])
            if ret.retcode:
                hub.log.info(
                    "Although '%s' was found in path, the current user "
                    "cannot execute it. Grains output might not be "
                    "accurate.",
                    command,
                )
            else:
                model = ret.stdout.lower()
                if "vmware" in model:
                    return "VMware"
                elif "virtualbox" in model:
                    # 00:04.0 System peripheral: InnoTek Systemberatung GmbH
                    #         VirtualBox Guest Service
                    return "VirtualBox"
                elif "qemu" in model:
                    return "kvm"
                elif "virtio" in model:
                    return "kvm"


async def _virt_kenv(hub) -> str:
    kenv = shutil.which("kenv")
    if kenv:
        product = (await hub.exec.cmd.run([kenv, "smbios.system.product"])).stdout
        maker = (await hub.exec.cmd.run([kenv, "smbios.system.maker"])).stdout

        if product.startswith("VMware"):
            return "VMware"
        elif product.startswith("VirtualBox"):
            return "VirtualBox"
        elif maker.startswith("Xen"):
            hub.grains.GRAINS.virtual_subtype = f"{maker} {product}"
            return "xen"
        elif maker.startswith("Microsoft") and product.startswith("Virtual"):
            return "VirtualPC"
        elif maker.startswith("OpenStack"):
            return "OpenStack"
        elif maker.startswith("Bochs"):
            return "kvm"


async def _virt_openbsd(hub) -> str:
    await hub.grains.init.wait_for("manufacturer")
    if hub.grains.GRAINS.get("manufacturer"):
        if hub.grains.GRAINS.manufacturer in ["QEMU", "Red Hat", "Joyent"]:
            return "kvm"
        elif hub.grains.GRAINS.manufacturer == "OpenBSD":
            return "vmm"


async def _virt_proc_vz(hub) -> str:
    if os.path.isdir("/proc/vz"):
        if os.path.isfile("/proc/vz/version"):
            return "openvzhn"
        elif os.path.isfile("/proc/vz/veinfo"):
            return "openvzve"


async def _virt_proc_status(hub) -> str:
    # Provide additional detection for OpenVZ
    status_path = "/proc/self/status"
    if os.path.isfile(status_path):
        async with aiofiles.open(status_path) as status_file:
            async for line in status_file:
                vz_match = re.match(r"^envID:\s+(\d+)$", line.rstrip("\n"))
                if vz_match and int(vz_match.groups()[0]) != 0:
                    return "openvzve"
                elif vz_match and int(vz_match.groups()[0]) == 0:
                    return "openvzhn"


async def _virt_proc_xen(hub) -> str:
    if (
        os.path.isdir("/proc/sys/xen")
        or os.path.isdir("/sys/bus/xen")
        or os.path.isdir("/proc/xen")
    ):
        if os.path.isfile("/proc/xen/xsd_kva"):
            # Tested on CentOS 5.3 / 2.6.18-194.26.1.el5xen
            # Tested on CentOS 5.4 / 2.6.18-164.15.1.el5xen
            hub.grains.GRAINS.virtual_subtype = "Xen Dom0"
        else:
            await hub.grains.init.wait_for("productname")
            if hub.grains.GRAINS.get("productname") == "HVM domU":
                # Requires dmidecode!
                hub.grains.GRAINS.virtual_subtype = "Xen HVM DomU"
            elif os.path.isfile("/proc/xen/capabilities") and os.access(
                "/proc/xen/capabilities", os.R_OK
            ):
                async with aiofiles.open("/proc/xen/capabilities") as fhr:
                    if "control_d" not in await fhr.read():
                        # Tested on CentOS 5.5 / 2.6.18-194.3.1.el5xen
                        hub.grains.GRAINS.virtual_subtype = "Xen PV DomU"
                    else:
                        # Shouldn't get to this, but just in case
                        hub.grains.GRAINS.virtual_subtype = "Xen Dom0"
            # Tested on Fedora 10 / 2.6.27.30-170.2.82 with xen
            # Tested on Fedora 15 / 2.6.41.4-1 without running xen
            elif os.path.isdir("/sys/bus/xen"):
                dmesg = shutil.which("dmesg")
                if dmesg:
                    ret = await hub.exec.cmd.run(dmesg)
                    if "xen:" in ret.stdout.lower():
                        hub.grains.GRAINS.virtual_subtype = "Xen PV DomU"
                    elif os.path.isfile("/sys/bus/xen/drivers/xenconsole"):
                        # An actual DomU will have the xenconsole driver
                        hub.grains.GRAINS.virtual_subtype = "Xen PV DomU"
        # If a Dom0 or DomU was detected, obviously this is xen
        if "dom" in (hub.grains.GRAINS.get("virtual_subtype") or "").lower():
            return "xen"


async def _virt_proc_cgroup(hub) -> str:
    # Check container type after hypervisors, to avoid variable overwrite on containers running in virtual environment.
    cgroup = "/proc/1/cgroup"
    if os.path.isfile(cgroup):
        try:
            async with aiofiles.open(cgroup, "r") as fhr:
                fhr_contents = await fhr.read()
                if ":/lxc/" in fhr_contents:
                    hub.grains.GRAINS.virtual_subtype = "LXC"
                    return "container"
                elif ":/kubepods/" in fhr_contents:
                    hub.grains.GRAINS.virtual_subtype = "kubernetes"
                    return "container"
                elif ":/libpod_parent/" in fhr_contents:
                    hub.grains.GRAINS.virtual_subtype = "libpod"
                    return "container"
                elif any(
                    x in fhr_contents
                    for x in (":/system.slice/docker", ":/docker/", ":/docker-ce/")
                ):
                    hub.grains.GRAINS.virtual_subtype = "Docker"
                    return "container"
        except IOError:
            pass


async def _virt_proc_cpuinfo(hub) -> str:
    if os.path.isfile("/proc/cpuinfo"):
        async with aiofiles.open("/proc/cpuinfo", "r") as fhr:
            if "QEMU Virtual CPU" in await fhr.read():
                return "kvm"


async def _virt_prtdiag(hub) -> str:
    command = shutil.which("prtdiag")
    if command:
        # prtdiag only works in the global zone, skip if it fails
        ret = await hub.exec.cmd.run([command])
        if not ret.retcode:
            model = ret.stdout.lower().split("\n")[0]
            if "vmware" in model:
                return "VMware"
            elif "virtualbox" in model:
                return "VirtualBox"
            elif "qemu" in model:
                return "kvm"
            elif "joyent smartdc hvm" in model:
                return "kvm"


async def _virt_sys(hub) -> str:
    product_name_path = "/sys/devices/virtual/dmi/id/product_name"
    if os.path.isfile(product_name_path):
        try:
            async with aiofiles.open(product_name_path, "r") as fhr:
                output = await fhr.read()
                if "VirtualBox" in output:
                    return "VirtualBox"
                elif "RHEV Hypervisor" in output:
                    hub.grains.GRAINS.virtual_subtype = "rhev"
                    return "kvm"
                elif "oVirt Node" in output:
                    hub.grains.GRAINS.virtual_subtype = "ovirt"
                    return "kvm"
                elif "Google" in output:
                    return "gce"
                elif "BHYVE" in output:
                    return "bhyve"
        except IOError:
            pass


async def _virt_sysctl_freebsd(hub) -> str:
    sysctl = shutil.which("sysctl")
    if sysctl:
        hv_vendor = (await hub.exec.cmd.run([sysctl, "-n", "hw.hv_vendor"])).stdout
        model = (await hub.exec.cmd.run([sysctl, "-n", "hw.model"])).stdout
        jail = (await hub.exec.cmd.run([sysctl, "-n", "security.jail.jailed"])).stdout

        if jail == "1":
            hub.grains.GRAINS.virtual_subtype = "jail"

        if "bhyve" in hv_vendor:
            return "bhyve"
        elif "QEMU Virtual CPU" in model:
            return "kvm"


async def _virt_sysctl_netbsd(hub) -> str:
    sysctl = shutil.which("sysctl")
    if sysctl:
        # NetBSD has Xen dom0 support
        if (
            await hub.exec.cmd.run([sysctl, "-n", "machdep.idle-mechanism"])
        ).stdout == "xen" and os.path.isfile("/var/run/xenconsoled.pid"):
            hub.grains.GRAINS.virtual_subtype = "Xen Dom0"

        if (
            "QEMU Virtual CPU"
            in (await hub.exec.cmd.run([sysctl, "-n", "machdep.cpu_brand"])).stdout
        ):
            return "kvm"
        elif (
            "VMware"
            in (
                await hub.exec.cmd.run([sysctl, "-n", "machdep.dmi.system-vendor"])
            ).stdout
        ):
            return "VMware"
        elif (
            "invalid"
            not in (
                await hub.exec.cmd.run([sysctl, "-n", "machdep.xen.suspend"])
            ).stdout
        ):
            return "Xen PV DomU"


async def _virt_systemd_detect_virt(hub) -> str:
    command = shutil.which("systemd-detect-virt")
    if command:
        ret = await hub.exec.cmd.run(command)
        if ret.stdout in (
            "qemu",
            "kvm",
            "oracle",
            "xen",
            "bochs",
            "chroot",
            "uml",
            "systemd-nspawn",
        ):
            return ret.stdout
        elif "vmware" in ret.stdout:
            return "VMware"
        elif "microsoft" in ret.stdout:
            return "VirtualPC"
        elif "lxc" in ret.stdout or "systemd-nspawn" in ret.stdout:
            return "LXC"
        elif ret.retcode:
            # systemd-detect-virt always returns > 0 on non-virtualized systems
            return "physical"


async def _virt_system_profiler(hub) -> str:
    command = shutil.which("system_profiler")
    if command:
        ret = await hub.exec.cmd.run([command, "SPDisplaysDataType"])
        if ret.retcode:
            hub.log.info(
                "Although '%s' was found in path, the current user "
                "cannot execute it. Grains output might not be "
                "accurate.",
                command,
            )
        else:
            macoutput = ret.stdout.lower()
            if "0x1ab8" in macoutput:
                return "Parallels"
            elif "parallels" in macoutput:
                return "Parallels"
            elif "vmware" in macoutput:
                return "VMware"
            elif "0x15ad" in macoutput:
                return "VMware"
            elif "virtualbox" in macoutput:
                return "VirtualBox"
    return "physical"


async def _virt_virtinfo(hub) -> str:
    command = shutil.which("virtinfo")
    if command:
        ret = await hub.exec.cmd.run([command, "-a"])
        if ret.retcode or "not supported" in ret.stdout:
            hub.log.info(
                "Although '%s' was found in path, the current user "
                "cannot execute it. Grains output might not be "
                "accurate.",
                command,
            )
        else:
            return "LDOM"


async def _virt_virt_what(hub) -> str:
    command = shutil.which("virt-what")
    if command:
        ret = await hub.exec.cmd.run(command)
        if ret.retcode:
            hub.log.info(
                "Although '%s' was found in path, the current user "
                "cannot execute it. Grains output might not be "
                "accurate.",
                command,
            )
        else:
            try:
                output = ret.stdout.splitlines()[-1]
            except IndexError:
                output = ret.stdout

            if output in ("kvm", "qemu", "uml", "xen", "lxc"):
                return output
            elif "vmware" in output:
                return "VMware"
            elif "parallels" in output:
                return "Parallels"
            elif "hyperv" in output:
                return "HyperV"


async def _virt_windows(hub) -> str:
    """
    Returns what type of virtual hardware is under the hood, kvm or physical
    """
    # It is possible that the 'manufacturer' and/or 'productname' grains
    # exist but have a value of None.
    await hub.grains.init.wait_for("manufacturer")
    manufacturer = hub.grains.GRAINS.get("manufacturer") or ""
    await hub.grains.init.wait_for("productname")
    productname = hub.grains.GRAINS.get("productname") or ""

    if "QEMU" in manufacturer:
        # FIXME: Make this detect between kvm or qemu
        return "kvm"
    if "Bochs" in manufacturer:
        return "kvm"
    elif "oVirt" in productname:
        # Product Name: (oVirt) www.ovirt.org
        # Red Hat Community virtualization Project based on kvm
        hub.grains.GRAINS.virtual_subtype = "oVirt"
        return "kvm"
    elif "RHEV Hypervisor" in productname:
        # Red Hat Enterprise Virtualization
        hub.grains.GRAINS.virtual_subtype = "rhev"
        return "kvm"
    elif "VirtualBox" in productname:
        # Product Name: VirtualBox
        return "VirtualBox"
    elif "VMware Virtual Platform" in productname:
        # Product Name: VMware Virtual Platform
        return "VMware"
    elif "Microsoft" in manufacturer and "Virtual Machine" in productname:
        # Manufacturer: Microsoft Corporation
        # Product Name: Virtual Machine
        return "VirtualPC"
    elif "Parallels Software" in manufacturer:
        # Manufacturer: Parallels Software International Inc.
        return "Parallels"
    elif "CloudStack KVM Hypervisor" in productname:
        # Apache CloudStack
        hub.grains.GRAINS.virtual_subtype = "cloudstack"
        return "kvm"
    return "physical"


async def _virtual_subtype_ldom(hub) -> str:
    if hub.grains.GRAINS.virtual == "LDOM":
        roles = []
        for role in ("control", "io", "root", "service"):
            cmd = shutil.which(role)
            if cmd:
                ret = await hub.exec.cmd.run(
                    [cmd, "-c", "current", "get", "-H", "-o", "value" f"{role}-role"]
                )
                if ret.stdout == "true":
                    roles.append(role)
        if roles:
            return " ".join(roles)


async def _virtual_subtype_proc(hub) -> str:
    if os.path.isdir("/proc"):
        try:
            self_root = os.stat("/")
            init_root = os.stat("/proc/1/root/.")
            if self_root != init_root:
                return "chroot"
        except (IOError, OSError):
            pass


async def _virt_zonename(hub) -> str:
    # Check if it's a "regular" zone. (i.e. Solaris 10/11 zone)
    zonename = shutil.which("zonename")
    if zonename:
        zone = (await hub.exec.cmd.run(zonename)).stdout
        if zone != "global":
            return "zone"


async def _virt_zone_branded(hub) -> str:
    # Check if it's a branded zone (i.e. Solaris 8/9 zone)
    if os.path.isdir("/.SUNWnative"):
        return "zone"


async def load_virtual(hub):
    """
    Returns what type of virtual hardware is under the hood, kvm or physical
    """
    await hub.grains.init.wait_for("kernel")

    if (
        hub.grains.GRAINS.kernel == "Linux"
        and hasattr(os, "uname")
        and "BrandZ virtual linux" in os.uname()
    ):
        # Quick backout for BrandZ (Solaris LX Branded zones)
        # Don't waste time trying other commands to detect the virtual grain
        hub.grains.GRAINS.virtual = "zone"
    elif hub.grains.GRAINS.kernel == "Darwin":
        hub.grains.GRAINS.virtual = await _virt_system_profiler(hub)
    elif hub.grains.GRAINS.kernel == "SunOS":
        hub.grains.GRAINS.virtual = (
            await _virt_virtinfo(hub)
            or await _virt_prtdiag(hub)
            or await _virt_zonename(hub)
            or await _virt_zone_branded(hub)
        )
        hub.grains.GRAINS.virtual_subtype = await _virtual_subtype_ldom(hub)
    elif hub.grains.GRAINS.kernel == "Windows":
        hub.grains.GRAINS.virtual = await _virt_windows(hub)
    elif hub.grains.GRAINS.kernel in ("Linux", "HP-UX"):
        hub.grains.GRAINS.virtual_subtype = await _virtual_subtype_proc(hub)
        hub.grains.GRAINS.virtual = (
            await _virt_proc_vz(hub)
            or await _virt_proc_status(hub)
            or await _virt_proc_xen(hub)
            or await _virt_proc_cgroup(hub)
            or await _virt_proc_cpuinfo(hub)
            or await _virt_sys(hub)
        )
    elif hub.grains.GRAINS.kernel == "FreeBSD":
        hub.grains.GRAINS.virtual = await _virt_kenv(hub) or await _virt_sysctl_freebsd(
            hub
        )
    elif hub.grains.GRAINS.kernel == "NetBSD":
        hub.grains.GRAINS.virtual = await _virt_sysctl_netbsd(hub)
    elif hub.grains.GRAINS.kernel == "OpenBSD":
        hub.grains.GRAINS.virtual = await _virt_openbsd(hub)

    # If all the previous commands failed, fall back to these
    if not hub.grains.GRAINS.get("virtual"):
        hub.grains.GRAINS.virtual = (
            await _virt_lspci(hub)
            or await _virt_virt_what(hub)
            or await _virt_systemd_detect_virt(hub)
            or await _virt_dmidecode(hub)
            # If all the previous commands yielded nothing we must be physical
            or "physical"
        )

    if hub.grains.GRAINS.virtual == "openvzhn":
        hub.grains.GRAINS.ps = (
            'ps -fH -p $(grep -l "^envID:[[:space:]]*0\\$" '
            '/proc/[0-9]*/status | sed -e "s=/proc/\\([0-9]*\\)/.*=\\1=")  '
            "| awk '{ $7=\"\"; print }'"
        )

    if "xen" in hub.grains.GRAINS.virtual:
        # This is only applicable to xen
        await _load_virtual_hypervisor_version(hub)
        await _load_virtual_hypervisor_features(hub)

    # If we have a virtual_subtype, we're virtual, but maybe we couldn't
    # figure out what specific virtual type we were?
    if (
        hub.grains.GRAINS.get("virtual_subtype")
        and hub.grains.GRAINS.virtual == "physical"
    ):
        hub.grains.GRAINS.virtual = "virtual"
