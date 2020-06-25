import socket
import os


def get_hostname():
    """
    Fetch the hostname of the machine
    """
    try:
        hostname = socket.gethostname()
    except:
        hostname = "Unknown"
    return hostname


def get_host():
    """
    Fetch the host of the machine
    """
    try:
        host = socket.gethostbyname(get_hostname())
    except:
        host = '-1'

    return host


def is_port_available(port: int, host="0.0.0.0"):
    """
    Check if a port is available
    """
    assert isinstance(port, int)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = True
    try:
        sock.bind((host, port))
    except:
        result = False
    sock.close()
    return result


def kill_port(port: int):
    """
    Kill a process which listening to a port
    """
    os.system('fuser -k {}/tcp'.format(port))
    pass
