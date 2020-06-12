import enum
import socket
import time
import threading
from .bytecodes import *

class ProtocolType(enum.Enum):
    LD686 = 1,
    LD382A = 2,
    LD382 = 3

def send_data(data_bytes: bytes, protocol_type: ProtocolType, sock: socket.socket):
    if protocol_type == ProtocolType.LD382A or protocol_type == ProtocolType.LD686:
        data_bytes = bytes([*data_bytes, BYTE_LD686_EXTRA_MYSTERY])

    checksum = 0
    for byte in data_bytes:
        checksum += byte
    checksum = checksum & 0xFF

    total_bytes = bytes([*data_bytes, checksum])

    print(f"Send: {total_bytes.hex()}")
    sock.sendall(total_bytes)

    sock.settimeout(1)
    response = []
    while True:
        try:
            r = sock.recv(1)
            response.append(r[0])
            print(r.hex())
        except socket.timeout:
            break

    return response


def scan(seconds: int) -> dict:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(("0.0.0.0", 48899))
    sock.settimeout(1)

    results = {}

    stop_receiver = threading.Event()
    receiver = threading.Thread(target=receive, args=(sock, stop_receiver, results))
    receiver.start()

    for i in range(seconds):
        sock.sendto(b"HF-A11ASSISTHREAD", ("255.255.255.255", 48899))
        time.sleep(1)
    stop_receiver.set()
    receiver.join()

    return results


def receive(sock: socket.socket, stop: threading.Event, results: dict):
    while not stop.is_set():
        try:
            data, (ip, port) = sock.recvfrom(200)
            if data == b"HF-A11ASSISTHREAD":
                continue
            if ip not in results:
                results[ip] = data
        except socket.timeout:
            continue