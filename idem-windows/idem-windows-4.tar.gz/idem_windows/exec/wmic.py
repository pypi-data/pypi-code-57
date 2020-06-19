import shutil
import subprocess


def get(hub, namespace: str, path: str, item: str) -> str:
    wmic = shutil.which("wmic")
    if not wmic:
        hub.log.error("Could not find wmic command")
        return ""

    proc = subprocess.Popen(
        [wmic, f"/namespace:{namespace}", "path", path, "get", item, "/format:table"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = proc.communicate()
    if proc.wait():
        stderr = stderr.decode().strip().replace("\r", "").replace("\n", " ")
        hub.log.debug(f"wmic encountered an error: {stderr}")
        return ""

    return stdout.decode().strip().replace("\r", "")
