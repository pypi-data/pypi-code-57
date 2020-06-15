""" connection module.

sources:
    - https://docs.python.org/3/howto/sockets.html
"""

import socket

get_hostname = socket.gethostname


def get_host_ip() -> str:
    return socket.gethostbyname(get_hostname())


def tcp_connect_to(hostname: str, port: int) -> socket.socket:
    local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    local_socket.connect((hostname, port))
    return local_socket


def tcp_serve(hostname: str, port: int, on_receive, on_close=None, persist: bool = True):
    from mindstone.embedded.reporting import display
    try:
        # start a persistent tcp connection that will only accept one
        # client connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as local_socket:
            # 1. start the tcp server
            display("starting server ({}, {})".format(hostname, port))
            local_socket.bind((hostname, port))
            # 2. listen for connections
            display("listening...")
            local_socket.listen()
            # 3. accept connection
            remote_socket, remote_address = local_socket.accept()
            display("connected by {}".format(remote_address))
            # event loop
            while True:
                # 4. receive data
                received_bytes = remote_socket.recv(1024)
                if received_bytes == b'':
                    # end this connection so that a new one can be started
                    raise ConnectionAbortedError
                # 5. process data and send request
                send_bytes = on_receive(received_bytes)
                remote_socket.sendall(send_bytes)
    except ConnectionResetError and ConnectionAbortedError:
        print("Socket connection with {} broken.".format(remote_address))
        if persist:
            tcp_serve(hostname, port, on_receive, on_close)
    if callable(on_close):
        on_close()
