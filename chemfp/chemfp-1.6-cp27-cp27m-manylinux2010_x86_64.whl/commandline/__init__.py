# Copyright (c) 2010-2020 Andrew Dalke Scientific, AB (Sweden)
# See the contents of "chemfp/__init__.py" for full license details.

def _check_python_version():
    import sys
    if sys.version_info.major != 2:
        raise SystemExit("Cannot run %s: This version of chemfp only supports Python 2.7." % (
            progname,))
    
def _check_toolkit_or_exit(progname, toolkit_name, toolkit_import):
    try:
        __import__(toolkit_import)
    except ImportError as err:
        if "Unable to use Python 2 with OpenEye Python Toolkits built for Python 3" in str(err):
            raise SystemExit("Cannot run %s: %s" % (progname, err))
        raise SystemExit("Cannot run %s: It appears that %s is not installed: %s" % (
            progname, toolkit_name, err))

def run_ob2fps():
    _check_python_version()
    _check_toolkit_or_exit("ob2fps", "Open Babel", "openbabel")
    from ob2fps import run
    run()

def run_oe2fps(args=None):
    _check_python_version()
    _check_toolkit_or_exit("oe2fps", "OEChem", "openeye.oechem")
    from oe2fps import run
    run(args)

def run_rdkit2fps():
    _check_python_version()
    _check_toolkit_or_exit("rdkit2fps", "RDKit", "rdkit.Chem")

    from rdkit2fps import run
    run()

def run_sdf2fps():
    _check_python_version()
    from sdf2fps import run
    run()

def run_simsearch():
    _check_python_version()
    from simsearch import run
    run()

def run_fpcat():
    _check_python_version()
    from fpcat import run
    run()
