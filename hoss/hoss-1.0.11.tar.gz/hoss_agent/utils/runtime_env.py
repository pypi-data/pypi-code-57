import platform


def get_runtime_env():
    return {
        "arch": platform.machine(),
        "hostname": platform.node() or "unknown",
        "platform:": platform.system(),
        "version": platform.python_version(),
    }
