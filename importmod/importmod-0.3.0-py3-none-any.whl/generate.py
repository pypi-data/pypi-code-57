import datetime
import hashlib
import os
import re
import shutil
import urllib
from logging import error, warning
from typing import Dict, List, Set

import black
import git
import patoolib
from colorama import Fore
from isort import SortImports
from portmod import File, InstallDir
from portmod.colour import colour
from portmod.globals import env
from portmod.main import configure_mods
from portmod.masters import get_masters
from portmod.prompt import prompt_bool
from portmod.repo.atom import Atom, version_gt
from portmod.repo.download import download, get_download, parse_arrow
from portmod.repo.loader import full_load_file, load_mod
from portmod.repo.manifest import create_manifest
from portmod.repo.metadata import get_categories
from portmod.repo.util import get_hash, get_newest_mod
from portmod.repos import Repo, get_repo
from redbaron import AtomtrailersNode, CallNode, RedBaron

from .atom import parse_atom
from .datadir import find_data_dirs, find_esp_bsa, get_dominant_texture_size
from .deps import DependencyException, get_esp_deps
from .sources.nexus import (
    APILimitExceeded,
    get_nexus_info,
    parse_nexus_url,
    validate_file,
)
from .util import clean_plugin, tr_patcher

API_LIMIT_EXCEEDED = False

LOCAL_REPO = Repo(
    "local", os.path.join(env.PORTMOD_LOCAL_DIR, "local"), False, None, None, 50,
)


def update_file(file: AtomtrailersNode, new_file: File):
    """Updates plugin to match new_plugin"""
    assert file.value[0].value == "File"
    assert isinstance(file.value[1], CallNode)
    # Plugin name
    inner = file.value[1].value
    inner[0] = f'"{new_file.NAME}"'


def try_find(node, attr, key):
    try:
        return node.find(attr, key)
    except ValueError:
        return None


def update_idir(idir: AtomtrailersNode, new_idir: InstallDir):
    """Updates idir to match new_idir"""
    assert idir.value[0].value == "InstallDir"
    assert isinstance(idir.value[1], CallNode)
    inner = idir.value[1]

    def update_string(idir, new_idir, key):
        if hasattr(new_idir, key) and try_find(idir, "name", key):
            idir.find("name", key).parent.value = f'"{getattr(new_idir, key)}"'
        elif hasattr(new_idir, key) and getattr(new_idir, key):
            idir.append(f'{key}="{getattr(new_idir, key)}"')
        elif try_find(idir, "name", key):
            idir.remove(idir.find("name", key).parent)

    inner[0].value = f'"{new_idir.PATH}"'

    for key in ["S", "RENAME", "SOURCE"]:
        update_string(inner, new_idir, key)

    for key in ["PLUGINS", "ARCHIVES"]:
        if hasattr(new_idir, key) and inner.find("name", key):
            pending_files = {file.NAME: file for file in getattr(new_idir, key)}
            list_for_key = inner.find("name", key).parent.value

            files = [
                file
                for file in list_for_key
                if isinstance(file, AtomtrailersNode) and file.value[0].value == "File"
            ]

            # If there is only one plugin, assume it is the same as the old one
            if len(files) == 1 and len(new_idir.PLUGINS) == 1:
                update_file(files[0], new_idir.PLUGINS[0])
            else:
                # Otherwise, leave any old files that match the new files names,
                # remove files that aren't in the new list,
                # and add any missing files to the list
                for file in files:
                    # File name
                    name = file.value[1].value[0]
                    if name in pending_files:
                        del pending_files[name]
                    else:
                        list_for_key.remove(file)

                for file in pending_files:
                    if pending_files[file].comment:
                        list_for_key.node_list.append(
                            RedBaron(pending_files[file].comment)
                        )
                        list_for_key.node_list.append(RedBaron("\n"))
                    list_for_key.node_list.append(
                        RedBaron(str(pending_files[file]) + ",")
                    )
        elif inner.find("name", key):
            # New idir doesn't have this element. Delete the old list
            inner.remove(inner.find("name", key).parent)
        elif hasattr(new_idir, key) and getattr(new_idir, key):
            inner.append(f"{key}={getattr(new_idir, key)}")


def generate_build_files(
    mod, *, noreplace=False, allow_failures=False, validate=False, repo="local"
):
    """
    Generates pybuilds from a mod decription dictionary.

    Valid Fields: atom, name, desc, homepage, category, url, file,
      author, needs_cleaning
    Other fields are ignored
    """

    if "atom" in mod:
        atom = Atom(mod["atom"])
    elif "category" in mod and "name" in mod:
        atom = parse_atom(mod["category"] + "/" + mod["name"])
    else:
        atom = None

    url = mod.get("url")
    if "file" in mod:
        file = os.path.expanduser(mod.get("file").replace(" ", "_"))
    else:
        file = None
    name = mod.get("name", None)
    desc = mod.get("desc", None) or mod.get("description", None)
    homepage = mod.get("homepage", None)
    author = mod.get("author")
    needs_cleaning = mod.get("needs_cleaning")

    sources = []
    source_string = url

    parsed = urllib.parse.urlparse(url)
    downloaded = False
    nexus_data = None
    REQUIRED_USE = []
    CLASS = ["Pybuild1"]
    OTHER_IMPORTS: Dict[str, List[str]] = {}
    OTHER_FIELDS = {}

    if parsed.hostname == "www.nexusmods.com":
        game, mod_id = parse_nexus_url(url)

        # Get Nexus API data, but if we've exceeded out limit,
        # just print an error and return
        global API_LIMIT_EXCEEDED
        if API_LIMIT_EXCEEDED:
            return
        else:
            try:
                nexus_data = get_nexus_info(game, mod_id)
            except APILimitExceeded:
                error("Nexus API limit has been exceeded. Try again tomorrow")
                API_LIMIT_EXCEEDED = True
                return

        if nexus_data is not None:
            homepage = homepage or nexus_data.homepage
            name = name or nexus_data.name
            if not atom:
                atom = Atom(mod["category"] + "/" + nexus_data.atom)
            elif not atom.MV:
                atom = Atom(atom + "-" + nexus_data.atom.MV)
            desc = desc or nexus_data.desc

            if noreplace and len(load_mod(atom)) > 0:
                return

            if not all([get_download(file, None) for file in nexus_data.files]):
                print("Please download the following files from the url at the bottom")
                print("before continuing and move them to the download directory:")
                print("  {}".format(env.DOWNLOAD_DIR))
                print()
                for source in nexus_data.files:
                    if not get_download(source, None):
                        print("  {}".format(source))
                print()
                print("  {}?tab=files".format(nexus_data.homepage))
                if not prompt_bool("Continue?"):
                    return

            for file in nexus_data.files:
                if validate and not validate_file(
                    game,
                    mod_id,
                    get_download(file, None),
                    get_hash(get_download(file, None), hashlib.md5),
                ):
                    raise Exception(f"File {file} has invalid hash!")

            url = None
            file = None
            downloaded = True
            sources = nexus_data.files
            source_string = " ".join(sources)
            if nexus_data.nudity:
                REQUIRED_USE.append("nudity")
            author = author or nexus_data.author
            OTHER_FIELDS["NEXUS_URL"] = f'"{nexus_data.homepage}"'
            CLASS.append("NexusMod")
            if "pyclass" not in OTHER_IMPORTS:
                OTHER_IMPORTS["pyclass"] = ["NexusMod"]
            elif "NexusMod" not in OTHER_IMPORTS["pyclass"]:
                OTHER_IMPORTS["pyclass"].append("NexusMod")

    elif parsed.hostname == "mw.modhistory.com":
        homepage = url
        match = re.search(r"\d+$", url)
        assert match is not None
        num = match.group()
        source_string = (
            f"http://mw.modhistory.com/file.php?id={num} -> {atom.C}_{atom.M}"
        )
        url = source_string
    elif parsed.hostname == "github.com" or parsed.hostname == "gitlab.com":
        source_string = ""
        CLASS.insert(0, "Git")
        if "pyclass" not in OTHER_IMPORTS:
            OTHER_IMPORTS["pyclass"] = ["Git"]
        elif "Git" not in OTHER_IMPORTS["pyclass"]:
            OTHER_IMPORTS["pyclass"].append("Git")
        OTHER_FIELDS["GIT_SRC_URI"] = '"{url}"'

        name, _ = os.path.splitext(os.path.basename(url))
        outdir = os.path.join(env.TMP_DIR, name)
        gitrepo = git.Repo.clone_from(url, outdir)
        date = datetime.date.fromtimestamp(gitrepo.head.commit.committed_date)
        print(date)
        atom = Atom(
            "{}-0_p{}{}{}".format(
                atom.CMN,
                str(date.year),
                str(date.month).zfill(2),
                str(date.day).zfill(2),
            )
        )
        OTHER_FIELDS["GIT_COMMIT_DATE"] = '"{date}"'
        shutil.rmtree(outdir)
        url = None
        downloaded = True
    elif (
        str(os.path.basename(parsed.path)).endswith(".php") and "->" not in url.split()
    ):
        source_string = url = f"{url} -> {atom.C}_{atom.M}"

    print("Importing {}...".format(atom))

    # Copyright Header
    headerstring = [
        f"# Copyright 2019-{datetime.datetime.now().year} Portmod Authors",
        "# Distributed under the terms of the GNU General Public License v3",
    ]

    oldmods = load_mod(Atom(atom.MN))
    if oldmods:
        newest = get_newest_mod(oldmods)
        if noreplace and not version_gt(newest.MVR, atom.MVR):
            print(f"Mod {atom} already exists.Skipping...")
            return

        with open(newest.FILE, "r") as pybuild_file:
            pybuild = RedBaron(pybuild_file.read())
    else:
        pybuild = RedBaron("\n".join(headerstring))

    if url is not None:
        # We permit arrow notation in the url field
        for source in parse_arrow(url.split()):
            if not get_download(source.name, None):
                download(source.url, source.name)
            sources.append(source.name)

    elif file is not None:
        download_name = os.path.basename(file).replace(" ", "_")
        shutil.copy(file, get_download(download_name, None))
        sources.append(download_name)
        source_string = os.path.basename(file)
    elif not downloaded:
        raise Exception(
            "Please provide a download name or file name in the import configuration"
        )

    C = atom.C or mod.get("category")
    M = atom.M
    MN = atom.MN

    dep_atoms: Set[Atom] = set()
    dep_uses: Set[str] = set()

    cleanr = re.compile("<.*?>")
    if desc is not None:
        desc = re.sub(cleanr, "", desc)
        desc = desc.replace("\n", " ").replace("\r", " ").replace('"', '\\"')
    if author is not None:
        author = re.sub(cleanr, "", author)

    data_dirs = []
    TEXTURE_SIZES = set()
    INSTALL_DIRS: List[InstallDir] = []
    build_deps: Set[Atom] = set()

    for source in sources:
        # Extract file into tmp
        outdir = os.path.join(env.TMP_DIR, source)
        os.makedirs(outdir, exist_ok=True)
        patoolib.extract_archive(
            get_download(source, None), outdir=outdir, interactive=False
        )

    for source in sources:
        # Search for data directories
        outdir = os.path.join(env.TMP_DIR, source)
        dirs = find_data_dirs(outdir)
        data_dirs.append((source, dirs))
        print(
            "Detected the following data directories for {}: {}".format(
                source, [dir.PATH for dir in dirs]
            )
        )

        for directory in dirs:
            (esps, bsas) = find_esp_bsa(os.path.join(outdir, directory.PATH))
            if bsas:
                directory.add_kwarg("ARCHIVES", [File(bsa) for bsa in bsas])

            source_name, _ = os.path.splitext(source)
            if source_name.endswith(".tar"):
                source_name, _ = os.path.splitext(source_name)

            texture_size = get_dominant_texture_size(
                os.path.join(env.TMP_DIR, source, directory.PATH)
            )

            if texture_size:
                TEXTURE_SIZES.add(texture_size)

            PLUGINS = []
            # Get dependencies for the ESP.
            for esp in esps:
                esp_path = os.path.join(outdir, directory.PATH, esp)
                print("Masters of esp {} are {}".format(esp, get_masters(esp_path)))
                try:
                    (dep_atom, dep_use) = get_esp_deps(
                        esp_path,
                        [
                            os.path.join(env.TMP_DIR, source, data_dir.PATH)
                            for (source, dirs) in data_dirs
                            for data_dir in dirs
                        ],
                        atom,
                    )
                    print(
                        'Found esp "{}" with deps of: {}'.format(
                            esp, dep_atom.union(dep_use)
                        )
                    )
                    dep_atoms |= dep_atom
                    dep_uses |= dep_use
                except DependencyException as e:
                    warning("{}. Continuing anyway at user's request", e)

                CLEAN = False
                TR_PATCH = False

                if needs_cleaning:
                    configure_mods(
                        dep_atom,
                        no_confirm=True,
                        oneshot=True,
                        update=True,
                        newuse=True,
                        noreplace=True,
                    )
                    if clean_plugin(esp_path):
                        CLEAN = True
                        if "CleanPlugin" not in CLASS:
                            CLASS.insert(0, "CleanPlugin")
                        if "pyclass" not in OTHER_IMPORTS:
                            OTHER_IMPORTS["pyclass"] = ["CleanPlugin"]
                        elif "CleanPlugin" not in OTHER_IMPORTS["pyclass"]:
                            OTHER_IMPORTS["pyclass"].append("CleanPlugin")
                        build_deps |= dep_atom

                if "TR_Data.esm" in get_masters(esp_path):
                    TR_PATCH = True
                    if "pyclass" not in OTHER_IMPORTS:
                        OTHER_IMPORTS["pyclass"] = ["TRPatcher"]
                    elif "TRPatcher" not in OTHER_IMPORTS["pyclass"]:
                        OTHER_IMPORTS["pyclass"].append("TRPatcher")
                    if "TRPatcher" not in CLASS:
                        CLASS.insert(0, "TRPatcher")
                    print("TR Patching file {}".format(esp))
                    tr_patcher(esp_path)

                plugin = File(esp)
                if CLEAN:
                    plugin.add_kwarg("CLEAN", True)

                if TR_PATCH:
                    plugin.add_kwarg("TR_PATCH", True)

                plugin.comment = "# Deps: " + " ".join(sorted(dep_atom | dep_use)) + ""
                PLUGINS.append(plugin)

            if PLUGINS:
                directory.add_kwarg("PLUGINS", PLUGINS)

            if texture_size:
                directory.comment = f"# Texture Size: {texture_size}"
            else:
                directory.comment = ""

            if oldmods:
                directory.comment += "\n# FIXME: New Directory. Please check"

            if len(sources) > 1:
                directory.add_kwarg("S", source_name)

            INSTALL_DIRS.append(directory)

    if "base/morrowind" in dep_atoms and dep_uses:
        dep_atoms.remove("base/morrowind")
        dep_atoms.add("base/morrowind[" + ",".join(sorted(dep_uses)) + "]")

    deps = " ".join(sorted(dep_atoms))

    for source in sources:
        # Clean up files
        path = os.path.join(env.TMP_DIR, source)
        print(f"Cleaning up {path}")
        shutil.rmtree(path)

    if TEXTURE_SIZES:
        OTHER_FIELDS["TEXTURE_SIZES"] = '"{}"'.format(
            " ".join(map(str, sorted(TEXTURE_SIZES)))
        )

    if not pybuild or pybuild[0:1] != headerstring:
        # Looks like an old copyright statement, but is not correct
        if pybuild and str(pybuild[0]).startswith("# Copyright"):
            pybuild[0:2] = headerstring
        else:
            for line in reversed(headerstring):
                pybuild.insert(0, line)

    # Import statements
    imports = {}
    for i in pybuild.find("FromImportNode") or []:
        imports[".".join([str(x) for x in i.value])] = i.parent

    main_imports = ["Pybuild1"]
    if INSTALL_DIRS:
        main_imports.append("InstallDir")
    if any(d.get_files() for d in INSTALL_DIRS):
        main_imports.append("File")

    if imports:
        # Update imports if any imports are missing
        if "portmod.pybuild" in imports:
            imports["portmod.pybuild"].value = "pybuild"
            imports["pybuild"] = imports["portmod.pybuild"]

        if "pybuild" in imports:
            for main_import in main_imports:
                if not imports["pybuild"].targets.find("name", main_import):
                    imports["pybuild"].targets.append(main_import)

        for imp in OTHER_IMPORTS:
            if imp in imports:
                for other_import in imports[imp]:
                    if not imports[imp].targets.find("name", other_import):
                        imports[imp].targets.append(other_import)
            else:
                pybuild.insert(3, f'from {imp} import {", ".join(OTHER_IMPORTS[imp])}')
    else:
        pybuild.insert(3, f'from pybuild import {", ".join(main_imports)}')
        index = 3
        for import_name in OTHER_IMPORTS:
            pybuild.insert(
                index,
                f'from {import_name} import {", ".join(OTHER_IMPORTS[import_name])}',
            )
            index += 1

    Mod = pybuild.find("class", "Mod")

    values = {
        "NAME": f'"{name}"',
        "DESC": f'"{desc}"',
        "HOMEPAGE": f'"{homepage}"',
        "LICENSE": '"TODO: FILLME"',
        "KEYWORDS": '"TODO: FILLME or Delete"',
    }

    if deps:
        values["RDEPEND"] = f'"{deps}"'
    if build_deps:
        values["DEPEND"] = '"{}"'.format(" ".join(sorted(build_deps)))
    for field in OTHER_FIELDS:
        values[field] = OTHER_FIELDS[field]
    if REQUIRED_USE:
        values["REQUIRED_USE"] = f'"{" ".join(REQUIRED_USE)}"'

    if Mod:
        # Add missing superclasses
        for superclass in CLASS:
            if not Mod.inherit_from.find("name", superclass):
                Mod.inherit_from.insert(0, superclass)

        # Add missing variables to mod
        for key in values:
            if not Mod.find("name", key):
                Mod.append(f"{key}={values[key]}")

        # Update SRC_URI unless there are no missing files
        if Mod.find("name", "SRC_URI"):
            old_value = Mod.find("name", "SRC_URI").parent.value
            for file in source_string.split():
                if file not in str(old_value):
                    Mod.find("name", "SRC_URI").parent.value = f'"{source_string}"'
                    break
        else:
            Mod.append(f'SRC_URI="{source_string}"')

        # Update S if present
        if Mod.find("name", "S") and len(sources) == 1:
            source_name, _ = os.path.splitext(sources[0])
            if source_name.endswith(".tar"):
                source_name, _ = os.path.splitext(source_name)
            Mod.find("name", "S").parent.value = f'"{source_name}"'
    else:
        valuestr = "\n    ".join(
            [f"{key}={values[key]}" for key in sorted(values.keys())]
        )
        pybuild.append(f'class Mod({", ".join(reversed(CLASS))}):\n   {valuestr}')
        Mod = pybuild.find("class", "Mod")
        Mod.append(f'SRC_URI="{source_string}"')

    if Mod.find("name", "INSTALL_DIRS"):
        dirs = [
            node
            for node in Mod.find("name", "INSTALL_DIRS").parent.value
            if isinstance(node, AtomtrailersNode)
            and node.value[0].value == "InstallDir"
        ]

        # Simplest case. If there is only one install directory,
        # assume it is the same one, and update its values
        if len(dirs) == 1 and len(INSTALL_DIRS) == 1:
            # Second element is a callnode containing the arguments we care about
            update_idir(dirs[0], INSTALL_DIRS[0])
        else:
            pending_dirs = {
                os.path.join(d.S, d.PATH): d for d in INSTALL_DIRS if d.S is not None
            }
            pending_dirs.update({d.PATH: d for d in INSTALL_DIRS if d.S is None})
            for node in dirs:
                if isinstance(node, AtomtrailersNode):
                    # Install dirs are identified uniquely by their source and first
                    # argument
                    idir = node.value[1]
                    path = idir.value[0]
                    S = idir.find("name", "S")
                    SOURCE = idir.find("name", "SOURCE")
                    if S:
                        entirepath = os.path.join(
                            str(S.parent.value).strip('"'), str(path.value).strip('"')
                        )
                    elif SOURCE:
                        source_str = str(SOURCE.parent.value).strip('"')
                        source_str, _ = os.path.splitext(source_str)
                        entirepath = os.path.join(
                            source_str, str(path.value).strip('"')
                        )
                    else:
                        entirepath = str(path.value).strip('"')

                    # Try to find dir in INSTALL_DIRS for new mod that matches.
                    # This is hard because S has probably changed
                    # If S is not specified, it is easier, but the PATH may have changed
                    # We could attempt to match based on other fields, but the simplest
                    # and most reliable way is to throw out old code
                    # and create a new InstallDir
                    if entirepath in pending_dirs:
                        update_idir(node, pending_dirs[entirepath])
                        del pending_dirs[entirepath]
                    else:
                        # If none exists, we remove this node
                        dirs.remove(node)

            # Add missing new directories
            dirlist = Mod.find("name", "INSTALL_DIRS").parent.value
            for new_dir in pending_dirs.values():
                if new_dir.comment:
                    dirlist.node_list.append(RedBaron(new_dir.comment))
                    dirlist.node_list.append(RedBaron("\n"))
                dirlist.node_list.append(RedBaron(str(new_dir) + ","))

    else:
        Mod.append(f'INSTALL_DIRS = [{", ".join(f"{d}" for d in INSTALL_DIRS)}]')

    build_file = pybuild.dumps()

    print(build_file)

    print("Sorting imports...")
    build_file = SortImports(file_contents=build_file).output
    print("Formatting code...")
    build_file = black.format_str(build_file, mode=black.FileMode())

    if repo == "local":
        REPO = LOCAL_REPO
    else:
        REPO = get_repo(repo)

    # User import repo may not exist. If not, create it
    if not os.path.exists(REPO.location):
        os.makedirs(os.path.join(REPO.location, "profiles"), exist_ok=True)
        metadata_file = os.path.join(REPO.location, "profiles", "repo_name")
        with open(metadata_file, "w") as file:
            print("user-repo", file=file)

        layout_file = os.path.join(REPO.location, "metadata", "layout.conf")
        os.makedirs(os.path.dirname(layout_file))
        with open(layout_file, "w") as file:
            print('masters="openmw"', file=file)
        # Add user repo to REPOS so that it can be used in further dependency resolution
        env.REPOS.append(REPO)
        # Write user import repo to repos.cfg
        with open(env.REPOS_FILE, "a") as file:
            userstring = """
[user]
location = {}
auto_sync = False
masters = openmw
priority = 50
"""
            print(userstring.format(REPO.location), file=file)

    if C not in get_categories(REPO.location):
        with open(
            os.path.join(REPO.location, "profiles", "categories"), "a"
        ) as categories:
            print(C, file=categories)

    outdir = os.path.join(REPO.location, C, MN)
    filename = os.path.join(outdir, M + ".pybuild")
    os.makedirs(outdir, exist_ok=True)

    build_files = [filename]

    print("Exporting pybuild to {}".format(filename))
    with open(filename, "w") as file:
        print(build_file, file=file)

    if parsed.hostname == "github.com" or parsed.hostname == "gitlab.com":
        # Create Live Pybuild
        Mod.remove(Mod.find("name", "GIT_COMMIT_DATE").parent)
        live_file = pybuild.dumps()

        M = atom.MN + "-9999"
        filename = os.path.join(outdir, M + ".pybuild")
        build_files.append(filename)
        print("Exporting pybuild to {}".format(filename))
        with open(filename, "w") as file:
            print(live_file, file=file)

    # Add author to metadata.yaml if provided
    if author:
        create_metadata(os.path.join(outdir, "metadata.yaml"), author)

    # Create manifest file
    for filename in build_files:
        create_manifest(full_load_file(filename))

    print(colour(Fore.GREEN, "Finished Importing {}".format(atom)))


def create_metadata(file, author):
    with open(file, "w") as metadata:
        print("upstream:", file=metadata)
        print(f"    maintainer: !person {author}", file=metadata)
