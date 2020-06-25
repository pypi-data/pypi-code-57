import socket
import threading

from litenet.utils import to_liteaddr


class LiteNetServer:
    def __init__(self, ip, port=5050, header=64, encoding="utf-8"):
        self.ip, self.port = ip, port

        self.header, self.encoding = header, encoding

        self._close_msg = "[CLOSE]"

        self.clients = {}

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self._stopped = False

    def start(self):
        threading.Thread(target=self._start).start()

    def _start(self):
        self.server.bind((self.ip, self.port))
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.listen()

        print(f"LiteNet Server Listening on {self.ip}:{self.port}")

        while not self._stopped:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[NEW CONNECTION] {addr}")

        self.server.close()

    def handle_client(self, conn, addr):
        self.clients[addr] = {
            "alias": to_liteaddr(addr),
            "connection": conn,
            "alive": True
        }

        while self.clients[addr]["alive"]:
            msg_length = self.clients[addr]["connection"].recv(self.header)
            if msg_length:
                msg_length = int(msg_length.decode(self.encoding))

                msg = self.clients[addr]["connection"].recv(msg_length).decode(self.encoding)

                if msg == self._close_msg:
                    break

                print(addr[0] + ":" + str(addr[1]), ">>", msg)

                msg = str(f"{addr[0] + ':' + str(addr[1])} >> {msg}")

                for client in self.clients.keys():
                    if client != addr:
                        self.clients.get(client)["connection"].send(
                            msg.encode(self.encoding) + b" " * (self.header - len(msg.encode(self.encoding)))
                        )

                        self.clients.get(client)["connection"].send(
                            msg.encode(self.encoding)
                        )

        conn.close()
        self.close_client(addr)

    def close_client(self, addr):
        if addr in self.clients:
            self.clients[addr]["alive"] = False
        else:
            raise socket.error(f"{addr} isn't connected to the server.")

    @property
    def active_client_count(self):
        return threading.activeCount()

    def stop(self):
        self._stopped = True
