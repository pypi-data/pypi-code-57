# Author: Scott Woods <scott.suzuki@gmail.com>
# MIT License
#
# Copyright (c) 2017, 2018, 2019, 2020 Scott Woods
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
The ``Folder`` class provides for one-time description of folder location and
contents. The description is inherited by any child objects (i.e. ``Files``
and sub-``Folders``) created, and by operations within the folder.

The class also provides for persistence of maps. Rather than using a file
to store an entire map, the ``Folder`` class can be used to store the
map on a one-file-per-entry basis.

.. autoclass:: Folder
   :members:
   :no-undoc-members:
"""

__docformat__ = 'restructuredtext'

__all__ = [
    'Folder',
]

import os
import errno
import re as regex

from .memory import *
from .runtime import *
from .message import *
from .codec import *
from .json import *
from .file import *

CREATE_FOLDER = 'create folder'
REMOVE_FOLDER = 'remove folder'
REMOVE_FILE = 'remove file'
#
#
def remove_folder(path):
    try:
        for f in os.listdir(path):
            p = os.path.join(path, f)
            if os.path.isdir(p):
                remove_folder(p)
            elif os.path.isfile(p):
                os.remove(p)
        os.rmdir(path)
    except OSError as e:
        if e.errno == errno.ENOENT:
            raise FileNotFound(REMOVE_FOLDER, p, 'name does not exist', e.errno)
        elif e.errno in (errno.EACCES, errno.EPERM):
            raise FileNoAccess(REMOVE_FOLDER, p, 'access or permissions', e.errno)
        elif e.errno == errno.ENOTDIR:
            raise FileNotAFile(REMOVE_FOLDER, p, 'name in path is not a folder', e.errno)
        raise FileFailure(REMOVE_FOLDER, p, 'unexpected platform code', code=0)

#
#
class Folder(object):
    '''
    Marks a location in the file system and saves a set of parameters for subsequent
    operations.

    This class allows for convenient creation of :py:class:`~ansar.file.File` objects
    and sub-``Folder`` objects. Those objects also inherit the relevant parameters
    saved in the parent ``Folder``, such as `pretty_format` and `decorate_names`.

    The ``Folder`` class supports the notion of a file-based collection of messages.
    An entire collection can be loaded with a single expression. Single entries can
    be modified and saved back to the associated file.

    If required, multiple collections can operate side-by-side within a single folder.
    The `re` (i.e. regular expression) parameter constrains all collection-related
    operations to those files matching the specified pattern. Multiple ``Folder``
    objects can created for the same location but with different declared `re`
    parameters.

    Folders are created in the file system as a side-effect of instantiation. This
    ensures that file operations arising from ``Folder`` hierarchies can operate
    on the assumption that the required structures are already in place.

    Parameters:

    - `path`, the unchanging location in the file system.
    - `re`, a regular expression used to filter scan results.
    - `message_type`, a registered message type.
    - `encoding`, a :py:mod:`~ansar.codec` class.
    - `pretty_format`, generate a human-readable layout.
    - `decorate_names`, auto-append a dot-extension suffix based on
      the encoding.
    - `create_default`, auto-generate a value if the file does not exist.
    - `keys_names`, a 2-tuple of functions that return a unique key or
      a unique file name, respectively.
    - `make_absolute`, convert the supplied path to an absolute path.

    The `keys_names` parameter is a 2-tuple of functions. These functions
    are applied to messages to generate a unique key (tuple[0]) or a unique
    file name (tuple[1]). A trivial example would be;

    .. code-block::

       keys_names=(lambda m: m.key, lambda m: '%08d' % (m.key,))

    By default the `path` provided to the ``Folder`` is converted to its
    absolute form, i.e. the ``..`` path will be converted to the full
    pathname of the parent folder. This ensures that all the calls to
    methods of this object will operate on the same folder, irrespective of
    how the host process may move around the file system. Setting the
    `make_absolute` value to false disables that behaviour.
    '''
    def __init__(self, path=None,
        re=None, message_type=None, encoding=None,
        pretty_format=True, decorate_names=True,
        create_default=False, keys_names=None,
        make_absolute=True):
        path = path or '.'
        if make_absolute:
            path = os.path.abspath(path)
        if message_type:
            message_type = fix_type(message_type)
        self.path = path
        if re is None:
            self.re = None
        else:
            self.re = regex.compile(re)
        self.message_type = message_type
        self.encoding = encoding or CodecJson
        self.pretty_format = pretty_format
        self.decorate_names = decorate_names
        self.create_default = create_default
        self.keys_names = keys_names


        try:
            os.makedirs(self.path)
        except OSError as e:
            if e.errno == errno.EEXIST:
                return
            elif e.errno in (errno.EACCES, errno.EPERM):
                raise FileNoAccess(CREATE_FOLDER, self.path, 'access or permissions', code=e.errno)
            elif e.errno == errno.ENOTDIR:
                raise FileNotAFile(CREATE_FOLDER, self.path, 'name in path is not a folder', code=e.errno)
            raise FileFailure(CREATE_FOLDER, self.path, 'unexpected platform code', code=e.errno)

    def folder(self, name, message_type=None, re=None, encoding=None,
        pretty_format=None, decorate_names=None, create_default=None, keys_names=None):
        '''
        Create a new ``Folder`` object representing a sub-folder at the current location. The
        new ``Folder`` inherits all the parameters from the parent. Parameters passed
        to this method override those defaults. Refer to the class documentation for
        parameter details.

        Parameters:

        - `name`, the name of the sub-folder.

        Returns:

        A ``Folder`` object referring to the named the sub-folder.
        '''
        if message_type:
            message_type = fix_type(message_type)
        message_type=message_type or self.message_type
        if re is None:
            self.re = None
        else:
            self.re = regex.compile(re)
        encoding=encoding or self.encoding
        if pretty_format is None: pretty_format = self.pretty_format
        if decorate_names is None: decorate_names = self.decorate_names
        if create_default is None: create_default = self.create_default
        keys_names=keys_names or self.keys_names

        path = os.path.join(self.path, name)
        return Folder(path, re=re, message_type=message_type, encoding=encoding,
            pretty_format=pretty_format, decorate_names=decorate_names, create_default=create_default,
            keys_names=keys_names, make_absolute=False)

    def file(self, name, message_type, encoding=None,
            pretty_format=None, decorate_names=None, create_default=None):
        '''
        Create a new :py:class:`~ansar.file.File` object representing a file at the current
        location. The new ``File`` inherits all the parameters from the parent. Parameters passed
        to this method override those defaults. Refer to the class documentation for
        parameter details.

        Parameters:

        - `name`, the name of the file.

        Returns:

        A ``File`` object ready for I/O operations.
        '''
        # Fixed in File ctor.
        # message_type = fix_type(message_type)
        encoding=encoding or self.encoding
        if pretty_format is None: pretty_format = self.pretty_format
        if decorate_names is None: decorate_names = self.decorate_names
        if create_default is None: create_default = self.create_default

        path = os.path.join(self.path, name)    # Let the I/O operation decorate.
        return File(path, message_type, encoding=encoding,
            pretty_format=pretty_format, decorate_names=decorate_names, create_default=create_default)

    def matching(self):
        '''
        A generator method used to scan the contents of the current
        folder. Each name returned is a reflection of the parameters
        passed to the ``Folder`` object (e.g. the `re` regular expression)
        and is suitable for passing to the :py:meth:`~ansar.folder.Folder.file`
        method.

        Parameters:

        None.

        Returns:

        A name detected in the folder. The name will reflect the current
        `re`, `encoding` and `decorate_names` settings, i.e. if the
        `decorate_names` parameter is true, all returned names will be
        minus their dot-extensions.
        '''
        re = self.re
        decorate_names = self.decorate_names
        extension = '.%s' % (self.encoding.EXTENSION,)
        for f in os.listdir(self.path):
            m = None
            p = os.path.join(self.path, f)
            if not os.path.isfile(p):
                continue
            if decorate_names:
                b, e = os.path.splitext(f)
                if e != extension:
                    continue
                f = b
            if re:
                m = re.match(f)
                if not m:
                    continue
            yield f

    def each(self):
        '''
        A generator function used to scan the files at the current location, producing
        a series of :py:class:`~file.File` objects. The ``matching`` method is used to
        compile the list of candidate names.

        Parameters:

        None.

        .. code-block:: python

           f = Folder(message_type=Job, keys_names=job_keys_names)
           jobs = [j.recover()[0] for j in f.each()]

        This list comprehension will load all the ``Job`` instances from
        the current folder. Note that the ``recover`` method returns a
        `message`, `version` tuple. The following fragment writes the
        collection back to the same folder ``f``.

        .. code-block:: python

           for i, j in enumerate(jobs):
               s = '%04d' % (i,)
               f.file(s).store(j)

        Returns:

        A ``File`` object.
        '''
        # Get a fresh image of folder/slice.
        # Use a snapshot for iteration to avoid
        # complications arising from changes to the folder.
        matched = [f for f in self.matching()]
        # Visit each named file.
        # Yield a file object, ready for I/O.
        for f in matched:
            yield self.file(f, self.message_type)

    def key(self, m):
        '''
        '''
        keys_names = self.keys_names
        if keys_names is None:
            raise FileFailure('compose key', self.path, 'key/name functions not set', code=0)
        return keys_names[0](m)

    def name(self, m):
        '''
        '''
        keys_names = self.keys_names
        if keys_names is None:
            raise FileFailure('compose name', self.path, 'key/name functions not set', code=0)
        return keys_names[1](m)

    def recover(self):
        '''
        A generator function used to scan the files at the current location. The
        contents of the files are recovered and returned to the caller. The ``matching``
        method is used to compile the list of candidate names.

        .. code-block:: python

           f = Folder(message_type=Job, keys_names=job_keys_names)
           jobs = {k: m for k, m, _ in f.recover()}

        This dictionary comprehension will recover all the ``Job`` instances at
        the current location and load them into a convenient key-value map.

        Parameters:

        None.

        Returns:

        A 3-tuple of `key`, `message` and `version`. The `key` has been generated
        by a call to the ``keys_names[0]`` function saved in the current
        ``Folder``. The `message` is the deserialized content of the file and
        `version` indicates the specific historical variant of the message.
        '''
        # Get a fresh image of folder/slice.
        matched = [f for f in self.matching()]
        # Visit each named file.
        # Yield the key, message, version tuple.
        for f in matched:
            io = self.file(f, self.message_type)
            m, v = io.recover()
            k = self.key(m)
            yield k, m, v

    def store(self, d):
        '''
        A method that accepts a map of messages and saves them to the current
        location, as a collection of files.

        Parameters:

        - `d`, the map of messages.

        Returns:

        Nothing.
        '''
        # Get a fresh image of folder/slice.
        matched = set(self.matching())
        stored = set()
        for k, v in d.items():
            name = self.name(v)
            io = self.file(name, self.message_type)
            io.store(v)
            stored.add(name)
        # Clean out files that look like they
        # have been previously written but are
        # no longer in the map.
        matched -= stored
        for m in matched:
            self.erase(m)

    def add(self, d, m):
        '''
        A method that accepts a map of messages and an additional, new
        instance. The message is stored in the expected file,
        overwriting any previous image.

        The `keys_names` parameter is used to acquire a key value. It is
        an error for the key to already exist in the map.

        The supplied message is inserted into the map.
        Parameters:

        - `d`, the map of messages.
        - `m`, the message to be added.

        Returns:

        Nothing.
        '''
        keys_names = self.keys_names
        if keys_names is None:
            raise FileFailure('add to', self.path, 'key/name functions not set', code=0)

        key = keys_names[0](m)
        name = keys_names[1](m)

        io = self.file(name, self.message_type)
        if key in d:
            raise FileFailure('add', io.name, 'entry already present', code=0)
        io.store(m)
        d[key] = m

    def update(self, d, m):
        '''
        A method that accepts a map of messages and a message that already
        exists within that map. The message is stored in the expected file,
        overwriting any previous image.

        The `keys_names` parameter is used to acquire a key value. It is
        an error for the key to not be present in the map.

        The map is updated with the supplied message.

        Parameters:

        - `d`, the map of messages.
        - `m`, the message to be added.

        Returns:

        Nothing.
        '''
        keys_names = self.keys_names
        if keys_names is None:
            raise FileFailure('update', self.path, 'key/name functions not set', code=0)

        key = keys_names[0](m)
        name = keys_names[1](m)

        io = self.file(name, self.message_type)
        if key not in d:
            raise FileFailure('update', io.name, 'not an existing entry', code=0)

        io.store(m)
        d[key] = m

    def remove(self, d, m):
        '''
        A method that accepts a map of messages and an additional
        instance. The file matching the instance is deleted from the
        current location and the instance is removed from the map.

        Removal of the file is based on the name value generated by the
        `keys_names[1]` function and the values of `encoding` and
        `decorate_names`.

        Removal from the map is based on the key value generated by the
        `keys_names[0]` function.

        Parameters:

        - `d`, the map of messages.
        - `m`, the message to be removed.

        Returns:

        Nothing.
        '''
        keys_names = self.keys_names
        if keys_names is None:
            raise FileFailure('remove from', self.path, 'key/name functions not set', code=0)
        key = keys_names[0](m)
        name = keys_names[1](m)

        self.erase(name)
        del d[key]

    def clear(self, d):
        '''
        A method that accepts a map of messages. The current folder is
        cleared of all associated files and the map is emptied.

        Parameters:

        - `d`, the map of messages.

        Returns:

        Nothing.
        '''
        # Brute force. Delete any candidates from
        # the folder and dump everything from the dict.
        matched = [f for f in self.matching()]
        for m in matched:
            self.erase(m)
        d.clear()

    def erase(self, name):
        '''
        The named file or folder is deleted from the folder, whichever
        is detected first.

        Parameters:

        None.

        Returns:

        True if a file or folder is deleted. False if neither is
        detected.
        '''
        path = os.path.join(self.path, name)
        name = path
        if self.decorate_names:
            name = '%s.%s' % (path, self.encoding.EXTENSION)
        if os.path.isfile(name):
            try:
                os.remove(name)
            except IOError as e:
                if e.errno == errno.ENOENT:
                    raise FileNotFound(REMOVE_FILE, name, 'name does not exist', e.errno)
                elif e.errno in (errno.EACCES, errno.EPERM):
                    raise FileNoAccess(REMOVE_FILE, name, 'access or permissions', e.errno)
                elif e.errno == errno.ENOTDIR:
                    raise FileNotAFile(REMOVE_FILE, name, 'name in path is not a folder', e.errno)
                raise FileFailure(REMOVE_FILE, name, 'unexpected platform code', code=0)
            return True
        elif os.path.isdir(path):
            remove_folder(path)
            return True
        return False

    def exists(self, name):
        '''
        The named file or folder is detected, whichever is detected first.

        .. code-block::

           Folder().exists('configuration')

        This returns true if the ``configuration.json`` file exists,
        or the ``configuration`` folder exists, in the current folder.

        Parameters:

        None.

        Returns:

        True if the expected name exists at the current location.
        '''
        path = os.path.join(self.path, name)
        name = path
        if self.decorate_names:
            name = '%s.%s' % (path, self.encoding.EXTENSION)
        if os.path.isfile(name):
            return True
        elif os.path.isdir(path):
            return True
        return False
