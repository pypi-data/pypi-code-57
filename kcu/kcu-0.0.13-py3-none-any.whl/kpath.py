from typing import List, Optional
import os

# allowed_extensions is an array, like ['jpg', 'jpeg', 'png']
def file_paths_from_folder(
    root_folder_path: str, 
    allowed_extensions: Optional[List[str]] = None, 
    recursive: bool = True
) -> List[str]:
    root_folder_path = os.path.abspath(root_folder_path)
    file_paths = []

    for (dir_path, _, file_names) in os.walk(root_folder_path):
        abs_dir_path = os.path.abspath(dir_path)

        for file_name in file_names:
            if allowed_extensions is not None and len(allowed_extensions) > 0:
                for extension in allowed_extensions:
                    if file_name.lower().endswith(extension.lower()):
                        file_paths.append(os.path.join(abs_dir_path, file_name))

                        break
            else:
                file_paths.append(os.path.join(abs_dir_path, file_name))
        
        if not recursive:
            break
    
    return file_paths

def path_of_file(f: str) -> str:
    return os.path.abspath(f)

# If left None, the file path of the caller will be used, but in that case, the return value can be None too
def folder_path_of_file(file: Optional[str] = None) -> Optional[str]:
    if file is None:
        try:
            import inspect

            file = inspect.stack()[1][1]
        except:
            return None

    return os.path.dirname(path_of_file(file))

def path_for_subpath_in_current_folder(subpath: str) -> Optional[str]:
    try:
        import inspect

        return os.path.join(os.path.dirname(path_of_file(inspect.stack()[1][1])), subpath)
    except:
        return None

def temp_path_for_path(_path: str) -> str:
    import random, string

    folder_path = folder_path_of_file(_path)
    ext = extension(_path, include_dot=True)

    while True:
        proposed_path = os.path.join(
            folder_path,
            '.' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + ext
        )

        if not os.path.exists(proposed_path):
            return proposed_path

def file_name(_path: str, include_extension: bool = True) -> str:
    basename = os.path.basename(_path)

    if not include_extension:
        basename = remove_extensions(basename)
    
    return basename

def extension(_path: str, include_dot: bool = False) -> Optional[str]:
    path_comps = _path.replace('/.', '/').split(".")

    if len(path_comps) == 1:
        return None
    
    ext = path_comps[-1]

    if include_dot:
        ext = '.' + ext
    
    return ext

def replace_extension(_path: str, new_extension: str) -> str:
    if not new_extension.startswith('.'):
        new_extension = '.' + new_extension
    
    return _path.replace(extension(_path, include_dot=True), new_extension)

def remove_extensions(_path: str) -> str:
    while True:
        ext = extension(_path, include_dot=True)

        if ext is None:
            return _path
        
        _path = _path.rstrip(ext)

def remove(_path: str) -> bool:
    if not os.path.exists(_path):
        return False

    try:
        if os.path.isdir(_path):
            import shutil

            shutil.rmtree(_path)
        else:
            os.remove(_path)
    except:
        return False

    return True