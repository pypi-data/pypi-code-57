import os


def print_setup_treepcd_path():
    """Print the path to the 'setup_treepcd.sh' file.

    This can be used to easily source the file in the .bashrc by adding the
    following line:

        source $(python -c "import treep; treep.print_setup_treepcd_path()")
    """
    print(os.path.join(os.path.dirname(__file__), "setup_treepcd.sh"))
