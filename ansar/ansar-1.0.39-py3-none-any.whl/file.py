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
from .message import *
from .codec import *
from .json import *


# Exceptions.
class FileFailure(Exception):
    '''Base exception for all file exceptions.
    
    :param what: the failed operation
    :type what: str
    :param name: the name of the file
    :type name: str
    :param note: a short, helpful description
    :type note: str
    :param code: the associated low-level, integer, error code
    :type code: int
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
    'The named file did not exist.'
    def __init__(self, what, name, note, code=0):
        FileFailure.__init__(self, what, name, note, code)

class FileNoAccess(FileFailure):
    'No access or a permissions problem.'
    def __init__(self, what, name, note, code=0):
        FileFailure.__init__(self, what, name, note, code)

class FileNotAFile(FileFailure):
    'Refers to a folder or the path includes a non-folder.'
    def __init__(self, what, name, note, code=0):
        FileFailure.__init__(self, what, name, note, code)

class FileAlreadyExists(FileFailure):
    'The named file already exists.'
    def __init__(self, what, name, note, code=0):
        FileFailure.__init__(self, what, name, note, code)

class FileIoFailed(FileFailure):
    'A device I/O operation failed.'
    def __init__(self, what, name, note, code=0):
        FileFailure.__init__(self, what, name, note, code)

class FileEncoding(FileFailure):
    'File or object content problem, encoding or decoding failed.'
    def __init__(self, what, name, note):
        FileFailure.__init__(self, what, name, note, 0)

#
#
class File(object):
    '''Store and recover application values using files.

    :param name: the name of the file
    :type name: str
    :param te: formal description of the content
    :type te: :ref:`type expression<type-expressions>`
    :param encoding: selection of representation, defaults to ``CodecJson``
    :type encoding: class
    :param create_default: return default instance on file not found, defaults to ``False``
    :type create_default: bool
    :param pretty_format: generate human-readable file contents, defaults to ``True``
    :type pretty_format: bool
    :param decorate_names: auto-append an encoding-dependent extension to the file name, defaults to ``True``
    :type decorate_names: bool
    '''
    def __init__(self, name, te, encoding=None, create_default=False, pretty_format=True, decorate_names=True):
        self.name = name
        self.te = fix_type(te)
        self.encoding = encoding
        self.create_default = create_default
        self.pretty_format = pretty_format
        self.decorate_names = decorate_names

    def store(self, value):
        '''Generate a representation of ``value`` and write to the saved ``name``.
        
        :param value: any application value matching the saved `te`
        :return: none
        '''
        write_to_file(value, self.name, te=self.te, encoding=self.encoding,
            decorate_names=self.decorate_names, pretty_format=self.pretty_format)

    def recover(self):
        '''Read from the saved ``name``, parse and marshal into an application value.
        
        :return: A 2-tuple of an application value and a version.
        :rtype: a value matching the saved ``te`` and a ``str``
        '''
        try:
            m, v = read_from_file(self.te, self.name, encoding=self.encoding, decorate_names=self.decorate_names)
            return m, v
        except FileNotFound:
            if self.create_default:
                c = self.te
                d = from_memory(c)
                return d, None
            raise
        return m, v

# The primitives.
def read_from_file(te, name, encoding=None, what=None, **kv):
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
        d, v = encoding.decode(s, te)
    except CodecFailed as e:
        s = str(e)
        raise FileEncoding(what, name, s)
    return d, v

#
#
def write_to_file(a, name, te=None, encoding=None, what=None, pretty_format=True, **kv):
    kv['pretty_format'] = pretty_format
    encoding = encoding or CodecJson
    encoding = encoding(**kv)
    what = what or 'write to'

    # Add the encoding suffix according
    # to automation settings.
    name = encoding.full_name(name)

    if te is None:
        if not isinstance(a, Message):
            raise FileFailure(what, name, 'type required for non-message', code=0)
        te = UserDefined(a.__class__)

    try:
        s = encoding.encode(a, te)
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
