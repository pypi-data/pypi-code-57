class Stub:
    def __init__(self, server, queue_name):
        self._server = server
        self._queue_name = queue_name

    def _send(self, handler, content):
        self._server.send_message(self._queue_name, handler, content)
