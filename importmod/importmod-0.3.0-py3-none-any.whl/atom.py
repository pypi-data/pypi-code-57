import re

from portmod.repo.atom import Atom, ver_re

__ver_re = re.compile(ver_re + "$")


def parse_atom(atom_str: str) -> Atom:
    version_v = re.search("v" + ver_re + "$", atom_str)
    version = __ver_re.search(atom_str)
    result = (version_v or version or [None])[0]
    if result is not None:
        return Atom(parse_name(atom_str.rstrip(result)) + "-" + parse_version(result))
    else:
        return Atom(parse_name(atom_str.rstrip(result)) + "-1.0")


def parse_name(name_str: str) -> str:
    lowered = name_str.lower().replace(" - ", "-").replace(" ", "-").replace("_", "-")
    stripped = re.sub(r"[^\w\/-]+", "", re.sub(r"-+", "-", lowered)).rstrip("-")
    return stripped


def parse_version(version_str: str) -> str:
    """
    Ensures that the given version string is properly formatted,
    modifying it if necessary
    """

    lstripped = re.sub(r"^\D+", "", version_str)

    # Ensure suffixes are formatted properly
    for suffix in ["pre", "p", "alpha", "beta", "rc"]:
        if re.search(rf"[^_]{suffix}\d*$", lstripped):
            lstripped = re.sub("-?" + suffix, "_" + suffix, lstripped)

    numparts = lstripped.count(".") + 1
    new_str = ""
    for index, part in enumerate(lstripped.split(".")):
        if index < numparts - 1:
            new_str += part + "."
        else:
            numeric = re.match(r"^\d+", part)
            if numeric:
                new_str += "{}".format(int(numeric[0])) + part.lstrip(numeric[0])
            else:
                new_str += part

    if not __ver_re.match(new_str):
        # Lacking a valid version, instead return numbers found in the string separated
        # by dots. If version had no numbers, this will be empty
        return re.sub(r"\D+", ".", new_str).lstrip(".").rstrip(".")

    return new_str
