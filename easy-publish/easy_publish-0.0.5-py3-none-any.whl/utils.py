import os

def listdir_fullpath(directory: str):
    return [os.path.join(directory, f) for f in os.listdir(directory)]

def array_splitter(file: list):
    # will refactor later; works fine for now as inline
    try:
        if file.index("~") == 0:
            file.pop(0)
            return array_splitter(file)
        else:
            return file.index("~")
    except ValueError:
        if file.index("~\n") == 0:
            file.pop(0)
            return array_splitter(file)
        else:
            return file.index("~\n")

