# -*- coding: utf-8 -*-

from __future__ import print_function

import ctypes
import random
import os
import socket
import sys
import threading
import time

try:
    import socketserver
except ImportError:
    import SocketServer as socketserver

import pytest

from rawdump import handlers
from rawdump import rawsocket


class EchoRequestHandler(socketserver.StreamRequestHandler):

    def handle(self):
        print('Accept new connection...')
        buff = b''
        while True:
            c = self.rfile.read(1)
            buff += c
            if c == b'\n':
                self.wfile.write(buff)
                buff = b''


def start_test_server(port):
    server = socketserver.TCPServer(('127.0.0.1', port), EchoRequestHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    return thread


def check_env():
    if sys.platform == 'win32':
        return ctypes.windll.shell32.IsUserAnAdmin()
    else:
        return os.getuid() == 0


def test_packet_manager():
    if not check_env():
        print('Check env failed, exit test', file=sys.stderr)
        return
    port = random.randint(10000, 65000)
    start_test_server(port)
    keyword = 'RawDumpTest'
    manager = handlers.PacketManager('tcp', None, [port], [keyword])
    socks = rawsocket.RawSockets(['127.0.0.1' if sys.platform == 'win32' else 'lo'])
    packets = []
    class MockPacketHandler(handlers.IPacketHandler):
        def on_new_packet(self, stream, timestamp, direction, packet):
            packets.append(packet)
    manager.register_handler(MockPacketHandler())

    def send_data():
        time.sleep(0.5)
        s = socket.socket()
        s.connect(('127.0.0.1', port))
        s.send(('%s\n' % keyword).encode())
        print('Recv', s.recv(4096))
        s.close()
    
    t = threading.Thread(target=send_data)
    t.daemon = True
    t.start()

    time0 = time.time()
    while time.time() - time0 < 2:
        ip_packet = socks.read_packet()
        if ip_packet:
            manager.on_packet(ip_packet)

    assert(len(packets) > 0)

if __name__ == '__main__':
    test_packet_manager()
