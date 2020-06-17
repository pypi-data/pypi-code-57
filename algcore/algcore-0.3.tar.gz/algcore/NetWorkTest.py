#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Version : $Id$

import socket

def isNetOK(testserver):
    s=socket.socket()
    s.settimeout(3)
    try:
        status = s.connect_ex(testserver)
        if status == 0:
            s.close()
            return True
        else:
            return False
    except Exception as e:
        return False

def isNetChainOK(testserver=('www.baidu.com',443)):
    isOK = isNetOK(testserver)
    return isOK
    

def isNetUSAOK(testserver=('www.google.com',443)):
    isOK = isNetOK(testserver)
    return isOK
    
def isNetYouTubeOK(testserver=('www.youtube.com',443)):
    isOK = isNetOK(testserver)
    return isOK

def main():

    chinanet = isNetChainOK()
    print(chinanet)
    usanet = isNetUSAOK()
    print(usanet)
    youtubenet = isNetYouTubeOK()
    print(youtubenet)
    

if __name__ == '__main__':
    main()
