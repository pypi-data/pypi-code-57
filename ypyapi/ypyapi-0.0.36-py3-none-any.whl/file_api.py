#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2020/5/13 0:20
# @Author : yangpingyan@gmail.com
from glob import glob

def file_get_filenames(pathname, *, recursive=False):
    """Return a list of paths matching a pathname pattern.

        The pattern may contain simple shell-style wildcards a la
        fnmatch. However, unlike fnmatch, filenames starting with a
        dot are special cases that are not matched by '*' and '?'
        patterns.

        If recursive is true, the pattern '**' will match any files and
        zero or more directories and subdirectories.
        """
    return glob(pathname, recursive=False)

if __name__ == '__main__':
    print("Mission start!")
    glob('{}/*.py'.format('C:\qqcloud\github\mercari_flask'))

    print("Mission complete!")

