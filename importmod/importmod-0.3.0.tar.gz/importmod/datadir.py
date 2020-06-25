import fnmatch
import math
import os
import re
import shlex
import shutil
import subprocess
from collections import Counter
from logging import error

from portmod import InstallDir
from portmod.globals import env

from .util import NotDDSException, get_texture_size


def find_data_dirs(path):
    # Search for possible data directories
    dirs = []
    for x in os.walk(path):
        result = is_data_dir(x)
        if type(result) is str:
            dirs.append(InstallDir(os.path.relpath(x[0], path), RENAME=result))
        elif result:
            dirs.append(InstallDir(os.path.relpath(x[0], path)))

    return dirs


def is_data_dir(directory):
    path = directory[0]
    for subdir in directory[1]:
        # Match textures and meshes directories
        if re.match(
            "^(textures|meshes|video|splash|music|fonts|"
            "sound|icons|bookart|distantland)$",
            subdir,
            re.IGNORECASE,
        ):
            return True
    for file in directory[2]:
        # Match .bsa, .esp and .esm files
        if re.match(r"^.*\.(esp|" r"bsa|esm|" r"omwaddon)$", file, re.IGNORECASE):
            return True
        if re.match(r"^.*\.(dds)$", file, re.IGNORECASE) and not re.match(
            r".*(textures|icons|bookart|distantland).*", path, re.IGNORECASE
        ):
            # Looks like its a textures directory that does not have a standard parent
            # directory. We may not pick it up otherwise.
            print(
                "Detected textures in directory that is not a subdir of a common "
                "directory. This may be an optional set of textures, or it may be "
                "something else. Double-check this: {}".format(path)
            )
            return "textures"
    return False


# Finds bsas and esps in a mod installation directory
def find_esp_bsa(directory):
    esps = []
    bsas = []
    for file in os.listdir(os.path.normpath(directory)):
        if fnmatch.fnmatch(file, "*.[bB][sS][aA]"):
            bsas.append(file)
        elif (
            fnmatch.fnmatch(file, "*.[eE][sS][pPmM]")
            or fnmatch.fnmatch(file, "*.[oO][mM][wW][aA][dD][dD][oO][nN]")
            or fnmatch.fnmatch(file, "*.[oO][mM][wW][gG][aA][mM][eE]")
        ):
            esps.append(file)
    return (esps, bsas)


def get_dominant_texture_size(directory: str) -> int:
    """
    Returns the average texture size in the given directory
    """
    values = []
    num = 0

    print(f"Scanning textures in {directory}")

    def scan_dir(directory):
        nonlocal num, values
        for (path, subdirs, files) in os.walk(directory):
            for file in files:
                if re.match(r"^.*\.dds$", file, re.IGNORECASE):
                    try:
                        width, height = get_texture_size(os.path.join(path, file))
                        values.append(width * height)
                        num += 1
                    except NotDDSException as e:
                        error(e)

    scan_dir(directory)
    for (path, subdirs, files) in os.walk(directory):
        for file in files:
            if re.match(r"^.*\.bsa$", file, re.IGNORECASE):
                tmp_path = os.path.join(env.TMP_DIR, "bsascan")
                os.makedirs(tmp_path, exist_ok=True)
                # Extract with bsatool and scan contents
                print(f"Extracting archive {file}...")
                bsatool = shutil.which("bsatool")
                if not bsatool:
                    raise Exception("bsatool is not installed")
                subprocess.check_call(
                    shlex.split(
                        '{} extractall "{}" {}'.format(
                            bsatool, os.path.join(path, file), tmp_path
                        )
                    ),
                    stdout=subprocess.DEVNULL,
                )
                print(f"Scanning archive {file}...")
                scan_dir(tmp_path)
                shutil.rmtree(tmp_path)

    count = Counter(values)
    if num > 0:
        return int(
            max(
                [(math.sqrt(x), x * y) for (x, y) in count.most_common()],
                key=lambda x: x[1],
            )[0]
        )
    else:
        return 0
