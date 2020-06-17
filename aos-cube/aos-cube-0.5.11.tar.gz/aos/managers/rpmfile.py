import os
import sys
import gzip
from io import BytesIO
import struct
import shutil

RPM_MAGIC = b'\xed\xab\xee\xdb'
GZIP_MAGIC = b'\x1f\x8b'


def gzip_decompress(data):
    """ Decompress data with gzip """
    gzstream = BytesIO(data)
    with gzip.GzipFile(fileobj=gzstream) as gzipper:
        data = gzipper.read()

    return data


class RPMFile():
    """ Class representing a rpm file """
    def __init__(self, rpmfile):
        self.rpmfile = rpmfile

    def is_rpm(self, fileobj):
        """ Check for rpm magic """
        lead = fileobj.read(96)
        return lead[0:4] == RPM_MAGIC

    def rpm2cpio(self):
        """ Convert rpm to cpio archive file """
        with open(self.rpmfile, "rb") as f:
            if not self.is_rpm(f):
                raise IOError("The input file is not a RPM package")
    
            data = f.read()
            idx = data.find(GZIP_MAGIC)
            if idx != -1:
                return gzip_decompress(data[idx:])
            else:
                raise IOError("Unknown compress data format")
    
            return data

    def install(self, destdir):
        if not os.path.isdir(destdir):
            os.makedirs(destdir)
  
        data = self.rpm2cpio()
        cf = CpioFile()
        cf.unpack_from(data)
        for member in cf.members:
            filename = member.name.decode()
            destfile = os.path.join(destdir, filename)
            basedir = os.path.dirname(destfile)
            if not os.path.exists(basedir):
                os.makedirs(basedir)

            with open(destfile, "wb") as f:
                f.write(member.content) 
        

class CpioFile():
    """ Class representing an entire cpio file """
    _members = []

    def __init__(self):
        self._members = []

    @property
    def members(self):
        return self._members

    @property
    def names(self):
        return [member.name.decode() for member in self.members]

    def unpack_from(self, block, offset=0):
        pointer = offset

        while 'TRAILER!!!' not in self.names:
            cm = CpioMember()
            self.members.append(cm.unpack_from(block, pointer))
            pointer += cm.size

        del self.members[-1]


class CpioMember():
    """ Class representing a member of a cpio archive """
    coder = struct.Struct(b'6s8s8s8s8s8s8s8s8s8s8s8s8s8s')
    name = None
    magic = None
    devmajor = None
    devminor = None
    ino = None
    mode = None
    uid = None
    gid = None
    nlink = None
    rdevmajor = None
    rdevminor = None
    mtime = None
    filesize = None

    def unpack_from(self, block, offset=0):
        (self.magic, ino, mode, uid,
         gid, nlink, mtime, filesize,
         devmajor, devminor, rdevmajor, rdevminor,
         namesize, check) = self.coder.unpack_from(block, offset)

        self.ino = int(ino,16)
        self.mode = int(mode,16)
        self.uid = int(uid,16)
        self.gid = int(gid,16)
        self.nlink = int(nlink,16)

        self.devmajor = int(devmajor,16)
        self.devminor = int(devminor,16)
        self.rdevmajor = int(rdevmajor,16)
        self.rdevminor = int(rdevminor,16)

        self.mtime = int(mtime,16)
        namesize = int(namesize,16)
        self.filesize = int(filesize,16)
        check = int(check,16)

        namestart = offset + self.coder.size
        nameend = namestart + namesize

        datastart = nameend + ((4 - (nameend % 4)) % 4) # pad
        dataend = datastart + self.filesize

        self.name = block[namestart:nameend - 1] # drop the null
        self.content = block[datastart:dataend]

        if check != 0:
            raise Exception("Checksum Error!")

        return self

    @property
    def size(self):
        retval = self.coder.size
        retval += len(self.name) + 1
        retval += ((4 - (retval % 4)) % 4)
        retval += self.filesize
        retval += ((4 - (retval % 4)) % 4)
        return retval
