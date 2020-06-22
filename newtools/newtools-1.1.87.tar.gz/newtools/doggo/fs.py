# (c) 2012-2020 Dativa, all rights reserved
# -----------------------------------------
#  This code is licensed under MIT license (see license.txt for details)

"""

         ,--._______,-.
       ,','  ,    .  ,_`-.
      / /  ,' , _` ``. |  )       `-..
     (,';'""`/ '"`-._ ` `/ ______    \\
       : ,o.-`- ,o.  )`` -'      `---.))
       : , d8b ^-.   '|   `.      `    `.
       |/ __:_     `. |  ,  `       `    \
       | ( ,-.`-.    ;'  ;   `       :    ;
       | |  ,   `.      /     ;      :    \
       ;-'`:::._,`.__),'             :     ;
      / ,  `-   `--                  ;     |
     /  `                   `       ,      |
    (    `     :              :    ,`      |
     `   `.    :     :        :  ,'  `    :
      `    `|-- `     ` ,'    ,-'     :-.-';
      :     |`--.______;     |        :    :
       :    /           |    |         |   \
       |    ;           ;    ;        /     ;
     _/--' |   -hrr-   :`-- /         `_:_:_|
   ,',','  |           |___ \
   `^._,--'           / , , .)
                      `-._,-'
"""

import shutil
import os
from glob import glob
import logging
from time import sleep, time
from random import random

from newtools.optional_imports import s3fs
from newtools.aws import S3Location
from .doggo import FileDoggo

logger = logging.getLogger("newtools.doggo.fs")


class DoggoFileSystem:
    """
    Implements common file operations using either S3 or local file system depending on whether the path
    begins "s3://"

    """
    __s3fs = None

    @property
    def _s3fs(self):
        """
        S3FS caching does not respect other applications updating S3 so therefore we invalidate
        the cache before using

        :return: the S3FS File system
        """
        if self.__s3fs is None:
            s3fs.S3FileSystem.read_timeout = 600
            self.__s3fs = s3fs.S3FileSystem()

        self.__s3fs.invalidate_cache()
        return self.__s3fs

    def _is_s3(self, path1, path2=None):
        """

        :param path1: the first path to check
        :param path2: the second path to check
        :return: True if both are S3, False if neither are, and raises an exception for mixed types
        """
        p1_s3 = path1.startswith("s3://")
        p2_s3 = p1_s3 if path2 is None else path2.startswith("s3://")

        if p1_s3 != p2_s3:
            raise NotImplementedError("DoggoFileSystem does not support copying between S3 and local")
        if path2 is not None:
            return path1.startswith("s3://") and path2.startswith("s3://")
        else:
            return path1.startswith("s3://")

    def _check_folders(self, path):
        if not self._is_s3(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)

    def cp(self, source, destination):
        """
        Copies a file

        :param source: source path
        :param destination: destination path
        """
        if self._is_s3(source, destination):
            return self._s3fs.cp(source, destination)
        else:
            self._check_folders(destination)
            return shutil.copy(source, destination)

    def mv(self, source, destination):
        """
        Moves a file

        :param source: source path
        :param destination: destination path
        """
        if self._is_s3(source, destination):
            return self._s3fs.mv(source, destination)
        else:
            self._check_folders(destination)
            return shutil.move(source, destination)

    def exists(self, path):
        """
        :param path: the path to check
        :return: True if the path exists, otherwise False
        """
        if self._is_s3(path):
            return self._s3fs.exists(path)
        else:
            return os.path.exists(path)

    def size(self, path):
        """
        :param path: the path to check
        :return: the size of the file at this path
        """
        if self._is_s3(path):
            return self._s3fs.size(path)
        else:
            return os.path.getsize(path)

    def rm(self, path):
        """
        Removes a file

        :param path: the file to remove
        """
        if self._is_s3(path):
            return self._s3fs.rm(path)
        else:
            return os.remove(path)

    def glob(self, glob_string):
        """
        Searched for a file using glob syntax with recursive set to True

        :param glob_string: the path to search
        :return:
        """
        if self._is_s3(glob_string):
            return [S3Location(a) for a in self._s3fs.glob(glob_string)]
        else:
            return glob(glob_string, recursive=True)

    def open(self, path, mode, *args, **kwargs):
        """
        Opens a file

        :param path: the path to open
        :param mode: the mode to open in
        :param args: any arguments in the FileDoggo class
        :param kwargs: any keyword arguments for the FileDoggo class
        :return: a file handle
        """
        if "w" in mode:
            self._check_folders(path)
        return FileDoggo(path, mode, *args, **kwargs)

    def join(self, path, *paths):
        if self._is_s3(path):
            return S3Location(path).join(*paths)
        else:
            return os.path.join(path, *paths)

    def split(self, path):
        if self._is_s3(path):
            loc = S3Location(path)
            if loc.prefix is not None:
                return S3Location(loc.bucket).join(loc.prefix), loc.file
            else:
                return S3Location(loc.bucket), loc.file
        else:
            return os.path.split(path)


class DoggoWait:
    def __init__(self, wait_period, time_out_seconds):
        """
        Implements generic wait and timeout functions.

        :param wait_period: the period to wait for between iterations
        :param time_out_seconds: the time after which a TimeoutError is raised
        """
        self.time_out_seconds = time_out_seconds
        self.wait_period = wait_period
        self._timeout = None

    def wait(self):
        """
        Waits for the defined period
        """
        sleep(self.wait_period)

    def start_timeout(self):
        """
        Starts a time out
        """
        self._timeout = time() + self.time_out_seconds

    def timed_out(self):
        """
        Checks for a time out

        :return: true if the timer has timed out, otherwise false
        """
        if self._timeout is not None:
            return time() > self._timeout
        else:
            raise ValueError("Someone has tried to call timed_out() before calling start_timeout()")

    def check_timeout(self):
        """
        Waits, and raises an exception if the timer has timed out
        """
        self.wait()
        if self.timed_out():
            raise TimeoutError("Timed out waiting for completion")


class DoggoLock:
    def __init__(self, file, wait_period=30, time_out_seconds=1800, maximum_age=3600):
        """
        Locks a file across multiple process and clients using an additional file on the file system.

        Includes waits for eventual consistency

        :param file: the file to lock
        :param wait_period: the period to wait before confirming file lock
        :param time_out_seconds: the time out to stop waiting after
        :param maximum_age: the maximum age of lock files to respect
        """
        self.dfs = DoggoFileSystem()
        self.dw = DoggoWait(wait_period, time_out_seconds)

        self.file = file
        self.lock_file = None
        self.lock_file_glob = self._get_lock_path(get_glob=True)
        self.maximum_age = maximum_age

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def acquire(self):
        # If the file is locked then wait for it to be unlocked
        self.dw.start_timeout()
        while len(self._get_lock_files()) > 0:
            self.dw.check_timeout()

        # create a lock file and wait to avoid contention
        self._create_lock_file()
        self.dw.wait()

        # wait until we are the earliest lock file
        self.dw.start_timeout()
        while self.lock_file != self._get_lock_files()[0]:  # pragma: no cover
            self.dw.check_timeout()  # exclude from coverage as only executed multi-threaded

    def release(self):
        if self.lock_file is not None:
            self.dfs.rm(self.lock_file)
        self.lock_file = None

    def _timestamp_is_valid(self, lock_file):
        timestamp = float(lock_file.split(".")[-1].split('-')[0])

        return timestamp > time() - self.maximum_age

    def _generate_lock_files(self):
        for file in sorted(self.dfs.glob(self.lock_file_glob)):
            if self._timestamp_is_valid(file):
                yield file

    def _get_lock_files(self):
        return [a for a in self._generate_lock_files()]

    def _get_lock_path(self, get_glob=False):
        file_path = self.dfs.split(self.file)
        if get_glob:
            return self.dfs.join(
                    file_path[0],
                    ".lock-{file}**".format(
                        file=file_path[1]))
        else:
            return self.dfs.join(
                    file_path[0],
                    ".lock-{file}.{timestamp}-{random}".format(
                        file=file_path[1],
                        timestamp=str(time()).replace(".", "-"),
                        random=str(random()).replace(".", "-")))

    def _create_lock_file(self):
        if self.lock_file is None:
            self.lock_file = self._get_lock_path()

        with self.dfs.open(self.lock_file, mode="wb") as f:
            f.write(b"woof!")
