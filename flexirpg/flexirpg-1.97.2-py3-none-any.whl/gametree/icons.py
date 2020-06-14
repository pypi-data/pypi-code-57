# Tree icon management.
#
# Copyright (C) 2011 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

from orpg.orpg_wx import *
from orpg.orpg_windows import *
from orpg.orpgCore import open_rpg
import orpg.dirpath

class node_icons(wx.ImageList):
    def __init__(self):
        wx.ImageList.__init__(self, 16, 16, False)

        self._icons = {}
        self._images = []
        self._names = []

        try:
            xml_dom = orpg.orpg_xml.parse_file(orpg.dirpath.dir_struct["icon"] + "icons.xml")
        except IOError:
            return
        except:
            raise

        for n in xml_dom.getElementsByTagName('icon'):
            key = n.getAttribute("name")
            path = orpg.dirpath.dir_struct["icon"] + n.getAttribute("file")
            try:
                img = wx.Image(path, wx.BITMAP_TYPE_ANY)
                self._images.append(img)
                self._icons[key] = self.Add(wx.Bitmap(img))
                self._names.append(key)
            except IOError:
                pass

    def __getitem__(self, icon_name):
        icon = self._icons.get(icon_name)
        if not icon:
            icon = self._icons.get("default")
        return icon

    def __contains__(self, icon_name):
        return icon_name in self._icons

    def count(self):
        return len(self._images)

    def name(self, index):
        return self._names[index]

    def image(self, index):
        return self._images[index]
