import asyncssh

class MySSHTCPSession(asyncssh.SSHTCPSession):
    def connection_made(self, chan):
        self._chan = chan

    def data_received(self, data, datatype):
        self._chan.write(data)


class KubeForwardingTCP(asyncssh.SSHTCPSession):
    def connection_made(self, chan):
        self._chan = chan

    def data_received(self, data, datatype):

