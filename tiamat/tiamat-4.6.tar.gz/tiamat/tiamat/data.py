# Import python libs
import os


def version(hub, bname):
    """
    Gather the version number of the pop project if possible
    """
    dir_ = hub.tiamat.BUILDS[bname]["dir"]
    name = hub.tiamat.BUILDS[bname]["name"]
    name = name.replace("-", "_")
    path = os.path.join(dir_, name, "version.py")
    _locals = {}
    version = "1"
    try:
        if os.path.isfile(path):
            with open(path) as fp:
                exec(fp.read(), None, _locals)
                version = _locals["version"]
    except Exception:
        pass
    hub.tiamat.BUILDS[bname]["version"] = version
