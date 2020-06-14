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
File I/O primitives, the ``File`` wrapper class and related exception classes. The
primitives use the codecs based on the :py:class:`~ansar.codec.Codec` class, to
transfer object representations to and from file storage. The class provides for
one-time description of a file and its contents.

.. autoclass:: FileFailure

.. autoclass:: FileNotFound

.. autoclass:: FileNoAccess

.. autoclass:: FileNotAFile

.. autoclass:: FileIoFailed

.. autoclass:: FileEncoding

.. autoclass:: File
   :members:
   :no-undoc-members:

.. autofunction:: read_from_file

.. autofunction:: write_to_file
"""
__docformat__ = 'restructuredtext'

__all__ = [
    'FileFailure',
    'FileNotFound',
    'FileNoAccess',
    'FileNotAFile',
    'FileIoFailed',
    'FileEncoding',
    'File',
    'read_from_file',
    'write_to_file',
]

import os
import errno

from .memory import *
#from .runtime import *
from .message import *
from .codec import *
from .json import *


# Exceptions.
class FileFailure(Exception):
    '''
    Base exception for all file operation errors.

    Parameters:

    - `what`, operation that failed.
    - `name`, the name of the file.
    - `note`, a short explanation.
    - `code`, the underlying system error.
    '''
    def __init__(self, what, name, note, code):
        self.what = what
        self.name = name
        self.note = note
        self.code = code

    def __str__(self):
        if self.code == 0:
            s = 'cannot %s "%s", %s' % (self.what, self.name, self.note)
        else:
            s = 'cannot %s "%s", %s (%s)' % (self.what, self.name, self.note, self.code)
        return s

class FileNotFound(FileFailure):
    '''
    The named file did not exist. This was not due to access,
    permissions or device errors. Derived from :py:class:`~ansar.file.FileFailure`.
    '''
    def __init__(self, what, name, note, code=0):
        FileFailure.__init__(self, what, name, note, code)

class FileNoAccess(FileFailure):
    '''
    No access or a permissions problem. Derived from :py:class:`~ansar.file.FileFailure`.
    '''
    def __init__(self, what, name, note, code=0):
        FileFailure.__init__(self, what, name, note, code)

class FileNotAFile(FileFailure):
    '''
    The name exists but cannot be used. It either refers to a folder, or the path includes
    a non-folder. Derived from :py:class:`~ansar.file.FileFailure`.
    '''
    def __init__(self, what, name, note, code=0):
        FileFailure.__init__(self, what, name, note, code)

class FileAlreadyExists(FileFailure):
    '''
    The named file already exists. Derived from :py:class:`~ansar.file.FileFailure`.
    '''
    def __init__(self, what, name, note, code=0):
        FileFailure.__init__(self, what, name, note, code)

class FileIoFailed(FileFailure):
    '''
    A device I/O operation failed. Derived from :py:class:`~ansar.file.FileFailure`.
    '''
    def __init__(self, what, name, note, code=0):
        FileFailure.__init__(self, what, name, note, code)

class FileEncoding(FileFailure):
    '''
    File or object content problem. Encoding or decoding failed.
    '''
    def __init__(self, what, name, note):
        FileFailure.__init__(self, what, name, note, 0)

#
#
class File(object):
    '''
    Thinnest layer over the 2 file I/O primitives. This object
    remembers a name and serialization parameters in one place.
    The 2 I/O methods can then be used repeatedly with the
    assurance that those details remain the same.

    Parameters:

    - `name`, the name of the file.
    - `message_type`, a registered message type.
    - `encoding`, one of the codec-bases classes.
    - `create_default`, auto-generate a value if the file does not exist.
    - `pretty_format`, generate a human-readable layout.
    - `decorate_names`, auto-append a dot-extent suffix based on the encoding.
    '''
    def __init__(self, name, message_type, encoding=None, create_default=False, pretty_format=True, decorate_names=True):
        self.name = name
        self.message_type = fix_type(message_type)
        self.encoding = encoding
        self.create_default = create_default
        self.pretty_format = pretty_format
        self.decorate_names = decorate_names

    def recover(self):
        '''
        Read the named file and decode the contents. This method
        passes all the deserialization parameters from the ``File``
        object, to the :py:func:`~ansar.file.read_from_file` primitive.

        Parameters:

        - none

        Returns:

        A 2-tuple of `message` and `version`.
        '''
        try:
            m, v = read_from_file(self.message_type, self.name, encoding=self.encoding, decorate_names=self.decorate_names)
            return m, v
        except FileNotFound:
            if self.create_default:
                c = self.message_type
                d = from_memory(c)
                return d, None
            raise
        return m, v

    def store(self, m):
        '''
        Encode the supplied message and write to the named file. This
        method passes all the serialization parameters from the ``File``
        object, to the :py:func:`~ansar.file.write_to_file` primitive.

        Parameters:

        - `m`, the message to be stored.

        Returns:

        None.
        '''
        write_to_file(m, self.name, message_type=self.message_type, encoding=self.encoding,
            decorate_names=self.decorate_names, pretty_format=self.pretty_format)


# The primitives.
def read_from_file(message_type, name, encoding=None, what=None, **kv):
    '''
    Recover a message previously written by the
    :py:func:`~ansar.file.write_to_file` function. This
    produces a 2-tuple of `message` and `version`, or
    fails with an exception.

    Additional key-value parameters are passed on to
    the construction of a :py:class:`~ansar.codec.Codec`,
    e.g. ``decorate_names=False``.

    Parameters:

    - `message_type`, a composition of :py:mod:`~ansar.memory`.
    - `name`, the name of the file to read.
    - `encoding`, a :py:mod:`~ansar.codec` class.
    - `what`, purpose of the read, for error messages.
    - `kv`, additional parameters passed to the codec.

    Returns:

    - a 2-tuple of `message` and `version`.
    '''    
    encoding = encoding or CodecJson
    encoding = encoding(**kv)

    # What is the caller up to;
    # Cannot read from /home/root (access or permissions) 
    what = what or 'read from'

    # Add the encoding suffix according
    # to automation settings.
    name = encoding.full_name(name)

    try:
        f = open(name, 'r')
    except IOError as e:
        if e.errno == errno.ENOENT:
            raise FileNotFound(what, name, 'name does not exist', e.errno)
        elif e.errno in (errno.EACCES, errno.EPERM):
            raise FileNoAccess(what, name, 'access or permissions', e.errno)
        elif e.errno == errno.ENOTDIR:
            raise FileNotAFile(what, name, 'name in path is not a folder', e.errno)
        elif e.errno == errno.EISDIR:
            raise FileNotAFile(what, name, 'name refers to a folder', e.errno)
        raise

    try:
        s = f.read()
    except IOError as e:
        if e.errno == errno.EIO:
            raise FileIoFailed(what, name, 'device I/O failed', e.errno)
        raise
    finally:
        f.close()

    try:
        d, v = encoding.decode(s, message_type)
    except CodecFailed as e:
        s = str(e)
        raise FileEncoding(what, name, s)
    return d, v

#
#
def write_to_file(a, name, message_type=None, encoding=None, what=None, pretty_format=True, **kv):
    '''
    Store a message into the named file. This silently
    succeeds or fails with an exception.

    Additional key-value parameters are passed on to
    the construction of a :py:class:`~ansar.codec.Codec`,
    e.g. ``decorate_names=False``.

    Parameters:

    - `message_type`, a composition of :py:mod:`~ansar.memory`.
    - `name`, the name of the file to read.
    - `encoding`, a :py:mod:`~ansar.codec` class.
    - `what`, purpose of the read, for error messages.
    - `pretty_format`, also passed to the codec but default set here.
    - `kv`, additional parameters passed to the codec.

    Returns:

    None.
    '''    
    kv['pretty_format'] = pretty_format
    encoding = encoding or CodecJson
    encoding = encoding(**kv)
    what = what or 'write to'

    # Add the encoding suffix according
    # to automation settings.
    name = encoding.full_name(name)

    if message_type is None:
        if not isinstance(a, Message):
            raise FileFailure(what, name, 'type required for non-message', code=0)
        message_type = UserDefined(a.__class__)

    try:
        s = encoding.encode(a, message_type)
    except CodecFailed as e:
        s = str(e)
        raise FileEncoding(what, name, s)

    try:
        # json.dumps produces a str that the file
        # module will not write to a binary handle.
        # Fair enough.
        f = open(name, 'w')
    except IOError as e:
        if e.errno == errno.ENOENT:
            # Not sure this happens, but cover the
            # case anyway.
            raise FileNotFound(what, name, 'name does not exist', e.errno)
        elif e.errno == errno.EEXIST:
            raise FileAlreadyExists(what, name, 'name already exists', e.errno)
        elif e.errno in (errno.EACCES, errno.EPERM):
            raise FileNoAccess(what, name, 'access or permissions', e.errno)
        elif e.errno == errno.ENOTDIR:
            raise FileNotAFile(what, name, 'name in path is not a folder', e.errno)
        elif e.errno == errno.EISDIR:
            raise FileNotAFile(what, name, 'name refers to a folder', e.errno)
        raise

    try:
        f.write(s)
    except IOError as e:
        if e.errno == errno.EIO:
            raise FileIoFailed(what, name, 'device I/O failed', e.errno)
        raise
    finally:
        f.close()
