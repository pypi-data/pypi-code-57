import shutil
import os


async def load_init_system(hub):
    if any(shutil.which(smf_cmd) for smf_cmd in ("svcs", "svcadm", "svcprop")) or any(
        os.path.exists(smf_path)
        for smf_path in ("/usr/bin/svcs", "/usr/sbin/svcadm", "/usr/bin/svcprop")
    ):
        # For solaris 10 and 11
        hub.grains.GRAINS.init = "smf"
    else:
        hub.grains.GRAINS.init = "unknown"

    # TODO it was sys v for solaris < 7, which files or commands should be checked for
    # TODO Solaris 8 and 9 it will be inittab, which files or commands should be checked for
