# -*- coding: utf-8 -*-

'''Administrator Shell in WIndows
'''

from __future__ import print_function

import ctypes
import os
import pickle
import random
import socket
import sys
try:
    import thread
except ImportError:
    import _thread as thread
import threading
import time


class AdminShell(object):

    UDP_PORT_ENV = 'RAWDUMP_UDP_PORT'

    def __init__(self):
        self._port = os.environ.get(self.UDP_PORT_ENV)
        if self._port:
            self._port = int(self._port)
            self._is_admin = True
        elif not ctypes.windll.shell32.IsUserAnAdmin():
            self._port = random.randint(10000, 65535)
            self._is_admin = False

    def run(self):
        if not self._port:
            return

        if not self._is_admin:
            server = socket.socket(type=socket.SOCK_DGRAM)
            server.bind(('127.0.0.1', self._port))
            server.settimeout(1)
            print('[+] Elevate to administrator privilege...')
            time.sleep(0.5)
            self.create_admin_shell()
            client_address = None
            break_flag = False

            while True:
                try:
                    try:
                        buffer, address = server.recvfrom(4096)
                        if not client_address:
                            client_address = address
                        elif client_address != address:
                            print('[+] Ignore message from address %s:%d' % address)
                            continue

                        data = pickle.loads(buffer)
                        if data['type'] == 'stdout':
                            sys.stdout.write(data['data'])
                        elif data['type'] == 'stderr':
                            sys.stderr.write(data['data'])
                    except socket.timeout:
                        if break_flag:
                            # exit process
                            sys.exit(0)
                except KeyboardInterrupt:
                    # notify admin shell process to exit
                    if client_address:
                        server.sendto(pickle.dumps({
                            'type': 'exit'
                        }), client_address)
                    else:
                        print('[+] No admin shell process to notify exit')
                        break
                    break_flag = True

            return False
        else:
            client = socket.socket(type=socket.SOCK_DGRAM)
            client.connect(('127.0.0.1', self._port))

            class OutStream(object):

                def __init__(self, stream_type, origin_stream):
                    self._stream_type = stream_type
                    self._origin_stream = origin_stream
                
                def write(self, data):
                    self._origin_stream.write(data)
                    buffer = pickle.dumps({
                                        'type': self._stream_type,
                                        'data': data
                                    })
                    client.send(buffer)
                    
                def flush(self):
                    pass

            sys.stdout = OutStream('stdout', sys.stdout)
            sys.stderr = OutStream('stderr', sys.stderr)

            def read_thread():
                while True:
                    buffer = client.recv(4096)
                    data = pickle.loads(buffer)
                    if data['type'] == 'exit':
                        thread.interrupt_main()
                        break
            th = threading.Thread(target=read_thread)
            th.daemon = True
            th.start()
            return True

    def create_admin_shell(self):
        params = ' '.join(sys.argv)
        if isinstance(params, bytes):
            params = params.decode()
        workdir = os.getcwd()
        if isinstance(workdir, bytes):
            workdir = workdir.decode()
        params = u'/c cd /d "%s" && set %s=%s && %s' % (workdir, self.UDP_PORT_ENV, self._port, params)
        ctypes.windll.shell32.ShellExecuteW(0, u'runas', u'cmd.exe', params, None, 0)
        