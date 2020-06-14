from dataclasses import dataclass, field
from typing import *
import json
import struct

class Message:
    def __init__(self, sid: int, dlc: int, data: List[int], timestamp: int):
        self.sid = sid
        self.dlc = dlc
        self.data = data
        self.timestamp = timestamp

    def encode_json(self):
        return bytes(
            json.dumps(
                {
                    "sid": self.sid,
                    "dlc": self.dlc,
                    "data": self.data,
                    "timestamp": self.timestamp,
                }
            ),
            "utf-8",
        )

    def encode_bstring(self):
        return bytes(
            f"{self.sid},{self.dlc},{self.data[0]},{self.data[1]},{self.data[2]},{self.data[3]},{self.timestamp}\n",
            "utf-8",
        )
    
    def encode_struct(self):
        s = struct.pack("HH4HI", self.sid, self.dlc, *self.data, self.timestamp)
        return s

    @staticmethod
    def decode_json(j):
        msg = Message()
        d = json.loads(j.decode())

        msg.sid = d.get("sid")
        msg.dlc = d.get("dlc")
        msg.data = d.get("data")
        msg.timestamp = d.get("timestamp")

        if (msg.sid and msg.dlc and msg.data and msg.timestamp) == None:
            raise ValueError("Received invalid message: " + j.decode())
            return

        return msg

    @staticmethod
    def decode_bytestring(bstring):
        msg = Message()
        #print(bstring)
        sid, dlc, *data, timestamp = bstring.decode().split(",")
        msg.sid = int(sid)
        msg.dlc = int(dlc)
        msg.timestamp = int(timestamp)
        msg.data = [0 for i in range(4)]
        for i,d in enumerate(data):
            msg.data[i] = int(d)
        return msg

    @staticmethod
    def decode_CANmessage(message):
        msg = Message()
        msg.sid = message.sid
        msg.dlc = message.dlc
        msg.data = [0, 0, 0, 0]
        for i in range(4):
            msg.data[i] = (message.data >> i * 16) & 0xFFFF
        return msg

    @staticmethod
    def decode_struct(s):
        sid, dlc, *data, timestamp = struct.unpack("HH4HI", s)

        #print(sid, dlc, data, timestamp)

        msg = Message()
        msg.sid = sid
        msg.dlc = dlc
        msg.data = data
        msg.timestamp = timestamp

        return msg

    def get_data8(self):
        data = []
        for i in range(4):
            data.append(self.data[i] & 0xFF)
            data.append(self.data[i] >> 8)

        return data
