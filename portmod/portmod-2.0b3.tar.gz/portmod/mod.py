# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

from typing import Optional, Set
import os
import shutil
import json
import lzma
import subprocess
import shlex
import sys
import git
import logging
from logging import warning, info, error
from shutil import which
from portmod.globals import env
from portmod.repo.download import download_mod
from portmod.repo.loader import full_load_mod, load_installed_mod, clear_cache_for_path
from portmod.colour import green
from portmod.repo import Atom
from portmod.repo.usestr import use_reduce
from .repo.loader import load_all_installed
from .config import get_config
from .pybuild import Pybuild, FullPybuild, FullInstalledPybuild
from .util import onerror, get_tree_size
from .io_guard import get_permissions, Permissions


def get_mod_path(mod: Pybuild) -> str:
    return os.path.join(env.MOD_DIR, mod.CATEGORY, mod.MN)


__PATHS_SET__: Set[str] = set()


def set_path():
    global __PATHS_SET__
    for mod in load_all_installed(flat=True):
        if mod.CMN not in __PATHS_SET__ and "exec" in use_reduce(
            mod.PROPERTIES, mod.INSTALLED_USE, flat=True
        ):
            bin_path = os.path.join(
                env.MOD_DIR, mod.CATEGORY, mod.MN, get_config()["EXEC_PATH"]
            )
            os.environ["PATH"] += os.pathsep + bin_path
            __PATHS_SET__.add(mod.CMN)


def _preamble(mod: FullPybuild, build_dir: str, curdir: str):
    mod.execute = execute
    if curdir is None:
        os.chdir(build_dir)
    else:
        os.chdir(curdir)


def src_unpack(mod: FullPybuild, build_dir: str, curdir: Optional[str] = None):
    _preamble(mod, build_dir, curdir)
    __PERMS = Permissions(  # noqa
        rw_paths=[build_dir],
        ro_paths=[env.DOWNLOAD_DIR],
        global_read=False,
        network=True,
    )
    mod.src_unpack()


def src_prepare(mod: FullPybuild, build_dir: str, curdir: Optional[str] = None):
    _preamble(mod, build_dir, curdir)
    __PERMS = Permissions(rw_paths=[build_dir], global_read=True, network=False)  # noqa
    mod.src_prepare()


def src_install(mod: FullPybuild, build_dir: str, curdir: Optional[str] = None):
    _preamble(mod, build_dir, curdir)
    __PERMS = Permissions(rw_paths=[build_dir], global_read=True, network=False)  # noqa
    mod.src_install()


def mod_postinst(mod: FullPybuild, final_install: str, curdir: str):
    os.chdir(curdir)
    mod.execute = execute
    __PERMS = Permissions(  # noqa
        rw_paths=[final_install], global_read=True, network=False
    )
    mod.mod_postinst()


def mod_prerm(mod: FullPybuild, root: str):
    mod.execute = execute
    __PERMS = Permissions(rw_paths=[root], global_read=True, network=False)  # noqa
    mod.mod_prerm()


def execute(
    command: str,
    *,
    pipe_output: bool = False,
    err_on_stderr: bool = False,
    check: bool = True,
    pipe_error: bool = False,
) -> Optional[str]:
    """
    Executes command

    This is designed to be assigned to the FullPybuild.execute field prior to phase function
    execution. It is not set by default as it is not permitted outside of phase functions
    (e.g. in __init__)
    """
    permissions = get_permissions()

    def cleanup():
        pass

    if sys.platform == "linux":
        pwd = os.getcwd()
        if permissions.global_read:
            ro_bind_str = "--ro-bind / /"
        else:
            dir_whitelist = [
                "/bin",
                "/etc",
                "/lib",
                "/lib32",
                "/lib64",
                "/run",
                "/opt",
                "/usr",
                "/var",
                env.CACHE_DIR,
            ]
            dir_whitelist += permissions.ro_paths
            ro_bind_str = " ".join(
                [
                    f"--ro-bind {path} {path}"
                    for path in dir_whitelist
                    if os.path.exists(path)
                ]
            )
        bind_str = " ".join([f"--bind {path} {path}" for path in permissions.rw_paths])

        sandbox_command = (
            f"bwrap {ro_bind_str} {bind_str} --dev /dev --proc /proc --unshare-all "
            f"--share-net --chdir {pwd} --die-with-parent"
        )
        if permissions.network:
            sandbox_command += " --share-net"
    elif sys.platform == "win32":
        START = f'"{which("start.exe")}"'
        SINI = f'"{which("sbieini.exe")}"'

        BOXNAME = "Portmod"
        delete_commands = []

        cleanup = lambda: [  # noqa
            subprocess.check_call(command) for command in delete_commands
        ]

        def add_command(command: str, typ: str, value: str):
            nonlocal delete_commands
            subprocess.check_call(f"{SINI} {command} {BOXNAME} {typ} {value}")
            delete_commands.append(f"{SINI} delete {BOXNAME} {typ} {value}")

        if not permissions.network:
            add_command("set", "ClosedFilePath", "InternetAccessDevices")

        add_command("set", "ReadFilePath", "SystemDrive")
        if permissions.global_read:
            add_command("append", "ReadFilePath", "UserProfile")
            add_command("append", "ReadFilePath", "AllUsersProfile")
        else:
            add_command("append", "ClosedFilePath", "UserProfile")
            add_command("append", "ClosedFilePath", "AllUsersProfile")

        for path in permissions.ro_paths:
            add_command("set", "ReadFilePath", path)

        for path in permissions.rw_paths:
            add_command("set", "OpenPipePath", path)
        add_command("set", "Enabled", "y")
        add_command("set", "AutoDelete", "yes")

        # We wrap the command with cmd /c to avoid sandboxie creating a popup error
        # due to a missing executable, in case the command is not found
        sandbox_command = f"{START} /box:{BOXNAME} /wait /silent /hide_window cmd /c"
    elif sys.platform == "darwin":
        sandbox_command = """sandbox-exec -p'
            (version 1)
            (deny default)
            (allow process-exec*)
        """

        if permissions.global_read:
            sandbox_command += """
                (allow file-read*)
            """
        else:
            sandbox_command += """
                (allow file-read-data file-read-metadata
                  (regex "^/dev/autofs.*")
                  (regex "^/usr/")
                  (regex "^/System/Library")
                  (regex "^/Applications/")
                  (regex "^/var")
                )
            """

        if permissions.network:
            sandbox_command += "\n(allow network*)"

        for path in permissions.ro_paths:
            sandbox_command += """
                (allow file-read-data file-read-metadata
                  (regex "^{path}")
                )
            """

        for path in permissions.rw_paths:
            sandbox_command += """
                (allow file-write* file-read*
                    (regex "^{BUILD_DIR}/")
                )
            """
    else:
        raise Exception("Unsupported Platform")

    if sys.platform == "win32":
        cmd = sandbox_command + ' "' + command + '"'
    else:
        cmd = shlex.split(sandbox_command + " " + command)

    output = None
    error = None
    if pipe_output or logging.root.level >= logging.WARN:
        output = subprocess.PIPE
    if err_on_stderr or pipe_error or logging.root.level >= logging.WARN:
        error = subprocess.PIPE
    proc = subprocess.run(cmd, check=check, stdout=output, stderr=error)

    cleanup()

    if err_on_stderr and proc.stderr:
        raise subprocess.CalledProcessError(0, cmd, proc.stdout, proc.stderr)

    output = ""
    if pipe_output and proc.stdout:
        output += proc.stdout.decode("utf-8")
    if pipe_error and proc.stderr:
        output += proc.stderr.decode("utf-8")
    if pipe_output or pipe_error:
        return output

    return None


def remove_mod(mod: FullInstalledPybuild, reinstall: bool = False):
    """
    Removes the given mod
    @param reinstall if true, don't touch the installed DB since we'll
                      need it to finish the install
    """
    # Make sure that the PATH env variable is updated to include any mods with executables
    set_path()

    print(">>> Removing " + green(mod.ATOM.CMF))

    old_curdir = os.getcwd()
    path = get_mod_path(mod)

    mod.USE = mod.INSTALLED_USE
    BUILD_DIR = os.path.join(env.TMP_DIR, mod.CATEGORY, mod.M)
    mod.T = os.path.join(BUILD_DIR, "temp")
    os.makedirs(mod.T, exist_ok=True)

    if os.path.exists(path):
        mod.ROOT = path
        os.chdir(mod.ROOT)
        mod_prerm(mod, path)
        del mod.ROOT
        os.chdir(old_curdir)

        if os.path.islink(path):
            os.remove(path)
        else:
            shutil.rmtree(path, onerror=onerror)

    db_path = os.path.join(env.INSTALLED_DB, mod.CATEGORY, mod.MN)
    if os.path.exists(db_path) and not reinstall:
        # Remove and stage changes
        gitrepo = git.Repo.init(env.INSTALLED_DB)
        gitrepo.git.rm(os.path.join(mod.CATEGORY, mod.MN), r=True, f=True)
        # Clean up unstaged files (e.g. pycache)
        shutil.rmtree(db_path, ignore_errors=True, onerror=onerror)
        clear_cache_for_path(os.path.join(db_path, os.path.basename(mod.FILE)))

    # Remove from pybuild cache
    path = os.path.join(env.PYBUILD_CACHE_DIR, "installed", mod.CATEGORY, mod.MF)
    if os.path.exists(path):
        os.remove(path)

    print(">>> Finished Removing " + green(mod.ATOM.CMF))


def install_mod(mod: FullPybuild):
    # Make sure that the PATH env variable is updated to include any mods with executables
    set_path()

    print(">>> Starting installation of " + green(mod.ATOM.CMF))
    old_curdir = os.getcwd()
    sources = download_mod(mod)
    if sources is None:
        error(f">>> Unable to download {green(mod.ATOM.CMF)}. Aborting.")
        return False

    mod.A = sources
    mod.USE = mod.get_use()[0]
    BUILD_DIR = os.path.join(env.TMP_DIR, mod.CATEGORY, mod.M)

    # Ensure build directory is clean
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR, onerror=onerror)

    mod.T = os.path.join(BUILD_DIR, "temp")
    mod.WORKDIR = os.path.join(BUILD_DIR, "work")
    # copy files from filesdir into BUILD_DIR/files so that they are accessible
    # from within the sandbox
    FILESDIR = os.path.join(os.path.dirname(mod.FILE), "files")
    mod.FILESDIR = os.path.join(BUILD_DIR, "files")
    if os.path.exists(FILESDIR):
        shutil.copytree(FILESDIR, mod.FILESDIR)
    os.makedirs(mod.WORKDIR, exist_ok=True)
    os.makedirs(mod.T, exist_ok=True)

    info("Unpacking Mod...")
    # Network access is allowed exclusively during src_unpack, and
    # adds additional filesystem restrictions to the sandbox
    src_unpack(mod, BUILD_DIR, mod.WORKDIR)

    if not mod.S:
        tmp_source = next(iter(mod.get_default_sources()), None)
        if tmp_source:
            sourcedir, ext = os.path.splitext(tmp_source.name)
            # Hacky way to handle tar.etc having multiple extensions
            if sourcedir.endswith("tar"):
                sourcedir, _ = os.path.splitext(sourcedir)
            mod.S = os.path.join(mod.WORKDIR, sourcedir)

    if mod.S and os.path.exists(os.path.join(mod.WORKDIR, mod.S)):
        WORKDIR = os.path.join(mod.WORKDIR, mod.S)
    else:
        WORKDIR = mod.WORKDIR

    src_prepare(mod, BUILD_DIR, WORKDIR)

    final_install_dir = os.path.join(env.MOD_DIR, mod.CATEGORY)
    os.makedirs(final_install_dir, exist_ok=True)
    final_install = os.path.join(final_install_dir, mod.MN)

    mod.D = os.path.join(BUILD_DIR, "image")
    os.makedirs(mod.D, exist_ok=True)
    src_install(mod, BUILD_DIR, WORKDIR)

    os.chdir(env.TMP_DIR)

    # If a previous version of this mod was already installed,
    # remove it before doing the final copy
    old_mod = load_installed_mod(Atom(mod.CMN))
    db_path = os.path.join(env.INSTALLED_DB, mod.CATEGORY, mod.MN)
    if old_mod:
        remove_mod(full_load_mod(old_mod), os.path.exists(db_path) and mod.INSTALLED)

    info(">>> Installing into {}".format(final_install))

    if os.path.islink(final_install):
        os.remove(final_install)

    if os.path.exists(final_install):
        warning("Installed directory already existed. Overwriting.")
        shutil.rmtree(final_install, onerror=onerror)

    # base/morrowind links the D directory to the morrowind install.
    # Copy the link, not the morrowind install
    if os.path.islink(mod.D):
        linkto = os.readlink(mod.D)
        os.symlink(linkto, final_install)
    else:
        shutil.copytree(mod.D, final_install)

    mod.ROOT = final_install
    mod_postinst(mod, final_install, mod.ROOT)

    if os.path.islink(mod.D):
        installed_size = "0 MiB"
    else:
        installed_size = "{:.3f} MiB".format(get_tree_size(mod.D) / 1024 / 1024)

    build_size = "{:.3f} MiB".format(get_tree_size(WORKDIR) / 1024 / 1024)

    info("")
    info(f' {green("*")} Final size of build directory: {build_size}')
    info(f' {green("*")} Final size of installed tree: {installed_size}')
    info("")

    # If installed database exists and there is no old mod, remove it
    if os.path.exists(db_path) and not old_mod:
        shutil.rmtree(db_path, onerror=onerror)

    # Update db entry for installed mod
    gitrepo = git.Repo.init(env.INSTALLED_DB)
    os.makedirs(db_path, exist_ok=True)

    # Copy pybuild to DB
    # unless source pybuild is in DB (i.e we're reinstalling)
    if not mod.FILE.startswith(db_path):
        shutil.copy(mod.FILE, db_path)
    gitrepo.git.add(os.path.join(mod.CATEGORY, mod.MN, os.path.basename(mod.FILE)))

    manifest_path = os.path.join(os.path.dirname(mod.FILE), "Manifest")
    if os.path.exists(manifest_path):
        # Copy Manifest to DB
        if not mod.FILE.startswith(db_path):
            shutil.copy(manifest_path, db_path)
        gitrepo.git.add(os.path.join(mod.CATEGORY, mod.MN, "Manifest"))

    # Copy installed use configuration to DB
    with open(os.path.join(db_path, "USE"), "w") as use:
        print(" ".join(mod.get_use()[0]), file=use)
    gitrepo.git.add(os.path.join(mod.CATEGORY, mod.MN, "USE"))

    # Copy repo pybuild was from to DB
    with open(os.path.join(db_path, "REPO"), "w") as repo:
        print(mod.REPO, file=repo)
    gitrepo.git.add(os.path.join(mod.CATEGORY, mod.MN, "REPO"))

    # Write pybuild environment to DB
    with open(os.path.join(db_path, "environment.xz"), "wb") as environment:
        # Serialize as best we can. Sets become lists and unknown objects are
        # just stringified
        def dumper(obj):
            if isinstance(obj, set):
                return list(obj)
            return "{}".format(obj)

        # Keys are sorted to produce consistent results and
        # easy to read commits in the DB
        dictionary = mod.__class__.__dict__.copy()
        dictionary.update(mod.__dict__)
        dictionary = dict(
            filter(
                lambda elem: not elem[0].startswith("_") and elem[0] != "execute",
                dictionary.items(),
            )
        )
        jsonstr = json.dumps(dictionary, default=dumper, sort_keys=True)
        environment.write(lzma.compress(str.encode(jsonstr)))

    gitrepo.git.add(os.path.join(mod.CATEGORY, mod.MN, "environment.xz"))
    clear_cache_for_path(os.path.join(db_path, os.path.basename(mod.FILE)))

    os.chdir(old_curdir)
    print(">>> Installed " + green(mod.ATOM.CMF))
    info("")

    if not env.DEBUG:
        shutil.rmtree(BUILD_DIR, onerror=onerror)
        info(f">>> Cleaned up {BUILD_DIR}")
    return True
