import re
from typing import List


async def pid(hub, sig: str) -> List[str]:
    """
    Return the PID or an empty list if the process is running or not.
    Pass a signature to use to find the process via ps.  Note you can pass
    a Python-compatible regular expression to return all pids of
    processes matching the regexp.
    """

    output = await hub.exec.cmd.run(hub.grains.GRAINS.ps, shell=True)

    pids = []
    for line in output.splitlines():
        if "status.pid" in line:
            continue
        if re.search(sig, line):
            pids.append(line.split()[1])

    return pids
