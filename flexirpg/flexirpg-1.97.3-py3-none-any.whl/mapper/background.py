# Copyright (C) 2000-2001 The OpenRPG Project
#
#    openrpg-dev@lists.sourceforge.net
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# --
#
# File: background.py
# Author: Chris Davis
# Maintainer:
# Version:
#   $Id: background.py,v 1.29 2007/03/09 14:11:55 digitalxero Exp $
#
# Description: This file contains some of the basic definitions for the chat
# utilities in the orpg project.
#
__version__ = "$Id: background.py,v 1.29 2007/03/09 14:11:55 digitalxero Exp $"

from orpg.mapper.base import *
import urllib.request, urllib.parse, urllib.error
import os.path
import time
from uuid import UUID
import orpg.orpg_xml as orpg_xml
from orpg.main import image_library

##-----------------------------
## background layer
##-----------------------------

class layer_back_ground(layer_base):
    def __init__(self, canvas):
        layer_base.__init__(self)

        self.canvas = canvas
        self.image = None
        self.clear()

    def clear(self):
        self.set_color(wx.WHITE)
        self.set_image(None)

    def set_color(self, color):
        self.isUpdated = True
        self.bg_color = color
        self.canvas.SetBackgroundColour(self.bg_color)

    def set_image(self, image):
        self.isUpdated = True
        if self.image:
            self.image.del_hook(self._set_image_callback)
        self.image = image
        if self.image:
            self.image.add_hook(self._set_image_callback)

    def _set_image_callback(self, image):
        self.canvas.Refresh()

    def layerDraw(self, dc, topleft, size):
        if self.image and self.image.has_image():
            dc.DrawBitmap(self.image.bitmap, 0, 0)

    def layerToXML(self, action="update"):
        xml_str = '<bg'
        xml_str += ' color="%s"' % self.bg_color.GetAsString(wx.C2S_HTML_SYNTAX)
        if self.image:
            xml_str += ' image-uuid="%s"' % self.image.uuid
        else:
            xml_str += ' image-uuid=""'
        xml_str += "/>"
        if (action == "update" and self.isUpdated) or action == "new":
            self.isUpdated = False
            return xml_str
        else:
            return ''

    def layerTakeDOM(self, xml_dom):
        self.clear()

        if xml_dom.hasAttribute("color"):
            color = wx.Colour(xml_dom.getAttribute("color"))
            self.set_color(color)

        if xml_dom.hasAttribute("image-uuid"):
            image_uuid = xml_dom.getAttribute("image-uuid")
            if image_uuid:
                uuid = UUID(image_uuid)
                self.set_image(image_library.get(uuid))
