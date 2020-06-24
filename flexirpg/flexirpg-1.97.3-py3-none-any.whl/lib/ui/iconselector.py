# Icon selector buttons.
#
# Copyright (C) 2011 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import math
import wx

IconSelectedType = wx.NewEventType()
EVT_ICON_SELECTED = wx.PyEventBinder(IconSelectedType, 1)

class IconSelectedEvent(wx.PyCommandEvent):
    def __init__(self, evt_type, id):
        wx.PyCommandEvent.__init__(self, evt_type, id)

class IconSelectorButton(wx.BitmapButton):
    def __init__(self, parent, icons, selected = 0):
        wx.BitmapButton.__init__(self, parent, wx.ID_ANY,
                                wx.Bitmap(icons.image(selected)))

        self._icons = icons
        self._popup = IconSelectorPopup(self, icons)

        self.Bind(wx.EVT_BUTTON, self.on_button)
        self._popup.Bind(EVT_ICON_SELECTED, self.on_icon_selected)

    def on_button(self, evt):
        (x, y) = self.GetScreenPosition()
        (w, h) = self.GetSize()
        self._popup.Position((x, y), (0, h))
        self._popup.Popup()

    def on_icon_selected(self, evt):
        self.SetBitmapLabel(wx.Bitmap(self._icons.image(evt.GetId())))
        evt.Skip()

class IconSelectorPopup(wx.PopupTransientWindow):

    COLUMNS_MAX_DEFAULT = 15
    WINDOW_BORDER = 1
    ICON_BORDER = 3

    def __init__(self, parent, icons):
        wx.PopupTransientWindow.__init__(self, parent, flags = wx.BORDER_SIMPLE)

        self._icons = icons
        self._icon_size = self._max_icon_dimension()
        self._max_columns = self.COLUMNS_MAX_DEFAULT
        self._selected = None

        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)

        (self.cols, self.rows) = self._grid_size()

        self._spacing = self._icon_size + 2 * self.ICON_BORDER + self.WINDOW_BORDER

        w = self.cols * self._spacing + self.WINDOW_BORDER
        h = self.rows * self._spacing + self.WINDOW_BORDER

        self.SetSize((w, h))

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)

    def _max_icon_dimension(self):
        d = 0
        for i in range(self._icons.count()):
            (w, h) = self._icons.image(i).GetSize()
            if w > d:
                d = w
            if h > d:
                d = h
        return d

    def _grid_size(self):
        num_icons = self._icons.count()

        # Aim for a roughly square grid of icons, but not too wide.
        cols = int(math.sqrt(self._icons.count()) + 0.5)
        if cols > self._max_columns:
            cols = self._max_columns
        rows = (num_icons + cols - 1) // cols

        return (cols, rows)

    def on_paint(self, evt):
        (w, h) = self.GetClientSize()
        sp = self._spacing
        wb = self.WINDOW_BORDER

        dc = wx.AutoBufferedPaintDC(self)
        rn = wx.RendererNative.GetDefault()

        dc.SetBrush(wx.Brush(wx.WHITE))
        dc.SetPen(wx.Pen(wx.LIGHT_GREY))
        dc.DrawRectangle(0, 0, w, h)

        for i in range(self._icons.count()):
            x = wb + i % self.cols * sp
            y = wb + i // self.cols * sp
            if i == self._selected:
                rn.DrawItemSelectionRect(self, dc, (x, y, sp - wb, sp - wb),
                                         wx.CONTROL_SELECTED | wx.CONTROL_FOCUSED)
            bmp = wx.Bitmap(self._icons.image(i))
            dc.DrawBitmap(bmp, x + (sp - bmp.Width) // 2, y + (sp - bmp.Height) // 2, True)

        dc.SetPen(wx.Pen(wx.LIGHT_GREY))
        for c in range(1, self.cols):
            x = wb + c * sp
            dc.DrawLine(x-1, 1, x-1, h - 1)
            for r in range(1,self.rows):
                y = wb + r * sp
                dc.DrawLine(1, y-1, w-1, y-1)

    def on_key_down(self, evt):
        if evt.GetKeyCode() == wx.WXK_ESCAPE:
            self.Dismiss()

    def on_mouse(self, evt):
        sel = None

        (w, h) = self.GetClientSize()
        (x, y) = evt.GetPosition()
        wb = self.WINDOW_BORDER
        x -= wb
        y -= wb
        if 0 <= x < (w - wb) and 0 <= y < (h - wb):
            c = x // self._spacing
            r = y // self._spacing
            i = c + r * self.cols
            if i < self._icons.count():
                sel = i
        if sel != self._selected:
            self._selected = sel
            self.Refresh()

        if  evt.LeftUp() and self._selected != None:
            evt = IconSelectedEvent(IconSelectedType, i)
            wx.PostEvent(self, evt)
            self.Dismiss()
