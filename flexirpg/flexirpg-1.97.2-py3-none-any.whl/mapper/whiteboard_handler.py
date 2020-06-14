# Copyright (C) 2000-2001 The OpenRPG Project
# Copyright (C) 2010 David Vrabel
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
# File: mapper/whiteboard_hander.py
# Author: OpenRPG Team
# Maintainer:
# Version:
#   $Id: whiteboard_handler.py,v 1.37 2007/03/09 14:11:56 digitalxero Exp $
#
# Description: Whiteboard layer handler
#
from orpg.mapper.base_handler import *
import orpg.tools.bitmap
from orpg.mapper.whiteboard_line import WhiteboardLine
from orpg.mapper.whiteboard_text import WhiteboardText
from orpg.mapper.whiteboard_mini import WhiteboardMini
from orpg.mapper.miniature_lib import *
from orpg.mapper.min_dialogs import *

MODE_SELECT   = 0
MODE_FREEFORM = 1
MODE_POLYLINE = 2
MODE_TEXT     = 3
MODE_ADD_MINI = 4
ZOOM_IN       = 5
ZOOM_OUT      = 6
RESET_VIEW    = 7

class whiteboard_handler(base_layer_handler):
    def __init__(self, parent, id, canvas):
        self.mode = MODE_SELECT
        self.drawing = False
        self.selected = None
        self.dragging = None
        self.right_clicked = None

        self.style = str(wx.NORMAL)
        self.weight = str(wx.NORMAL)
        self.pointsize = str(12)

        self.minilib = parent.minilib

        base_layer_handler.__init__(self, parent, id, canvas)
        self.build_text_properties_menu()

    def build_ctrls(self):
        base_layer_handler.build_ctrls(self)

        self.toolbar = wx.ToolBar(self)
        self.toolbar.AddRadioTool(MODE_SELECT, "Select",
                                  orpg.tools.bitmap.create_from_file("tool_select.png"),
                                  shortHelp="Select objects")
        self.toolbar.AddRadioTool(MODE_FREEFORM, "Freehand",
                                  orpg.tools.bitmap.create_from_file("tool_freehand.png"),
                                  shortHelp="Draw freehand lines")
        self.toolbar.AddRadioTool(MODE_POLYLINE, "Polyline",
                                  orpg.tools.bitmap.create_from_file("tool_polyline.png"),
                                  shortHelp="Draw straight lines")
        self.toolbar.AddRadioTool(MODE_TEXT, "Text",
                                  orpg.tools.bitmap.create_from_file("tool_text.png"),
                                  shortHelp="Add text")
        self.toolbar.AddRadioTool(MODE_ADD_MINI, "Add Mini",
                                  orpg.tools.bitmap.create_from_file("tool_add_mini.png"),
                                  shortHelp="Add miniatures")
        self.toolbar.ToggleTool(self.mode, True);
        self.toolbar.AddSeparator()

        self.color_button = wx.Button(self.toolbar, wx.ID_ANY, "Pen Color")
        self.color_button.SetBackgroundColour(wx.BLACK)
        self.color_button.SetForegroundColour(wx.WHITE)
        self.toolbar.AddControl(self.color_button)
        self.toolbar.AddSeparator()

        self.toolbar.AddControl(wx.StaticText(self.toolbar, wx.ID_ANY, "Line Width: "))
        self.widthList = wx.Choice(self.toolbar, wx.ID_ANY,
                                   choices=['1','2','3','4','5','6','7','8','9','10'])
        self.widthList.SetSelection(0)
        self.toolbar.AddControl(self.widthList)
        self.toolbar.AddSeparator()

        self.mini_choice = wx.Choice(self.toolbar, wx.ID_ANY)
        self.toolbar.AddControl(self.mini_choice)
        self.toolbar.AddSeparator()
        self.update_mini_choice()

        self.toolbar.AddTool(ZOOM_IN, "Zoom in",
                             orpg.tools.bitmap.create_from_file("tool_zoom_in.png"),
                             shortHelp="Zoom in")
        self.toolbar.AddTool(ZOOM_OUT, "Zoom out",
                             orpg.tools.bitmap.create_from_file("tool_zoom_out.png"),
                             shortHelp="Zoom out")
        self.toolbar.AddTool(RESET_VIEW, "Reset view",
                             orpg.tools.bitmap.create_from_file("tool_reset_view.png"),
                             shortHelp="Reset view to default")

        self.toolbar.Realize()
        self.sizer.Add(self.toolbar)

        self.Bind(wx.EVT_TOOL, self.on_mode_change, id=MODE_SELECT)
        self.Bind(wx.EVT_TOOL, self.on_mode_change, id=MODE_FREEFORM)
        self.Bind(wx.EVT_TOOL, self.on_mode_change, id=MODE_POLYLINE)
        self.Bind(wx.EVT_TOOL, self.on_mode_change, id=MODE_TEXT)
        self.Bind(wx.EVT_TOOL, self.on_mode_change, id=MODE_ADD_MINI)
        self.Bind(wx.EVT_TOOL, self.canvas.on_zoom_in, id=ZOOM_IN)
        self.Bind(wx.EVT_TOOL, self.canvas.on_zoom_out, id=ZOOM_OUT)
        self.Bind(wx.EVT_TOOL, self.canvas.on_reset_view, id=RESET_VIEW)

        self.Bind(wx.EVT_MOTION, self.on_motion)
        self.Bind(wx.EVT_BUTTON, self.on_pen_color, self.color_button)
        self.Bind(wx.EVT_CHOICE, self.on_pen_width, self.widthList)

    def build_text_properties_menu(self, label="Text Properties"):
        self.text_properties_dialog = wx.Dialog(self, -1, "Text Properties",  name = "Text Properties")
        self.text_props_sizer = wx.BoxSizer(wx.VERTICAL)

        okay_boxer = wx.BoxSizer(wx.HORIZONTAL)

        okay_button = wx.Button(self.text_properties_dialog, wx.ID_OK, "APPLY")
        cancel_button = wx.Button(self.text_properties_dialog, wx.ID_CANCEL,"CANCEL")
        okay_boxer.Add(okay_button, 1)
        okay_boxer.Add(wx.Size(10,10))
        okay_boxer.Add(cancel_button, 1)

        self.txt_boxer = wx.BoxSizer(wx.HORIZONTAL)
        self.txt_static = wx.StaticText(self.text_properties_dialog, -1, "Text: ")
        self.text_control = wx.TextCtrl(self.text_properties_dialog, wx.ID_ANY, "", name = "Text: ")
        self.txt_boxer.Add(self.txt_static,0,wx.EXPAND)
        self.txt_boxer.Add(wx.Size(10,10))
        self.txt_boxer.Add(self.text_control,1,wx.EXPAND)

        self.point_boxer = wx.BoxSizer(wx.HORIZONTAL)
        self.point_static = wx.StaticText(self.text_properties_dialog, -1, "Text Size: ")
        self.point_control = wx.SpinCtrl(self.text_properties_dialog, wx.ID_ANY, value = "12",min = 1, initial = 12, name = "Font Size: ")

        self.point_boxer.Add(self.point_static,1,wx.EXPAND)
        self.point_boxer.Add(wx.Size(10,10))
        self.point_boxer.Add(self.point_control,0,wx.EXPAND)

        self.text_color_control = wx.Button(self.text_properties_dialog, wx.ID_ANY, "TEXT COLOR",style=wx.BU_EXACTFIT)

        self.weight_control = wx.RadioBox(self.text_properties_dialog, wx.ID_ANY, "Weight", choices = ["Normal","Bold"])
        self.style_control = wx.RadioBox(self.text_properties_dialog, wx.ID_ANY, "Style", choices = ["Normal", "Italic"])

        self.text_props_sizer.Add(self.txt_boxer,0,wx.EXPAND)
        self.text_props_sizer.Add(self.point_boxer,0, wx.EXPAND)
        self.text_props_sizer.Add(self.weight_control,0, wx.EXPAND)
        self.text_props_sizer.Add(self.style_control,0, wx.EXPAND)
        self.text_props_sizer.Add(self.text_color_control, 0, wx.EXPAND)
        self.text_props_sizer.Add(wx.Size(10,10))
        self.text_props_sizer.Add(okay_boxer,0, wx.EXPAND)

        self.text_props_sizer.Fit(self)
        self.text_properties_dialog.SetSizer(self.text_props_sizer)
        self.text_properties_dialog.Fit()
        self.text_properties_dialog.Bind(wx.EVT_BUTTON, self.on_text_color, self.text_color_control)
        self.text_properties_dialog.Bind(wx.EVT_BUTTON, self.on_text_properties, okay_button)

        #self.text_properties_dialog.Destroy()


    def build_menu(self):
        base_layer_handler.build_menu(self)
        self.main_menu.AppendSeparator()

        item = wx.MenuItem(self.main_menu, wx.ID_ANY, "Show &Labels", "Show Miniature Labels",
                           wx.ITEM_CHECK)
        self.canvas.Bind(wx.EVT_MENU, self.on_show_labels, item)
        self.main_menu.Append(item)
        item.Check(self.canvas.layers['whiteboard'].show_labels.bool)

        self.line_menu = wx.Menu()
        self.add_z_order_menu_items(self.line_menu)

        item = wx.MenuItem(self.line_menu, wx.ID_ANY, "&Delete")
        self.canvas.Bind(wx.EVT_MENU, self.on_delete, item)
        self.line_menu.Append(item)

        self.text_menu = wx.Menu()
        self.add_z_order_menu_items(self.text_menu)

        item = wx.MenuItem(self.text_menu, wx.ID_ANY, "&Properties", "Properties")
        self.canvas.Bind(wx.EVT_MENU, self.get_text_properties, item)
        self.text_menu.Append(item)

        item = wx.MenuItem(self.text_menu, wx.ID_ANY, "&Delete")
        self.canvas.Bind(wx.EVT_MENU, self.on_delete, item)
        self.text_menu.Append(item)

        self.mini_menu = wx.Menu()
        self.add_z_order_menu_items(self.mini_menu)

        self.add_to_library_item = wx.MenuItem(self.mini_menu, wx.ID_ANY, "&Add to Library")
        self.canvas.Bind(wx.EVT_MENU, self.on_add_to_library, self.add_to_library_item)
        self.mini_menu.Append(self.add_to_library_item)

        item = wx.MenuItem(self.mini_menu, wx.ID_ANY, "&Properties", "Properties")
        self.canvas.Bind(wx.EVT_MENU, self.get_mini_properties, item)
        self.mini_menu.Append(item)

        item = wx.MenuItem(self.mini_menu, wx.ID_ANY, "&Delete")
        self.canvas.Bind(wx.EVT_MENU, self.on_delete, item)
        self.mini_menu.Append(item)

    def add_z_order_menu_items(self, menu):
        item = wx.MenuItem(menu, wx.ID_ANY, "&Raise")
        self.canvas.Bind(wx.EVT_MENU, self.on_raise, item)
        menu.Append(item)
        item = wx.MenuItem(menu, wx.ID_ANY, "&Lower")
        self.canvas.Bind(wx.EVT_MENU, self.on_lower, item)
        menu.Append(item)
        item = wx.MenuItem(menu, wx.ID_ANY, "Raise to &Top")
        self.canvas.Bind(wx.EVT_MENU, self.on_raise_to_top, item)
        menu.Append(item)
        item = wx.MenuItem(menu, wx.ID_ANY, "Lower to &Bottom")
        self.canvas.Bind(wx.EVT_MENU, self.on_lower_to_bottom, item)
        menu.Append(item)
        menu.AppendSeparator()

    def update_mini_choice(self):
        self.mini_choice.Clear()
        for m in self.minilib:
            self.mini_choice.Append(m.name, m)
        self.mini_choice.SetSelection(0)

    def do_line_menu(self):
        self.right_clicked.highlight()
        self.canvas.Refresh()
        self.canvas.PopupMenu(self.line_menu)

    def on_text_properties(self,evt):
        text_string = self.text_control.GetValue()
        if self.style_control.GetStringSelection() == 'Normal':
            style = wx.NORMAL
        else:
            style = wx.ITALIC
        if self.weight_control.GetStringSelection() == 'Normal':
            weight = wx.NORMAL
        else:
            weight = wx.BOLD
        point = str(self.point_control.GetValue())
        color = self.text_color_control.GetForegroundColour()
        self.right_clicked.set_text_props(text_string, style, point, weight, color)
        self.update_object(self.right_clicked)
        self.text_properties_dialog.Show(False)

    def on_text_color(self,evt):
        dlg = wx.ColourDialog(self)
        if dlg.ShowModal() == wx.ID_OK:
            c = dlg.GetColourData()
            self.text_color_control.SetForegroundColour(c.GetColour())
        dlg.Destroy()

    def update_object(self, obj):
        xml_str = "<map><whiteboard>"
        xml_str += obj.toxml('update')
        xml_str += "</whiteboard></map>"
        self.canvas.frame.session.send(xml_str)
        self.canvas.Refresh(False)

    def get_text_properties(self, event=None):
        self.text_color_control.SetForegroundColour(self.right_clicked.textcolor)
        self.text_control.SetValue(self.right_clicked.text_string)
        self.point_control.SetValue(int(self.right_clicked.pointsize))

        if int(self.right_clicked.weight) == wx.NORMAL:
            self.weight_control.SetSelection(0)
        else:
            self.weight_control.SetSelection(1)

        if int(self.right_clicked.style) == wx.NORMAL:
            self.style_control.SetSelection(0)
        else:
            self.style_control.SetSelection(1)

        self.text_properties_dialog.Center()
        self.text_properties_dialog.Show(True)

    def do_text_menu(self):
        self.right_clicked.highlight()
        self.canvas.Refresh()
        self.canvas.PopupMenu(self.text_menu)

    def on_add_to_library(self, evt):
        name = re.sub(' [0-9]$', '', self.right_clicked.label)
        self.minilib.add(name, self.right_clicked.image)
        self.minilib.save()
        self.update_mini_choice()

    def get_mini_properties(self, evt):
        dlg = min_edit_dialog(self.canvas.frame.GetParent(), self.right_clicked)
        if dlg.ShowModal() == wx.ID_OK:
            self.update_object(self.right_clicked)

    def do_mini_menu(self):
        self.right_clicked.highlight()
        self.add_to_library_item.Enabled = self.right_clicked.image.has_image()
        self.canvas.Refresh()
        self.canvas.PopupMenu(self.mini_menu)

    def on_right_down(self,evt):
        self.right_clicked = None

        pos = self.canvas.get_position_from_event(evt)

        if self.mode == MODE_POLYLINE:
            self.polyline_last_point(evt)

        self.right_clicked = self.canvas.layers['whiteboard'].find_object_at_position(pos)
        if self.right_clicked:
            if isinstance(self.right_clicked, WhiteboardLine):
                self.do_line_menu()
            elif isinstance(self.right_clicked, WhiteboardText):
                self.do_text_menu()
            elif isinstance(self.right_clicked, WhiteboardMini):
                self.do_mini_menu()
        else:
            base_layer_handler.on_right_down(self,evt)

        if self.right_clicked:
            self.right_clicked.highlight(False)
            self.canvas.Refresh()

    def on_pen_color(self,evt):
        data = wx.ColourData()
        data.SetChooseFull(True)
        dlg = wx.ColourDialog(self.canvas, data)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetColourData()
            color = data.GetColour()
            self.canvas.layers['whiteboard'].setcolor(color)
            self.color_button.SetBackgroundColour(color)
        dlg.Destroy()

    def on_pen_width(self,evt):
        width = int(self.widthList.GetStringSelection())
        self.canvas.layers['whiteboard'].setwidth(width)

    def on_show_labels(self, evt):
        if evt.IsChecked():
            self.canvas.layers['whiteboard'].show_labels.bool = True
        else:
            self.canvas.layers['whiteboard'].show_labels.bool = False
        self.canvas.Refresh()

    def delete_all_objects(self):
        self.un_highlight()
        self.canvas.layers['whiteboard'].del_all_objects()

    def on_delete(self, evt):
        if self.right_clicked == self.selected:
            self.un_highlight()
        self.canvas.layers['whiteboard'].del_object(self.right_clicked)
        self.right_clicked = None

    def on_raise(self, evt):
        self.canvas.layers['whiteboard'].raise_object(self.right_clicked)

    def on_lower(self, evt):
        self.canvas.layers['whiteboard'].lower_object(self.right_clicked)

    def on_raise_to_top(self, evt):
        self.canvas.layers['whiteboard'].raise_object_to_top(self.right_clicked)

    def on_lower_to_bottom(self, evt):
        self.canvas.layers['whiteboard'].lower_object_to_bottom(self.right_clicked)

    def on_mode_change(self, event):
        self.mode = event.GetId()
        if self.mode != MODE_SELECT:
            self.un_highlight()

    # Altered on_left_up to toggle between
    # drawing modes freeform vs polyline
    # 05-09-2003  Snowdog
    def on_left_down(self,evt):
        session = self.canvas.frame.session
        if session.use_roles() and session.my_role() != session.ROLE_GM and session.my_role() != session.ROLE_PLAYER:
            open_rpg.get_component("chat").InfoPost("You must be either a player or GM to use this feature")
            return

        pos = self.canvas.get_position_from_event(evt)
        
        if self.mode == MODE_SELECT:
            self.try_select(pos)

        elif self.mode == MODE_FREEFORM:
            self.freeform_start(pos)

        elif self.mode == MODE_POLYLINE:
            self.polyline_add_point(pos)

        elif self.mode == MODE_TEXT:
            self.on_text_left_down(pos)

        elif self.mode == MODE_ADD_MINI:
            pass



    # Added handling for double clicks within the map
    # 05-09-2003  Snowdog
    def on_left_dclick(self, evt):
        if self.mode == MODE_FREEFORM:
            #Freeform mode ignores the double click
            pass
        elif self.mode == MODE_POLYLINE:
            self.polyline_last_point( evt )
        elif self.mode == MODE_TEXT:
            pass



    # Altered on_left_up to toggle between
    # drawing modes freeform vs polyline
    # 05-09-2003  Snowdog
    def on_left_up(self,evt):
        pos = self.canvas.get_position_from_event(evt)

        if self.mode == MODE_SELECT:
            if self.dragging:
                self.dragging.snap_to_grid(self.canvas.layers['grid'])
                self.update_object(self.dragging)
                self.dragging = False
        if self.mode == MODE_FREEFORM:
            self.on_freeform_left_up(evt)
        elif self.mode == MODE_POLYLINE:
            #Polyline mode relies on the down click
            #not the mouse button release
            pass
        elif self.mode == MODE_TEXT:
            pass
        elif self.mode == MODE_ADD_MINI:
            selected = self.mini_choice.GetSelection()
            if selected == wx.NOT_FOUND:
                return
            mini_tmpl = self.mini_choice.GetClientData(selected)
            self.canvas.layers['whiteboard'].add_miniature(mini_tmpl, pos)

    # Altered on_left_up to toggle between
    # drawing modes freeform vs polyline
    # 05-09-2003  Snowdog
    def on_motion(self,evt):
        session = self.canvas.frame.session
        if (session.my_role() != session.ROLE_GM) \
            and (session.my_role()!=session.ROLE_PLAYER) \
            and (session.use_roles()):
            return

        pos = self.canvas.get_position_from_event(evt)

        if self.mode == MODE_SELECT:
            if evt.LeftIsDown() and self.selected:
                self.dragging = self.selected
                self.dragging.move(pos - self.last_pos)
                self.last_pos = pos
                self.canvas.Refresh()
        elif self.mode == MODE_FREEFORM:
            if evt.LeftIsDown():
                self.freeform_motion(evt)
        elif self.mode == MODE_POLYLINE:
            if self.drawing:
                self.polyline_motion( evt )

    def try_select(self, pos):
        hit = self.canvas.layers['whiteboard'].find_object_at_position(pos)
        if hit:
            self.highlight(hit)
        else:
            self.un_highlight()
        self.last_pos = pos

    def highlight(self, obj):
        if self.selected == obj:
            return;
        if self.selected:
            self.selected.highlight(False)
        self.selected = obj
        self.selected.highlight(True)
        self.canvas.Refresh(True)

    def un_highlight(self):
        if self.selected:
            self.selected.highlight(False)
            self.selected = None
            self.canvas.Refresh(True)

    # Polyline Add Point
    # adds a new point to the polyline
    # 05-09-2003  Snowdog
    def polyline_add_point(self, pos):
        #if this point doens't end the line
        #add a new point into the line string
        if not self.drawing:
            self.working_line = self.canvas.layers['whiteboard'].new_line()
            self.working_line.add_point(pos.x, pos.y)
            self.working_line.add_point(pos.x, pos.y)
            self.drawing = True
        else:
            if not self.polyline_end_check(pos):
                self.working_line.add_point(pos.x, pos.y)
            else: #end of line. Send and reset vars for next line
                self.drawing = False
                self.canvas.layers['whiteboard'].complete_line(self.working_line)
        self.canvas.Refresh()

    # Polyline Last Point
    # adds a final point to the polyline and ends it
    # 05-09-2003  Snowdog
    def polyline_last_point(self, evt):
        if not self.drawing:
            return
        self.drawing = False

        self.canvas.layers['whiteboard'].complete_line(self.working_line)
        self.canvas.Refresh()


    # Check if the last two points are sufficiently close to consider
    # the poly line as ended.
    def polyline_end_check(self, pos):
        tol = 5

        (xa, ya) = self.working_line.points[-2]
        (xb, yb) = self.working_line.points[-1]

        if xa - tol <= xb <= xa + tol and ya - tol <= yb <= ya + tol:
            self.working_line.points.pop()
            return True
        return False

    def polyline_motion(self, evt):
        if self.drawing != True:
            return

        pos = self.canvas.get_position_from_event(evt)

        self.working_line.points[-1] = pos
        self.canvas.Refresh()

    def freeform_start(self, pos):
        self.working_line = self.canvas.layers['whiteboard'].new_line()
        self.working_line.add_point(pos.x, pos.y)
        self.drawing = True

    # moved original on_motion to this function
    # to allow alternate drawing method to be used
    # 05-09-2003  Snowdog
    def freeform_motion(self, evt):
        if not self.drawing:
            return
        pos = self.canvas.get_position_from_event(evt)
        self.working_line.add_point(pos.x, pos.y)
        self.canvas.Refresh()

    # moved original on_left_up to this function
    # to allow alternate drawing method to be used
    # 05-09-2003  Snowdog
    def on_freeform_left_up(self,evt):
        if self.drawing == True:
            self.canvas.layers['whiteboard'].complete_line(self.working_line)
            self.working_line = None
            self.drawing = False

    def on_text_left_down(self, pos):
        dlg = wx.TextEntryDialog(self,"Text to add to whiteboard", caption="Enter text")
        if dlg.ShowModal() == wx.ID_OK:
            text_string = dlg.GetValue()
            self.canvas.layers['whiteboard'].add_text(text_string,pos, self.style,
                             self.pointsize, self.weight,
                             self.canvas.layers['whiteboard'].color)
