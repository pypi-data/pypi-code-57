# Copyright (C) 2018 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import socket
from struct import calcsize
from threading import Lock
import time
from xml.sax.saxutils import escape

import orpg.networking.mplay_conn as mplay_conn
import queue
from orpg.orpg_version import *

MPLAY_LENSIZE = calcsize('i')
MPLAY_DISCONNECTED = 0
MPLAY_CONNECTED = 1
MPLAY_DISCONNECTING = 3

# This should be configurable
OPENRPG_PORT = 6774

class client_base:

    # Player role definitions
    def __init__(self):
        self.outbox = queue.Queue(0)
        self.inbox = queue.Queue(0)
        self.id = "0"
        self.group_id = "0"
        self.name = ""
        self.role = "GM"
        self.ROLE_GM = "GM"
        self.ROLE_PLAYER = "PLAYER"
        self.ROLE_LURKER = "LURKER"
        self.ip = socket.gethostbyname(socket.gethostname())
        self.version = VERSION
        self.protocol_version = PROTOCOL_VERSION
        self.client_string = CLIENT_STRING
        self.status = MPLAY_DISCONNECTED
        self.log_console = None
        self.sock = None
        self.text_status = "Idle"
        self.statLock = Lock()
        self.useroles = 0

    def connected(self):
        self.set_status(MPLAY_CONNECTED)
        self.conn = mplay_conn.connection(self.sock, self.inbox, self.outbox)

    def disconnect(self):
        if self.get_status() == MPLAY_CONNECTED:
            self.set_status(MPLAY_DISCONNECTING)
            self.conn.disconnect()
            self.set_status(MPLAY_DISCONNECTED)

    def reset(self, sock):
        self.disconnect()
        self.sock = sock
        self.connected()

    def update_role(self,role):
        self.useroles = 1
        self.role = role

    def use_roles(self):
        if self.useroles:
            return 1
        else:
            return 0

    def update_self_from_player(self, player):
        try:
            (self.name, self.ip, self.id, self.text_status, self.version, self.protocol_version, self.client_string,role) = player
        except Exception as e:
            print(e)

# The IP field should really be deprecated as too many systems are NAT'd and/or behind firewalls for a
# client provided IP address to have much value.  As such, we now label it as deprecated.
    def toxml(self,action):
        xml_data = '<player name="' + escape(self.name, {"\"":""}) + '"'
        xml_data += ' action="' + action + '"'
        xml_data += ' id="' + self.id + '"'
        xml_data += ' group_id="' + self.group_id + '"'
        xml_data += ' status="' + self.text_status + '"'
        xml_data += ' version="' + self.version + '"'
        xml_data += ' protocol_version="' + self.protocol_version + '"'
        xml_data += ' client_string="' + self.client_string + '"'
        xml_data += ' />'
        return xml_data

    def log_msg(self,msg):
        if self.log_console:
            self.log_console(msg)

    def get_status(self):
        self.statLock.acquire()
        status = self.status
        self.statLock.release()
        return status

    def my_role(self):
#Why create the three different objects?  Why not just assign a value to self.role and use that? Prof_Ebral ponders.
        if self.role == "GM":
            return self.ROLE_GM
        elif self.role == "Player":
            return self.ROLE_PLAYER
        elif self.role == "Lurker":
            return self.ROLE_LURKER
        return -1

    def set_status(self,status):
        self.statLock.acquire()
        self.status = status
        self.statLock.release()

    def __str__(self):
        return "%s(%s)\nIP:%s\ngroup_id:%s\n" % (self.name, self.id, self.ip, self.group_id)

    def idle_time(self):
        curtime = time.time()
        idletime = curtime - self.conn.last_message_time
        return idletime

    def idle_status(self):
        idletime = self.idle_time()
        idlemins = idletime / 60
        status = "Unknown"
        if idlemins < 3:
            status = "Active"
        elif idlemins < 10:
            status = "Idle ("+str(int(idlemins))+" mins)"
        else:
            status = "Inactive ("+str(int(idlemins))+" mins)"
        return status

    def connected_time(self):
        curtime = time.time()
        timeoffset = curtime - self.conn.connect_time
        return timeoffset

    def connected_time_string(self):
        "returns the time client has been connected as a formated time string"
        ct = self.connected_time()
        d = int(ct/86400)
        h = int( (ct-(86400*d))/3600 )
        m = int( (ct-(86400*d)-(3600*h))/60)
        s = int( (ct-(86400*d)-(3600*h)-(60*m)) )
        return f"{d:02}:{h:02}:{m:02}:{s:02}"
