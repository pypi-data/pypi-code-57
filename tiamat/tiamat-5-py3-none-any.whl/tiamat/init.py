# Import python libs
import os
import uuid
import tempfile


def __init__(hub):
    hub.pop.sub.load_subdirs(hub.tiamat)
    os.environ["POP_BUILD"] = "1"
    os.environ["TIAMAT_BUILD"] = "1"
    hub.tiamat.BUILDS = {}
    hub.tiamat.SYSTEMD = ("rhel7", "rhel8", "arch", "debian10")
    hub.tiamat.SYSTEMD_DIR = "usr/lib/systemd/system/"
    hub.tiamat.SYSV = ("rhel5", "rhel6")
    hub.tiamat.SYSV_DIR = "etc/init.d"


def cli(hub):
    """
    Execute the routine from the CLI
    """
    hub.pop.config.load(["tiamat"], cli="tiamat")
    hub.tiamat.init.builder(
        hub.OPT.tiamat["name"],
        hub.OPT.tiamat["requirements"],
        hub.OPT.tiamat["system_site"],
        hub.OPT.tiamat["exclude"],
        hub.OPT.tiamat["directory"],
        hub.OPT.tiamat["dev_pyinstaller"],
        hub.OPT.tiamat["pyinstaller_runtime_tmpdir"],
        hub.OPT.tiamat["build"],
        hub.OPT.tiamat["pkg"],
        hub.OPT.tiamat["onedir"],
        hub.OPT.tiamat["pyenv"],
        hub.OPT.tiamat["run"],
        hub.OPT.tiamat["no_clean"],
        hub.OPT.tiamat["locale_utf8"],
        hub.OPT.tiamat["dependencies"],
        hub.OPT.tiamat["release"],
        hub.OPT.tiamat["pkg_tgt"],
        hub.OPT.tiamat["pkg_builder"],
        hub.OPT.tiamat["srcdir"],
        hub.OPT.tiamat["system_copy_in"],
        hub.OPT.tiamat["tgt_version"],
    )


def new(
    hub,
    name,
    requirements,
    sys_site,
    exclude,
    directory,
    dev_pyinst=False,
    pyinstaller_runtime_tmpdir=None,
    build=None,
    pkg=None,
    onedir=False,
    pyenv="system",
    run="run.py",
    locale_utf8=False,
    dependencies=None,
    release=None,
    pkg_tgt=None,
    pkg_builder=None,
    srcdir=None,
    system_copy_in=None,
    tgt_version=None,
):
    venv_dir = tempfile.mkdtemp()
    is_win = os.name == "nt"
    if is_win:
        python_bin = os.path.join(venv_dir, "Scripts", "python")
        s_path = os.path.join(venv_dir, "Scripts", name)
    else:
        python_bin = os.path.join(venv_dir, "bin", "python3")
        if locale_utf8:
            s_path = "env PYTHONUTF8=1 LANG=POSIX " + os.path.join(
                venv_dir, "bin", name
            )
        else:
            s_path = os.path.join(venv_dir, "bin", name)
    bname = str(uuid.uuid1())
    requirements = os.path.join(directory, requirements)
    hub.tiamat.BUILDS[bname] = {
        "name": name,
        "build": build,
        "pkg": pkg,
        "pkg_tgt": pkg_tgt,
        "pkg_builder": pkg_builder,
        "dependencies": dependencies,
        "release": release,
        "binaries": [],
        "is_win": is_win,
        "exclude": exclude,
        "requirements": requirements,
        "sys_site": sys_site,
        "dir": os.path.abspath(directory),
        "srcdir": srcdir,
        "dev_pyinst": dev_pyinst,
        "pyinstaller_runtime_tmpdir": pyinstaller_runtime_tmpdir,
        "system_copy_in": system_copy_in,
        "run": os.path.join(directory, run),
        "spec": os.path.join(directory, f"{name}.spec"),
        "pybin": python_bin,
        "s_path": s_path,
        "venv_dir": venv_dir,
        "vroot": os.path.join(venv_dir, "lib"),
        "onedir": onedir,
        "all_paths": set(),
        "imports": set(),
        "datas": set(),
        "cmd": f"{python_bin} -B -OO -m PyInstaller ",
        "pyenv": pyenv,
        "pypi_args": [
            s_path,
            "--log-level=INFO",
            "--noconfirm",
            "--onedir" if onedir else "--onefile",
            "--clean",
        ],
        "locale_utf8": locale_utf8,
    }
    req = hub.tiamat.init.mk_requirements(bname)
    hub.tiamat.BUILDS[bname]["req"] = req
    return bname


def mk_requirements(hub, bname):
    opts = hub.tiamat.BUILDS[bname]
    req = os.path.join(opts["dir"], "__build_requirements.txt")
    with open(opts["requirements"], "r") as rfh:
        data = rfh.read()
    with open(req, "w+") as wfh:
        wfh.write(data)
    return req


def builder(
    hub,
    name,
    requirements,
    sys_site,
    exclude,
    directory,
    dev_pyinst=False,
    pyinstaller_runtime_tmpdir=None,
    build=None,
    pkg=None,
    onedir=False,
    pyenv="system",
    run="run.py",
    no_clean=False,
    locale_utf8=False,
    dependencies=None,
    release=None,
    pkg_tgt=None,
    pkg_builder=None,
    srcdir=None,
    system_copy_in=None,
    tgt_version=None,
):
    bname = hub.tiamat.init.new(
        name,
        requirements,
        sys_site,
        exclude,
        directory,
        dev_pyinst,
        pyinstaller_runtime_tmpdir,
        build,
        pkg,
        onedir,
        pyenv,
        run,
        locale_utf8,
        dependencies,
        release,
        pkg_tgt,
        pkg_builder,
        srcdir,
        system_copy_in,
    )
    hub.tiamat.venv.create(bname)
    if tgt_version:
        hub.tiamat.BUILDS[bname]["version"] = tgt_version
    else:
        hub.tiamat.data.version(bname)
    hub.tiamat.build.make(bname)
    hub.tiamat.venv.scan(bname)
    hub.tiamat.venv.mk_adds(bname)
    hub.tiamat.inst.mk_spec(bname)
    hub.tiamat.inst.call(bname)
    if pkg_tgt:
        hub.tiamat.pkg.init.build(bname)
    hub.tiamat.post.report(bname)
    if not no_clean:
        hub.tiamat.post.clean(bname)
