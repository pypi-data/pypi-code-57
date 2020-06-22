# -*- coding: utf-8 -*-

## Connect to server using socket from stdlib

import socket

# Socket server data:
gnc_socket = './gnc.socket'

# Connect to socket

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Connect to socket

sock.connect(gnc_socket)

# Set timeout

timeout = 1
sock.settimeout(timeout)

# The client should read ever the socket

# While

# Read from input

# Send to socket

# Read from socket
sock.connect(gnc_socket)
