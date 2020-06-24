# FlexiRPG -- Whiteboard text
#
# Copyright (C) 2000-2001 The OpenRPG Project
# Copyright (C) 2009-2010 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

from orpg.mapper.base import *
from orpg.mapper.map_utils import *
from orpg.mapper.whiteboard_object import WhiteboardObject

class WhiteboardText(WhiteboardObject):
    def __init__(self, window, id, text_string="", pos=wx.Point(0,0),
                 style="0", pointsize="0", weight="0", color=wx.BLACK):
        WhiteboardObject.__init__(self, window, id)
        self.text_string = text_string
        self.weight = int(weight)
        self.pointsize = int(pointsize)
        self.style = int(style)
        self.textcolor = wx.Colour(color)
        self.posx = pos.x
        self.posy = pos.y

        self.font = wx.Font(self.pointsize, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                            wx.FONTWEIGHT_NORMAL, False,
                            open_rpg.get_component('settings').get_setting('defaultfont'))

        self.bbox = None

    def move(self, delta):
        self.posx += delta.x
        self.posy += delta.y
        self.is_updated = True

    def set_text_props(self, text_string, style, point, weight, color):
        self.text_string = text_string
        self.textcolor = color

        self.style = int(style)
        self.font.SetStyle(self.style)

        self.pointsize = int(point)
        self.font.SetPointSize(self.pointsize)

        self.weight = int(weight)
        self.font.SetWeight(self.weight)

        self.is_updated = True
        self.bbox = None

    def hit_test(self, pt):
        if self.bbox:
            return self.bbox.Contains(pt.x - self.posx, pt.y - self.posy)
        return False

    def _update_bbox(self, dc):
        dc.SetFont(self.font)
        (w,h,d,v) = dc.GetFullTextExtent(self.text_string)
        self.bbox = wx.Rect(0, 0, w, h)

    def draw_object(self, layer, dc):
        dc.SetTextForeground(self.textcolor)
        dc.SetFont(self.font)
        dc.DrawText(self.text_string, self.posx, self.posy)
        dc.SetTextForeground(wx.Colour(0,0,0))

        if not self.bbox:
            self._update_bbox(dc)

    def draw_handles(self, layer, dc):
        dc.SetPen(wx.BLACK_PEN)
        dc.SetBrush(wx.LIGHT_GREY_BRUSH)

        l = self.posx
        t = self.posy
        r = self.posx + self.bbox.width
        b = self.posy + self.bbox.height

        dc.DrawRectangle(l-7, t-7, 7, 7)
        dc.DrawRectangle(r,   t-7, 7, 7)
        dc.DrawRectangle(l-7, b,   7, 7)
        dc.DrawRectangle(r,   b,   7, 7)

    def toxml(self, action="update"):
        if action == "del":
            xml_str = "<text action='del' id='" + self.id + "'/>"
            return xml_str

        xml_str = "<text"

        xml_str += " action='" + action + "'"
        xml_str += " id='" + self.id + "'"
        xml_str += " zorder='" + str(self.z_order) + "'"

        if self.pointsize != None:
            xml_str += " pointsize='" + str(self.pointsize) + "'"

        if self.style != None:
            xml_str += " style='" + str(self.style) + "'"

        if self.weight != None:
            xml_str += " weight='" + str(self.weight) + "'"

        if self.posx != None:
            xml_str+= " posx='" + str(self.posx) + "'"

        if not (self.posy is None):
            xml_str += " posy='" + str(self.posy) + "'"

        if self.text_string != None:
            xml_str+= " text_string='" + self.text_string + "'"

        if self.textcolor != None:
            xml_str += " color='" + self.textcolor.GetAsString(wx.C2S_HTML_SYNTAX) + "'"

        xml_str += "/>"

        if (action == "update" and self.is_updated) or action == "new":
            self.isUpdated = False
            return xml_str
        else:
            return ''

    def takedom(self, xml_dom):
        self.text_string = xml_dom.getAttribute("text_string")

        if xml_dom.hasAttribute("posy"):
            self.posy = int(xml_dom.getAttribute("posy"))

        if xml_dom.hasAttribute("posx"):
            self.posx = int(xml_dom.getAttribute("posx"))

        if xml_dom.hasAttribute("weight"):
            self.weight = int(xml_dom.getAttribute("weight"))
            self.font.SetWeight(self.weight)

        if xml_dom.hasAttribute("style"):
            self.style = int(xml_dom.getAttribute("style"))
            self.font.SetStyle(self.style)

        if xml_dom.hasAttribute("pointsize"):
            self.pointsize = int(xml_dom.getAttribute("pointsize"))
            self.font.SetPointSize(self.pointsize)

        if xml_dom.hasAttribute("color") and xml_dom.getAttribute("color") != '':
            self.textcolor.Set(xml_dom.getAttribute("color"))

        self.bbox = None
