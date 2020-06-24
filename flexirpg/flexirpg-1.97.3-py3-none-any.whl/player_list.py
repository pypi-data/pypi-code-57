# Player list window
#
# Copyright 2020 David Vrabel
# Copyright (C) 2000-2001 The OpenRPG Project
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

from orpg.orpg_windows import *
import orpg.dirpath

# global definitions
global ROLE_GM; ROLE_GM = "GM"
global ROLE_PLAYER; ROLE_PLAYER = "PLAYER"
global ROLE_LURKER; ROLE_LURKER = "LURKER"

#########################
#player frame window
#########################
PLAYER_BOOT = wx.NewId()
PLAYER_WHISPER = wx.NewId()
PLAYER_IGNORE = wx.NewId()
PLAYER_ROLE_MENU = wx.NewId()
PLAYER_ROLE_LURKER = wx.NewId()
PLAYER_ROLE_PLAYER = wx.NewId()
PLAYER_ROLE_GM = wx.NewId()
PLAYER_SHOW_VERSION = wx.NewId()
WG_LIST = {}

PLAYER_WG_MENU = wx.NewId()
PLAYER_WG_CREATE = wx.NewId()
PLAYER_WG_CLEAR_ALL = wx.NewId()
WG_MENU_LIST = {}

PLAYER_COMMAND_MENU = wx.NewId()
PLAYER_COMMAND_PASSWORD_ALTER = wx.NewId()
PLAYER_COMMAND_ROOM_RENAME = wx.NewId()

class player_list(wx.ListCtrl):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, wx.DefaultPosition, wx.DefaultSize,
                             wx.LC_REPORT|wx.SUNKEN_BORDER|wx.EXPAND|wx.LC_HRULES)
        self.session = open_rpg.get_component("session")
        self.settings = open_rpg.get_component('settings')
        self.chat = open_rpg.get_component('chat')
        self.password_manager = open_rpg.get_component("password_manager")

        self._imageList = wx.ImageList( 16, 16, False )
        self._imageList.Add(orpg.tools.bitmap.create_from_file("icon_player.png"))
        self.SetImageList( self._imageList, wx.IMAGE_LIST_SMALL )

        # Create our column headers
        self.InsertColumn( 0, "ID", width=wx.LIST_AUTOSIZE )
        self.InsertColumn( 1, "Player", width=wx.LIST_AUTOSIZE )
        self.InsertColumn( 2, "Status" )

        # Main Menu
        self.wgMenu = wx.Menu()
        # Add the Base Menu items, so they are always at the bottom
        self.wgMenu.Append(PLAYER_WG_CREATE, "Create")
        self.wgMenu.Append(PLAYER_WG_CLEAR_ALL, "Delete All Groups")

        # Create the role menu
        self.roleMenu = wx.Menu()
        self.roleMenu.SetTitle( "Assign Role" )
        self.roleMenu.Append( PLAYER_ROLE_LURKER, "Lurker" )
        self.roleMenu.Append( PLAYER_ROLE_PLAYER, "Player" )
        self.roleMenu.Append( PLAYER_ROLE_GM, "GM" )

        # Create the room control menu
        self.commandMenu = wx.Menu()
        self.commandMenu.SetTitle( "Room Controls" )
        self.commandMenu.Append( PLAYER_COMMAND_PASSWORD_ALTER, "Password" )
        self.commandMenu.Append( PLAYER_COMMAND_ROOM_RENAME, "Room Name" )
        self.commandMenu.AppendSeparator()

        # Create the pop up menu
        self.menu = wx.Menu()
        self.menu.SetTitle( "Player Menu" )
        self.menu.Append( PLAYER_BOOT, "Boot" )
        self.menu.AppendSeparator()
        self.menu.Append( PLAYER_IGNORE, "Toggle &Ignore" )
        self.menu.AppendSeparator()
        self.menu.Append( PLAYER_WHISPER, "Whisper" )
        self.menu.Append(PLAYER_WG_MENU, "Whisper Groups", self.wgMenu)
        self.menu.AppendSeparator()
        self.menu.Append( PLAYER_COMMAND_MENU, "Room Control", self.commandMenu )
        self.menu.AppendSeparator()
        self.menu.Append( PLAYER_ROLE_MENU, "Assign Role", self.roleMenu )
        self.menu.AppendSeparator()
        self.menu.Append( PLAYER_SHOW_VERSION, "Version" )

        # Event processing for our menu
        self.Bind(wx.EVT_MENU, self.on_menu_item, id=PLAYER_BOOT)
        self.Bind(wx.EVT_MENU, self.on_menu_item, id=PLAYER_IGNORE)
        self.Bind(wx.EVT_MENU, self.on_menu_item, id=PLAYER_WHISPER)
        self.Bind(wx.EVT_MENU, self.on_menu_role_change, id=PLAYER_ROLE_LURKER)
        self.Bind(wx.EVT_MENU, self.on_menu_role_change, id=PLAYER_ROLE_PLAYER)
        self.Bind(wx.EVT_MENU, self.on_menu_role_change, id=PLAYER_ROLE_GM)
        self.Bind(wx.EVT_MENU, self.on_menu_item, id=PLAYER_SHOW_VERSION)
        self.Bind(wx.EVT_MENU, self.on_menu_whispergroup, id=PLAYER_WG_CREATE)
        self.Bind(wx.EVT_MENU, self.on_menu_whispergroup, id=PLAYER_WG_CLEAR_ALL)
        self.Bind(wx.EVT_MENU, self.on_menu_password, id=PLAYER_COMMAND_PASSWORD_ALTER)
        self.Bind(wx.EVT_MENU, self.on_menu_room_rename, id=PLAYER_COMMAND_ROOM_RENAME)
        self.Bind(wx.EVT_LEFT_DCLICK, self.on_d_lclick)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_menu)
        self.sized = 1

    def on_menu_password( self, evt ):
        id = evt.GetId()
        self.session = open_rpg.get_component("session")
        self.password_manager = open_rpg.get_component("password_manager")
        self.chat = open_rpg.get_component("chat")
        boot_pwd = self.password_manager.GetPassword("admin",int(self.session.group_id))
        if boot_pwd != None:
            alter_pwd_dialog = wx.TextEntryDialog(self,"Enter new room password: (blank for no password)","Alter Room Password")
            if alter_pwd_dialog.ShowModal() == wx.ID_OK:
                new_pass = alter_pwd_dialog.GetValue()
                self.chat.InfoPost( "Requesting password change on server..." )
                self.session.set_room_pass(new_pass, boot_pwd)

    def on_menu_room_rename( self, evt ):
        id = evt.GetId()
        self.session = open_rpg.get_component("session")
        self.password_manager = open_rpg.get_component("password_manager")
        self.chat = open_rpg.get_component("chat")
        boot_pwd = self.password_manager.GetPassword("admin",int(self.session.group_id))
        if boot_pwd != None:
            alter_name_dialog = wx.TextEntryDialog(self,"Enter new room name: ","Change Room Name")
            if alter_name_dialog.ShowModal() == wx.ID_OK:
                new_name = alter_name_dialog.GetValue()
                self.chat.InfoPost( "Requesting room name change on server..." )
                loc = new_name.find("&")
                oldloc=0
                while loc > -1:
                    loc = new_name.find("&",oldloc)
                    if loc > -1:
                        b = new_name[:loc]
                        e = new_name[loc+1:]
                        new_name = b + "&amp;" + e
                        oldloc = loc +1
                loc = new_name.find("'")
                oldloc=0
                while loc > -1:
                    loc = new_name.find("'",oldloc)
                    if loc > -1:
                        b = new_name[:loc]
                        e = new_name[loc+1:]
                        new_name = b + "&#39;" + e
                        oldloc = loc +1
                loc = new_name.find('"')
                oldloc=0
                while loc > -1:
                    loc = new_name.find('"',oldloc)
                    if loc > -1:
                        b = new_name[:loc]
                        e = new_name[loc+1:]
                        new_name = b + "&quote" + e
                        oldloc = loc +1
                self.session.set_room_name(new_name, boot_pwd)

    def clean_sub_menus(self):
        for mid in WG_MENU_LIST:
            try:
                self.wgMenu.Remove(WG_MENU_LIST[mid]["menuid"])
                WG_MENU_LIST[mid]["menu"].Destroy()
            except:
                self.wgMenu.UpdateUI()
        if self.wgMenu.GetMenuItemCount() == 2:
            WG_MENU_LIST.clear()
        return

    def on_menu_whispergroup( self, evt ):
        self.session = open_rpg.get_component("session")
        self.settings = open_rpg.get_component('settings')
        self.chat = open_rpg.get_component('chat')
        "Add/Remove players from Whisper Groups"
        id = evt.GetId()
        item = self.GetItem( self.selected_item )
        #See if it is the main menu
        if id == PLAYER_WG_CREATE:
            create_new_group_dialog = wx.TextEntryDialog(self,"Enter Group Name","Create New Whisper Group")
            if create_new_group_dialog.ShowModal() == wx.ID_OK:
                group_name = create_new_group_dialog.GetValue()
                WG_LIST[group_name] = {}
            return
        elif id == PLAYER_WG_CLEAR_ALL:
            WG_LIST.clear()
            return

        #Check Sub Menus
        for mid in WG_MENU_LIST:
            if id == WG_MENU_LIST[mid]["add"]:
                WG_LIST[mid][int(item.GetText())] = int(item.GetText())
                return
            elif id == WG_MENU_LIST[mid]["remove"]:
                del WG_LIST[mid][int(item.GetText())]
                return
            elif id == WG_MENU_LIST[mid]["clear"]:
                WG_LIST[mid].clear()
                return
            elif id == WG_MENU_LIST[mid]["whisper"]:
                self.chat.set_chat_text("/gw " + mid + "=")
                return
        return

    def on_menu_role_change( self, evt ):
        self.session = open_rpg.get_component("session")
        "Change the role of the selected id."
        id = evt.GetId()
        self.chat = open_rpg.get_component( "chat" )
        playerID = self.GetItemData( self.selected_item )
        roleString = None
        roleBase = "/role %d=%s"
        infoBase = "Attempting to assign the role of %s to (%d) %s..."
        # Do type specific processing
        recycle_bin = {PLAYER_ROLE_LURKER: ROLE_LURKER, PLAYER_ROLE_PLAYER: ROLE_PLAYER, PLAYER_ROLE_GM: ROLE_GM}
        if id in recycle_bin:
            roleName = recycle_bin[id]
            roleString = (roleBase % ( playerID, roleName ))
            recycle_bin = {}

        # Now, send it to the server
        if roleString:
            self.chat.chat_cmds.docmd( roleString )
            # Now, provide local feedback as to what we requested
            displayName = self.session.get_player_by_player_id( str(playerID) )[0]
            infoString = (infoBase % ( roleName, playerID, displayName ))
            self.chat.InfoPost( infoString )

    def on_d_lclick(self,evt):
        pos = wx.Point(evt.GetX(),evt.GetY())
        (item, flag) = self.HitTest(pos)
        if item > -1:
            self.do_whisper(item)

    def on_menu_item(self,evt):
        id = evt.GetId()
        self.session = open_rpg.get_component("session")
        self.password_manager = open_rpg.get_component("password_manager")

        if id == PLAYER_BOOT:
            id = str(self.GetItemData(self.selected_item))
            boot_pwd = self.password_manager.GetPassword("admin",int(self.session.group_id))
            if boot_pwd != None:
                self.session.boot_player(id,boot_pwd)

        elif id == PLAYER_WHISPER:
            self.do_whisper(self.selected_item)

        elif id == PLAYER_IGNORE:
            id = str(self.GetItemData(self.selected_item))
            self.chat = open_rpg.get_component("chat")
            (result,id,name) = session.toggle_ignore(id)
            if result == 0:
                self.chat.Post(chat.colorize(chat.syscolor, "Player " + name + " with ID:" + id +" no longer ignored"))
            else:
                self.chat.Post(chat.colorize(chat.syscolor, "Player " + name + " with ID:" + id +" now being ignored"))

        elif id == PLAYER_SHOW_VERSION:
            id = str(self.GetItemData(self.selected_item))
            version_string = self.session.players[id][6]
            if version_string:
                wx.MessageBox("Running client version " + version_string,"Version")
            else:
                wx.MessageBox("No client version available for this player","Version")

    def on_menu(self, evt):
        pos = wx.Point(evt.GetX(),evt.GetY())
        (item, flag) = self.HitTest(pos)
        if item > -1:
            self.SetItemState(item, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
            self.selected_item = item
            #  This if-else block makes the menu item to boot players active or inactive, as appropriate
            if open_rpg.get_component("session").group_id == "0":
                self.menu.Enable(PLAYER_BOOT,0)
                self.menu.SetLabel(PLAYER_BOOT,"Can't boot from Lobby")
            else:
                self.menu.Enable(PLAYER_BOOT,1)
                self.menu.SetLabel(PLAYER_BOOT,"Boot")
            self.menu.Enable(PLAYER_WG_MENU, True)
            item = self.GetItem( self.selected_item )

            if len(WG_MENU_LIST) > len(WG_LIST):
                self.clean_sub_menus()

            if len(WG_LIST) == 0:
                self.wgMenu.Enable(PLAYER_WG_CLEAR_ALL, False)
            else:
                self.wgMenu.Enable(PLAYER_WG_CLEAR_ALL, True)

            for gid in WG_LIST:
                if gid not in WG_MENU_LIST:
                    WG_MENU_LIST[gid] = {}
                    WG_MENU_LIST[gid]["menuid"] = wx.NewId()
                    WG_MENU_LIST[gid]["whisper"] = wx.NewId()
                    WG_MENU_LIST[gid]["add"] = wx.NewId()
                    WG_MENU_LIST[gid]["remove"] = wx.NewId()
                    WG_MENU_LIST[gid]["clear"] = wx.NewId()
                    WG_MENU_LIST[gid]["menu"] = wx.Menu()
                    WG_MENU_LIST[gid]["menu"].SetTitle(gid)
                    WG_MENU_LIST[gid]["menu"].Append(WG_MENU_LIST[gid]["whisper"], "Whisper")
                    WG_MENU_LIST[gid]["menu"].Append(WG_MENU_LIST[gid]["add"], "Add")
                    WG_MENU_LIST[gid]["menu"].Append(WG_MENU_LIST[gid]["remove"], "Remove")
                    WG_MENU_LIST[gid]["menu"].Append(WG_MENU_LIST[gid]["clear"], "Clear")
                    self.wgMenu.PrependMenu(WG_MENU_LIST[gid]["menuid"], gid, WG_MENU_LIST[gid]["menu"])

                if int(item.GetText()) in WG_LIST[gid]:
                    WG_MENU_LIST[gid]["menu"].Enable(WG_MENU_LIST[gid]["remove"], True)
                    WG_MENU_LIST[gid]["menu"].Enable(WG_MENU_LIST[gid]["add"], False)
                else:
                    WG_MENU_LIST[gid]["menu"].Enable(WG_MENU_LIST[gid]["remove"], False)
                    WG_MENU_LIST[gid]["menu"].Enable(WG_MENU_LIST[gid]["add"], True)

                if len(WG_LIST[gid]) == 0:
                    WG_MENU_LIST[gid]["menu"].Enable(WG_MENU_LIST[gid]["whisper"], False)
                    WG_MENU_LIST[gid]["menu"].Enable(WG_MENU_LIST[gid]["clear"], False)
                else:
                    WG_MENU_LIST[gid]["menu"].Enable(WG_MENU_LIST[gid]["whisper"], True)
                    WG_MENU_LIST[gid]["menu"].Enable(WG_MENU_LIST[gid]["clear"], True)

                #Event Stuff
                self.Bind(wx.EVT_MENU, self.on_menu_whispergroup, id=WG_MENU_LIST[gid]["whisper"] )
                self.Bind(wx.EVT_MENU, self.on_menu_whispergroup, id=WG_MENU_LIST[gid]["add"] )
                self.Bind(wx.EVT_MENU, self.on_menu_whispergroup, id=WG_MENU_LIST[gid]["remove"] )
                self.Bind(wx.EVT_MENU, self.on_menu_whispergroup, id=WG_MENU_LIST[gid]["clear"] )
            self.PopupMenu(self.menu,pos)

    def add_player(self,player):
        i = self.InsertItem(0,player[2],0)
        self.SetItem(i,1,self.strip_html(player))
        self.SetItemData(i,int(player[2]))
        self.SetItem(i, 2,player[3])
        self.refresh_list()

    def del_player(self,player):
        i = self.FindItem(-1,int(player[2]))
        self.DeleteItem(i)
        for gid in WG_LIST:
            if int(player[2]) in WG_LIST[gid]:
                del WG_LIST[gid][int(player[2])]
        self.refresh_list()

    #  This method updates the player info
    #
    #  self:  reference to this PlayerList
    #  player:  reference to a player structure(list)
    #
    #  Returns:  None
    #
    def update_player(self,player):
        i = self.FindItem(-1,int(player[2]))  #  finds the right list box index
        self.SetItem(i,1,self.strip_html(player))
        self.SetItem(i,2,player[3])
        self.refresh_list()

    def refresh_list(self):
        self.colorize_player_list()
        self.resize_columns()

    def colorize_player_list(self):
        session = open_rpg.get_component("session")
        settings = open_rpg.get_component('settings')
        mode = settings.get_setting("ColorizeRoles")
        if mode.lower() == "off":
            return
        gmColor = settings.get_setting("GMRoleColor")
        plColor = settings.get_setting("PlayerRoleColor")
        lkColor = settings.get_setting("LurkerRoleColor")
        players = session.players
        for m in list(players.keys()):
            item_list_location = self.FindItem(-1,int(m))
            if item_list_location == -1: continue
            player_info = session.get_player_by_player_id(m)
            item = self.GetItem(item_list_location)
            role = player_info[7].lower()
            color = wx.GREEN
            if self.session.group_id != "0":
                recycle_bin = {'lurker': lkColor, 'player': plColor, 'gm': gmColor }
                item.SetTextColour(recycle_bin[role])
                recycle_bin = {}
            self.SetItem(item)

    def resize_columns(self):
        self.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.SetColumnWidth(2, self.GetClientSize().x - self.GetColumnWidth(0) - self.GetColumnWidth(1))

    def reset(self):
        WG_LIST.clear()
        self.DeleteAllItems()

    def do_whisper(self, item):
        id = self.GetItemText(item)
        self.chat = open_rpg.get_component("chat")
        if self.chat.tabbed_whispers.bool:
            self.chat.open_whisper_tab(id)
        else:
            self.chat.set_chat_text("/w " + id + "=")

    def strip_html(self,player):
        ret_string = ""
        x = 0
        in_tag = 0

        for x in range(len(player[0])) :
            if player[0][x] == "<" or player[0][x] == ">" or in_tag == 1 :
                if player[0][x] == "<" :
                    in_tag = 1
                elif player[0][x] == ">" :
                    in_tag = 0
                else :
                    pass
            else :
                ret_string = ret_string + player[0][x]
        return ret_string
