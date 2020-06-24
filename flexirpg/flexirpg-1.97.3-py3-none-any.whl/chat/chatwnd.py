# FlexiRPG -- Chat window.
#
# Copyright (C) 2000-2001 The OpenRPG Project
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

from html.parser import HTMLParser
from string import *
import codecs
import os
import re
import sys
import time
import time
import traceback
import webbrowser

import orpg.lib.ui as ui
from orpg.orpg_windows import *
from orpg.player_list import WG_LIST
import orpg.dirpath
import orpg.tools.rgbhex
import orpg.tools.inputValidator
from orpg.orpgCore import open_rpg
from orpg.orpg_version import PRODUCT, VERSION
from orpg.chat import commands
import orpg.chat.chat_msg as chat_msg
from orpg.dieroller.parser import parse_all_dice_rolls, dice_roll_error
import orpg.chat.chat_util as chat_util
import orpg.chat.dice_tag as dice_tag

from orpg.networking.client_base import MPLAY_CONNECTED
from orpg.tools.tab_complete import tab_complete

DICE_D4   = 4
DICE_D6   = 6
DICE_D8   = 8
DICE_D10  = 10
DICE_D12  = 12
DICE_D20  = 20
DICE_D100 = 100

FORMAT_BOLD      = 101
FORMAT_ITALIC    = 102
FORMAT_UNDERLINE = 103
FORMAT_COLOR     = 104

SAVE_CHAT = 105

# Global parser for stripping HTML tags:
# The 'tag stripping' is implicit, because this parser echoes every
# type of html data *except* the tags.
class HTMLStripper(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.accum = ""
        self.special_tags = ['hr', 'br', 'img']
    def handle_data(self, data):  # quote cdata literally
        self.accum += data
    def handle_starttag(self, tag, attrs):
        if tag in self.special_tags:
            self.accum += '<' + tag
            for attrib in attrs:
                self.accum += ' ' + attrib[0] + '="' + attrib[1] + '"'
            self.accum += '>'
htmlstripper = HTMLStripper()

# utility function;  see Post().
def strip_html(string):
    "Return string tripped of html tags."
    htmlstripper.reset()
    htmlstripper.accum = ""
    htmlstripper.feed(string)
    htmlstripper.close()
    return htmlstripper.accum

def log( settings, text ):
    filename = settings.get_setting('GameLogPrefix')
    if filename > '' and filename[0] != commands.ANTI_LOG_CHAR:
        filename = filename + time.strftime( '-%Y-%m-%d.html', time.localtime( time.time() ) )
        #filename = time.strftime( filename, time.localtime( time.time() ) )
        timestamp = time.ctime(time.time())
        header = '[%s] : ' % ( timestamp );
        if settings.get_setting('TimeStampGameLog') != '1':
            header = ''
        try:
            f = codecs.open( orpg.dirpath.dir_struct["user"] + filename, 'a', 'utf-8' )
            f.write( '%s%s<br />\n' % ( header, text ) )
            f.close()
        except:
            print("could not open " + orpg.dirpath.dir_struct["user"] + filename + ", ignoring...")
            pass

# This class displayes the chat information in html?
#
# Defines:
#   __init__(self, parent, id)
#   CalculateAllFonts(self, defaultsize)
#   SetDefaultFontAndSize(self, fontname)
#
class chat_html_window(wx.html.HtmlWindow):
    """ a wxHTMLwindow that will load links  """
    # initialization subroutine
    #
    # !self : instance of self
    # !parent :
    # !id :
    def __init__(self, parent, id):
        wx.html.HtmlWindow.__init__(self, parent, id, style=wx.SUNKEN_BORDER | wx.html.HW_SCROLLBAR_AUTO|wx.NO_FULL_REPAINT_ON_RESIZE)
        self.parent = parent
        self.build_menu()
        self.Bind(wx.EVT_RIGHT_DOWN, self.onPopup)
        self.Bind(wx.EVT_SCROLLWIN, self.on_scrollwin)
        self.Bind(wx.html.EVT_HTML_LINK_CLICKED, self.on_link_clicked)

        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()

        self.auto_scroll = True

    def onPopup(self, evt):
        self.PopupMenu(self.menu)

    def on_scrollwin(self, evt):
        # FIXME: should use EVT_SCROLLWIN_CHANGED but it's not
        # available until 2.9.
        wx.CallAfter(self.done_scrolling)
        evt.Skip()

    def on_link_clicked(self, evt):
        href = evt.GetLinkInfo().GetHref()
        s = href.split(':', 2)
        if s[0] == "dice":
            tree = open_rpg.get_component("frame").tree
            tree.set_roll_value(int(s[1]))
        else:
            webbrowser.get().open(href)

    def done_scrolling(self):
        (vx, vy) = self.GetViewStart()
        page_size = self.GetScrollPageSize(wx.VERTICAL)
        max_range = self.GetScrollRange(wx.VERTICAL)

        # Enable auto-scrolling if the window is scrolled to the end
        # or scroll bars aren't present.
        self.auto_scroll = vy + page_size >= max_range or page_size == 0

    def build_menu(self):
        self.menu = wx.Menu()
        item = wx.MenuItem(self.menu, wx.ID_COPY, "Copy", "Copy")
        self.menu.Append(item)

    def save_scroll(self):
        (vx, vy) = self.GetViewStart()
        return vy

    def restore_scroll(self, vy):
        #
        # Bug workaround: If the window transitioned to needing
        # scrollbars then calling self.Scroll() does not correctly
        # scroll and a wx.CallAfter is required.  However, defering
        # the scroll sometimes gives a visual glitch (the window jumps
        # briefy to the top).  So, only defer the scroll when
        # absolutely necessary.
        #
        defer_scroll = vy <= 1

        if self.auto_scroll or vy < 0:
            max_range = self.GetScrollRange(wx.VERTICAL)
            page_size = self.GetScrollPageSize(wx.VERTICAL)
            vy = max_range - page_size

        if defer_scroll:
            wx.CallAfter(self.Scroll, -1, vy)
        else:
            self.Scroll(-1, vy)

    def scroll_down(self):
        self.restore_scroll(-1)

    def mouse_wheel(self, event):
        amt = event.GetWheelRotation()
        units = amt/(-(event.GetWheelDelta()))
        self.ScrollLines(units*3)

    def Header(self):
        return '<html><body bgcolor="' + self.parent.bgcolor + '" text="' + self.parent.textcolor + '">'

    def StripHeader(self):
        return self.GetPageSource().replace(self.Header(), '')

    def GetPageSource(self):
        return self.GetParser().GetSource()

    def CalculateAllFonts(self, defaultsize):
        return [int(defaultsize * 0.4),
                int(defaultsize * 0.7),
                int(defaultsize),
                int(defaultsize * 1.3),
                int(defaultsize * 1.7),
                int(defaultsize * 2),
                int(defaultsize * 2.5)]

    def SetDefaultFontAndSize(self, fontname, fontsize):
        """Set 'fontname' to the default chat font.
           Returns current font settings in a (fontname, fontsize) tuple."""
        self.SetFonts(fontname, "", self.CalculateAllFonts(int(fontsize)))
        return (self.GetFont().GetFaceName(), self.GetFont().GetPointSize())


#########################
#chat frame window
#########################
# These are kinda global...and static..and should be located somewhere else
# then the middle of a file between two classes.

###################
# Tab Types
###################
MAIN_TAB = wx.NewId()
WHISPER_TAB = wx.NewId()
GROUP_TAB = wx.NewId()
NULL_TAB = wx.NewId()

# This class defines the tabbed 'notebook' that holds multiple chatpanels.
# It's the widget attached to the main application frame.
#
# Inherits:  wxNotebook
#
# Defines:
#   create_private_tab(self, playerid)
#   get_tab_index(self, chatpanel)
#   destroy_private_tab(self, chatpanel)
#   OnPageChanged(self, event)
#   set_default_font(self, font, fontsize)

class chat_notebook(orpgTabberWnd):
    def __init__(self, parent, size):
        self.log = open_rpg.get_component("log")
        orpgTabberWnd.__init__(self, parent, True, size=size, style=FNB.FNB_DROPDOWN_TABS_LIST|FNB.FNB_NO_NAV_BUTTONS|FNB.FNB_MOUSE_MIDDLE_CLOSES_TABS)
        self.settings = open_rpg.get_component("settings")
        self.whisper_tabs = []
        self.group_tabs = []
        self.null_tabs = []
        self.il = wx.ImageList(16, 16)
        self.il.Add(orpg.tools.bitmap.create_from_file("icon_player.png"))
        self.il.Add(orpg.tools.bitmap.create_from_file("icon_blank.png"))
        self.SetImageList(self.il)
        # Create "main" chatpanel tab, undeletable, connected to 'public' room.
        self.MainChatPanel = chat_panel(self, -1, MAIN_TAB, 'all')
        self.AddPage(self.MainChatPanel, "Main Room")
        self.SetPageImage(0, 1)
        self.chat_timer = wx.Timer(self, wx.NewId())
        self.Bind(wx.EVT_TIMER, self.MainChatPanel.typingTimerFunc)
        self.chat_timer.Start(1000)
        # Hook up event handler for flipping tabs
        self.Bind(FNB.EVT_FLATNOTEBOOK_PAGE_CHANGED, self.onPageChanged)
        self.Bind(FNB.EVT_FLATNOTEBOOK_PAGE_CHANGING, self.onPageChanging)
        self.Bind(FNB.EVT_FLATNOTEBOOK_PAGE_CLOSING, self.onCloseTab)
        # html font/fontsize is global to all the notebook tabs.
        self.font, self.fontsize =  self.MainChatPanel.chatwnd.SetDefaultFontAndSize(self.settings.get_setting('defaultfont'), self.settings.get_setting('defaultfontsize'))
        self.GMChatPanel = None
        if self.settings.get_setting("GMWhisperTab") == '1':
            self.create_gm_tab()
        self.SetSelection(0)

    def get_tab_index(self, chatpanel):
        "Return the index of a chatpanel in the wxNotebook."
        for i in range(self.GetPageCount()):
            if (self.GetPage(i) == chatpanel):
                return i

    def create_gm_tab(self):
        if self.GMChatPanel == None:
            self.GMChatPanel = chat_panel(self, -1, MAIN_TAB, 'gm')
            self.AddPage(self.GMChatPanel, "GM", False)
            self.SetPageImage(self.GetPageCount()-1, 1)
            self.GMChatPanel.chatwnd.SetDefaultFontAndSize(self.font, self.fontsize)

    def create_whisper_tab(self, playerid):
        "Add a new chatpanel directly connected to integer 'playerid' via whispering."
        private_tab = chat_panel(self, -1, WHISPER_TAB, playerid)
        playername = strip_html(self.MainChatPanel.session.get_player_by_player_id(playerid)[0])
        self.AddPage(private_tab, playername, False)
        private_tab.chatwnd.SetDefaultFontAndSize(self.font, self.fontsize)
        self.whisper_tabs.append(private_tab)
        self.newMsg(self.GetPageCount()-1)
        return private_tab

    def create_group_tab(self, group_name):
        "Add a new chatpanel directly connected to integer 'playerid' via whispering."
        private_tab = chat_panel(self, -1, GROUP_TAB, group_name)
        self.AddPage(private_tab, group_name, False)
        private_tab.chatwnd.SetDefaultFontAndSize(self.font, self.fontsize)
        self.group_tabs.append(private_tab)
        self.newMsg(self.GetPageCount()-1)
        return private_tab

    def create_null_tab(self, tab_name):
        "Add a new chatpanel directly connected to integer 'playerid' via whispering."
        private_tab = chat_panel(self, -1, NULL_TAB, tab_name)
        self.AddPage(private_tab, tab_name, False)
        private_tab.chatwnd.SetDefaultFontAndSize(self.font, self.fontsize)
        self.null_tabs.append(private_tab)
        self.newMsg(self.GetPageCount()-1)
        return private_tab

    def open_whisper_tab(self, player_id):
        whisper_tab = False
        for tab in self.whisper_tabs:
            if tab.sendtarget == player_id:
                whisper_tab = tab
                break;
        if not whisper_tab:
            whisper_tab = self.create_whisper_tab(player_id)
        self.SetSelection(self.GetPageIndex(whisper_tab))
        whisper_tab.chattxt.SetFocus()

    def onCloseTab(self, evt):
        try:
            tabid = evt.GetSelection()
        except:
            tabid = self.GetSelection()

        if self.GetPageText(tabid) == 'Main Room':
            #send no close error to chat
            evt.Veto()
            return
        if self.GetPageText(tabid) == 'GM':
            msg = "Are You Sure You Want To Close This Page?"
            dlg = wx.MessageDialog(self, msg, "NotebookCtrl Question",
                                   wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

            if wx.Platform != '__WXMAC__':
                dlg.SetFont(wx.Font(8, wx.NORMAL, wx.NORMAL, wx.NORMAL, False))

            if dlg.ShowModal() in [wx.ID_NO]:
                dlg.Destroy()
                evt.Veto()
                return
            dlg.Destroy()
            self.GMChatPanel = None
            self.settings.set_setting("GMWhisperTab", "0")
        panel = self.GetPage(tabid)
        if panel in self.whisper_tabs:
            self.whisper_tabs.remove(panel)
        elif panel in self.group_tabs:
            self.group_tabs.remove(panel)
        elif panel in self.null_tabs:
            self.null_tabs.remove(panel)

    def newMsg(self, tabid):
        if tabid != self.GetSelection():
            self.SetPageImage(tabid, 0)

    def onPageChanging(self, event):
        """When private chattabs are selected, set the bitmap back to 'normal'."""
        event.Skip()

    def onPageChanged(self, event):
        """When private chattabs are selected, set the bitmap back to 'normal'."""
        selected_idx = event.GetSelection()
        self.SetPageImage(selected_idx, 1)
        page = self.GetPage(selected_idx)
        #wx.CallAfter(page.set_chat_text_focus, 0)
        event.Skip()

# This class defines and builds the Chat Frame for OpenRPG
#
# Inherits: wxPanel
#
# Defines:
#   __init__((self, parent, id, openrpg, sendtarget)
#   build_ctrls(self)
#   on_buffer_size(self,evt)
#   set_colors(self)
#   set_buffersize(self)
#   set_chat_text(self,txt)
#   on_chat_save(self,evt)
#   on_text_color(self,event)
#   colorize(self, color, text)
#   on_text_format(self,event)
#   OnSize(self,event)
#   InfoPost(self,s)
#   Post(self,s="",send=False,myself=False)
#   ParsePost(self,s,send=False,myself=False)
#   ParseDice(self,s)
#   get_sha_checksum(self)
#   get_color(self)
#

class chat_panel(wx.Panel):

    # This is the initialization subroutine
    #
    # !self : instance of self
    # !parent : parent that defines the chatframe
    # !id :
    # !openrpg :
        # !sendtarget:  who gets outbound messages: either 'all' or a playerid
    def __init__(self, parent, id, tab_type, sendtarget):
        self.log = open_rpg.get_component("log")
        wx.Panel.__init__(self, parent, id)
        self.session = open_rpg.get_component('session')
        self.settings = open_rpg.get_component('settings')
        self.parent = parent
        # who receives outbound messages, either "all" or "playerid" string
        self.sendtarget = sendtarget
        self.type = tab_type
        # create rpghex tool
        self.r_h = orpg.tools.rgbhex.RGBHex()
        self.h = 0
        self.histidx = -1
        self.temptext = ""
        self.history = []
        #self.lasthistevt = None
        self.parsed=0
        #chat commands
        self.chat_cmds = commands.chat_commands(self)
        self.html_strip = strip_html
        self.lastSend = 0         #  this is used to help implement the player typing indicator
        self.lastPress = 0        #  this is used to help implement the player typing indicator

        self.__init_settings()

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CHAR_HOOK, self.on_panel_char)
        self.build_ctrls()
        # html font/fontsize is global to all the notebook tabs.
        StartupFont = self.settings.get_setting("defaultfont")
        StartupFontSize = self.settings.get_setting("defaultfontsize")
        if(StartupFont != "") and (StartupFontSize != ""):
            try:
                self.set_default_font(StartupFont, int(StartupFontSize))
            except:
                pass
        self.font = self.chatwnd.GetFont().GetFaceName()
        self.fontsize = self.chatwnd.GetFont().GetPointSize()
        self.chatwnd.scroll_down()
        self.sendTyping(False)

    def __init_settings(self):
        self.tabbed_whispers = self.settings.lookup('chat', 'tabbedwhispers', 'bool', 'true',
                                                    'Use tabs for whispers')

    def set_default_font(self, fontname=None, fontsize=None):
        """Set all chatpanels to new default fontname/fontsize. Returns current font settings in a (fontname, fontsize) tuple."""
        if (fontname is not None):
            newfont = fontname
        else:
            newfont = self.font
        if (fontsize is not None):
            newfontsize = int(fontsize)
        else:
            newfontsize = int(self.fontsize)
        self.chatwnd.SetDefaultFontAndSize(newfont, newfontsize)
        self.InfoPost("Font is now " + newfont + " point size " + str(newfontsize))
        self.font = newfont
        self.fontsize = newfontsize
        return (self.font, self.fontsize)

    def build_menu(self):
        top_frame = open_rpg.get_component('frame')
        menu = wx.Menu()
        item = wx.MenuItem(menu, wx.ID_ANY, "&Background color", "Background color")
        top_frame.Bind(wx.EVT_MENU, self.OnMB_BackgroundColor, item)
        menu.Append(item)
        item = wx.MenuItem(menu, wx.ID_ANY, "&Text color", "Text color")
        top_frame.Bind(wx.EVT_MENU, self.OnMB_TextColor, item)
        menu.Append(item)
        menu.AppendSeparator()
        item = wx.MenuItem(menu, wx.ID_ANY, "&Chat Focus\tCtrl-H", "Chat Focus")
        self.setChatFocusMenu = item
        top_frame.Bind(wx.EVT_MENU, self.set_chat_text_focus, item)
        menu.Append(item)
        menu.AppendSeparator()
        item = wx.MenuItem(menu, wx.ID_ANY, "Save Chat &Log", "Save Chat Log")
        top_frame.Bind(wx.EVT_MENU, self.on_chat_save, item)
        menu.Append(item)
        item = wx.MenuItem(menu, wx.ID_ANY, "Next Tab\tCtrl+Tab", "Swap Tabs")
        top_frame.Bind(wx.EVT_MENU, self.forward_tabs, item)
        menu.Append(item)
        item = wx.MenuItem(menu, wx.ID_ANY, "Previous Tab\tCtrl+Shift+Tab", "Swap Tabs")
        top_frame.Bind(wx.EVT_MENU, self.back_tabs, item)
        menu.Append(item)
        menu.AppendSeparator()
        settingmenu = wx.Menu()
        wndmenu = wx.Menu()
        tabmenu = wx.Menu()
        toolmenu = wx.Menu()
        item = wx.MenuItem(wndmenu, wx.ID_ANY, "Show Images", "Show Images", wx.ITEM_CHECK)
        top_frame.Bind(wx.EVT_MENU, self.OnMB_ShowImages, item)
        wndmenu.Append(item)
        if self.settings.get_setting("Show_Images_In_Chat") == '1':
            item.Check(True)
        item = wx.MenuItem(wndmenu, wx.ID_ANY, "Strip HTML", "Strip HTML", wx.ITEM_CHECK)
        top_frame.Bind(wx.EVT_MENU, self.OnMB_StripHTML, item)
        wndmenu.Append(item)
        if self.settings.get_setting("striphtml") == '1':
            item.Check(True)
        item = wx.MenuItem(wndmenu, wx.ID_ANY, "Chat Time Index", "Chat Time Index", wx.ITEM_CHECK)
        top_frame.Bind(wx.EVT_MENU, self.OnMB_ChatTimeIndex, item)
        wndmenu.Append(item)
        if self.settings.get_setting("Chat_Time_Indexing") == '1':
            item.Check(True)
        item = wx.MenuItem(wndmenu, wx.ID_ANY, "Show ID in Chat", "Show ID in Chat", wx.ITEM_CHECK)
        top_frame.Bind(wx.EVT_MENU, self.OnMB_ShowIDinChat, item)
        wndmenu.Append(item)
        if self.settings.get_setting("ShowIDInChat") == '1':
            item.Check(True)
        item = wx.MenuItem(wndmenu, wx.ID_ANY, "Log Time Index", "Log Time Index", wx.ITEM_CHECK)
        top_frame.Bind(wx.EVT_MENU, self.OnMB_LogTimeIndex, item)
        wndmenu.Append(item)
        if self.settings.get_setting("TimeStampGameLog") == '1':
            item.Check(True)
        settingmenu.Append(wx.ID_ANY, 'Chat Window', wndmenu )
        item = wx.MenuItem(tabmenu, wx.ID_ANY, "Tabbed Whispers", "Tabbed Whispers", wx.ITEM_CHECK)
        top_frame.Bind(wx.EVT_MENU, self.OnMB_TabbedWhispers, item)
        tabmenu.Append(item)
        if self.tabbed_whispers.bool:
            item.Check(True)
        item = wx.MenuItem(tabmenu, wx.ID_ANY, "GM Tab", "GM Tab", wx.ITEM_CHECK)
        top_frame.Bind(wx.EVT_MENU, self.OnMB_GMTab, item)
        tabmenu.Append(item)
        if self.settings.get_setting("GMWhisperTab") == '1':
            item.Check(True)
        item = wx.MenuItem(tabmenu, wx.ID_ANY, "Group Whisper Tabs", "Group Whisper Tabs", wx.ITEM_CHECK)
        top_frame.Bind(wx.EVT_MENU, self.OnMB_GroupWhisperTabs, item)
        tabmenu.Append(item)
        if self.settings.get_setting("GroupWhisperTab") == '1':
            item.Check(True)
        settingmenu.Append(wx.ID_ANY, 'Chat Tabs', tabmenu)
        menu.Append(wx.ID_ANY, 'Chat Settings', settingmenu)
        top_frame.mainmenu.Insert(2, menu, '&Chat')

    ## Settings Menu Events
    def OnMB_ShowImages(self, event):
        if event.IsChecked():
            self.settings.set_setting("Show_Images_In_Chat", '1')
        else:
            self.settings.set_setting("Show_Images_In_Chat", '0')

    def OnMB_StripHTML(self, event):
        if event.IsChecked():
            self.settings.set_setting("Sstriphtml", '1')
        else:
            self.settings.set_setting("striphtml", '0')

    def OnMB_ChatTimeIndex(self, event):
        if event.IsChecked():
            self.settings.set_setting("Chat_Time_Indexing", '1')
        else:
            self.settings.set_setting("Chat_Time_Indexing", '0')

    def OnMB_ShowIDinChat(self, event):
        if event.IsChecked():
            self.settings.set_setting("ShowIDInChat", '1')
        else:
            self.settings.set_setting("ShowIDInChat", '0')

    def OnMB_LogTimeIndex(self, event):
        if event.IsChecked():
            self.settings.set_setting("TimeStampGameLog", '1')
        else:
            self.settings.set_setting("TimeStampGameLog", '0')

    def OnMB_TabbedWhispers(self, event):
        self.tabbed_whispers.bool = event.IsChecked()

    def OnMB_GMTab(self, event):
        if event.IsChecked():
            self.settings.set_setting("GMWhisperTab", '1')
            self.parent.create_gm_tab()
        else:
            self.settings.set_setting("GMWhisperTab", '0')

    def OnMB_GroupWhisperTabs(self, event):
        if event.IsChecked():
            self.settings.set_setting("GroupWhisperTab", '1')
        else:
            self.settings.set_setting("GroupWhisperTab", '0')

    def OnMB_BackgroundColor(self, event):
        top_frame = open_rpg.get_component('frame')
        hexcolor = self.get_color()
        if hexcolor != None:
            vy = self.chatwnd.save_scroll()
            self.bgcolor = hexcolor
            self.settings.set_setting('bgcolor', hexcolor)
            self.chatwnd.SetPage(self.ResetPage())
            if self.settings.get_setting('ColorTree') == '1':
                top_frame.tree.SetBackgroundColour(self.settings.get_setting('bgcolor'))
                top_frame.tree.Refresh()
                top_frame.players.SetBackgroundColour(self.settings.get_setting('bgcolor'))
                top_frame.players.Refresh()
            else:
                top_frame.tree.SetBackgroundColour('white')
                top_frame.tree.SetForegroundColour('black')
                top_frame.tree.Refresh()
                top_frame.players.SetBackgroundColour('white')
                top_frame.players.SetForegroundColour('black')
                top_frame.players.Refresh()
            self.chatwnd.restore_scroll(vy)

    def OnMB_TextColor(self, event):
        top_frame = open_rpg.get_component('frame')
        hexcolor = self.get_color()
        if hexcolor != None:
            vy = self.chatwnd.save_scroll()
            self.textcolor = hexcolor
            self.settings.set_setting('textcolor', hexcolor)
            self.chatwnd.SetPage(self.ResetPage())
            if self.settings.get_setting('ColorTree') == '1':
                top_frame.tree.SetForegroundColour(self.settings.get_setting('textcolor'))
                top_frame.tree.Refresh()
                top_frame.players.SetForegroundColour(self.settings.get_setting('textcolor'))
                top_frame.players.Refresh()
            else:
                top_frame.tree.SetBackgroundColour('white')
                top_frame.tree.SetForegroundColour('black')
                top_frame.tree.Refresh()
                top_frame.players.SetBackgroundColour('white')
                top_frame.players.SetForegroundColour('black')
                top_frame.players.Refresh()
            self.chatwnd.restore_scroll(vy)

    def forward_tabs(self, evt):
        self.parent.AdvanceSelection()

    def back_tabs(self, evt):
        self.parent.AdvanceSelection(False)

    # This subroutine builds the controls for the chat frame
    #
    # !self : instance of self
    def build_ctrls(self):
        self.chatwnd = chat_html_window(self,-1)
        self.set_colors()
        wx.CallAfter(self.chatwnd.SetPage, self.chatwnd.Header())
        self.chattxt = wx.TextCtrl(self, -1, "", style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)
        self.build_bar()
        self.basesizer = wx.BoxSizer(wx.VERTICAL)
        self.basesizer.Add( self.chatwnd,1,wx.EXPAND )
        self.basesizer.Add( self.toolbar_sizer, 0, wx.EXPAND )
        self.basesizer.Add( self.chattxt, 0, wx.EXPAND )
        self.SetSizer(self.basesizer)
        self.SetAutoLayout(True)
        self.Fit()
        #events
        self.Bind(wx.EVT_TOOL, self.onDieRoll, id=DICE_D4)
        self.Bind(wx.EVT_TOOL, self.onDieRoll, id=DICE_D6)
        self.Bind(wx.EVT_TOOL, self.onDieRoll, id=DICE_D8)
        self.Bind(wx.EVT_TOOL, self.onDieRoll, id=DICE_D10)
        self.Bind(wx.EVT_TOOL, self.onDieRoll, id=DICE_D12)
        self.Bind(wx.EVT_TOOL, self.onDieRoll, id=DICE_D20)
        self.Bind(wx.EVT_TOOL, self.onDieRoll, id=DICE_D100)
        self.Bind(wx.EVT_TOOL, self.on_text_format, id=FORMAT_BOLD)
        self.Bind(wx.EVT_TOOL, self.on_text_format, id=FORMAT_ITALIC)
        self.Bind(wx.EVT_TOOL, self.on_text_format, id=FORMAT_UNDERLINE)
        self.Bind(wx.EVT_TOOL, self.on_text_color, id=FORMAT_COLOR)
        self.Bind(wx.EVT_TOOL, self.on_chat_save, id=SAVE_CHAT)
        self.chattxt.Bind(wx.EVT_MOUSEWHEEL, self.chatwnd.mouse_wheel)
        self.chattxt.Bind(wx.EVT_CHAR, self.on_text_char)

    def build_bar(self):
        self.toolbar_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.numDieText = None
        self.dieModText = None

        self.toolbar = ui.ToolBar(self)

        # Dice tools.
        self.numDieText = wx.TextCtrl(self.toolbar, wx.ID_ANY, "1", size=wx.Size(48, 25),
                                      validator=orpg.tools.inputValidator.MathOnlyValidator())
        self.numDieText.SetToolTip(wx.ToolTip("Number of dice"))
        self.toolbar.AddControl(self.numDieText)

        self.toolbar.AddTool(DICE_D4, "d4",
                             bitmap=orpg.tools.bitmap.create_from_file("tool_d4.png"),
                             shortHelp="Roll d4")
        self.toolbar.AddTool(DICE_D6, "d6",
                             bitmap=orpg.tools.bitmap.create_from_file("tool_d6.png"),
                             shortHelp="Roll d6")
        self.toolbar.AddTool(DICE_D8, "d8",
                             bitmap=orpg.tools.bitmap.create_from_file("tool_d8.png"),
                             shortHelp="Roll d8")
        self.toolbar.AddTool(DICE_D10, "d10",
                             bitmap=orpg.tools.bitmap.create_from_file("tool_d10.png"),
                             shortHelp="Roll d10")
        self.toolbar.AddTool(DICE_D12, "d12",
                             bitmap=orpg.tools.bitmap.create_from_file("tool_d12.png"),
                             shortHelp="Roll d12")
        self.toolbar.AddTool(DICE_D20, "d20",
                             bitmap=orpg.tools.bitmap.create_from_file("tool_d20.png"),
                             shortHelp="Roll d20")
        self.toolbar.AddTool(DICE_D100, "d100",
                             bitmap=orpg.tools.bitmap.create_from_file("tool_d100.png"),
                             shortHelp="Roll d100")

        self.dieModText = wx.TextCtrl(self.toolbar, wx.ID_ANY, "", size= wx.Size(48, 25),
                                      validator=orpg.tools.inputValidator.MathOnlyValidator())
        self.dieModText.SetToolTip(wx.ToolTip("Dice roll modifier"))
        self.toolbar.AddControl(self.dieModText)

        # Format tools.
        self.toolbar.AddTool(FORMAT_BOLD, "Bold",
                             bitmap=orpg.tools.bitmap.create_from_file("tool_bold.png"),
                             shortHelp="Bold text")
        self.toolbar.AddTool(FORMAT_ITALIC, "Italic",
                             bitmap=orpg.tools.bitmap.create_from_file("tool_italic.png"),
                             shortHelp="Italic text")
        self.toolbar.AddTool(FORMAT_BOLD, "Underline",
                             bitmap=orpg.tools.bitmap.create_from_file("tool_underline.png"),
                             shortHelp="Underline text")
        self.color_icon = orpg.tools.bitmap.ColorIcon("tool_color.png")
        self.toolbar.AddTool(FORMAT_COLOR, "Text color",
                             self.color_icon.bitmap(wx.Colour(self.mytextcolor)),
                             shortHelp="Text color")

        # Other tools.
        self.toolbar.AddTool(SAVE_CHAT, "Save chat",
                             orpg.tools.bitmap.create_from_file("tool_save.png"),
                             shortHelp="Save chat text")

        self.toolbar.Realize()
        self.toolbar_sizer.Add((3, 0))
        self.toolbar_sizer.Add( self.toolbar, 0, wx.EXPAND)

    def on_text_char(self, event):
        if self.session.get_status() == MPLAY_CONNECTED:
            thisPress = time.time()
            if (thisPress - self.lastSend) > 4:
                self.sendTyping(1)
            self.lastPress = thisPress
        event.Skip()

    #  This subroutine gets called once a second by the typing Timer
    #  It checks if we need to send a not_typing message
    #
    #  self:  duh
    def typingTimerFunc(self, event):
        if self.lastSend:                          #  This will be zero when not typing, so equiv to if is_typing
            thisTime = time.time()                 #  thisTime is a local temp variable
            if (thisTime - self.lastPress) > 4:    #  Check to see if it's been 5 seconds since our last keystroke
                                               #    If we're not already typing, then self.lastSend will be 0

                self.sendTyping(0)                 #  send a typing event here (0 for False)
    #  This subroutine actually takes care of sending the messages for typing/not_typing events
    #
    #  self:  duh
    #  typing:  boolean
    def sendTyping(self, typing):
        if typing:
            self.lastSend = time.time()  #  remember our send time for use in myKeyHook()
            #I think this is cleaner
            status_text = self.settings.get_setting('TypingStatusAlias')
            if status_text == "" or status_text == None:
                status_text = "Typing"
            self.session.set_text_status(status_text)
        else:
            self.lastSend = 0                            #  set lastSend to zero to indicate we're not typing
            #I think this is cleaner
            status_text = self.settings.get_setting('IdleStatusAlias')
            if status_text == "" or status_text == None:
                status_text = "Idle"
            self.session.set_text_status(status_text)

    # This subroutine sets the colors of the chat based on the settings in the
    # self instance.
    #
    # !self : instance of self
    def set_colors(self):
        # chat window backround color
        self.bgcolor = self.settings.get_setting('bgcolor')
        # chat window normal text color
        self.textcolor = self.settings.get_setting('textcolor')
        # color of text player types
        self.mytextcolor = self.settings.get_setting('mytextcolor')
        # color of system warnings
        self.syscolor = self.settings.get_setting('syscolor')
        # color of system info messages
        self.infocolor = self.settings.get_setting('infocolor')
        # color of emotes
        self.emotecolor = self.settings.get_setting('emotecolor')
        # color of whispers
        self.whispercolor = self.settings.get_setting('whispercolor')

    # This subroutine will insert text into the chat window
    #
    # !self : instance of self
    # !txt : text to be inserted into the chat window
    def set_chat_text(self, txt):
        self.chattxt.SetValue(txt)
        self.chattxt.SetFocus()
        self.chattxt.SetInsertionPointEnd()

    def get_chat_text(self):
        return self.chattxt.GetValue()

    # This subroutine sets the focus to the chat window
    def set_chat_text_focus(self, event):
        wx.CallAfter(self.chattxt.SetFocus)

    # This subrtouine grabs the user input and make the special keys and
    # modifiers work.
    #
    # !self : instance of self
    # !event :
    #
    # Note:  self.chattxt now handles it's own Key events.  It does, however still
    #        call it's parent's (self) OnChar to handle "default" behavior.
    def on_panel_char(self, event):
        s = self.chattxt.GetValue()
        #self.histlen = len(self.history) - 1

        ## RETURN KEY (no matter if there is text in chattxt)
        #  This section is run even if there is nothing in the chattxt (as opposed to the next wx.WXK_RETURN handler
        if event.GetKeyCode() == wx.WXK_RETURN:
            self.set_colors()
            if self.session.get_status() == MPLAY_CONNECTED:          #  only do if we're connected
                self.sendTyping(0)                                    #  Send a "not_typing" event on enter key press
        macroText=""


        recycle_bin = {wx.WXK_F1: 'event.GetKeyCode() == wx.WXK_F1', wx.WXK_F2: 'event.GetKeyCode() == wx.WXK_F2', wx.WXK_F3: 'event.GetKeyCode() == wx.WXK_F3', wx.WXK_F4: 'event.GetKeyCode() == wx.WXK_F4', wx.WXK_F5: 'event.GetKeyCode() == wx.WXK_F5', wx.WXK_F6: 'event.GetKeyCode() == wx.WXK_F6', wx.WXK_F7: 'event.GetKeyCode() == wx.WXK_F7', wx.WXK_F8: 'event.GetKeyCode() == wx.WXK_F8', wx.WXK_F9: 'event.GetKeyCode() == wx.WXK_F9', wx.WXK_F10: 'event.GetKeyCode() == wx.WXK_F10', wx.WXK_F11: 'event.GetKeyCode() == wx.WXK_F11', wx.WXK_F12: 'event.GetKeyCode() == wx.WXK_F12'}
# Recycle Bin and Lambda should reduce this whole IF ELIF statement block.
        bin_event = event.GetKeyCode()
        if bin_event in recycle_bin:
            macroText = self.settings.get_setting(recycle_bin[bin_event][29:])
            recycle_bin = {}; del bin_event

        # Append to the existing typed text as needed and make sure the status doesn't change back.
        if len(macroText):
            self.sendTyping(0)
            s = macroText

        ## RETURN KEY (and not text in control)
        if (event.GetKeyCode() == wx.WXK_RETURN and len(s)) or len(macroText):
            self.histidx = -1
            self.temptext = ""
            self.history = [s] + self.history#prepended instead of appended now, so higher index = greater age
            if not len(macroText):
                self.chattxt.SetValue("")
            if s[0] != "/": ## it's not a slash command
                s = self.ParsePost( s, True, True )
            else:
                self.chat_cmds.docmd(s) # emote is in chatutils.py

        ## UP KEY
        elif event.GetKeyCode() == wx.WXK_UP:
            if self.histidx < len(self.history)-1:
                #text that's not in history but also hasn't been sent to chat gets stored in self.temptext
                #this way if someone presses the up key, they don't lose their current message permanently
                #(unless they also press enter at the time)
                if self.histidx is -1:
                    self.temptext = self.chattxt.GetValue()
                self.histidx += 1
                self.chattxt.SetValue(self.history[self.histidx])
                self.chattxt.SetInsertionPointEnd()
            else:
                self.histidx = len(self.history) -1#in case it got too high somehow, this should fix it
                #self.InfoPost("**Going up? I don't think so.**")
            #print self.histidx, "in",self.history

        ## DOWN KEY
        elif event.GetKeyCode() == wx.WXK_DOWN:
            #histidx of -1 indicates currently viewing text that's not in self.history
            if self.histidx > -1:
                self.histidx -= 1
                if self.histidx is -1: #remember, it just decreased
                    self.chattxt.SetValue(self.temptext)
                else:
                    self.chattxt.SetValue(self.history[self.histidx])
                self.chattxt.SetInsertionPointEnd()
            else:
                self.histidx = -1 #just in case it somehow got below -1, this should fix it
                #self.InfoPost("**Going down? I don't think so.**")
            #print self.histidx, "in",self.history

        ## TAB KEY
        elif  event.GetKeyCode() == wx.WXK_TAB:
            if s !="":
                partial_nick = s
                nicks = []

                # Get all possible nicks.
                striphtmltag = re.compile('<[^>]+>*')
                for getnames in list(self.session.players.keys()):
                    nick = striphtmltag.sub("", self.session.players[getnames][0])
                    nicks.append(nick)

                # Try and complete the partial nick.
                completed_nick = tab_complete(partial_nick, nicks)
                if completed_nick:
                    self.chattxt.SetValue(completed_nick)
                    self.chattxt.SetInsertionPointEnd()

        ## PAGE UP
        elif event.GetKeyCode() == wx.WXK_PAGEUP:
            self.chatwnd.ScrollPages(-1)

        ## PAGE DOWN
        elif event.GetKeyCode() == wx.WXK_PAGEDOWN:
            self.chatwnd.ScrollPages(1)

        ## END
        elif event.GetKeyCode() == wx.WXK_END:
            event.Skip()

        ## NOTHING
        else:
            event.Skip()

    def onDieRoll(self, evt):
        """Roll the dice based on the button pressed and the die modifiers entered, if any."""
        # Get any die modifiers if they have been entered
        numDie = self.numDieText.GetValue()
        dice = evt.GetId()
        dieMod = self.dieModText.GetValue()
        if len(dieMod) and dieMod[0] not in "*/-+":
            dieMod = "+" + dieMod
        # Now, apply and roll die mods based on the button that was pressed
        self.ParsePost(f"[{numDie}d{dice}{dieMod}]", 1, 1)
        self.chattxt.SetFocus()

    # This subroutine saves a chat buffer as html to a file chosen via a
    # FileDialog.
    #
    # !self : instance of self
    # !evt :
    def on_chat_save(self, evt):
        f = wx.FileDialog(self,"Save Chat Buffer",".","","HTM* (*.htm*)|*.htm*|HTML (*.html)|*.html|HTM (*.htm)|*.htm",wx.FD_SAVE)
        if f.ShowModal() == wx.ID_OK:
            file = open(f.GetPath(), "w")
            file.write(self.ResetPage() + "</body></html>")
            file.close()
        f.Destroy()

    def ResetPage(self):
        self.set_colors()
        buffertext = self.chatwnd.Header() + "\n"
        buffertext += chat_util.strip_body_tags(self.chatwnd.StripHeader()).replace("<br>", "<br />").replace('</html>', '').replace("<br />", "<br />\n").replace("\n\n", '')
        return buffertext

    # This subroutine sets the color of selected text, or base text color if
    # nothing is selected
    def on_text_color(self, event):
        hexcolor = self.r_h.do_hex_color_dlg(self)
        if hexcolor != None:
            (beg,end) = self.chattxt.GetSelection()
            if beg != end:
                txt = self.chattxt.GetValue()
                txt = txt[:beg]+self.colorize(hexcolor,txt[beg:end]) +txt[end:]
                self.chattxt.SetValue(txt)
                self.chattxt.SetInsertionPointEnd()
            else:
                self.settings.set_setting('mytextcolor',hexcolor)
                self.set_colors()
                self.toolbar.SetToolNormalBitmap(FORMAT_COLOR,
                                                 self.color_icon.bitmap(wx.Colour(self.mytextcolor)))

    # This subroutine take a color and a text string and formats it into html.
    #
    # !self : instance of self
    # !color : color for the text to be set
    # !text : text string to be included in the html.
    def colorize(self, color, text):
        """Puts font tags of 'color' around 'text' value, and returns the string"""
        return "<font color='" + color + "'>" + text + "</font>"

    # This subroutine takes and event and inserts text with the basic format
    # tags included.
    #
    # !self : instance of self
    # !event :
    def on_text_format(self, event):
        tool = event.GetId()
        txt = self.chattxt.GetValue()
        (beg,end) = self.chattxt.GetSelection()
        if beg != end:
            sel_txt = txt[beg:end]
        else:
            sel_txt = txt
        if tool == FORMAT_BOLD:
            sel_txt = "<b>" + sel_txt + "</b>"
        elif tool == FORMAT_ITALIC:
            sel_txt = "<i>" + sel_txt + "</i>"
        elif tool == FORMAT_UNDERLINE:
            sel_txt = "<u>" + sel_txt + "</u>"
        if beg != end:
            txt = txt[:beg] + sel_txt + txt[end:]
        else:
            txt = sel_txt
        self.chattxt.SetValue(txt)
        self.chattxt.SetInsertionPointEnd()
        self.chattxt.SetFocus()

    # This subroutine will change the dimension of the window
    #
    # !self : instance of self
    # !event :
    def OnSize(self, event=None):
        self.chatwnd.scroll_down()
        event.Skip()

    def open_whisper_tab(self, player_id):
        self.parent.open_whisper_tab(player_id)

    ###### message helpers ######
    def PurgeChat(self):
        self.set_colors()
        self.chatwnd.SetPage(self.chatwnd.Header())

    def system_message(self, text):
        self.send_chat_message(text,chat_msg.SYSTEM_MESSAGE)
        self.SystemPost(text)

    def info_message(self, text):
        self.send_chat_message(text,chat_msg.INFO_MESSAGE)
        self.InfoPost(text)

    def get_gms(self):
        the_gms = []
        for playerid in self.session.players:
            if len(self.session.players[playerid])>7:
                if self.session.players[playerid][7]=="GM" and self.session.group_id != '0':
                    the_gms += [playerid]
        return the_gms

    def GetName(self):
        player = self.session.get_my_info()
        return self.chat_display_name(player)

    def emote_message(self, text):
        text = self.NormalizeParse(text)
        text = self.colorize(self.emotecolor, text)

        if self.type == MAIN_TAB and self.sendtarget == 'all':
            self.send_chat_message(text,chat_msg.EMOTE_MESSAGE)
        elif self.type == MAIN_TAB and self.sendtarget == "gm":
            msg_type = chat_msg.WHISPER_EMOTE_MESSAGE
            the_gms = self.get_gms()
            for each_gm in the_gms:
                self.send_chat_message(text,chat_msg.WHISPER_EMOTE_MESSAGE, str(each_gm))
        elif self.type == GROUP_TAB and self.sendtarget in WG_LIST:
            for pid in WG_LIST[self.sendtarget]:
                self.send_chat_message(text,chat_msg.WHISPER_EMOTE_MESSAGE, str(pid))
        elif self.type == WHISPER_TAB:
            self.send_chat_message(text,chat_msg.WHISPER_EMOTE_MESSAGE, str(self.sendtarget))
        elif self.type == NULL_TAB:
            pass
        name = self.GetName()
        text = "** " + name + " " + text + " **"
        self.EmotePost(text)

    def whisper_to_players(self, text, player_ids):
        # Heroman - apply any filtering selected
        text = self.NormalizeParse(text)
        player_names = ""
        # post to our chat before we colorize
        for m in player_ids:
            id = m.strip()
            if self.session.is_valid_id(id):
                returned_name = self.session.get_player_by_player_id(id)[0]
                player_names += returned_name
                player_names += ", "
            else:
                player_names += " Unknown!"
                player_names += ", "
        comma = ","
        comma.join(player_ids)
        if (self.sendtarget == "all"):
            self.InfoPost("<i>whispering to "+ player_names + " " + text + "</i> ")
        # colorize and loop, sending whisper messages to all valid clients
        text = self.colorize(self.mytextcolor, text)
        for id in player_ids:
            id = id.strip()
            if self.session.is_valid_id(id):
                self.send_chat_message(text,chat_msg.WHISPER_MESSAGE,id)
            else:
                self.InfoPost(id + " Unknown!")

    def send_chat_message(self, text, type=chat_msg.CHAT_MESSAGE, player_id="all"):
        send = 1
        msg = chat_msg.chat_msg()
        msg.set_text(text)
        msg.set_type(type)
        turnedoff = False
        if self.settings.get_setting("ShowIDInChat") == "1":
            turnedoff = True
            self.settings.set_setting("ShowIDInChat", "0")
        playername = self.GetName()

        if turnedoff:
            self.settings.set_setting("ShowIDInChat", "1")
        msg.set_alias(playername)
        if send:
            self.session.send(msg.toxml(),player_id)
        del msg

    #### incoming chat message handler #####
    def post_incoming_msg(self, msg, player):
        # pull data
        type = msg.get_type()
        text = msg.get_text()
        alias = msg.get_alias()
        # who sent us the message?
        if alias:
            display_name = self.chat_display_name([alias, player[1], player[2]])
        elif player:
            display_name = self.chat_display_name(player)
        else:
            display_name = "Server Administrator"

        #image stripping for players' names
        strip_img = self.settings.get_setting("Show_Images_In_Chat")
        if (strip_img == "0"):
            display_name = chat_util.strip_img_tags(display_name)
        #end image stripping. --mDuo13, July 11th, 2005
        # act on the type of messsage
        if (type == chat_msg.CHAT_MESSAGE):
            text = "<b>" + display_name + "</b>: " + text
            self.Post(text)
            self.parent.newMsg(0)
        elif type == chat_msg.WHISPER_MESSAGE or type == chat_msg.WHISPER_EMOTE_MESSAGE:
            displaypanel = self
            whisperingstring = " (whispering): "
            panelexists = 0
            GMWhisperTab = self.settings.get_setting("GMWhisperTab")
            GroupWhisperTab = self.settings.get_setting("GroupWhisperTab")
            name = '<i><b>' + display_name + '</b>: '
            text += '</i>'
            panelexists = 0
            created = 0
            try:
                if GMWhisperTab == '1':
                    the_gms = self.get_gms()
                    #Check if whisper if from a GM
                    if player[2] in the_gms:
                        msg = name + ' (GM Whisper:) ' + text
                        if type == chat_msg.WHISPER_MESSAGE:
                            self.parent.GMChatPanel.Post(msg)
                        else:
                            self.parent.GMChatPanel.EmotePost("**" + msg + "**")
                        idx = self.parent.get_tab_index(self.parent.GMChatPanel)
                        self.parent.newMsg(idx)
                        panelexists = 1
                #See if message if from someone in our groups or for a whisper tab we already have
                if not panelexists and GroupWhisperTab == "1":
                    for panel in self.parent.group_tabs:
                        if panel.sendtarget in WG_LIST and int(player[2]) in WG_LIST[panel.sendtarget]:
                            msg = name + text
                            if type == chat_msg.WHISPER_MESSAGE:
                                panel.Post(msg)
                            else:
                                panel.EmotePost("**" + msg + "**")
                            idx = self.parent.get_tab_index(panel)
                            self.parent.newMsg(idx)
                            panelexists = 1
                            break
                if not panelexists and self.tabbed_whispers.bool:
                    for panel in self.parent.whisper_tabs:
                        #check for whisper tabs as well, to save the number of loops
                        if panel.sendtarget == player[2]:
                            msg = name + whisperingstring + text
                            if type == chat_msg.WHISPER_MESSAGE:
                                panel.Post(msg)
                            else:
                                panel.EmotePost("**" + msg + "**")
                            idx = self.parent.get_tab_index(panel)
                            self.parent.newMsg(idx)
                            panelexists = 1
                            break
                #We did not fint the tab
                if not panelexists:
                    #If we get here the tab was not found
                    if GroupWhisperTab == "1":
                        for group in list(WG_LIST.keys()):
                            #Check if this group has the player in it
                            if int(player[2]) in WG_LIST[group]:
                                #Yup, post message. Player may be in more then 1 group so continue as well
                                panel = self.parent.create_group_tab(group)
                                msg = name + text
                                if type == chat_msg.WHISPER_MESSAGE:
                                    wx.CallAfter(panel.Post, msg)
                                else:
                                    wx.CallAfter(panel.EmotePost, "**" + msg + "**")
                                created = 1
                    #Check to see if we should create a whisper tab
                    if not created and self.tabbed_whispers.bool:
                        panel = self.parent.create_whisper_tab(player[2])
                        msg = name + whisperingstring + text
                        if type == chat_msg.WHISPER_MESSAGE:
                            wx.CallAfter(panel.Post, msg)
                        else:
                            wx.CallAfter(panel.EmotePost, "**" + msg + "**")
                        created = 1
                    #Final check
                    if not created:
                        #No tabs to create, just send the message to the main chat tab
                        msg = name + whisperingstring + text
                        if type == chat_msg.WHISPER_MESSAGE:
                            self.parent.MainChatPanel.Post(msg)
                        else:
                            self.parent.MainChatPanel.EmotePost("**" + msg + "**")
                        self.parent.newMsg(0)
            except Exception as e:
                self.log.log(traceback.format_exc(), ORPG_GENERAL)
                self.log.log("EXCEPTION: 'Error in posting whisper message': " + str(e), ORPG_GENERAL)
        elif (type == chat_msg.EMOTE_MESSAGE):
            text = "** " + display_name + " " + text + " **"
            self.EmotePost(text)
            self.parent.newMsg(0)
        elif (type == chat_msg.INFO_MESSAGE):
            text = "<b>" + display_name + "</b>: " + text
            self.InfoPost(text)
            self.parent.newMsg(0)
        elif (type == chat_msg.SYSTEM_MESSAGE):
            text = "<b>" + display_name + "</b>: " + text
            self.SystemPost(text)
            self.parent.newMsg(0)

    def InfoPost(self, s):
        self.Post(self.colorize(self.infocolor, s))

    def SystemPost(self, s):
        self.Post(self.colorize(self.syscolor, s))

    def EmotePost(self, s):
        self.Post(self.colorize(self.emotecolor, s))

    #### Standard Post method #####
    def Post(self, s="", send=False, myself=False):
        strip_p = self.settings.get_setting("striphtml")
        strip_img = self.settings.get_setting("Show_Images_In_Chat")#moved back 7-11-05. --mDuo13
        if (strip_p == "1"):
            s = strip_html(s)
        if (strip_img == "0"):
            s = chat_util.strip_img_tags(s)
        s = chat_util.simple_html_repair(s)
        s = chat_util.strip_script_tags(s)
        s = chat_util.strip_li_tags(s)
        s = chat_util.strip_body_tags(s)#7-27-05 mDuo13
        s = chat_util.strip_misalignment_tags(s)#7-27-05 mDuo13
        display_name = self.GetName()
        newline = ''
        if myself:
            name = "<b>" + display_name + "</b>: "
            s = self.colorize(self.mytextcolor, s)
        else:
            name = ""
        # Only add lines with visible text.
        lineHasText = strip_html(s).replace(" ","").strip() != ""
        if lineHasText:
            #following added by mDuo13
            if myself:
                s2 = s
                if s2 != "":
                    #Italici the messages from tabbed whispers
                    if self.type == WHISPER_TAB or self.type == GROUP_TAB or self.sendtarget == 'gm':
                        s2 = s2 + '</i>'
                        name = '<i>' + name
                        if self.type == WHISPER_TAB:
                            name += " (whispering): "
                        elif self.type == GROUP_TAB:
                            name += self.settings.get_setting("gwtext") + ' '
                        elif self.sendtarget == 'gm':
                            name += " (whispering to GM) "
                    newline = self.TimeIndexString() + name +  s2 + "<br />"
                    log( self.settings, name + s2 )
            else:
                newline = self.TimeIndexString() + name +  s + "<br />"
                log( self.settings, name + s )
        else:
            send = False

        self.append_to_page(newline)

        if send:
            if self.type == MAIN_TAB and self.sendtarget == 'all':
                self.send_chat_message(s)
            elif self.type == MAIN_TAB and self.sendtarget == "gm":
                the_gms = self.get_gms()
                self.whisper_to_players(s, the_gms)
            elif self.type == GROUP_TAB and self.sendtarget in WG_LIST:
                members = []
                for pid in WG_LIST[self.sendtarget]:
                    members.append(str(WG_LIST[self.sendtarget][pid]))
                self.whisper_to_players(self.settings.get_setting("gwtext") + s, members)
            elif self.type == WHISPER_TAB:
                self.whisper_to_players(s, [self.sendtarget])
            elif self.type == NULL_TAB:
                pass
            else:
                self.InfoPost("Failed to send message, unknown send type for this tab")
        self.parsed=0

    #
    # TimeIndexString()
    #
    # time indexing for chat display only (don't log time indexing)
    # added by Snowdog 4/04
    def TimeIndexString(self):
        try:
            mtime = ""
            if self.settings.get_setting('Chat_Time_Indexing') == "0":
                pass
            elif self.settings.get_setting('Chat_Time_Indexing') == "1":
                mtime = time.strftime("[%X] ", time.localtime())
            return mtime
        except Exception as e:
            self.log.log(traceback.format_exc(), ORPG_GENERAL)
            self.log.log("EXCEPTION: " + str(e), ORPG_GENERAL)
            return "[ERROR]"

    ####  Post with parsing dice ####
    def ParsePost(self, s, send=False, myself=False, symtab=None):
        s = self.NormalizeParse(s, symtab)
        self.set_colors()
        self.Post(s,send,myself)

    def NormalizeParse(self, s, symtab=None):
        if self.parsed == 0:
            s = self.ParseDice(s, symtab)
            self.parsed = 1
        return s

    def ParseDice(self, s, symtab):
        """Parses player input for embedded dice rolls"""
        try:
            return parse_all_dice_rolls(symtab, s)
        except dice_roll_error as e:
            self.InfoPost("Dice error: " + e.str)
            return ""

    def append_to_page(self, text):
        vy = self.chatwnd.save_scroll()
        self.chatwnd.AppendToPage(text)
        self.chatwnd.restore_scroll(vy)

    # This subroutine builds a chat display name.
    #
    def chat_display_name(self, player):
        if self.settings.get_setting("ShowIDInChat") == "0":
            display_name = player[0]
        else:
            display_name = "("+player[2]+") " + player[0]
        return display_name

    # This subroutine will get a hex color and return it, or return nothing
    #
    def get_color(self):
        data = wx.ColourData()
        data.SetChooseFull(True)
        dlg = wx.ColourDialog(self, data)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetColourData()
            (red,green,blue) = data.GetColour().Get(includeAlpha=False)
            hexcolor = self.r_h.hexstring(red, green, blue)
            dlg.Destroy()
            return hexcolor
        else:
            dlg.Destroy()
            return None
