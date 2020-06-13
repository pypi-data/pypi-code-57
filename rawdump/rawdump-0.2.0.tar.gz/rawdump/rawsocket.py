# -*- coding: utf-8 -*-
'''Raw socket

https://sock-raw.org/papers/sock_raw
'''

import select
import socket
import struct
import sys

try:
    long
except NameError:
    long = int


class Field(object):
    format = ''

    def __len__(self):
        return 0


class IPv4Addr(Field):
    format = 'I'

    def __init__(self, addr):
        if addr == None:
            self._addr = 0
        elif isinstance(addr, IPv4Addr):
            self._addr = addr._addr
        elif isinstance(addr, (int, long)):
            self._addr = addr
        else:
            self._addr = socket.ntohl(
                struct.unpack("I", socket.inet_aton(addr))[0])

    def __len__(self):
        return 4

    def __str__(self):
        return socket.inet_ntoa(struct.pack('I', socket.htonl(self._addr)))

    def __repr__(self):
        return '<IPv4Addr object at 0x%.8X [%s]>' % (id(self), self)

    def __int__(self):
        return self._addr

    def __eq__(self, other):
        if isinstance(other, IPv4Addr):
            return self._addr == other._addr
        elif isinstance(other, int):
            return self._addr == other
        else:
            return str(self) == other

    def __ne__(self, other):
        return not self == other


class Packet(object):
    '''Packet base class
    '''
    big_ending = True
    __fields__ = []

    def __init__(self, buffer):
        self._buffer = buffer
        self._fields = []
        clazz = self.__class__
        while clazz != Packet:
            self._fields = clazz.__fields__ + self._fields
            clazz = clazz.__bases__[0]
        assert (len(self._fields) > 0)
        self._format = '>' if self.__class__.big_ending else '<'
        self._body = b''
        for field, type in self._fields:
            setattr(self, field, None)
            self._format += type if isinstance(type, str) else type.format
        self.parse(buffer)

    @property
    def buffer(self):
        return self._buffer

    @property
    def body(self):
        return self._body

    def check(self, header):
        pass

    def parse(self, buffer):
        items = struct.unpack_from(self._format, buffer)
        index = 0
        for i in range(len(self._fields)):
            field_type = self._fields[i][1]
            item_count = len(field_type if isinstance(field_type, str
                                                      ) else field_type.format)
            if item_count > 1:
                value = items[index:index + item_count]
            else:
                value = items[index]
            index += item_count
            if not isinstance(field_type, str) and issubclass(
                    field_type, Field):
                value = field_type(value)
            setattr(self, self._fields[i][0], value)
        header_len = struct.calcsize(self._format)
        self._body = buffer[header_len:]
        try:
            self.check(buffer[:header_len])
        except AssertionError:
            logging.exception('Check packet failed')


class EnumIPPacketType(object):
    ICMP = 1
    TCP = 6
    UDP = 17


class IPPacket(Packet):

    __fields__ = [
        ('version_length', 'B'),
        ('tos', 'B'),
        ('total_length', 'H'),
        ('identification', 'H'),
        ('flags_and_frag_off', 'H'),
        ('ttl', 'B'),
        ('protocol', 'B'),  # subprotocol
        ('checksum', 'H'),
        ('src_addr', IPv4Addr),
        ('dst_addr', IPv4Addr)
    ]


class TCPPacket(Packet):

    __fields__ = [
        ('src_port', 'H'),
        ('dst_port', 'H'),
        ('seq_num', 'I'),
        ('ack_num', 'I'),
        ('data_offset', 'B'),  # 报头长度
        ('flags', 'B'),
        ('window', 'H'),
        ('checksum', 'H'),
        ('urgent_pointer', 'H')
    ]

    def get_flags(self):
        flags = []
        for key in ('FIN', 'SYN', 'RST', 'PSH', 'ACK', 'URG'):
            if self.flags & getattr(EnumTCPPacketFlag, key):
                flags.append(key)
        return flags


class EnumTCPPacketFlag(object):

    FIN = 1
    SYN = 2
    RST = 4
    PSH = 8
    ACK = 16
    URG = 32


class UDPPacket(Packet):

    __fields__ = [
        ('src_port', 'H'),
        ('dst_port', 'H'),
        ('length', 'H'),
        ('checksum', 'H'),
    ]


class EnumICMPPacketType(object):

    ECHO_REPLY = 0
    ECHO = 8

    @staticmethod
    def get_name(type):
        for it in dir(EnumICMPPacketType):
            if it[0] == '_':
                continue
            if it != it.upper():
                continue
            if getattr(EnumICMPPacketType, it) == type:
                return it
        return type


class ICMPPacket(Packet):

    __fields__ = [
        ('type', 'B'),
        ('code', 'B'),
        ('checksum', 'H'),
    ]

    def get_type(self):
        return EnumICMPPacketType.get_name(self.type)


class RawSocket(object):
    '''Raw Socket
    '''

    def __init__(self, listen_addr):
        if sys.platform == 'win32':
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                                       socket.IPPROTO_IP)
            self._sock.bind((listen_addr, 0))
            self._sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        elif sys.platform == 'linux2':
            self._sock = socket.socket(socket.AF_PACKET, socket.SOCK_DGRAM,
                                       socket.htons(0x800))
            self._sock.bind((listen_addr, socket.SOCK_RAW))
            #self._sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        elif sys.platform == 'darwin':
            import pcap
            self._sock = pcap.pcap(name=listen_addr, promisc=True, immediate=True, timeout_ms=0)
        else:
            raise NotImplementedError(sys.platform)

    def fileno(self):
        return self._sock.fileno()

    def read_packet(self):
        if sys.platform == 'darwin':
            _, buffer = self._sock.next() if hasattr(self._sock, 'next') else self._sock.__next__()
            if buffer[:4] == b'\x02\x00\x00\x00':
                buffer = buffer[4:]
            else:
                protocol_type = buffer[12:14]
                if protocol_type != b'\x08\x00':
                    return None
                buffer = buffer[14:]
        else:
            try:
                buffer, remote_addr = self._sock.recvfrom(1024 * 64)
            except socket.timeout:
                return None

        return IPPacket(buffer)


class RawSockets(object):
    def __init__(self, addr_list, timeout=1):
        self._socks = []
        for addr in addr_list:
            self._socks.append(RawSocket(addr))
        self._timeout = timeout

    def read_packet(self):
        rfds, _, _ = select.select(self._socks, [], [], self._timeout)
        if rfds:
            return rfds[0].read_packet()
