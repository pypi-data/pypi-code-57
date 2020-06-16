"""
Used to take care of the options that end in `_dir`. The assumption is that
`_dir` options need to be treated differently. They need to verified to exist
and they need to be rooted based on the user, root option etc.
"""
# Import python libs
import os
import re


# can't two modules have root_dir?
def _new_root(ret, raw, cli):
    default_root = _get_default(raw, cli, "root_dir")
    root_dir = ret.get(cli, {}).get("root_dir")
    if root_dir and root_dir is not default_root:
        return root_dir
    if hasattr(os, "geteuid"):
        if not os.geteuid() == 0:
            return os.path.expanduser(f"~/.{cli}")

    return False


NO_DEFAULT = object()


def _get_default(raw, imp, key):
    return raw.get(imp, {}).get("CONFIG", {}).get(key, {}).get("default", NO_DEFAULT)


def _transform_path(val, imp, new_root):
    match = re.search(f"{os.sep + imp}($|{os.sep})", val)
    if match:
        if new_root.endswith(os.sep):
            # val is guaranteed to start with '/' as it's an absolute path
            #  remove one of the duplicate os separators
            return new_root[:-1] + val
        else:
            return new_root + val
    return val


def _transform_paths(ret, raw, new_root):
    for imp in ret:
        for key, val in ret[imp].items():
            if key == "root_dir":
                ret[imp][key] = new_root
            elif (
                (key.endswith("_dir") or key.endswith("_path") or key.endswith("_file"))
                and val is not None
                and val is _get_default(raw, imp, key)
                and os.path.isabs(val)
            ):
                # only update absolute paths that
                #  are default values
                #  of keys ending in _dir, _path or _file
                ret[imp][key] = _transform_path(val, imp, new_root)


def apply(hub, ret, raw, cli):
    new_root = _new_root(ret, raw, cli)
    if new_root:
        _transform_paths(ret, raw, new_root)
    return ret
