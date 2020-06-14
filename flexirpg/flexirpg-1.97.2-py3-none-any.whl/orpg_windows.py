# Copyright (C) 2000-2001 The OpenRPG Project
#
#        openrpg-dev@lists.sourceforge.net
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
# File: orpg_windows.py
# Author: Chris Davis
# Maintainer:
# Version:
#   $Id: orpg_windows.py,v 1.42 2007/12/07 20:59:16 digitalxero Exp $
#
# Description: orpg custom windows
#

__version__ = "$Id: orpg_windows.py,v 1.42 2007/12/07 20:59:16 digitalxero Exp $"

from orpg.orpg_wx import *
from orpg.orpgCore import *
import orpg.orpg_xml
import orpg.dirpath

################################
## Tabs
################################
class orpgTabberWnd(FNB.FlatNotebook):
    def __init__(self, parent, closeable=False, size=wx.DefaultSize, style = 0):
        style |= FNB.FNB_HIDE_ON_SINGLE_TAB
        if wx.VERSION[0] <= 2 and wx.VERSION[1] <= 8 and wx.VERSION[2] <= 10:
            FNB.FlatNotebook.__init__(self, parent, -1, size=size, style=style)
        else:
            FNB.FlatNotebook.__init__(self, parent, -1, size=size, agwStyle=style)


###########################
## Some misc dialogs
###########################

class orpgMultiCheckBoxDlg(wx.Dialog):
    """ notes """
    def __init__(self, parent, opts, text, caption, selected=[], pos=wx.DefaultPosition):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, caption, pos, wx.DefaultSize)
        sizers = { 'ctrls' : wx.BoxSizer(wx.VERTICAL), 'buttons' : wx.BoxSizer(wx.HORIZONTAL) }
        self.opts = opts
        self.list = wx.CheckListBox(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,opts)
        for s in selected:
            self.list.Check(s,1)
        sizers['ctrls'].Add(wx.StaticText(self, -1, text), 0, 0)
        sizers['ctrls'].Add(wx.Size(10,10))
        sizers['ctrls'].Add(self.list, 1, wx.EXPAND)
        sizers['buttons'].Add(wx.Button(self, wx.ID_OK, "OK"), 1, wx.EXPAND)
        sizers['buttons'].Add(wx.Size(10,10))
        sizers['buttons'].Add(wx.Button(self, wx.ID_CANCEL, "Cancel"), 1, wx.EXPAND)
        sizers['ctrls'].Add(sizers['buttons'], 0, wx.EXPAND)
        self.SetSizer(sizers['ctrls'])
        self.SetAutoLayout(True)
        self.Fit()
        self.Bind(wx.EVT_BUTTON, self.on_ok, id=wx.ID_OK)

    def on_ok(self,evt):
        checked = []
        for i in range(len(self.opts)):
            if self.list.IsChecked(i):
                checked.append(i)
        self.checked = checked
        self.EndModal(wx.ID_OK)

    def get_selections(self):
        return self.checked

#####################
## Some misc utilties for the GUI
#####################

def createMaskedButton( parent, image, tooltip, id, mask_color=wx.WHITE, image_type=wx.BITMAP_TYPE_GIF ):
    gif = wx.Image( image, image_type, ).ConvertToBitmap()
    mask = wx.Mask( gif, mask_color )
    gif.SetMask( mask )
    btn = wx.BitmapButton( parent, id, gif )
    btn.SetToolTip( wx.ToolTip( tooltip ) )
    return btn
