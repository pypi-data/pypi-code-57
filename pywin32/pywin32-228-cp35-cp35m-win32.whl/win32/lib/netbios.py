import sys
import win32wnet
import struct

# Constants generated by h2py from nb30.h
NCBNAMSZ = 16
MAX_LANA = 254
NAME_FLAGS_MASK = 0x87
GROUP_NAME = 0x80
UNIQUE_NAME = 0x00
REGISTERING = 0x00
REGISTERED = 0x04
DEREGISTERED = 0x05
DUPLICATE = 0x06
DUPLICATE_DEREG = 0x07
LISTEN_OUTSTANDING = 0x01
CALL_PENDING = 0x02
SESSION_ESTABLISHED = 0x03
HANGUP_PENDING = 0x04
HANGUP_COMPLETE = 0x05
SESSION_ABORTED = 0x06
ALL_TRANSPORTS = "M\0\0\0"
MS_NBF = "MNBF"
NCBCALL = 0x10
NCBLISTEN = 0x11
NCBHANGUP = 0x12
NCBSEND = 0x14
NCBRECV = 0x15
NCBRECVANY = 0x16
NCBCHAINSEND = 0x17
NCBDGSEND = 0x20
NCBDGRECV = 0x21
NCBDGSENDBC = 0x22
NCBDGRECVBC = 0x23
NCBADDNAME = 0x30
NCBDELNAME = 0x31
NCBRESET = 0x32
NCBASTAT = 0x33
NCBSSTAT = 0x34
NCBCANCEL = 0x35
NCBADDGRNAME = 0x36
NCBENUM = 0x37
NCBUNLINK = 0x70
NCBSENDNA = 0x71
NCBCHAINSENDNA = 0x72
NCBLANSTALERT = 0x73
NCBACTION = 0x77
NCBFINDNAME = 0x78
NCBTRACE = 0x79
ASYNCH = 0x80
NRC_GOODRET = 0x00
NRC_BUFLEN = 0x01
NRC_ILLCMD = 0x03
NRC_CMDTMO = 0x05
NRC_INCOMP = 0x06
NRC_BADDR = 0x07
NRC_SNUMOUT = 0x08
NRC_NORES = 0x09
NRC_SCLOSED = 0x0a
NRC_CMDCAN = 0x0b
NRC_DUPNAME = 0x0d
NRC_NAMTFUL = 0x0e
NRC_ACTSES = 0x0f
NRC_LOCTFUL = 0x11
NRC_REMTFUL = 0x12
NRC_ILLNN = 0x13
NRC_NOCALL = 0x14
NRC_NOWILD = 0x15
NRC_INUSE = 0x16
NRC_NAMERR = 0x17
NRC_SABORT = 0x18
NRC_NAMCONF = 0x19
NRC_IFBUSY = 0x21
NRC_TOOMANY = 0x22
NRC_BRIDGE = 0x23
NRC_CANOCCR = 0x24
NRC_CANCEL = 0x26
NRC_DUPENV = 0x30
NRC_ENVNOTDEF = 0x34
NRC_OSRESNOTAV = 0x35
NRC_MAXAPPS = 0x36
NRC_NOSAPS = 0x37
NRC_NORESOURCES = 0x38
NRC_INVADDRESS = 0x39
NRC_INVDDID = 0x3B
NRC_LOCKFAIL = 0x3C
NRC_OPENERR = 0x3f
NRC_SYSTEM = 0x40
NRC_PENDING = 0xff


UCHAR = "B"
WORD = "H"
DWORD = "I"
USHORT = "H"
ULONG = "I"

ADAPTER_STATUS_ITEMS = [
    ("6s",        "adapter_address"),
    (UCHAR,   "rev_major"),
    (UCHAR,   "reserved0"),
    (UCHAR,   "adapter_type"),
    (UCHAR,   "rev_minor"),
    (WORD,    "duration"),
    (WORD,    "frmr_recv"),
    (WORD,    "frmr_xmit"),

    (WORD,    "iframe_recv_err"),

    (WORD,    "xmit_aborts"),
    (DWORD,   "xmit_success"),
    (DWORD,   "recv_success"),

    (WORD,    "iframe_xmit_err"),

    (WORD,    "recv_buff_unavail"),
    (WORD,    "t1_timeouts"),
    (WORD,    "ti_timeouts"),
    (DWORD,   "reserved1"),
    (WORD,    "free_ncbs"),
    (WORD,    "max_cfg_ncbs"),
    (WORD,    "max_ncbs"),
    (WORD,    "xmit_buf_unavail"),
    (WORD,    "max_dgram_size"),
    (WORD,    "pending_sess"),
    (WORD,    "max_cfg_sess"),
    (WORD,    "max_sess"),
    (WORD,    "max_sess_pkt_size"),
    (WORD,    "name_count"),
]

NAME_BUFFER_ITEMS = [
    (str(NCBNAMSZ) + "s", "name"),
    (UCHAR,   "name_num"),
    (UCHAR,   "name_flags"),
]

SESSION_HEADER_ITEMS = [
    (UCHAR,   "sess_name"),
    (UCHAR,   "num_sess"),
    (UCHAR,   "rcv_dg_outstanding"),
    (UCHAR,   "rcv_any_outstanding"),
]

SESSION_BUFFER_ITEMS = [
    (UCHAR,   "lsn"),
    (UCHAR,   "state"),
    (str(NCBNAMSZ)+"s",   "local_name"),
    (str(NCBNAMSZ)+"s",   "remote_name"),
    (UCHAR,   "rcvs_outstanding"),
    (UCHAR,   "sends_outstanding"),
]

LANA_ENUM_ITEMS = [
    ("B",   "length"),         # Number of valid entries in lana[]
    (str(MAX_LANA+1) + "s", "lana"),
]

FIND_NAME_HEADER_ITEMS = [
    (WORD,    "node_count"),
    (UCHAR,   "reserved"),
    (UCHAR,   "unique_group"),
]

FIND_NAME_BUFFER_ITEMS = [
    (UCHAR,   "length"),
    (UCHAR,   "access_control"),
    (UCHAR,   "frame_control"),
    ("6s",   "destination_addr"),
    ("6s", "source_addr"), 
    ("18s", "routing_info"),
]

ACTION_HEADER_ITEMS = [
    (ULONG,   "transport_id"),
    (USHORT,  "action_code"),
    (USHORT,  "reserved"),
]
    
del UCHAR, WORD, DWORD, USHORT, ULONG

NCB = win32wnet.NCB
def Netbios(ncb):
    ob = ncb.Buffer
    is_ours = hasattr(ob, "_pack")
    if is_ours:
        ob._pack()
    try:
        return win32wnet.Netbios(ncb)
    finally:
        if is_ours:
            ob._unpack()
        
class NCBStruct:
    def __init__(self, items):
        self._format = "".join([item[0] for item in items])
        self._items = items
        self._buffer_ = win32wnet.NCBBuffer(struct.calcsize(self._format))

        for format, name in self._items:
            if len(format)==1:
                if format == 'c':
                    val = '\0'
                else:
                    val = 0
            else:
                l = int(format[:-1])
                val = '\0' * l
            self.__dict__[name] = val

    def _pack(self):
        vals = []
        for format, name in self._items:
            try:
                vals.append(self.__dict__[name])
            except KeyError:
                vals.append(None)
        
        self._buffer_[:] = struct.pack(*(self._format,) + tuple(vals))

    def _unpack(self):
        items = struct.unpack(self._format, self._buffer_)
        assert len(items)==len(self._items), "unexpected number of items to unpack!"
        for (format, name), val in zip(self._items, items):
            self.__dict__[name] = val

    def __setattr__(self, attr, val):
        if attr not in self.__dict__ and attr[0]!='_':
            for format, attr_name in self._items:
                if attr==attr_name:
                    break
            else:
                raise AttributeError(attr)
        self.__dict__[attr] = val

def ADAPTER_STATUS():
    return NCBStruct(ADAPTER_STATUS_ITEMS)

def NAME_BUFFER():
    return NCBStruct(NAME_BUFFER_ITEMS)

def SESSION_HEADER():
    return NCBStruct(SESSION_HEADER_ITEMS)

def SESSION_BUFFER():
    return NCBStruct(SESSION_BUFFER_ITEMS)

def LANA_ENUM():
    return NCBStruct(LANA_ENUM_ITEMS)

def FIND_NAME_HEADER():
    return NCBStruct(FIND_NAME_HEADER_ITEMS)

def FIND_NAME_BUFFER():
    return NCBStruct(FIND_NAME_BUFFER_ITEMS)

def ACTION_HEADER():
    return NCBStruct(ACTION_HEADER_ITEMS)

def byte_to_int(b):
    """Given an element in a binary buffer, return its integer value"""
    if sys.version_info >= (3,0):
        # a byte is already an int in py3k
        return b
    return ord(b) # its a char from a string in py2k.

if __name__=='__main__':
    # code ported from "HOWTO: Get the MAC Address for an Ethernet Adapter"
    # MS KB ID: Q118623 
    ncb = NCB()
    ncb.Command = NCBENUM
    la_enum = LANA_ENUM()
    ncb.Buffer = la_enum
    rc = Netbios(ncb)
    if rc != 0: raise RuntimeError("Unexpected result %d" % (rc,))
    for i in range(la_enum.length):
        ncb.Reset()
        ncb.Command = NCBRESET
        ncb.Lana_num = byte_to_int(la_enum.lana[i])
        rc = Netbios(ncb)
        if rc != 0: raise RuntimeError("Unexpected result %d" % (rc,))
        ncb.Reset()
        ncb.Command = NCBASTAT
        ncb.Lana_num = byte_to_int(la_enum.lana[i])
        ncb.Callname = "*               ".encode("ascii") # ensure bytes on py2x and 3k
        adapter = ADAPTER_STATUS()
        ncb.Buffer = adapter
        Netbios(ncb)
        print("Adapter address:", end=' ')
        for ch in adapter.adapter_address:
            print("%02x" % (byte_to_int(ch),), end=' ')
        print()
