import re
import os
import shutil
import time
import warnings
import pathlib
from typing import Union, List, Pattern, Match


class Watcher(object):
    def __init__(self,
                 path: Union[str, pathlib.Path],
                 watchfor: Union[str, Pattern] = '',
                 includesubfolders: bool = True,
                 subdirectory: str = None,
                 watch_type: str = 'file',
                 exclude_subfolders: List[str] = None,
                 match_exact: bool = False,
                 ignore_case: bool = True,
                 ):
        """
        Watches a folder for file changes.

        :param path: The folder path to watch for changes
        :param watchfor: Watch for this item. This can be a full filename, or an extension (denoted by *., e.g. "*.ext")
        :param bool includesubfolders: wehther to search subfolders
        :param str subdirectory: specified subdirectory
        :param str watch_type: The type of item to watch for ('file' or 'folder')
        :param exclude_subfolders: specific sub folders to exclude when looking for files. These subfolders will be
            globally excluded.
        :param match_exact: whether the watcher should only look for exact matches of the provided pattern
        :param ignore_case: case sensitivity for matches
        """
        # protected attributes for properties
        self._path = None
        self._subdir = None
        self._watchfor = None
        self._ignore_case: bool = True

        self.match_exact: bool = match_exact
        self.path = path
        self.includesubfolders = includesubfolders
        self.watchfor = watchfor
        self.ignore_case = ignore_case
        self.watch_type = watch_type
        if exclude_subfolders is None:
            exclude_subfolders = []
        self.exclude_subfolders = exclude_subfolders
        self.subdirectory = subdirectory

    def __repr__(self):
        return f'{self.__class__.__name__}({len(self.contents)} {self.watchfor})'

    def __str__(self):
        return f'{self.__class__.__name__} with {len(self.contents)} matches of {self.watchfor}'

    def __len__(self):
        return len(self.contents)

    def __iter__(self):
        for file in self.contents:
            yield file

    @property
    def path(self) -> pathlib.Path:
        """path to watch"""
        return self._path

    @path.setter
    def path(self, newpath: Union[str, pathlib.Path]):
        if isinstance(newpath, pathlib.Path) is False:
            newpath = pathlib.Path(newpath)
        if not os.path.isdir(newpath):
            raise ValueError(f'The specified path\n{newpath}\ndoes not exist.')
        self._path = newpath

    @property
    def subdirectory(self) -> str:
        """specific subdirectory to watch within the path"""
        return self._subdir

    @subdirectory.setter
    def subdirectory(self, newdir: str):
        if newdir is None:
            del self.subdirectory
            return
        if os.path.isdir(self.path / newdir) is False:
            raise ValueError(f'The subdirectory {newdir} does not exist in the path {self.path}.')
        if newdir in self.exclude_subfolders:
            raise ValueError(f'The subdirectory {newdir} is specifically excluded in the exclude_subfolders attribute.')
        self._subdir = newdir

    @subdirectory.deleter
    def subdirectory(self):
        self._subdir = None

    @property
    def full_path(self) -> pathlib.Path:
        """full watch path (including subdirectory)"""
        if self.subdirectory is not None:
            return self.path / self.subdirectory
        return self.path

    @property
    def watchfor(self) -> Pattern:
        """the pattern to watch for in the directory"""
        return self._watchfor

    @watchfor.setter
    def watchfor(self, value: Union[str, Pattern]):
        if value is None:
            value = ''
        if type(value) is str and value.startswith('*'):
            warnings.warn(f'the value "{value}" is an invalid regex pattern, please remove the "*"')
            value = '.' + value
        if isinstance(value, Pattern) is False:
            value = re.compile(
                value,
                flags=re.IGNORECASE if self.ignore_case else 0
            )
        self._watchfor = value

    @watchfor.deleter
    def watchfor(self):
        self.watchfor = ''

    @property
    def ignore_case(self) -> bool:
        """whether instance will be case sensitive"""
        return self._ignore_case

    @ignore_case.setter
    def ignore_case(self, value: bool):
        if value != self._ignore_case:
            self._ignore_case = value
            # regenerate pattern
            self.watchfor = self.watchfor.pattern

    @property
    def contents(self) -> List[str]:
        """Finds all instances of the watchfor item in the path"""
        # todo make this less arduous for large directories
        path = self.full_path
        contents = []

        if self.includesubfolders is True:
            for root, dirs, files in os.walk(path):  # walk through specified path
                dirs[:] = [d for d in dirs if d not in self.exclude_subfolders]
                if self.watch_type == 'file':
                    for filename in files:  # check each file
                        if self._condition_match(filename) is not None:  # search for pattern match
                            file_path = os.path.join(root, filename)
                            if os.path.isfile(file_path) is True:  # ensure file
                                contents.append(file_path)
                elif self.watch_type == 'folder':
                    for directory in dirs:
                        if self._condition_match(directory) is not None:
                            dir_path = os.path.join(root, directory)
                            if os.path.isdir(dir_path) is True:  # ensure directory
                                contents.append(dir_path)
        else:
            for file in os.listdir(path):
                if self._condition_match(file) is not None:
                    file_path = os.path.join(path, file)
                    if self.watch_type == 'file' and os.path.isfile(file_path):
                        contents.append(file_path)
                    elif self.watch_type == 'folder' and os.path.isdir(file_path):
                        contents.append(file_path)
        return contents

    def _condition_match(self, string: str) -> Match:
        """
        Performs the condition match on the provided string

        :param string: string to perform match/search against
        :return: match or none
        """
        if self.match_exact is True:
            return self.watchfor.match(string)
        else:
            return self.watchfor.search(string)

    def check_path_for_files(self):
        """Finds all instances of the watchfor item in the path"""
        warnings.warn('The check_path_for_files method has be depreciated, access .contents directly',
                      DeprecationWarning)
        return self.contents

    def find_subfolder(self):
        """returns the subdirectory path within the full path where the target file is"""
        path = self.full_path
        contents = []
        for root, dirs, files in os.walk(path):  # walk through specified path
            for filename in files:  # check each file
                if self._condition_match(filename) is not None:
                    # todo catch file/folder?
                    contents.append(root)
        return contents

    def wait_for_presence(self, waittime=1.) -> List[str]:
        """waits for a specified match to appear in the watched path"""
        contents = self.contents
        while len(contents) == 0:
            time.sleep(waittime)
            contents = self.contents
        return contents

    def oldest_instance(self, wait=False, **kwargs):
        """
        Retrieves the first instance of the watched files.

        :param wait: if there are no instances, whether to wait for one to appear
        :return: path to first instance (None if there are no files present)
        """
        contents = self.contents
        if len(contents) == 0:  # if there are no files
            if wait is True:  # if waiting is specified
                contents = self.wait_for_presence(**kwargs)
            else:  # if no wait and no files present, return None
                return None
        if len(contents) == 1:  # if there is only one file
            return contents[0]
        else:  # if multiple items in list
            return min(  # return path to oldest (last modified) file in directory
                zip(
                    contents,  # files in directory
                    [  # last modifiation time for files in directory
                        os.path.getmtime(
                            os.path.join(self._path, filename)
                        ) for filename in self.contents
                    ]
                ),
                key=lambda x: x[1]
            )[0]

    def newest_instance(self):
        """
        Retrieves the newest instance of the watched files.

        :return: path to newest instance
        :rtype: str
        """
        contents = self.contents
        if len(contents) == 0:  # if there are no files
            # if wait is True:  # if waiting is specified
            #     self.wait_for_presence(**kwargs)
            # else:  # if no wait and no files present, return None
            return None
        if len(contents) == 1:  # if there is only one file
            return self.contents[0]
        else:  # if multiple items in list
            return max(  # return path to oldest (last modified) file in directory
                zip(
                    self.contents,  # files in directory
                    [os.path.getmtime(  # last modifiation time for files in directory
                        os.path.join(self._path, filename)
                    ) for filename in self.contents]
                ),
                key=lambda x: x[1]
            )[0]


class Component:
    def __init__(self,
                 name: str,
                 path: str,
                 ):
        """
        Class that Folder inherits from, created in case there are other components to be tracked in folders in the
        future, such as files.

        On instantiation, create and save the component at the path specified. If there is something already there at
        the path, then update the name and path by appending "_copy_#" where # is a number to the end of the name and
        path of the component

        :param str, name: name of the component
        :param str, path: path to save the component in. The last part of the path must be the name of the component
        """
        self._name = name
        self._path = path
        self._parent = None  # parent Component this component belongs to; can be set to None if it is the first
        # component being made

        try:
            self.save_to_disk()
        except FileExistsError as error:
            # rename the component to something else
            for i in range(50):  # the 50 here means that if something already exists at the path, to try to add
                # '_copy_#' up to # == 50 to the end of the name and path so that the component can actually be saved
                try:
                    old_name = self.name
                    old_path = self.path
                    new_name = old_name + f'_copy_{i}'
                    new_path = old_path + f'_copy_{i}'
                    self.name = new_name
                    self.path = new_path
                    self.save_to_disk()
                    break
                except FileExistsError as error:
                    self.name = old_name
                    self.path = old_path

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self,
             value: str):
        if isinstance(value, str) is False:
            raise TypeError('value must be of type string')
        self._name = value

    @name.deleter
    def name(self) -> None:
        self._name = None

    @property
    def path(self) -> str:
        return self._path

    @path.setter
    def path(self,
             value: str):
        if isinstance(value, str) is False:
            raise TypeError('value must be of type string')
        self._path = value

    @path.deleter
    def path(self) -> None:
        self._path = None

    @property
    def parent(self) -> str:
        return self._parent

    @parent.setter
    def parent(self,
               value: str):
        if isinstance(value, str) is False:
            raise TypeError('value must be of type string')
        self._parent = value

    @parent.deleter
    def parent(self) -> None:
        self._parent = None

    def save_to_disk(self):
        """
        Actually create the component on the computer at its path with its name
        :return:
        """

        raise NotImplementedError

    def delete_from_disk(self):
        """
        Actually delete the component from the computer
        :return:
        """
        shutil.rmtree(path=self.path)


class Folder(Component):
    """
    Class to create and store a folder hierarchy and to easily create folders and access paths to save files and
    folders in

    Example using the Folder class - run each line one at a time to see changes to disk:

    root_path = os.getcwd()

    test_folder_name = 'test'
    test_folder_path = os.path.join(root_path, test_folder_name)

    test_folder = Folder(folder_name=test_folder_name, folder_path=test_folder_path)

    sub_folder_one = test_folder.make_and_add_sub_folder(sub_folder_name='sub_folder_one')
    sub_folder_two = test_folder.make_and_add_sub_folder(sub_folder_name='sub_folder_two')
    sub_sub_folder_one = sub_folder_one.make_and_add_sub_folder(sub_folder_name='sub_sub_folder_one')

    sub_folder_one.delete_from_disk()
    sub_folder_two.delete_from_disk()

    test_folder_two = Folder(folder_name=test_folder_name, folder_path=test_folder_path)

    test_folder.delete_from_disk()
    test_folder_two.delete_from_disk()

    """

    def __init__(self,
                 folder_name: str,
                 folder_path: str,
                 ):
        """
        A folder can have files and folders in it, but for now just care about it containing folders. The name of the
        folder should be the same as the last part of the folder path.

        :param str, folder_path: path to save the folder on disk
        :param str, folder_name: Should be the same as the last part of the folder path
        """
        super().__init__(
            name=folder_name,
            path=folder_path
        )
        self._children = set()

    @property
    def children(self) -> set:
        return self._children

    @children.setter
    def children(self,
                 value: set):
        if isinstance(value, set) is False:
            raise TypeError('value must be of type set')
        self._children = value

    @children.deleter
    def children(self) -> None:
        self._children = set()

    def save_to_disk(self):
        os.makedirs(
            name=self.path,
        )

    def delete_from_disk(self):
        super().delete_from_disk()

    def add_child_component(self,
                            component: Component,
                            ):
        """
        Add a component to the set of children and set the parent of the child component to be this folder

        :param Component, component:
        :return:
        """
        self.children.add(component)
        component.parent = self

    def remove_and_delete_component(self,
                                    component: Component,
                                    ):
        """
        Remove a child component from the children set and delete it from disk

        :param Component, component:
        :return:
        """
        self.children.remove(component)
        component.delete_from_disk()

    def make_and_add_sub_folder(self,
                                sub_folder_name: str,
                                ):
        """
        Create a sub-folder with a given name under the main folder; the path of the sub-folder is the name of the
        sub-folder concatenated on to the end of the path of the main folder

        :return: Folder, sub_folder: the sub-folder that was created
        """

        if sub_folder_name in self.children:
            raise Exception(f'Main folder already has a sub-folder called {sub_folder_name}')
        else:
            parent_folder_path = self.path
            sub_folder_path = os.path.join(
                parent_folder_path,
                sub_folder_name
            )
            sub_folder = Folder(
                folder_name=sub_folder_name,
                folder_path=sub_folder_path,
            )
            sub_folder.parent = self

            self.add_child_component(component=sub_folder)

        return sub_folder

