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
            str(self.sid)+","+str(self.dlc)+","+str(self.data[0])+","+str(self.data[1])+","+str(self.data[2])+","+str(self.data[3])+","+str(self.timestamp)+"\n",
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

        msg = Message(sid, dlc, data, timestamp)

        return msg

    def get_data8(self):
        data = []
        for i in range(4):
            data.append(self.data[i] & 0xFF)
            data.append(self.data[i] >> 8)

        return data

    def __repr__(self):
        return str(self.encode_json())[1:]


def test_encode_json():
    msg = Message(100, 8, [1,2,3,4], 100)
    j = json.loads(msg.encode_json())
    assert j["sid"] == 100
    assert j["dlc"] == 8
    assert j["data"] == [1,2,3,4]
    assert j["timestamp"] == 100

def test_encode_bstring():
    msg = Message(100, 8, [1,2,3,4], 100)
    js = msg.encode_bstring().split(b",")
    js = [int(j) for j in js]

    assert js[0] == 100
    assert js[1] == 8
    assert js[2] == 1
    assert js[3] == 2 
    assert js[4] == 3 
    assert js[5] == 4 
    assert js[6] == 100

def test_encode_struct():
    msg = Message(100, 8, [1,2,3,4], 100)
    msg = Message.decode_struct(msg.encode_struct())

    assert msg.sid == 100
    assert msg.dlc == 8
    assert msg.data == [1,2,3,4]
    assert msg.timestamp == 100
