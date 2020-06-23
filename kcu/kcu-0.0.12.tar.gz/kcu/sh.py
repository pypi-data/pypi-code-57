def path(path: str) -> str:
    return path.replace(' ', '\\ ').replace('\\\\ ', '\\ ')

def sh(
    cmd: str,
    debug: bool = False
) -> str:
    import subprocess
    
    if debug:
        print(cmd)

    return subprocess.getoutput(cmd)