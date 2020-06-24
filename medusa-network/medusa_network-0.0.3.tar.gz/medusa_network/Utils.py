import socket


def get_random_port():
    with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as sock:
        sock.bind(("::1", 0))
        sock.listen()
        return sock.getsockname()[1]
