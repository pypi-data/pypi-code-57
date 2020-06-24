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
# File: mapper/map.py
# Author: OpenRPG
# Maintainer:
# Version:
#   $Id: map.py,v 1.73 2007/12/07 20:39:49 digitalxero Exp $
#
# Description:
#
__version__ = "$Id: map.py,v 1.73 2007/12/07 20:39:49 digitalxero Exp $"

from orpg.mapper.map_version import MAP_VERSION
from orpg.mapper.map_msg import *
from orpg.mapper.min_dialogs import *
from orpg.mapper.map_prop_dialog import *
from orpg.mapper.miniature_lib import MiniatureLib
import orpg.dirpath
import os
import traceback
from orpg.mapper.mapcontrols import MapControls
from orpg.orpgCore import open_rpg
from orpg.main import image_library
from orpg.mapper.whiteboard_object import EVT_WHITEBOARD_OBJECT_UPDATED

# Various marker modes for player tools on the map
MARKER_MODE_NONE = 0
MARKER_MODE_MEASURE = 1
MARKER_MODE_TARGET = 2
MARKER_MODE_AREA_TARGET = 3

MINIMUM_ZOOM = 0.2

class MapCanvas(wx.Panel):
    def __init__(self, parent, ID, isEditor=0):
        self.parent = parent
        self.log = open_rpg.get_component("log")
        self.settings = open_rpg.get_component("settings")
        self.session = open_rpg.get_component("session")
        wx.Panel.__init__(self, parent, ID, style=wx.FULL_REPAINT_ON_RESIZE | wx.SUNKEN_BORDER )
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.frame = parent
        self.layers = {}
        self.layers['bg'] = layer_back_ground(self)
        self.layers['grid'] = grid_layer(self)
        self.layers['whiteboard'] = whiteboard_layer(self)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_DCLICK, self.on_left_dclick)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_MIDDLE_DOWN, self.on_middle_down)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_right_down)
        self.Bind(wx.EVT_MOTION, self.on_motion)
        self.Bind(wx.EVT_MOUSEWHEEL, self.on_mousewheel)
        self.root_dir = os.getcwd()
        self.isEditor = isEditor
        self.map_version = MAP_VERSION

        self.view_port_origin = wx.Point(0, 0)
        self.zoom = 1.0
        self.scrolling = False

        self.Bind(orpg.mapper.whiteboard_object.EVT_WHITEBOARD_OBJECT_UPDATED,
                  self.on_whiteboard_object_updated)

    def send_map_data(self, action="update"):
        wx.BeginBusyCursor()
        send_text = self.toxml(action)
        if send_text:
            if not self.isEditor:
                self.frame.session.send(send_text)
        wx.EndBusyCursor()

    def on_paint(self, evt):
        scale = self.zoom
        topleft = self.view_port_origin
        clientsize = self.GetClientSize()
        clientsize.Scale(1/scale, 1/scale)

        dc = wx.AutoBufferedPaintDC(self)
        dc.SetDeviceOrigin(-topleft.x*scale, -topleft.y*scale)
        dc.SetUserScale(scale, scale)

        dc.SetBackground(wx.Brush(self.GetBackgroundColour(), wx.SOLID))
        dc.Clear()

        self.layers['bg'].layerDraw(dc, topleft, clientsize)
        self.layers['grid'].layerDraw(dc, topleft, clientsize)
        self.layers['whiteboard'].layerDraw(dc)

    def on_left_down(self, evt):
        if evt.ShiftDown():
            self.last_pos = self.get_relative_position_from_event(evt)
            self.scrolling = True
        else:
            self.frame.controls.on_left_down(evt)

    def on_right_down(self, evt):
        if evt.ShiftDown():
            pass
        else:
            self.frame.controls.on_right_down(evt)

    def on_left_dclick(self, evt):
        if evt.ShiftDown():
            pass
        else:
            self.frame.controls.on_left_dclick(evt)

    def on_left_up(self, evt):
        if self.scrolling:
            self.scrolling = False
        else:
            self.frame.controls.on_left_up(evt)

    def on_middle_down(self, evt):
        self.last_pos = self.get_relative_position_from_event(evt)

    def on_motion(self, evt):
        if self.scrolling or evt.MiddleIsDown():
            pos = self.get_relative_position_from_event(evt)
            self.view_port_origin.x -= pos.x - self.last_pos.x
            self.view_port_origin.y -= pos.y - self.last_pos.y
            self.last_pos = pos
            self.Refresh()
        else:
            self.frame.controls.on_motion(evt)

    def on_mousewheel(self, evt):
        rot = evt.GetWheelRotation() // evt.GetWheelDelta()
        self._zoom_adjust(evt, rot * 0.1)

    def on_zoom_out(self, evt):
        self._zoom_adjust(None, -0.1)

    def on_zoom_in(self, evt):
        self._zoom_adjust(None, 0.1)

    def _zoom_adjust(self, evt, zoom_delta):
        # Zoom about the centre of the window if there's no mouse event.
        if evt is None:
            evt = wx.MouseEvent()
            evt.SetX(round(self.GetClientSize().x / 2))
            evt.SetY(round(self.GetClientSize().y / 2))
        pos = self.get_position_from_event(evt)
        self.zoom = max(self.zoom + zoom_delta, MINIMUM_ZOOM)
        self.view_port_origin = pos - self.get_relative_position_from_event(evt)
        self.Refresh()

    def on_reset_view(self, evt):
        self.zoom = 1.0
        self.view_port_origin.x = 0
        self.view_port_origin.y = 0
        self.Refresh()

    def on_prop(self, evt):
        self.session = open_rpg.get_component("session")
        self.chat = open_rpg.get_component("chat")
        if (self.session.my_role() != self.session.ROLE_GM):
            open_rpg.get_component('chat').InfoPost("You must be a GM to use this feature")
            return
        dlg = general_map_prop_dialog(self.frame.GetParent(), 
                                      self.layers['bg'], self.layers['grid'])
        if dlg.ShowModal() == wx.ID_OK:
            self.send_map_data()
            self.Refresh(False)
        dlg.Destroy()
        os.chdir(self.root_dir)

    def on_whiteboard_object_updated(self, evt):
        self.Refresh(True)

    def get_relative_position_from_event(self, evt):
        dc = wx.ClientDC(self)
        dc.SetUserScale(self.zoom, self.zoom)
        return evt.GetLogicalPosition(dc)

    def get_position_from_event(self, evt):
        pos = self.get_relative_position_from_event(evt)
        return wx.Point(self.view_port_origin.x + pos.x, self.view_port_origin.y + pos.y)

    def toxml(self, action="update"):
        xml_str = "<map version='" + self.map_version + "'"

        s = ""
        keys = list(self.layers.keys())
        for k in keys:
            if (k != "fog" or action != "update"):
                s += self.layers[k].layerToXML(action)

        if s or action == "new":
            return "<map version='" + self.map_version + "' action='" + action + "'>" + s + "</map>"
        else:
            return ""

    def takexml(self, xml, new_ids=False):
        try:
            #parse the map DOM
            xml_dom = parseXml(xml)
            if xml_dom == None:
                self.log.log("xml_dom == None\n" + xml, ORPG_INFO)
                return
            node_list = xml_dom.getElementsByTagName("map")

            if new_ids:
                self._generate_new_ids(xml_dom);

            if len(node_list) < 1:
                self.log.log("Invalid XML format for mapper", ORPG_INFO)
            else:
                # set map version to incoming data so layers can convert
                self.map_version = node_list[0].getAttribute("version")
                action = node_list[0].getAttribute("action")
                if action == "new":
                    self.layers = {}
                    try:
                        self.layers['bg'] = layer_back_ground(self)
                    except:
                        pass
                    try:
                        self.layers['grid'] = grid_layer(self)
                    except:
                        pass
                    try:
                        self.layers['whiteboard'] = whiteboard_layer(self)
                    except:
                        pass
                children = node_list[0].childNodes
                for c in children:
                    name = c.nodeName
                    if name in self.layers:
                        self.layers[name].layerTakeDOM(c)
                # all map data should be converted, set map version to current version
                self.map_version = MAP_VERSION
                self.Refresh(False)
            xml_dom.unlink()  # eliminate circular refs
        except:
            self.log.log(traceback.format_exc(), ORPG_GENERAL)
            self.log.log("EXCEPTION: Critical Error Loading Map!!!", ORPG_GENERAL)

    def _generate_new_ids(self, xml_dom):
        for mini in xml_dom.getElementsByTagName("miniature"):
            mini.setAttribute('id', 'mini-' + self.frame.session.get_next_id())
        for line in xml_dom.getElementsByTagName("line"):
            line.setAttribute('id', 'line-' + self.frame.session.get_next_id())
        for text in xml_dom.getElementsByTagName("text"):
            text.setAttribute('id', 'text-' + self.frame.session.get_next_id())


class map_wnd(wx.Panel):
    def __init__(self, parent, id):
        self.log = open_rpg.get_component('log')
        wx.Panel.__init__(self, parent, id)

        self.session = open_rpg.get_component('session')
        self.settings = open_rpg.get_component('settings')
        self.chat = open_rpg.get_component('chat')
        self.top_frame = open_rpg.get_component('frame')
        self.root_dir = os.getcwd()

        self.minilib = MiniatureLib()

        self.canvas = MapCanvas(self, -1)
        self.controls = MapControls(self, -1, self.canvas)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.EXPAND)
        self.sizer.Add(self.controls, 0, wx.EXPAND)
        self.SetSizer(self.sizer)

        self.load_default()

    def load_default(self):
        if self.session.is_connected() and (self.session.my_role() != self.session.ROLE_GM) and (self.session.use_roles()):
            open_rpg.get_component('chat').InfoPost("You must be a GM to use this feature")
            return
        f = open(orpg.dirpath.dir_struct["template"] + "default_map.xml")
        self.new_data(f.read())
        f.close()
        self.canvas.send_map_data("new")
        if not self.session.is_connected() and (self.session.my_role() != self.session.ROLE_GM):
            self.session.update_role("GM")

    def new_data(self, data):
        self.canvas.takexml(data)

    def on_clear_map(self, evt):
        if self.session.my_role() != self.session.ROLE_GM:
            open_rpg.get_component('chat').InfoPost("You must be a GM to use this feature")
            return
        self.controls.delete_all_objects()

    def on_save(self,evt):
        if (self.session.my_role() != self.session.ROLE_GM):
            open_rpg.get_component('chat').InfoPost("You must be a GM to use this feature")
            return
        d = wx.FileDialog(self.GetParent(), "Save map data", orpg.dirpath.dir_struct["user"],
                          "", "*.xml", wx.FD_SAVE)
        if d.ShowModal() == wx.ID_OK:
            f = open(d.GetPath(), "w")
            data = '<nodehandler class="min_map" icon="compass" module="core" name="miniature Map">'
            data += self.canvas.toxml("new")
            data += "</nodehandler>"
            data = data.replace(">",">\n")
            f.write(data)
            f.close()
        d.Destroy()
        os.chdir(self.root_dir)

    def on_open(self, evt):
        if self.session.is_connected() and (self.session.my_role() != self.session.ROLE_GM) and (self.session.use_roles()):
            open_rpg.get_component('chat').InfoPost("You must be a GM to use this feature")
            return
        d = wx.FileDialog(self.GetParent(), "Select a file", orpg.dirpath.dir_struct["user"],
                          "", "*.xml", wx.FD_OPEN)
        if d.ShowModal() == wx.ID_OK:
            f = open(d.GetPath())
            map_xml = f.read()
            self.canvas.takexml(map_xml, True)
            self.canvas.send_map_data("new")
            if not self.session.is_connected() and (self.session.my_role() != self.session.ROLE_GM):
                    self.session.update_role("GM")
        d.Destroy()
        os.chdir(self.root_dir)

    def on_add_mini(self, evt):
        d = wx.FileDialog(self.GetParent(), "Add Miniatures to Library",
                          orpg.dirpath.dir_struct["user"], "",
                          "Images (*.png;*.jpg;*.jpeg)|*.png;*.jpg;*.jpeg",
                          wx.FD_OPEN | wx.FD_MULTIPLE)
        if d.ShowModal() == wx.ID_OK:
            added = False
            for path in d.GetPaths():
                image = image_library.get_from_file(path)
                if image:
                    name = os.path.splitext(os.path.basename(path))[0].replace("_", " ")
                    self.minilib.add(name, image)
                    added = True
            if added:
                self.minilib.save()

    def build_menu(self):
        # temp menu
        menu = wx.Menu()
        item = wx.MenuItem(menu, wx.ID_ANY, "&Clear Map")
        self.top_frame.Bind(wx.EVT_MENU, self.on_clear_map, item)
        menu.Append(item)
        item = wx.MenuItem(menu, wx.ID_ANY, "&Load Map", "Load Map")
        self.top_frame.Bind(wx.EVT_MENU, self.on_open, item)
        menu.Append(item)
        item = wx.MenuItem(menu, wx.ID_ANY, "&Save Map", "Save Map")
        self.top_frame.Bind(wx.EVT_MENU, self.on_save, item)
        menu.Append(item)
        menu.AppendSeparator()
        item = wx.MenuItem(menu, wx.ID_ANY, "&Add Miniatures to Library...")
        self.top_frame.Bind(wx.EVT_MENU, self.on_add_mini, item)
        menu.Append(item)
        menu.AppendSeparator()
        item = wx.MenuItem(menu, wx.ID_ANY, "&Properties", "Properties")
        self.top_frame.Bind(wx.EVT_MENU, self.canvas.on_prop, item)
        menu.Append(item)
        self.top_frame.mainmenu.Insert(2, menu, '&Map')
