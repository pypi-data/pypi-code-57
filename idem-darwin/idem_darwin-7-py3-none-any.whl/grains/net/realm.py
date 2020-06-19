import plistlib
import shutil


async def load_windows_domain(hub):
    hub.grains.GRAINS.windowsdomain = ""
    hub.grains.GRAINS.windowsdomaintype = ""
    dsconfigad = shutil.which("dsconfigad")
    if dsconfigad:
        ret = (
            (await hub.exec.cmd.run([dsconfigad, "-show", "-xml"]))
            .stdout.strip()
            .encode()
        )
        if ret:
            hub.grains.GRAINS.windowsdomaintype = "Unknown"
            plist = plistlib.loads(ret)
            hub.grains.GRAINS.windowsdomain = plist.get("General Info", {}).get(
                "Active Directory Domain", ""
            )
            hub.grains.GRAINS.windowsdomaintype = (
                plist.get("Administrative", {}).get("Namespace mode", "").title()
            )
