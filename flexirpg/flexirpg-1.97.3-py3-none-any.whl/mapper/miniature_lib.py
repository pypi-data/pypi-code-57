# FlexiRPG -- library of miniature templates.
#
# Copyright (C) 2010 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
import codecs
import os
from string import *
import json
from uuid import UUID

import wx

import orpg.dirpath
from orpg.orpgCore import open_rpg
from orpg.main import image_library

class MiniatureTemplate(object):
    def __init__(self, uuid, name):
        """Create a miniature template.

        uuid: UUID for the miniature image.
        name: Name for the miniature.

        """
        self._uuid = uuid
        self._name = name
        self._size = (20, 20) # HACK: assuming this size.
        self._serial = 0

    def __get_uuid(self):
        return self._uuid

    def __get_name(self):
        return self._name

    def __get_size(self):
        return self._size

    uuid = property(__get_uuid)
    name = property(__get_name)
    size = property(__get_size)

    def new_label(self):
        self._serial += 1
        return "%s %d" % (self.name, self._serial)

    def image(self):
        return image_library.get(self._uuid).wximage

    def tool_bitmap(self, toolbar):
        """Return bitmap suitable for a toolbar icon.

        This returns a subset of the miniature image as a wx.Bitmap.

        """
        image = self.image()
        r = wx.Rect(0, 0,
                    min(image.Width, toolbar.ToolBitmapSize.x),
                    min(image.Height, toolbar.ToolBitmapSize.y))
        return wx.Bitmap(image.GetSubImage(r))

class MiniatureLib(object):
    def __init__(self):
        """Create a miniature template library.

        The library is populated from the configuration file
        ~/.flexirpg/miniatures.json
        """
        self._library = []

        self._config_file = os.path.join(orpg.dirpath.dir_struct["user"], "miniatures.json")
        self._load()

    def _load(self):
        if not os.path.exists(self._config_file):
            return

        try:
            with codecs.open(self._config_file, "r", "utf-8") as f:
                d = json.load(f)
        except (OSError, IOError, ValueError):
            return

        for e in d:
            self._library.append(MiniatureTemplate(UUID(e["uuid"]), e["name"]))

    def save(self):
        d = []
        for mini in self._library:
            e = {}
            e["uuid"] = str(mini.uuid)
            e["name"] = mini.name
            d.append(e)

        with codecs.open(self._config_file, "w", "utf-8") as f:
            json.dump(d, f, indent=4)

    def add(self, name, image):
        for template in self._library:
            if template.uuid == image.uuid:
                return
        self._library.append(MiniatureTemplate(image.uuid, name))

    def __getitem__(self, n):
        return self._library[n]

    def __iter__(self):
        for i in self._library:
            yield i

    def count(self):
        return len(self._library)

    def image(self, index):
        return self._library[index].image()
