import os

from portmod.masters import get_masters
from portmod.repo.loader import load_all

from .datadir import find_esp_bsa


class DependencyException(Exception):
    pass


# Detect masters using tes3cmd and determine which atom they correspond to
def get_esp_deps(file, datadirs, atom):
    masters = get_masters(file)

    use = set()
    # Check if masters correspond to Tribunal.esm or Bloodmoon.esm, as they are pulled
    # in with global use flags instead of a mod
    if "Tribunal.esm" in masters:
        use.add("tribunal")
        masters.remove("Tribunal.esm")

    if "Bloodmoon.esm" in masters:
        use.add("bloodmoon")
        masters.remove("Bloodmoon.esm")

    atoms = set()
    # For other masters, look for a reference to them in the repository and get the atom
    mods = load_all()
    for mod in mods:
        for data_dir in mod.INSTALL_DIRS:
            if hasattr(data_dir, "PLUGINS"):
                for esp in data_dir.PLUGINS:
                    if esp.NAME in masters:
                        atoms.add(mod.ATOM.CMN)
                        masters.remove(esp.NAME)

    for data_dir in datadirs:
        (esps, _) = find_esp_bsa(data_dir)
        print(data_dir, esps)
        for espfile in esps:
            if espfile in masters:
                masters.discard(espfile)

    atoms.discard(atom.CMN)
    if masters:
        raise DependencyException(
            'Could not find master(s) "{}" for file: "{}"'.format(
                " ".join(masters), os.path.basename(file)
            )
        )

    return (atoms, use)
