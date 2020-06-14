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

import orpg.dirpath
from orpg.orpg_windows import *
from orpg.orpg_xml import *
import orpg.tools.orpg_settings
import orpg.tools.rgbhex
from orpg.orpgCore import open_rpg
import traceback
from orpg.networking.mplay_client import OPENRPG_PORT

gs_host = 1
gs_join = 2
# constants

LIST_SERVER = wx.NewId()
LIST_ROOM = wx.NewId()
ADDRESS = wx.NewId()
GS_CONNECT = wx.NewId()
GS_DISCONNECT = wx.NewId()
GS_JOIN = wx.NewId()
GS_JOINLOBBY = wx.NewId()
GS_CREATE_ROOM = wx.NewId()
GS_PWD = wx.NewId()
GS_CLOSE = wx.NewId()

class server_instance:
    def __init__(self, address, port):
        self.address = address
        self.port = port

    def name(self):
        return self.address + ":" + str(self.port)

def roomCmp(room1, room2):
    if int(room1) > int(room2):
        return 1
    elif int(room1) < int(room2):
        return -1
    return 0

class game_server_panel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent, -1)
        self.parent = parent
        self.log = open_rpg.get_component('log')
        self.password_manager = open_rpg.get_component('password_manager') # passtool --SD 8/03
        self.frame = open_rpg.get_component('frame')
        self.session = open_rpg.get_component('session')
        self.settings = open_rpg.get_component('settings')
        self.xml = open_rpg.get_component('xml')
        self.serverNameSet = 0
        self.last_motd = ""
        self.buttons = {}
        self.texts = {}
        self.svrList = []
        self.build_ctrls()
        self.get_server_bookmarks()
        self.refresh_server_list()
        self.refresh_room_list()

#---------------------------------------------------------
# [START] Snowdog: Updated Game Server Window 12/02
#---------------------------------------------------------
    def build_ctrls(self):
        ## Section Sizers (with frame edges and text captions)
        self.box_sizers = {}
        self.box_sizers["server"] = wx.StaticBox(self, -1, "Server")
        self.box_sizers["room"] = wx.StaticBox(self, -1, "Rooms")
        self.box_sizers["c_room"] = wx.StaticBox(self, -1, "Create Room")

        ## Layout Sizers
        self.sizers = {}
        self.sizers["main"] = wx.GridBagSizer(hgap=12, vgap=6)
        self.sizers["server"] = wx.StaticBoxSizer(self.box_sizers["server"], wx.VERTICAL)
        self.sizers["rooms"] = wx.StaticBoxSizer(self.box_sizers["room"], wx.VERTICAL)
        self.sizers["c_room"] = wx.StaticBoxSizer(self.box_sizers["c_room"], wx.VERTICAL)

        #Build Server Sizer
        adder = wx.StaticText(self, -1, "Address:")
        self.texts["address"] = wx.TextCtrl(self, ADDRESS)
        servers = wx.StaticText(self, -1, "Recently Used:")
        self.server_list = wx.ListCtrl(self, LIST_SERVER, style=wx.LC_REPORT | wx.SUNKEN_BORDER )
        self.server_list.InsertColumn(0, "Address", wx.LIST_FORMAT_LEFT, 0)
        self.server_list.InsertColumn(1, "Port", wx.LIST_FORMAT_LEFT, 0)
        self.buttons[GS_CONNECT] = wx.Button(self, GS_CONNECT, "Connect")
        self.buttons[GS_DISCONNECT] = wx.Button(self, GS_DISCONNECT, "Disconnect")
        self.sizers["svrbtns"] = wx.BoxSizer(wx.HORIZONTAL)
        self.sizers["svrbtns"].Add(self.buttons[GS_CONNECT], 0, wx.EXPAND)
        self.sizers["svrbtns"].Add(self.buttons[GS_DISCONNECT], 0, wx.EXPAND)
        self.sizers["server"].Add(adder, 0, wx.EXPAND)
        self.sizers["server"].Add(self.texts["address"], 0, wx.EXPAND)
        self.sizers["server"].Add(servers, 0, wx.EXPAND)
        self.sizers["server"].Add(self.server_list, 1, wx.EXPAND)
        self.sizers["server"].Add(self.sizers["svrbtns"], 0, wx.EXPAND)

        #Build Rooms Sizer
        self.room_list = wx.ListCtrl(self, LIST_ROOM, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.room_list.InsertColumn(0,"Game", wx.LIST_FORMAT_LEFT,0)
        self.room_list.InsertColumn(1,"Players", wx.LIST_FORMAT_LEFT,0)
        self.room_list.InsertColumn(2,"PW", wx.LIST_FORMAT_LEFT,0)
        self.buttons[GS_JOIN] = wx.Button(self, GS_JOIN, "Join Room")
        self.buttons[GS_JOINLOBBY] = wx.Button(self, GS_JOINLOBBY, "Lobby")
        self.sizers["roombtns"] = wx.BoxSizer(wx.HORIZONTAL)
        self.sizers["roombtns"].Add(self.buttons[GS_JOIN], 0, wx.EXPAND)
        self.sizers["roombtns"].Add(self.buttons[GS_JOINLOBBY], 0, wx.EXPAND)
        self.sizers["rooms"].Add(self.room_list, 1, wx.EXPAND)
        self.sizers["rooms"].Add(self.sizers["roombtns"], 0, wx.EXPAND)

        #Build Create Room Sizer
        rname = wx.StaticText(self,-1, "Room Name:")
        self.texts["room_name"] = wx.TextCtrl(self, -1)
        self.buttons[GS_PWD] = wx.CheckBox(self, GS_PWD, "Password:")
        self.texts["room_pwd"] = wx.TextCtrl(self, -1)
        self.texts["room_pwd"].Enable(0)
        apass = wx.StaticText(self,-1, "Admin Password:")
        self.texts["room_boot_pwd"] = wx.TextCtrl(self, -1)
        minver = wx.StaticText(self,-1, "Minimum Version:")
        self.texts["room_min_version"] = wx.TextCtrl(self, -1)
        self.sizers["c_room_layout"] = wx.FlexGridSizer(rows=8, cols=2, hgap=1, vgap=1)
        self.sizers["c_room_layout"].Add(rname, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL)
        self.sizers["c_room_layout"].Add(self.texts["room_name"], 0, wx.EXPAND)
        self.sizers["c_room_layout"].Add(self.buttons[GS_PWD],0,wx.ALIGN_CENTER_VERTICAL|wx.ALL)
        self.sizers["c_room_layout"].Add(self.texts["room_pwd"], 1, wx.EXPAND)
        self.sizers["c_room_layout"].Add(apass, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL)
        self.sizers["c_room_layout"].Add(self.texts["room_boot_pwd"], 0, wx.EXPAND)
        self.sizers["c_room_layout"].Add(minver, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL)
        self.sizers["c_room_layout"].Add(self.texts["room_min_version"], 0, wx.EXPAND)
        self.sizers["c_room_layout"].AddGrowableCol(1)
        self.buttons[GS_CREATE_ROOM] = wx.Button(self, GS_CREATE_ROOM, "Create Room")
        self.sizers["c_room"].Add(self.sizers["c_room_layout"], 1, wx.EXPAND)
        self.sizers["c_room"].Add(self.buttons[GS_CREATE_ROOM], 0, wx.EXPAND)

        #Build Main Sizer
        self.sizers["main"].Add(self.sizers["server"], (0,0), span=(3,1), flag=wx.EXPAND)
        self.sizers["main"].Add(self.sizers["rooms"], (0,1), flag=wx.EXPAND)
        self.sizers["main"].Add(self.sizers["c_room"], (1,1), span=(2,1), flag=wx.EXPAND)
        self.sizers["main"].AddGrowableCol(0)
        self.sizers["main"].AddGrowableCol(1)
        self.sizers["main"].AddGrowableRow(0)

        self.buttons[GS_CLOSE] = wx.Button(self, GS_CLOSE, "Close")

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.sizers["main"], 1, wx.EXPAND)
        vbox.Add((0,12))
        vbox.Add(self.buttons[GS_CLOSE], 0, wx.ALIGN_RIGHT)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(vbox, 1, wx.EXPAND | wx.ALL, border=12)

        self.SetSizer(box)
        self.SetAutoLayout(True)
        self.Fit()

        ## Event Handlers
        self.Bind(wx.EVT_BUTTON, self.on_button, id=GS_CONNECT)
        self.Bind(wx.EVT_BUTTON, self.on_button, id=GS_DISCONNECT)
        self.Bind(wx.EVT_BUTTON, self.on_button, id=GS_CREATE_ROOM)
        self.Bind(wx.EVT_BUTTON, self.on_button, id=GS_JOIN)
        self.Bind(wx.EVT_BUTTON, self.on_button, id=GS_JOINLOBBY)
        self.Bind(wx.EVT_BUTTON, self.on_button, id=GS_CLOSE)
        self.Bind(wx.EVT_CHECKBOX, self.on_button, id=GS_PWD)

        # Added double click handlers 5/05 -- Snowdog
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_server_dbclick, id=LIST_SERVER)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_room_dbclick, id=LIST_ROOM)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_select, id=LIST_ROOM)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_select, id=LIST_SERVER)
        self.texts['address'].Bind(wx.EVT_SET_FOCUS, self.on_text)
        self.set_connected(self.session.is_connected())
        self.cur_room_index = -1
        self.cur_server_index = -1
        self.rmList = {}

#---------------------------------------------------------
# [END] Snowdog: Updated Game Server Window 12/02
#---------------------------------------------------------


    #-----------------------------------------------------
    # on_server_dbclick()
    # support for double click selection of server.
    # 5/16/05 -- Snowdog
    #-----------------------------------------------------
    def on_server_dbclick(self, evt=None):
        #make sure address is updated just in case list select wasn't done
        try:
            self.on_select(evt)
        except:
            pass
        address = self.texts["address"].GetValue()
        if self.session.is_connected():
            if self.session.host_server == address :
                #currently connected to address. Do nothing.
                return
            else:
                #address differs, disconnect.
                self.frame.kill_mplay_session()
        self.do_connect(address)


    #-----------------------------------------------------
    # on_room_dbclick()
    # support for double click selection of server.
    # 5/16/05 -- Snowdog
    #-----------------------------------------------------

    def on_room_dbclick(self, evt=None):
        #make sure address is updated just in case list select wasn't done
        try:
            self.on_select(evt)
        except:
            pass
        group_id = str(self.room_list.GetItemData(self.cur_room_index))

        if self.NoGroups:
            self.NoGroups = False
            self.session.group_id = group_id
            self.on_server_dbclick()
            return

        self.do_join_group()

    def on_select(self,evt):
        id = evt.GetId()
        if id == LIST_ROOM:
            self.cur_room_index = evt.Index
        elif id==LIST_SERVER:
            self.cur_server_index = evt.Index
            self.name = self.svrList[self.cur_server_index].name()
            address = self.svrList[self.cur_server_index].address
            port = self.svrList[self.cur_server_index].port
            self.texts["address"].SetValue(self.name)
            self.refresh_room_list()

    def on_text(self,evt):
        id = evt.GetId()
        if (id == ADDRESS) and (self.cur_server_index >= 0):
            #print "ADDRESS id = ", id, "index = ", self.cur_server_index
            self.cur_server_index = -1
        evt.Skip()

    def add_room(self,data):
        i = self.room_list.GetItemCount()
        if (data[2]=="1") or (data[2]=="True"):
            pwd="yes"
        else:
            pwd="no"
        self.room_list.InsertItem(i,data[1])
        self.room_list.SetItem(i,1,data[3])
        self.room_list.SetItem(i,2,pwd)
        self.room_list.SetItemData(i,int(data[0]))
        self.refresh_room_list()

    def del_room(self, data):
        i = self.room_list.FindItem(-1, int(data[0]))
        self.room_list.DeleteItem(i)
        self.refresh_room_list()

#---------------------------------------------------------
# [START] Snowdog Password/Room Name altering code 12/02
#---------------------------------------------------------

    def update_room(self,data):
        #-------------------------------------------------------
        # Udated 12/02 by Snowdog
        # allows refresh of all room data not just player counts
        #-------------------------------------------------------
        i = self.room_list.FindItem(-1,int(data[0]))
        if data[2]=="1" : pwd="yes"
        else: pwd="no"
        self.room_list.SetItem(i,0,data[1])
        self.room_list.SetItem(i,1,data[3])
        self.room_list.SetItem(i,2,pwd)
        self.refresh_room_list()

#---------------------------------------------------------
# [END] Snowdog Password/Room Name altering code 12/02
#---------------------------------------------------------

    def set_cur_room_text(self,name):
        pass
        #self.texts["cur_room"].SetLabel(name)
        #self.sizers["room"].Layout()

    def set_lobbybutton(self,allow):
        self.buttons[GS_JOINLOBBY].Enable(allow)

    def set_connected(self,connected):
        self.buttons[GS_CONNECT].Enable(not connected)
        self.buttons[GS_DISCONNECT].Enable(connected)
        self.buttons[GS_JOIN].Enable(connected)
        self.buttons[GS_CREATE_ROOM].Enable(connected)
        if not connected:
            self.buttons[GS_JOINLOBBY].Enable(connected)
            self.room_list.DeleteAllItems()
            self.set_cur_room_text("Not Connected!")
            self.cur_room_index = -1
        else:
            self.set_cur_room_text("Lobby")

    def on_button(self,evt):
        id = evt.GetId()
        if id == GS_CONNECT:
            address = self.texts["address"].GetValue()
            ### check to see if this is a manual entry vs. list entry.
            try:
                dummy = self.name
            except:
                self.name = str(address)
            self.do_connect(address)
        elif id == GS_DISCONNECT:
            self.frame.kill_mplay_session()
        elif id == GS_CREATE_ROOM:
            self.do_create_group()
        elif id == GS_JOIN:
            self.do_join_group()
        elif id == GS_JOINLOBBY:
            self.do_join_lobby()
        elif id == GS_PWD:
            self.texts["room_pwd"].Enable(evt.Checked())
        elif id == GS_CLOSE:
            self.parent.hide_browse_servers_window()

    def refresh_room_list(self):
        self.room_list.DeleteAllItems()
        address = self.texts["address"].GetValue()
        try:
            cadder = self.session.host_server
        except:
            cadder = ''
        if address in self.rmList and len(self.rmList[address]) > 0 and cadder != address:
            groups = self.rmList[address]
            self.NoGroups = True
        else:
            self.NoGroups = False
            groups = self.session.get_groups()
        for g in groups:
            i = self.room_list.GetItemCount()
            if (g[2]=="True") or (g[2]=="1"):
                pwd="yes"
            else:
                pwd="no"
            self.room_list.InsertItem(i, g[1])
            self.room_list.SetItem(i, 1, g[3])
            self.room_list.SetItem(i, 2, pwd)
            self.room_list.SetItemData(i, int(g[0]))
        if self.room_list.GetItemCount() > 0:
            self.colorize_group_list(groups)
            self.room_list.SortItems(roomCmp)
            wx.CallAfter(self.autosizeRooms)

    def autosizeRooms(self):
        self.room_list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.room_list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.room_list.SetColumnWidth(2, wx.LIST_AUTOSIZE)

    def get_server_bookmarks(self):
        bookmarks = self.settings.get_setting('ServerBookmarks')
        if bookmarks:
            if bookmarks == '':
                self.server_bookmarks = []
            else:
                self.server_bookmarks = bookmarks.split(',')
        else:
            self.settings.add_setting("Networking", "ServerBookmarks", "", "string", 
                                      "List of server bookmarks.")
            self.server_bookmarks = []

    def refresh_server_list(self):
        self.svrList = []
        self.cur_server_index = -1
        self.server_list.DeleteAllItems()

        for server in self.server_bookmarks:
            a = server.split(':')
            address = a[0]
            if len(a) > 1:
                port = int(a[1])
            else:
                port = OPENRPG_PORT
            self.svrList.append(server_instance(address, port))
            i = self.server_list.GetItemCount()
            self.server_list.InsertItem(i, address)
            self.server_list.SetItem(i, 1, str(port))

        self.server_list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.server_list.SetColumnWidth(1, wx.LIST_AUTOSIZE)

    def add_server_bookmark(self, server):
        a = server.split(':')
        address = a[0]
        if len(a) > 1:
            port = a[1]
        else:
            port = str(OPENRPG_PORT)
        server = address + ":" + port
        try:
            self.server_bookmarks.remove(server)
        except:
            pass
        self.server_bookmarks.insert(0, server)
        if len(self.server_bookmarks) > 5:
            self.server_bookmarks.pop()
        servers = self.settings.set_setting('ServerBookmarks', ','.join(self.server_bookmarks))

        self.refresh_server_list()

    def do_connect(self, address):
        chat = open_rpg.get_component('chat')
        chat.InfoPost("Locating server at " + address + "...")
        if self.session.connect(address):
            self.add_server_bookmark(address)
            self.frame.start_timer()
        else:
            chat.SystemPost("Failed to connect to game server...")

    def do_join_lobby(self):
        self.cur_room_index = 0
        self.session.send_join_group("0","")
        self.set_lobbybutton(0);

    def do_join_group(self):
        if self.cur_room_index < 0:
            # No room selected
            return

        if self.cur_room_index != 0:
            self.set_lobbybutton(1);
        else:
            self.set_lobbybutton(0);

        group_id = str(self.room_list.GetItemData(self.cur_room_index))
        group = self.session.get_group_info(group_id)
        pwd = ""
        if (group[2] == "True") or (group[2] == "1"):
            pwd = self.password_manager.GetPassword("room", group_id)
        else:
            pwd = ""
        if pwd != None: #pwd==None means the user clicked "Cancel"
            self.session.send_join_group(group_id,pwd)

    def do_create_group(self):
        name = self.texts["room_name"].GetValue()
        boot_pwd = self.texts["room_boot_pwd"].GetValue()
        minversion = self.texts["room_min_version"].GetValue()
        #
        # Check for & in name.  We want to allow this becaus of its common use in D&D.
        #
        loc = name.find("&")
        oldloc=0
        while loc > -1:
            loc = name.find("&",oldloc)
            if loc > -1:
                b = name[:loc]
                e = name[loc+1:]
                name = b + "&amp;" + e
                oldloc = loc+1
        loc = name.find('"')
        oldloc=0
        while loc > -1:
            loc = name.find('"',oldloc)
            if loc > -1:
                b = name[:loc]
                e = name[loc+1:]
                name = b + "&quote;" + e
                oldloc = loc+1
        loc = name.find("'")
        oldloc=0
        while loc > -1:
            loc = name.find("'",oldloc)
            if loc > -1:
                b = name[:loc]
                e = name[loc+1:]
                name = b + "&#39;" + e
                oldloc = loc+1
        if self.buttons[GS_PWD].GetValue():
            pwd = self.texts["room_pwd"].GetValue()
        else:
            pwd = ""
        if name == "":
            wx.MessageBox("Invalid Name","Error");
        else:
            msg = "%s is creating room \'%s.\'" % (self.session.name, name)
            self.session.send( msg )
            self.session.send_create_group(name,pwd,boot_pwd,minversion)
            self.set_lobbybutton(1); #enable the Lobby quickbutton

#---------------------------------------------------------
# [START] Snowdog: Updated Game Server Window 12/02
#---------------------------------------------------------

    def on_size(self,evt):
        # set column widths for room list


        # set column widths for server list
        pass



#---------------------------------------------------------
# [END] Snowdog: Updated Game Server Window 12/02
#---------------------------------------------------------


    def colorize_group_list(self, groups):
        try:
            hex = orpg.tools.rgbhex.RGBHex()
            for gr in groups:
                item_list_location = self.room_list.FindItem(-1,int(gr[0]))
                if item_list_location != -1:
                    item = self.room_list.GetItem(item_list_location)
                    if gr[0] == "0":
                        r,g,b = hex.rgb_tuple(self.settings.get_setting("RoomColor_Lobby"))
                    elif gr[3] != "0":
                        if gr[2] == "True" or gr[2] == "1":
                           r,g,b = hex.rgb_tuple(self.settings.get_setting("RoomColor_Locked"))
                        else:
                           r,g,b = hex.rgb_tuple(self.settings.get_setting("RoomColor_Active"))
                    else:
                        r,g,b = hex.rgb_tuple(self.settings.get_setting("RoomColor_Empty"))
                    color = wx.Colour(red=r,green=g,blue=b)
                    item.SetTextColour(color)
                    self.room_list.SetItem(item)
        except:
            traceback.print_exc()
