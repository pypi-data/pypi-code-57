#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = "HeliantHuS"
__version__ = "1.0"
"""
@ Author: HeliantHuS
@ Codes are far away from bugs with the animal protecting
@ Time:  2019/7/13
@ FileName: port_scanner.py
"""
import sys
import queue
import socket
import threading

q = queue.Queue()

class PortScanner(threading.Thread):
    def __init__(self, host):
        super().__init__()
        self.host: str = host

    def run(self) -> None:
        while True:
            port = q.get()
            self.scanner(port)
            q.task_done()

    def scanner(self, port):
        conn = socket.socket()
        try:
            conn.connect((self.host, port))
            print(f"[+] {port} is Open")

        except:
            pass


if __name__ == '__main__':
    # ...py www.baidu.com 1 1000 200       扫描baidu, 从1端口到1000端口 启动200个线程
    host = sys.argv[1]
    ip = socket.gethostbyname(host)
    startPort = sys.argv[2]
    endPort = sys.argv[3]
    threadNum = sys.argv[4]

    for i in range(int(threadNum)):
        t = PortScanner(ip)
        t.setDaemon(True)
        t.start()

    for i in range(int(startPort), int(endPort)):
        q.put(i)

    q.join()