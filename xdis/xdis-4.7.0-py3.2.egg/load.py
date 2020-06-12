# Copyright (c) 2015-2020 by Rocky Bernstein
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import marshal, py_compile, sys, tempfile, time
from struct import unpack, pack
import os.path as osp

import xdis.unmarshal
from xdis.version_info import PYTHON3, PYTHON_VERSION
from xdis.magics import (
    IS_PYPY3,
    PYTHON_MAGIC_INT,
    int2magic,
    magic_int2float,
    magic2int,
    magicint2version,
    versions,
)
from xdis.dropbox.decrypt25 import fix_dropbox_pyc


def check_object_path(path):
    if path.endswith(".py"):
        try:
            import importlib
            bytecode_path = importlib.util.cache_from_source(path, optimization="")
            if osp.exists(bytecode_path):
                return bytecode_path
        except:
            try:
                import imp

                imp.cache_from_source(path, debug_override=False)
            except:
                pass
            pass
        basename = osp.basename(path)[0:-3]
        if PYTHON3:
            spath = path
        else:
            spath = path.decode("utf-8")
        path = tempfile.mkstemp(prefix=basename + "-", suffix=".pyc", text=False)[1]
        py_compile.compile(spath, cfile=path, doraise=True)

    if not path.endswith(".pyc") and not path.endswith(".pyo"):
        raise ValueError("path %s must point to a .py or .pyc file\n" % path)
    return path


def is_pypy(magic_int):
    return magic_int in ((62211 + 7, 3180 + 7) + IS_PYPY3)


def load_file(filename, out=sys.stdout):
    """
    load a Python source file and compile it to byte-code
    _load_file(filename: string): code_object
    filename:	name of file containing Python source code
                (normally a .py)
    code_object: code_object compiled from this source code
    This function does NOT write any file!
    """
    fp = open(filename, "rb")
    try:
        source = fp.read()
        try:
            if PYTHON_VERSION < 2.6:
                co = compile(source, filename, "exec")
            else:
                co = compile(source, filename, "exec", dont_inherit=True)
        except SyntaxError:
            out.write(">>Syntax error in %s\n" % filename)
            raise
    finally:
        fp.close()
    return co


def load_module(filename, code_objects=None, fast_load=False, get_code=True):
    """load a module without importing it.
    Parameters:
       filename:    name of file containing Python byte-code object
                    (normally a .pyc)

       code_objects: list of additional code_object from this
                     file. This might be a types.CodeType or one of
                     the portable xdis code types, e.g. Code38, Code3,
                     Code2, etc. This can be empty

       get_code:     bool. Parsing the code object takes a bit of
                     parsing time, but sometimes all you want is the
                     module info, time string, code size, python
                     version, etc. For that, set `get_code` to
                     `False`.

    Return values are as follows:
        float_version: float; the floating-point version number for the given magic_int,
                       e.g. 2.7 or 3.4
        timestamp: int; the seconds since EPOCH of the time of the bytecode creation, or None
                        if no timestamp was stored
        magic_int: int, a more specific than version number. The actual byte code version of the
                   code object
        co         : code object
        ispypy     : True if this was a PyPy code object
        source_size: The size of the source code mod 2**32, if that was stored in the bytecode.
                     None otherwise.
        sip_hash   : the SIP Hash for the file (only in Python 3.7 or greater), if the file
                     was created with a SIP hash or None otherwise. Note that if the sip_hash is not
                     none, then the timestamp and source_size will be invalid.
    """

    # Some sanity checks
    if not osp.exists(filename):
        raise ImportError("File name: '%s' doesn't exist" % filename)
    elif not osp.isfile(filename):
        raise ImportError("File name: '%s' isn't a file" % filename)
    elif osp.getsize(filename) < 50:
        raise ImportError(
            "File name: '%s (%d bytes)' is too short to be a valid pyc file"
            % (filename, osp.getsize(filename))
        )

    with open(filename, "rb") as fp:
        return load_module_from_file_object(
            fp,
            filename=filename,
            code_objects=code_objects,
            fast_load=fast_load,
            get_code=get_code,
        )


def load_module_from_file_object(
    fp, filename="<unknown>", code_objects=None, fast_load=False, get_code=True
):
    """load a module from a file object without importing it.

    See :func:load_module for a list of return values.
    """

    if code_objects is None:
        code_objects = {}

    timestamp = 0
    try:
        magic = fp.read(4)
        magic_int = magic2int(magic)

        # For reasons I don't understand, PyPy 3.2 stores a magic
        # of '0'...  The two values below are for Python 2.x and 3.x respectively
        if magic[0:1] in ["0", b"0"]:
            magic = int2magic(3180 + 7)

        try:
            # FIXME: use the internal routine below
            float_version = magic_int2float(magic_int)
        except KeyError:
            if magic_int in (2657, 22138):
                raise ImportError("This smells like Pyston which is not supported.")

            if len(magic) >= 2:
                raise ImportError(
                    "Unknown magic number %s in %s"
                    % (ord(magic[0:1]) + 256 * ord(magic[1:2]), filename)
                )
            else:
                raise ImportError("Bad magic number: '%s'" % magic)

        if magic_int in (
            3010,
            3020,
            3030,
            3040,
            3050,
            3060,
            3061,
            3071,
            3361,
            3091,
            3101,
            3103,
            3141,
            3270,
            3280,
            3290,
            3300,
            3320,
            3330,
            3371,
            62071,
            62071,
            62081,
            62091,
            62092,
            62111,
        ):
            raise ImportError(
                "%s is interim Python %s (%d) bytecode which is "
                "not supported.\nFinal released versions are "
                "supported." % (filename, versions[magic], magic2int(magic))
            )
        elif magic_int == 62135:
            fp.seek(0)
            return fix_dropbox_pyc(fp)
        elif magic_int == 62215:
            raise ImportError(
                "%s is a dropbox-hacked Python %s (bytecode %d).\n"
                "See https://github.com/kholia/dedrop for how to "
                "decrypt." % (filename, versions[magic], magic2int(magic))
            )

        try:
            # print version
            my_magic_int = PYTHON_MAGIC_INT
            magic_int = magic2int(magic)
            version = magic_int2float(magic_int)

            timestamp = None
            source_size = None
            sip_hash = None

            ts = fp.read(4)
            if version >= 3.7:
                # PEP 552. https://www.python.org/dev/peps/pep-0552/
                pep_bits = ts[-1]
                if PYTHON_VERSION <= 2.7:
                    pep_bits = ord(pep_bits)
                if (pep_bits & 1) or magic_int == 3393:  # 3393 is 3.7.0beta3
                    # SipHash
                    sip_hash = unpack("<Q", fp.read(8))[0]
                else:
                    # Uses older-style timestamp and size
                    timestamp = unpack("<I", fp.read(4))[0]  # pep552_bits
                    source_size = unpack("<I", fp.read(4))[0]  # size mod 2**32
                    pass
            else:
                timestamp = unpack("<I", ts)[0]
                # Note: a higher magic number doesn't necessarily mean a later
                # release.  At Python 3.0 the magic number decreased
                # significantly. Hence the range below. Also note inclusion of
                # the size info, occurred within a Python major/minor
                # release. Hence the test on the magic value rather than
                # PYTHON_VERSION, although PYTHON_VERSION would probably work.
                if (
                    (3200 <= magic_int < 20121)
                    and version >= 1.5
                    or magic_int in IS_PYPY3
                ):
                    source_size = unpack("<I", fp.read(4))[0]  # size mod 2**32

            if get_code:
                if my_magic_int == magic_int:
                    bytecode = fp.read()
                    co = marshal.loads(bytecode)
                elif fast_load:
                    co = xdis.marsh.load(fp, magicint2version[magic_int])
                else:
                    co = xdis.unmarshal.load_code(fp, magic_int, code_objects)
                pass
            else:
                co = None
        except:
            kind, msg = sys.exc_info()[0:2]
            import traceback

            traceback.print_exc()
            raise ImportError(
                "Ill-formed bytecode file %s\n%s; %s" % (filename, kind, msg)
            )

    finally:
        fp.close()

    return (
        float_version,
        timestamp,
        magic_int,
        co,
        is_pypy(magic_int),
        source_size,
        sip_hash,
    )


def write_bytecode_file(bytecode_path, code, magic_int, filesize=0):
    """Write bytecode file _bytecode_path_, with code for having Python
    magic_int (i.e. bytecode associated with some version of Python)
    """
    fp = open(bytecode_path, "wb")
    try:
        if PYTHON3:
            fp.write(pack("<Hcc", magic_int, b"\r", b"\n"))
        else:
            fp.write(pack("<Hcc", magic_int, "\r", "\n"))
        fp.write(pack("<I", int(time.time())))
        if 3000 <= magic_int < 20121:
            # In Python 3 you need to write out the size mod 2**32 here
            fp.write(pack("<I", filesize))
        fp.write(marshal.dumps(code))
    finally:
        fp.close()


if __name__ == "__main__":
    co = load_file(__file__)
    obj_path = check_object_path(__file__)
    version, timestamp, magic_int, co2, pypy, source_size, sip_hash = load_module(
        obj_path
    )
    print("version", version, "magic int", magic_int, "is_pypy", pypy)
    if timestamp is not None:
        import datetime

        print(datetime.datetime.fromtimestamp(timestamp))
    if source_size is not None:
        print("source size mod 2**32: %d" % source_size)
    if sip_hash is not None:
        print("Sip Hash: 0x%x" % sip_hash)
    assert co == co2
