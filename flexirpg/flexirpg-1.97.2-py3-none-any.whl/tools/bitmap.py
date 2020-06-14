# Utilities for managing bitmaps
#
# Copyright (C) 2010 David Vrabel
#
import orpg.dirpath
import wx

def create_from_file(filename):
    return wx.Bitmap(orpg.dirpath.dir_struct["icon"] + filename)
