from interfaceTest.ClientAbc import clientAbc
from interfaceTest.TestConf import testConf
import socket
import struct

class TcpClient(clientAbc):
    def __init__(self, ):
        super(TcpClient, self).__init__()
        self.s = self.newTcpConnection()

    def newTcpConnection(self):
        conf = testConf()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((conf.host, conf.port))
        return s

    # def

    def sendRequest(self, reqObj, respObj):
        package_byte = reqObj.SerializeToString()
        package_len = len(package_byte)
        bytes = struct.pack("iH{}p".format(package_len), package_len, package_byte)
        print(bytes)
        print(struct.unpack("iH{}p".format(package_len), bytes))
        self.s.send(reqObj)
        self.s.recv(1024)

if __name__ == "__main__":
    a = TcpClient()
    print(a.s)