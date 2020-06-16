import sys
import importlib
import subprocess


def _check_module(module: str, install_missing_module: bool = True):
    try:
        importlib.import_module(module)
    except ImportError:
        if install_missing_module:
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])
        else:
            print(f"Missing module: '{module}'")

def handle_dependencies(*module_names: str, install_missing_modules: bool = True):
    """ Check the module names' importability and install them if needed.

    Args:
        *module_names: Variable length module name list.
        install_missing_modules (:obj:`bool`): If True then it installs the missing modules else print that the module is missing. Defaults to True.

    """
    for module_name in module_names:
        _check_module(module_name, install_missing_modules)

