import time
import socket
import sys
import select

class TCPConn:
    def __init__(self, ConnTarget):
        #IP and port
        #9760 is the default address of modules -
        #In Qis do a '$list details' and it will show you ports
        TCP_PORT = 9760
        self.ConnTarget = ConnTarget
        #Creates connection socket
        self.Connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Sets buffer size
        self.BufferSize = 4096
        #Opens the ocnnection
        self.Connection.connect((self.ConnTarget, TCP_PORT))

    def close(self):
        self.Connection.close()
        return True

    def sendCommand(self, Command, readUntilCursor=True, expectedResponse=True):
        time.sleep(0.015)
        # Prepares the message to be sent
        MESSAGE_ready = (chr(len(Command + "\r\n")) + chr(0) + Command + "\r\n").encode()

        # Sends the message
        self.Connection.send(MESSAGE_ready)

        if expectedResponse == True:

            if sys.version_info >= (3, 0):  # Python3
                # Receives the raw response
                packet = self.Connection.recv(self.BufferSize)
                # the first two bytes are the size of the message
                messageLength = packet[0] + packet[1] * 256
                data = packet[2:]
                # the rest of the package is part of the message
                while (len(data) < messageLength):
                    packet = self.Connection.recv(self.BufferSize)
                    data = data + packet

                data = data.decode()
                data = data.strip('> \t\n\r')
            else:  # python2
                # Receives raw the answer
                data_raw = self.Connection.recv(self.BufferSize)

                # Decodes data and ignores the first character
                data = data_raw.decode("ISO-8859-1")[1:-3]

            return data
        else:
            return None

