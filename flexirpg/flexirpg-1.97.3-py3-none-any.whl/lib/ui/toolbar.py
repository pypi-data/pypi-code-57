# Toolbar with additional helpers.
#
# Copyright 2020 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import wx

from .iconselector import IconSelectorPopup, EVT_ICON_SELECTED

class IconSelectorTool(IconSelectorPopup):
    def __init__(self, toolbar, toolid, icons):
        IconSelectorPopup.__init__(self, toolbar, icons)
        self._toolbar = toolbar
        self._toolid = toolid
        self.Bind(EVT_ICON_SELECTED, self.on_icon_selected)

    @property
    def icons(self):
        return self._icons

    def on_icon_selected(self, evt):
        self._toolbar.SetSelected(self._toolid, self.icons[evt.GetId()])

class ToolBar(wx.ToolBar):
    """A toolbar with support for some specialized buttons."""
    def __init__(self, parent, *args, **kwargs):
        wx.ToolBar.__init__(self, parent, *args, **kwargs)
        self.SetToolBitmapSize(wx.Size(24, 24))
        self._selected = {}

    def AddIconSelector(self, toolid, label, icons, shortHelp=""):
        """Add a button which can choose an icon."""
        self.AddTool(toolid, label, wx.Bitmap(self.GetToolBitmapSize()), shortHelp=shortHelp)
        self.SetToolClientData(toolid, icons)
        self.SetSelected(toolid, icons[0])

    def SetSelected(self, toolid, icon):
        """Set the selected icon for a tool."""
        self._selected[toolid] = icon
        self.SetToolNormalBitmap(toolid, icon.tool_bitmap(self))

    def GetSelected(self, toolid):
        """Get the icon selected by a tool."""
        return self._selected.get(toolid, None)

    def PopupIconSelector(self, toolid):
        icons = self.GetToolClientData(toolid)
        tool = IconSelectorTool(self, toolid, icons)
        (x, y) = self.GetScreenPosition()
        tx = self.GetToolPos(toolid) * self.GetToolSize().x
        sy = self.GetClientSize().y
        tool.Position((x + tx, y), (0, sy))
        tool.Popup()
