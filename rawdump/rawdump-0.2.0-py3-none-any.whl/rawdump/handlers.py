# -*- coding: utf-8 -*-
'''Handler
'''

from __future__ import print_function

import socket
import struct
import sys
import time

from . import rawsocket


start_time = None

def time_clock():
    if hasattr(time, 'perf_counter'):
        return time.perf_counter()
    else:
        return time.clock()


def timestamp():
    global start_time
    if not start_time:
        start_time = time.time()
        start_time -= time_clock()
    return start_time + time_clock()


class EnumPacketDirection(object):
    UP = 'up'
    DOWN = 'down'


class Stream(object):
    instances = {}

    def __new__(cls, protocol, src_addr, dst_addr, src_port, dst_port):
        key1 = '%s:%s:%s:%s:%s' % (protocol, src_addr, dst_addr, src_port,
                                   dst_port)
        key2 = '%s:%s:%s:%s:%s' % (protocol, dst_addr, src_addr, dst_port,
                                   src_port)
        if not key1 in cls.instances and not key2 in cls.instances:
            cls.instances[key1] = super(Stream, cls).__new__(cls)
            cls.instances[key1].__my_init__(protocol, src_addr, dst_addr,
                                            src_port, dst_port)
        return cls.instances.get(key1) or cls.instances.get(key2)

    def __my_init__(self, protocol, src_addr, dst_addr, src_port, dst_port):
        self._protocol = protocol
        self._src_addr = src_addr
        self._dst_addr = dst_addr
        self._src_port = src_port
        self._dst_port = dst_port
        self._packets = []
        self._filtered = False

    @property
    def protocol(self):
        return self._protocol.upper()

    @property
    def src_addr(self):
        return self._src_addr

    @property
    def src_port(self):
        return self._src_port

    @property
    def dst_addr(self):
        return self._dst_addr

    @property
    def dst_port(self):
        return self._dst_port

    @property
    def packets(self):
        return self._packets

    @property
    def filtered(self):
        return self._filtered

    @filtered.setter
    def filtered(self, value):
        self._filtered = value

    def add_packet(self, direction, packet):
        self._packets.append((timestamp(), direction, packet))


class IPacketHandler(object):
    def on_new_stream(self, stream):
        pass

    def on_new_packet(self, stream, timestamp, direction, packet):
        pass

    def on_unload(self):
        pass


class Singleton(object):
    '''Singleton Decorator
    '''

    def __init__(self, cls):
        self.__instance = None
        self.__cls = cls

    def __call__(self, *args, **kwargs):
        if not self.__instance:
            self.__instance = self.__cls(*args, **kwargs)
        return self.__instance


@Singleton
class PacketManager(object):
    def __init__(self,
                 protocol,
                 hosts=None,
                 ports=None,
                 keywords=None,
                 filter_list=None):
        self._protocol = protocol
        self._hosts = hosts or []
        self._ports = ports or []
        self._keywords = keywords or []
        self._handlers = []
        self._filter_list = filter_list or []

    def on_packet(self, packet):
        if self._protocol != 'ip':
            protocol = socket.getprotobyname(self._protocol)
            if packet.protocol != protocol:
                return

        if self._hosts:
            for host in self._hosts:
                if packet.src_addr == host or packet.dst_addr == host:
                    break
            else:
                # host not matched
                return

        src_port = dst_port = 0
        padding = b''
        if packet.protocol == rawsocket.EnumIPPacketType.TCP:
            protocol = 'tcp'
            tcp_packet = rawsocket.TCPPacket(packet.body)
            src_port = tcp_packet.src_port
            dst_port = tcp_packet.dst_port

            if self._ports:
                for port in self._ports:
                    if src_port == port or dst_port == port:
                        break
                else:
                    # port not matched
                    return
            padding = tcp_packet.body
        elif packet.protocol == rawsocket.EnumIPPacketType.UDP:
            protocol = 'udp'
            udp_packet = rawsocket.UDPPacket(packet.body)
            src_port = udp_packet.src_port
            dst_port = udp_packet.dst_port

            if self._ports:
                for port in self._ports:
                    if src_port == port or dst_port == port:
                        break
                else:
                    # port not matched
                    return
        elif packet.protocol == rawsocket.EnumIPPacketType.ICMP:
            protocol = 'icmp'
        else:
            print('[+] Unsupported protocol %s' % packet.protocol,
                  file=sys.stderr)
            return

        for it in self._filter_list:
            if it['protocol'] == protocol and (
                    it['host'] == packet.src_addr and it['port'] == src_port or
                    it['host'] == packet.dst_addr and it['port'] == dst_port):
                return

        stream = Stream(protocol, packet.src_addr, packet.dst_addr, src_port,
                        dst_port)

        if not stream.packets:
            if self._keywords:
                # 存在关键字时默认过滤
                stream.filtered = True
            else:
                self.notify('new_stream', stream)

        if self._keywords and stream.filtered:
            for keyword in self._keywords:
                if not isinstance(keyword, bytes):
                    keyword = keyword.encode('utf8')
                if keyword in padding:
                    stream.filtered = False
                    self.notify('new_stream', stream)
                    for ts, direction, _packet in stream.packets:
                        self.notify('new_packet', stream, ts, direction,
                                    _packet)
                    break

        direction = EnumPacketDirection.UP
        if stream.src_addr == packet.dst_addr and stream.src_port == dst_port:
            direction = EnumPacketDirection.DOWN
        if not stream.filtered:
            self.notify('new_packet', stream, timestamp(), direction, packet)
        stream.add_packet(direction, packet)

    def register_handler(self, handler):
        self._handlers.append(handler)

    def notify(self, event, *args, **kwargs):
        for handler in self._handlers:
            getattr(handler, 'on_' + event)(*args, **kwargs)


class StreamPacketHandler(IPacketHandler):
    def on_new_stream(self, stream):
        pass

    def on_new_packet(self, stream, timestamp, direction, packet):
        padding_size = len(packet.body)
        flags = []
        if stream.protocol == 'TCP':
            padding_size -= 20
            flags = rawsocket.TCPPacket(packet.body).get_flags()
        elif stream.protocol == 'UDP':
            padding_size -= 8
        elif stream.protocol == 'ICMP':
            flags.append(rawsocket.ICMPPacket(packet.body).get_type())
        flags = ' '.join([('[%s]' % flag) for flag in flags])
        if stream.src_port and stream.dst_port:
            if direction == EnumPacketDirection.UP:
                print('[*] %s %s:%d => %s:%d %d %s' %
                      (stream.protocol, stream.src_addr, stream.src_port,
                       stream.dst_addr, stream.dst_port, padding_size, flags))
            else:
                print('[*] %s %s:%d => %s:%d %d %s' %
                      (stream.protocol, stream.dst_addr, stream.dst_port,
                       stream.src_addr, stream.src_port, padding_size, flags))
        else:
            if direction == EnumPacketDirection.UP:
                print('[*] %s %s => %s %d %s' % (stream.protocol, stream.src_addr,
                                              stream.dst_addr, padding_size, flags))
            else:
                print('[*] %s %s => %s %d %s' %
                      (stream.protocol, stream.dst_addr, stream.src_addr,
                       padding_size, flags))


class PcapPacketHandler(IPacketHandler):

    max_cache_size = 1024 * 1024

    def __init__(self, save_path):
        self._save_path = save_path
        self._buffer = b''
        self.write_header()

    def write_file(self, buffer, append=True):
        mode = 'ab' if append else 'wb'
        with open(self._save_path, mode) as fp:
            fp.write(buffer)

    def write_header(self):
        buffer = struct.pack('<I', 0xA1B2C3D4)
        buffer += struct.pack('<H', 2)
        buffer += struct.pack('<H', 4)
        buffer += struct.pack('<I', 0)
        buffer += struct.pack('<I', 0)
        buffer += struct.pack('<I', 0xFFFF)
        buffer += struct.pack('<I', 0x65)  # “raw IP”, with no link
        self.write_file(buffer, False)

    def write_packet(self, timestamp, packet):
        data = struct.pack('<I', int(timestamp))
        data += struct.pack('<I', int(1000000 * (timestamp - int(timestamp))))
        data += struct.pack('<I', len(packet.buffer))
        data += struct.pack('<I', len(packet.buffer))
        self._buffer += data
        self._buffer += packet.buffer
        if len(self._buffer) >= self.max_cache_size:
            self.write_file(self._buffer)
            self._buffer = b''

    def on_new_packet(self, stream, timestamp, direction, packet):
        if not hasattr(self, '_last_timestamp'):
            self._last_timestamp = timestamp
        assert(timestamp >= self._last_timestamp)
        self._last_timestamp = timestamp
        self.write_packet(timestamp, packet)

    def on_unload(self):
        self.write_file(self._buffer)
        self._buffer = b''
        print('[+] File saved to %s' % self._save_path)
