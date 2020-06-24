'''
This submodule contains the read directory function, a helper function so that the
contents of a whole directory can be passed into the Documentation object. It also
contains the FileInfo object. This is used to specify information about files that
are input into and output from BuildUp.
'''
import os
import re
import logging

_LOGGER = logging.getLogger('BuildUp')

def _pop_starting_with(pathlist, beginning):
    poplist = []
    for n, path in enumerate(pathlist):
        if path.startswith(beginning):
            poplist.append(n)
    #Pop them from the directory list in reverse order to keep indexes valid
    for n in poplist[::-1]:
        pathlist.pop(n)

def read_directory(path='.',
                   exclude_list=None,
                   allow_hidden=False,
                   allow_leading_underscore=False):

    '''
    Recursively walks a directory and returns a list of all files as
    FileInfo objects. These objects contain only the path for all files
    except buildup files where they contain the contents of the file.
    '''

    if exclude_list is None:
        exclude_list = []

    directory_files = []
    for root, dirs, files in os.walk(path):
        #find any hidden unix directories/files (inc .git) and
        #any beginning with an underscore

        if not allow_hidden:
            _pop_starting_with(dirs, '.')
            _pop_starting_with(files, '.')
        if not allow_leading_underscore:
            _pop_starting_with(dirs, '_')
            _pop_starting_with(files, '_')

        for file in files:
            if not os.path.basename(file) in exclude_list:
                page_path = os.path.join(root, file)
                page_path_rel = os.path.relpath(page_path, start=path)
                _warn_unsafe(page_path_rel)
                if file.endswith((".md", '.yml', '.yaml')):
                    with open(page_path, 'r', encoding='utf-8') as stream:
                        directory_files.append(FileInfo(page_path_rel,
                                                        dynamic_content=True,
                                                        content=stream.read()))
                else:
                    directory_files.append(FileInfo(page_path_rel))
    return directory_files

def _warn_unsafe(path):
    unsafe = re.findall(r'[^a-zA-z0-9\.\\\/\-_~ ]', path)
    if len(unsafe) > 0:
        char_string = ''.join(set(unsafe))
        _LOGGER.warning('The unsafe characters %s detected in the filename "%s". '
                        'This may cause unexpected behaviour.',
                        char_string,
                        path)


class FileInfo():
    """
    Class files input into the BuildUp and the files in after building
    `path` is the path of the file relative to the root documentation directory. This
    must be relative and link to a file inside the root, BuildUp does not recognise
    files outside of root. Use `location_on_disk` to spoof the location of a file elsewhere.
    `dynamic_content` should be True for file that buildup can process, or any file
    that buildup generates.
    File a file that build up doesn't process the `location_on_disk` can be set,
    as default this is assumed to be the path. This is None if `dynamic_content` is True
    `content` is none if `dynamic_content` is False, else it is the contents of the buildup
    file.
    """

    def __init__(self, path, location_on_disk=None, dynamic_content: bool = False, content=None):

        self._path = os.path.normpath(path)
        if os.path.isabs(self._path):
            raise RuntimeError('FileInfo objects cannot specify paths outside the build'
                               ' directory.')

        self._dynamic_content = bool(dynamic_content)

        if self._dynamic_content:
            self._location_on_disk = None
            if content is None:
                raise RuntimeError('Buildup file must have a content string')
            self._content = str(content)
        else:
            self._content = None
            if location_on_disk is None:
                self._location_on_disk = self._path
            else:
                self._location_on_disk = os.path.normpath(location_on_disk)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str(self.as_dict())

    def __eq__(self, obj):
        if isinstance(obj, str):
            return self.path == os.path.normpath(obj)
        if isinstance(obj, FileInfo):
            #This is a bit of a hack, should implement a file hash
            if self.path != obj.path:
                return False
            if self.dynamic_content != obj.dynamic_content:
                return False
            if self.location_on_disk != obj.location_on_disk:
                return False
            # if everything else matches return if the contents are equal
            return self.content == obj.content
        #equality not implemented for all other types
        return NotImplemented

    @property
    def dynamic_content(self):
        '''False if the output file is just a coppied file
        True if the content is dynamic_content by gitbuilding'''
        return self._dynamic_content

    @property
    def path(self):
        '''
        The output path of the file relative to the output directory or
        server root
        '''
        if self._path.startswith('..'):
            return os.path.join('orphaned_files', os.path.basename(self._path))
        return self._path

    @property
    def location_on_disk(self):
        '''
        The current location of the file. This is None if the output
        content is dynamic_content.
        '''
        return self._location_on_disk

    @property
    def content(self):
        '''
        Returns the content of the file (this is only valid if `dynamic_content` is True)
        '''
        return self._content

    def as_dict(self):
        '''
        Serialise the file object as a dictionary
        '''
        output = {'path': self.path,
                  'dynamic_content': self._dynamic_content}
        if self.dynamic_content:
            output['content'] = self._content
        else:
            output['location_on_disk'] = self._location_on_disk
        return output
