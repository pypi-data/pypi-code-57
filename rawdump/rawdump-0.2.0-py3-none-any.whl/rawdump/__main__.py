# -*- coding: utf-8 -*-
'''Module entry
'''

from __future__ import print_function

import argparse
import ctypes
import os
import socket
import struct
import sys

from . import VERSION, BANNER
from . import admin_shell
from . import handlers
from . import rawsocket

try:
    raw_input
except NameError:
    raw_input = input


def check_permission():
    if sys.platform == 'win32':
        sh = admin_shell.AdminShell()
        ret = sh.run()
        if ret == True:
            print('[+] Elevate privilege success')
        elif ret == False:
            sys.exit(0)
    else:
        uid = os.getuid()
        if uid != 0:
            print('[-] Rawdump must run in root user', file=sys.stderr)
            sys.exit(-1)
    return True


def get_interface_list():
    if_list = []
    if sys.platform == 'win32':
        import win32com.client
        wmi = win32com.client.GetObject('winmgmts:')
        index = 0
        for interface in wmi.InstancesOf('Win32_NetworkAdapterConfiguration'):
            if not interface.IPEnabled:
                continue
            index += 1
            if_list.append({
                'id': str(index),
                'ip': interface.IPAddress[0],
                'name': interface.Description
            })
        if_list.append({
            'id': str(index + 1),
            'ip': '127.0.0.1',
            'name': 'Loopback'
        })
    elif sys.platform == 'linux':
        import fcntl
        dirpath = '/sys/class/net'
        if not os.path.isdir(dirpath):
            return if_list
        for intf in os.listdir(dirpath):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                data = fcntl.ioctl(s.fileno(), 0x8915,
                            struct.pack('256s', intf[:15].encode()))
            except:
                continue
            ip = socket.inet_ntoa(data[20:24])
            if_list.append({'id': intf, 'ip': ip, 'name': 'Loopback' if intf == 'lo' else 'Ethernet'})
    elif sys.platform == 'darwin':
        import netifaces
        for id in netifaces.interfaces():
            intf = netifaces.ifaddresses(id)
            for key in intf:
                for it in intf[key]:
                    if 'addr' not in it or 'netmask' not in it:
                        continue
                    if ':' in it['addr']:
                        continue 
                    if_list.append({'id': id, 'ip': it['addr'], 'name': 'Loopback' if intf == 'lo' else 'Ethernet'})
    else:
        raise NotImplementedError('Unsupported system %s' % sys.platform)
    return if_list


def get_interface_ip(interface):
    if_list = get_interface_list()
    for it in if_list:
        if it['id'] == interface:
            return it['ip']


def main():
    print(BANNER)
    check_permission()
    parser = argparse.ArgumentParser(prog='rawdump',
                                     description='rawdump version %s' %
                                     VERSION)
    parser.add_argument('-i', '--interface', help='netcard interface')
    parser.add_argument('-p',
                        '--protocol',
                        help='protocol to capture',
                        default='ip')
    parser.add_argument(
        '-H',
        '--host',
        help='capture packet match source address or destination address',
        action='append')
    parser.add_argument(
        '-P',
        '--port',
        type=int,
        help='capture packet match source port or destination port',
        action='append')
    parser.add_argument('--keyword',
                        help='capture packet contains keyword',
                        action='append')
    parser.add_argument('-w',
                        '--file',
                        help='pcap file save path',
                        default='rawdump.pcap')

    args = parser.parse_args()

    interface = args.interface
    if_list = get_interface_list()
    print('[+] Following interfaces will be captured:')
    ip_list = []
    for intf in if_list:
        if not interface or intf['id'] == interface:
            print('[+]   %s - %s - %s' %
                  (intf['id'], intf['ip'], intf['name']))
            ip_list.append(intf['ip'] if sys.platform == 'win32' else intf['id'])

    if not ip_list:
        print('[+] Interface %s not found' % interface, file=sys.stderr)
        return -1
    print()
    protocol = args.protocol
    if protocol not in ('ip', 'tcp', 'udp', 'icmp'):
        print('[+] Invalid protocol %s' % protocol, file=sys.stderr)
        return -1
    hosts = args.host or []
    ports = args.port or []
    keywords = args.keyword or []
    filter_list = []
    filter_udp_port = os.environ.get(admin_shell.AdminShell.UDP_PORT_ENV)
    if filter_udp_port:
        filter_list.append({
            'protocol': 'udp',
            'host': '127.0.0.1',
            'port': int(filter_udp_port)
        })
    manager = handlers.PacketManager(protocol, hosts, ports, keywords,
                                     filter_list)
    manager.register_handler(handlers.StreamPacketHandler())
    if args.file:
        manager.register_handler(
            handlers.PcapPacketHandler(os.path.abspath(args.file)))

    socks = rawsocket.RawSockets(ip_list)
    while True:
        try:
            ip_packet = socks.read_packet()
            if ip_packet:
                manager.on_packet(ip_packet)
        except KeyboardInterrupt:
            manager.notify('unload')
            print('[+] Rawdump exit warmly...')
            break


if __name__ == '__main__':
    sys.exit(main())
