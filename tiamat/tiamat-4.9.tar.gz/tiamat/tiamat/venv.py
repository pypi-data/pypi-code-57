"""
Create and manage the venvs used for build environments
"""
# Import python libs
import venv
import os
import sys
import shutil
import subprocess
import tarfile


OMIT = (
    "__pycache__",
    "PyInstaller",
)


def bin(hub, bname):
    """
    Ensure that the desired binary version is present and return the path to
    the python bin to call
    """
    opts = hub.tiamat.BUILDS[bname]
    root = (
        subprocess.run(
            "pyenv root", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        .stdout.strip()
        .decode()
    )
    avail = set()
    for line in (
        subprocess.run(
            "pyenv versions", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        .stdout.strip()
        .decode()
        .split("\n")
    ):
        avail.add(line.strip())
    python_env = "env PYTHONUTF8=1 LANG=POSIX " if opts["locale_utf8"] else ""
    if opts["pyenv"] not in avail:
        subprocess.run(
            f'{python_env} PYTHON_CONFIGURE_OPTS="--enable-shared --enable-ipv6" CONFIGURE_OPTS="--enable-shared --enable-ipv6" pyenv install {opts["pyenv"]}',
            shell=True,
        )
    bin_path = python_env + os.path.join(
        root, "versions", opts["pyenv"], "bin", "python3"
    )
    return bin_path


def create(hub, bname):
    """
    Make a virtual environment based on the version of python used to call this script
    """
    opts = hub.tiamat.BUILDS[bname]
    if opts["pyenv"] == "system":
        venv.create(
            opts["venv_dir"],
            clear=True,
            with_pip=True,
            system_site_packages=opts["sys_site"],
        )
    else:
        env_bin = hub.tiamat.venv.bin(bname)
        cmd = f'{env_bin} -m venv {opts["venv_dir"]} --clear '
        if opts["sys_site"]:
            cmd += "--system-site-packages"
        subprocess.run(cmd, shell=True)
    pip_cmd = f"{opts['pybin']} -m pip "
    if opts["srcdir"]:
        files = _get_srcdir_files(opts["srcdir"])
        subprocess.run(f"{pip_cmd} install {files}")
    else:
        # update pip, cant update setuptools due to PyInstaller bug
        subprocess.run(f"{pip_cmd} install -U pip", shell=True)
        # I am hardcoding this in for now, it should be removed when Python 3.8 has been out longer
        subprocess.run(f"{pip_cmd} install distro", shell=True)
        reqcmd = subprocess.run(
            f'{pip_cmd} install -r {opts["req"]}', shell=True
        ).returncode
        projcmd = 0
        if os.path.isfile(os.path.join(opts["dir"], "setup.py")):
            projcmd = subprocess.run(
                f'{pip_cmd} install {opts["dir"]}', shell=True
            ).returncode
        exit = False
        if reqcmd != 0:
            print("Failed to install requirements, please check pip output for details")
            exit = True
        if projcmd != 0:
            print("Failed to setup project, please check pip output for details")
            exit = True
        if exit:
            sys.exit(1)
    # Install old pycparser to fix: https://github.com/eliben/pycparser/issues/291 on Windows
    if opts["is_win"]:
        subprocess.run(f"{pip_cmd} install pycparser==2.14", shell=True)
    if opts["dev_pyinst"]:
        # Install development version of pyinstaller to run on python 3.8
        subprocess.run(
            f"{pip_cmd} install https://github.com/pyinstaller/pyinstaller/tarball/develop",
            shell=True,
        )
    else:
        subprocess.run(f"{pip_cmd} install PyInstaller==3.6", shell=True)
    if opts["system_copy_in"]:
        _copy_in(opts)
    if os.path.isfile(opts["exclude"]):
        subprocess.run(f'{pip_cmd} uninstall -y -r {opts["exclude"]}', shell=True)
    os.environ[
        "LD_LIBRARY_PATH"
    ] = f'{os.environ.get("LD_LIBRARY_PATH")}:{os.path.join(opts["venv_dir"], "lib")}'.strip(
        ":"
    )


def _copy_in(opts):
    """
    Copy in any extra directories from the puthon install
    """
    cmd = f"{opts['pybin']} -c 'import sys;print(sys.path)'"
    tgt = ""
    dtgt = os.path.join(os.path.join(opts["venv_dir"], "lib"))
    for fn in os.listdir(dtgt):
        tmptgt = os.path.join(dtgt, fn)
        if os.path.isdir(tmptgt):
            tgt = os.path.join(tmptgt, "site-packages")
    data = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE).stdout
    done = set()
    for path in eval(data):
        if not path:
            continue
        if not os.path.isdir(path):
            continue
        for fn in os.listdir(path):
            if fn in done:
                continue
            if fn in opts["system_copy_in"]:
                full = os.path.join(path, fn)
                if os.path.isdir(full):
                    shutil.copytree(full, os.path.join(tgt, fn))
                    done.add(fn)


def _get_srcdir_files(srcdir):
    """
    Return the files that are python archives
    """
    files = ""
    for fn in os.listdir(srcdir):
        if fn.endswith(".whl"):
            files += f"{fn} "
        if fn.endswith(".tar.gz"):
            # Might be a source archive
            with tarfile.open(fn) as tfp:
                for name in tfn.getnames():
                    if name.count(os.sep) > 1:
                        continue
                    if os.path.basename(name) == "PKG-INFO":
                        files += f"{fn} "
                        break
    return files


def _omit(test):
    for bad in OMIT:
        if bad in test:
            return True
    return False


def _to_import(path):
    ret = path[path.index("site-packages") + 14 :].replace(os.sep, ".")
    if ret.endswith(".py"):
        ret = ret[:-3]
    return ret


def _to_data(path):
    dest = path[path.index("site-packages") + 14 :]
    src = path
    if not dest.strip():
        return None
    ret = f"{src}{os.pathsep}{dest}"
    return ret


def scan(hub, bname):
    """
    Scan the new venv for files and imports
    """
    opts = hub.tiamat.BUILDS[bname]
    for root, dirs, files in os.walk(opts["vroot"]):
        if _omit(root):
            continue
        for d in dirs:
            full = os.path.join(root, d)
            if _omit(full):
                continue
            opts["all_paths"].add(full)
        for f in files:
            full = os.path.join(root, f)
            if _omit(full):
                continue
            opts["all_paths"].add(full)


def mk_adds(hub, bname):
    """
    Make the imports and datas for pyinstaller
    """
    opts = hub.tiamat.BUILDS[bname]
    for path in opts["all_paths"]:
        if not "site-packages" in path:
            continue
        if os.path.isfile(path):
            if not path.endswith(".py"):
                continue
            if path.endswith("__init__.py"):
                # Skip it, we will get the dir
                continue
            imp = _to_import(path)
            if imp:
                opts["imports"].add(imp)
        if os.path.isdir(path):
            data = _to_data(path)
            imp = _to_import(path)
            if imp:
                opts["imports"].add(imp)
            if data:
                opts["datas"].add(data)
