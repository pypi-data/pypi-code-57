def __init__(hub):
    pass


def build(hub, bname):
    """
    Given the build arguments, Make a package!
    """
    pkg_builder = hub.OPT["tiamat"]["pkg_builder"]
    getattr(hub, f"tiamat.pkg.{pkg_builder}.build")(bname)
