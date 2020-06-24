#!/usr/bin/env python
#
# Copyright (C) 2009 David Vrabel
# Copyright (C) 2000-2001 The OpenRPG Project
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
# The main entry point of the client application.
#

from orpg.orpg_wx import *
from orpg.orpgCore import *
from orpg.orpg_version import *
from orpg.orpg_windows import *
import orpg.dirpath
import orpg.orpg_xml
import orpg.player_list
import orpg.tools.orpg_settings
import orpg.tools.orpg_log
import orpg.tools.passtool
import orpg.lib.ui as ui

import orpg.mapper.image
import orpg.mapper.imageprovider
import orpg.mapper.imagelibrary
import orpg.mapper.displayimage

image_library = orpg.mapper.imagelibrary.ImageLibrary(orpg.mapper.displayimage.DisplayImage)

import orpg.tools.validate
import orpg.tools.rgbhex
import orpg.gametree.gametree
import orpg.chat.chatwnd
import orpg.networking.mplay_client
import orpg.networking.mplay_queue
import orpg.networking.gsclient
import orpg.mapper.map

####################################
## Main Frame
####################################

OPT_FILE_SERVERS = 1000
OPT_FILE_QUIT = 1001
OPT_EDIT_PREFS = 1002
OPT_HELP_ABOUT = 1003

class orpgFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.Point(100, 100), wx.Size(600,420), style=wx.DEFAULT_FRAME_STYLE)

        self.log = open_rpg.get_component("log")
        self.xml = open_rpg.get_component("xml")
        self.dir_struct = open_rpg.get_component("dir_struct")
        self.validate = open_rpg.get_component("validate")
        self.settings = open_rpg.get_component("settings")
        self.rgbcovert = orpg.tools.rgbhex.RGBHex()
        self._mgr = AUI.AuiManager(self)

        if wx.Platform == '__WXMSW__':
            icon = wx.Icon(orpg.dirpath.dir_struct["icon"]+'icon_flexirpg.ico', wx.BITMAP_TYPE_ICO)
        else:
            icon = wx.Icon(orpg.dirpath.dir_struct["icon"]+'icon_flexirpg.png', wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)

        # create session
        call_backs = {"on_receive":self.on_receive,
                "on_mplay_event":self.on_mplay_event,
                "on_group_event":self.on_group_event,
                "on_player_event":self.on_player_event,
                "on_password_signal":self.on_password_signal}
        self.session = orpg.networking.mplay_client.mplay_client(
            self.settings.get_setting("player"), self, call_backs)
        self.Bind(orpg.networking.mplay_queue.EVT_QUEUE_READY, self.session.poll)
        self.ping_timer = wx.Timer(self, wx.NewId())
        self.Bind(wx.EVT_TIMER, self.session.update, self.ping_timer)

        image_library.register_provider(orpg.mapper.imageprovider.ImageProviderCache())
        image_library.register_provider(orpg.mapper.imageprovider.ImageProviderClient(self.session,
                                                                                      image_library))

        #create password manager --SD 8/03
        self.password_manager = orpg.tools.passtool.PassTool()
        open_rpg.add_component("session", self.session)
        open_rpg.add_component('frame', self)
        open_rpg.add_component('password_manager', self.password_manager)

        # build frame windows
        self.build_menu()
        self.build_gui()
        self.build_additional_menus()
        open_rpg.add_component("chat",self.chat)
        open_rpg.add_component("map",self.map)

        tree_xml = self.settings.get_setting("gametree")
        if not tree_xml:
            tree_xml = orpg.dirpath.dir_struct["user"] + "tree.xml"
            self.settings.set_setting("gametree", tree_xml)
        self.tree.load_tree(tree_xml)

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def on_password_signal(self,signal,type,id,data):
        try:
            id = int(id)
            type = str(type)
            data = str(data)
            signal = str(signal)
            if signal == "fail":
                if type == "server":
                    self.password_manager.ClearPassword("server", 0)
                elif type == "admin":
                    self.password_manager.ClearPassword("admin", int(id))
                elif type == "room":
                    self.password_manager.ClearPassword("room", int(id))
                else:
                    pass
        except:
            traceback.print_exc()

    def build_menu(self):
        self.mainmenu = wx.MenuBar()

        menu = wx.Menu()
        menu.Append(OPT_FILE_SERVERS, "&Browse Servers\tCtrl-B")
        menu.AppendSeparator()
        menu.Append(OPT_FILE_QUIT, "&Quit\tCtrl-Q")
        self.mainmenu.Append(menu, "&File")

        menu = wx.Menu()
        menu.Append(OPT_EDIT_PREFS, "&Preferences")
        self.mainmenu.Append(menu, "&Edit")

        menu = wx.Menu()
        menu.Append(OPT_HELP_ABOUT, "&About")
        self.mainmenu.Append(menu, "&Help")

        self.SetMenuBar(self.mainmenu)

        self.Bind(wx.EVT_MENU, self.on_menu_file_servers, id=OPT_FILE_SERVERS)
        self.Bind(wx.EVT_MENU, self.on_menu_file_quit, id=OPT_FILE_QUIT)
        self.Bind(wx.EVT_MENU, self.on_menu_edit_prefs, id=OPT_EDIT_PREFS)
        self.Bind(wx.EVT_MENU, self.on_menu_help_about, id=OPT_HELP_ABOUT)

    #################################
    ## All Menu Events
    #################################

    # File Menu
    def on_menu_file_servers(self, evt):
        if self._mgr.GetPane("Browse Server Window").IsShown():
            self.hide_browse_servers_window()
        else:
            self.show_browse_servers_window()

    def on_menu_file_quit(self, evt):
        self.OnCloseWindow(0)

    # Edit Menu
    def on_menu_edit_prefs(self, evt):
        dlg = orpg.tools.orpg_settings.orpgSettingsWnd(self)
        dlg.Centre()
        dlg.ShowModal()

    # Windows Menu
    def on_menu_windows(self, event):
        menuid = event.GetId()
        name = self.mainwindows[menuid]
        if self._mgr.GetPane(name).IsShown():
            self._mgr.GetPane(name).Hide()
        else:
            self._mgr.GetPane(name).Show()
        self._mgr.Update()

    # Help Menu
    def on_menu_help_about(self, evt):
        dlg = ui.AboutDialog(self, orpg.dirpath.dir_struct["template"] + "about.html",
                             PRODUCT, VERSION)
        dlg.ShowModal()
        dlg.Destroy()

    #################################
    ##    Build the GUI
    #################################
    def build_gui(self):
        self.Freeze()
        self.validate.config_file("layout.xml","default_layout.xml")
        filename = orpg.dirpath.dir_struct["user"] + "layout.xml"
        temp_file = open(filename)
        txt = temp_file.read()
        self.layout_doc = self.xml.parseXml(txt)
        xml_dom = self.layout_doc.documentElement
        temp_file.close()

        self.windowsmenu = wx.Menu()
        self.mainwindows = {}
        h = int(xml_dom.getAttribute("height"))
        w = int(xml_dom.getAttribute("width"))
        posx = int(xml_dom.getAttribute("posx"))
        posy = int(xml_dom.getAttribute("posy"))
        maximized = int(xml_dom.getAttribute("maximized"))
        self.SetSize(posx, posy, w, h)

        children = xml_dom.childNodes
        for c in children:
            self.build_window(c, self)
        self.mainmenu.Insert(2, self.windowsmenu, 'Windows')

        #Create the Browse Server Window
        self.gs = orpg.networking.gsclient.game_server_panel(self)
        wndinfo = AUI.AuiPaneInfo()
        wndinfo.DestroyOnClose(False)
        wndinfo.Name("Browse Server Window")
        wndinfo.Caption("Game Server")
        wndinfo.Float()
        wndinfo.Dockable(False)
        wndinfo.MinSize(wx.Size(640,480))
        wndinfo.Hide()
        self._mgr.AddPane(self.gs, wndinfo)

        if wx.VERSION_STRING > "2.8":
            self.Bind(AUI.EVT_AUI_PANE_CLOSE, self.onPaneClose)
        else:
            self.Bind(AUI.EVT_AUI_PANECLOSE, self.onPaneClose)

        #Load the layout if one exists
        layout = xml_dom.getElementsByTagName("DockLayout")
        try:
            textnode = self.xml.safe_get_text_node(layout[0])
            self._mgr.LoadPerspective(textnode.nodeValue)
        except:
            pass
        self._mgr.Update()
        self.Maximize(maximized)
        self.Thaw()

    def do_tab_window(self,xml_dom,parent_wnd):
        # if cotainer window loop through childern and do a recursive call
        temp_wnd = orpgTabberWnd(parent_wnd, style=FNB.FNB_ALLOW_FOREIGN_DND)
        children = xml_dom.childNodes
        for c in children:
            wnd = self.build_window(c,temp_wnd)
            name = c.getAttribute("name")
            temp_wnd.AddPage(wnd, name, False)
        return temp_wnd

    def build_window(self, xml_dom, parent_wnd):
        name = xml_dom.nodeName
        if name == "DockLayout" or name == "dock":
            return
        dir = xml_dom.getAttribute("direction")
        pos = xml_dom.getAttribute("pos")
        height = xml_dom.getAttribute("height")
        width = xml_dom.getAttribute("width")
        cap = xml_dom.getAttribute("caption")
        dockable = xml_dom.getAttribute("dockable")
        layer = xml_dom.getAttribute("layer")

        try:
            layer = int(layer)
            dockable = int(dockable)
        except:
            layer = 0
            dockable = 1

        if name == "tab":
            temp_wnd = self.do_tab_window(xml_dom, parent_wnd)
        elif name == "map":
            temp_wnd = orpg.mapper.map.map_wnd(parent_wnd, -1)
            self.map = temp_wnd
        elif name == "tree":
            temp_wnd = orpg.gametree.gametree.game_tree(parent_wnd, -1)
            self.tree = temp_wnd
            if self.settings.get_setting('ColorTree') == '1':
                self.tree.SetBackgroundColour(self.settings.get_setting('bgcolor'))
                self.tree.SetForegroundColour(self.settings.get_setting('textcolor'))
            else:
                self.tree.SetBackgroundColour('white')
                self.tree.SetForegroundColour('black')

        elif name == "chat":
            temp_wnd = orpg.chat.chatwnd.chat_notebook(parent_wnd, wx.DefaultSize)
            self.chattabs = temp_wnd
            self.chat = temp_wnd.MainChatPanel

        elif name == "player":
            temp_wnd = orpg.player_list.player_list(parent_wnd)
            self.players = temp_wnd
            if self.settings.get_setting('ColorTree') == '1':
                self.players.SetBackgroundColour(self.settings.get_setting('bgcolor'))
                self.players.SetForegroundColour(self.settings.get_setting('textcolor'))
            else:
                self.players.SetBackgroundColour('white')
                self.players.SetForegroundColour('black')
        if parent_wnd != self:
            #We dont need this if the window are beeing tabed
            return temp_wnd
        menuid = wx.NewId()
        self.windowsmenu.Append(menuid, cap, kind=wx.ITEM_CHECK)
        self.windowsmenu.Check(menuid, True)
        self.Bind(wx.EVT_MENU, self.on_menu_windows, id=menuid)
        self.mainwindows[menuid] = cap
        wndinfo = AUI.AuiPaneInfo()
        wndinfo.DestroyOnClose(False)
        wndinfo.Name(cap)
        wndinfo.FloatingSize(wx.Size(int(width), int(height)))
        wndinfo.BestSize(wx.Size(int(width), int(height)))
        wndinfo.Layer(int(layer))
        wndinfo.Caption(cap)

# Lambda here should work!
        if dir.lower() == 'top':
            wndinfo.Top()
        elif dir.lower() == 'bottom':
            wndinfo.Bottom()
        elif dir.lower() == 'left':
            wndinfo.Left()
        elif dir.lower() == 'right':
            wndinfo.Right()
        elif dir.lower() == 'center':
            wndinfo.Center()
            wndinfo.CaptionVisible(False)

        if dockable != 1:
            wndinfo.Dockable(False)
            wndinfo.Floatable(False)
        if pos != '' or pos != '0' or pos != None:
            wndinfo.Position(int(pos))
        wndinfo.Show()
        self._mgr.AddPane(temp_wnd, wndinfo)
        return temp_wnd

    def onPaneClose(self, evt):
        pane = evt.GetPane()
        for wndid, wname in list(self.mainwindows.items()):
            if pane.name == wname:
                self.windowsmenu.Check(wndid, False)
                break
        evt.Skip()
        self._mgr.Update()

    def saveLayout(self):
        (x_size,y_size) = self.GetClientSize()
        (x_pos,y_pos) = self.GetPosition()
        if self.IsMaximized():
            max = 1
        else:
            max = 0
        dock_layout = str(self._mgr.SavePerspective())

        xml_dom = self.layout_doc.documentElement
        xml_dom.setAttribute("height", str(y_size))
        xml_dom.setAttribute("width", str(x_size))
        xml_dom.setAttribute("posx", str(x_pos))
        xml_dom.setAttribute("posy", str(y_pos))
        xml_dom.setAttribute("maximized", str(max))
        layout = xml_dom.getElementsByTagName("DockLayout")
        if layout:
            elem = layout[0]
        else:
            elem = self.layout_doc.createElement('DockLayout')
            xml_dom.appendChild(elem)
        textnode = self.xml.safe_get_text_node(elem)
        textnode.nodeValue = str(self._mgr.SavePerspective())

        filename = orpg.dirpath.dir_struct["user"] + "layout.xml"
        temp_file = open(filename, "w")
        temp_file.write(orpg.orpg_xml.toxml(xml_dom, 1))
        temp_file.close()

    def build_additional_menus(self):
        self.chat.build_menu()
        self.map.build_menu()

    def start_timer(self):
        s = open_rpg.get_component('settings')
        if s.get_setting("Heartbeat") == "1":
            self.ping_timer.Start(1000*60)

    def kill_mplay_session(self):
        self.game_name = ""
        self.session.start_disconnect()

    def on_player_event(self, evt):
        id = evt.get_id()
        player = evt.get_data()
        display_name = self.chat.chat_display_name(player)
        time_str = time.strftime("%H:%M", time.localtime())
        if id == orpg.networking.mplay_client.PLAYER_NEW:
            self.players.add_player(player)
            self.chat.InfoPost(display_name + " (enter): " + time_str)
        elif id == orpg.networking.mplay_client.PLAYER_DEL:
            self.players.del_player(player)
            self.chat.InfoPost(display_name + " (exit): " + time_str)
        elif id == orpg.networking.mplay_client.PLAYER_UPDATE:
            self.players.update_player(player)
        self.players.Refresh()

    def on_group_event(self, evt):
        id = evt.get_id()
        group = evt.get_data()

        if id == orpg.networking.mplay_client.GROUP_NEW:
            self.gs.add_room(group)
        elif id == orpg.networking.mplay_client.GROUP_DEL:
            self.password_manager.RemoveGroupData(group.id)
            self.gs.del_room(group)
        elif id == orpg.networking.mplay_client.GROUP_UPDATE:
            self.gs.update_room(group)

    def on_receive(self, data, player):
        # see if we are ignoring this user
        (ignore_id,ignore_name) = self.session.get_ignore_list()
        for m in ignore_id:
            if m == player[2]:
                # yes we are
                return

        # ok we are not ignoring this message
        if player:
            display_name = self.chat.chat_display_name(player)
        else:
            display_name = "Server Administrator"

        if data[:5] == "<tree":
            self.tree.on_receive_data(data,player)
            self.chat.InfoPost(display_name + " has sent you a tree node...")
            #self.tree.OnNewData(data)

        elif data[:4] == "<map":
            self.map.new_data(data)

        elif data[:5] == "<chat":
            msg = orpg.chat.chat_msg.chat_msg(data)
            self.chat.post_incoming_msg(msg,player)
        else:
        ##############################################################################################
        #  all this below code is for comptiablity with older clients and can be removed after a bit #
        ##############################################################################################
            if data[:3] == "/me":
                # This fixes the emote coloring to comply with what has been asked for by the user
                # population, not to mention, what I committed to many moons ago.
                #  In doing so, Woody's scheme has been tossed out.  I'm sure Woody won't be
                # happy but I'm invoking developer priveledge to satisfy user request, not to mention,
                # this scheme actually makes more sense.  In Woody's scheme, a user could over-ride another
                # users emote color.  This doesn't make sense, rather, people dictate their OWN colors...which is as
                # it should be in the first place and is as it has been with normal text.  In short, this makes
                # sense and is consistent.
                data = data.replace( "/me", "" )

                # Check to see if we find the closing ">" for the font within the first 22 values
                index = data[:22].find(  ">" )
                if index == -1:
                    data = "** " + self.chat.colorize( self.chat.infocolor, display_name + data ) + " **"

                else:
                    # This means that we found a valid font string, so we can simply plug the name into
                    # the string between the start and stop font delimiter
                    print("pre data = " + data)
                    data = data[:22] + "** " + display_name + " " + data[22:] + " **"
                    print("post data = " + data)

            elif data[:2] == "/w":
                data = data.replace("/w","")
                data = "<b>" + display_name + "</b> (whispering): " + data

            else:
                # Normal text
                if player:
                    data = "<b>" + display_name + "</b>: " + data
                else:
                    data = "<b><i><u>" + display_name + "</u>-></i></b> " + data
            self.chat.Post(data)

    def on_mplay_event(self, evt):
        id = evt.get_id()
        if id == orpg.networking.mplay_client.MPLAY_CONNECTED:
            self.chat.InfoPost("Game connected!")
            self.gs.set_connected(1)
            self.password_manager.ClearPassword("ALL")

        elif id == orpg.networking.mplay_client.MPLAY_DISCONNECTED:
            self.ping_timer.Stop()
            self.chat.SystemPost("Game disconnected!")
            self.players.reset()
            self.gs.set_connected(0)

        elif id== orpg.networking.mplay_client.MPLAY_GROUP_CHANGE:
            group = evt.get_data()
            self.chat.InfoPost("Moving to room '"+group[1]+"'..")
            if self.gs : self.gs.set_cur_room_text(group[1])
            self.players.reset()
        elif id== orpg.networking.mplay_client.MPLAY_GROUP_CHANGE_F:
            self.chat.SystemPost("Room access denied!")

    def OnCloseWindow(self, event):
        dlg = wx.MessageDialog(self, "Quit " + PRODUCT + "?", PRODUCT, wx.YES_NO)
        if dlg.ShowModal() == wx.ID_YES:
            dlg.Destroy()
            self.closed_confirmed()

    def closed_confirmed(self):
        # Hide any windows that should always start hidden before
        # saving the current window layout,
        self._mgr.GetPane("Browse Server Window").Hide()

        self.saveLayout()
        try:
            self.settings.save()
        except:
            self.log.log("[WARNING] Error saving 'settings' component", ORPG_GENERAL, True)

        try:
            save_tree = self.settings.lookup(
                "Game Tree", "SaveGameTreeOnExit", bool, True,
                "Automatically save the game tree when exiting.")
            if save_tree:
                self.tree.save_tree(self.settings.get_setting("gametree"))
        except:
            self.log.log("[WARNING] Error saving gametree", ORPG_GENERAL, True)

        if self.session.get_status() == orpg.networking.mplay_client.MPLAY_CONNECTED:
            self.kill_mplay_session()

        self.ping_timer.Stop()
        self.chat.parent.chat_timer.Stop()

        self._mgr.UnInit()
        mainapp = wx.GetApp()
        mainapp.ExitMainLoop()
        self.Destroy()

    def show_browse_servers_window(self):
        self._mgr.GetPane("Browse Server Window").Show()
        self._mgr.Update()

    def hide_browse_servers_window(self):
        self._mgr.GetPane("Browse Server Window").Hide()
        self._mgr.Update()


########################################
## Application class
########################################
class orpgApp(wx.App):
    def OnInit(self):
        self.log = orpg.tools.orpg_log.orpgLog(orpg.dirpath.dir_struct["user"] + "runlogs/")
        #Add the initial global components of the openrpg class
        #Every class should be passed openrpg
        open_rpg.add_component("log", self.log)
        open_rpg.add_component("xml", orpg.orpg_xml)
        open_rpg.add_component("dir_struct", orpg.dirpath.dir_struct)
        open_rpg.add_component("tabbedWindows", [])
        self.validate = orpg.tools.validate.Validate()
        open_rpg.add_component("validate", self.validate)
        self.settings = orpg.tools.orpg_settings.orpgSettings()
        open_rpg.add_component("settings", self.settings)
        self.log.setLogLevel(int(self.settings.get_setting('LoggingLevel')))

        self.frame = orpgFrame(None, wx.ID_ANY, PRODUCT)
        self.frame.Raise()
        self.frame.Refresh()
        self.frame.Show(True)
        self.SetTopWindow(self.frame)

        return True

def run_client():
    """Run the FlexiRPG application."""
    mainapp = orpg.main.orpgApp()
    mainapp.MainLoop()
