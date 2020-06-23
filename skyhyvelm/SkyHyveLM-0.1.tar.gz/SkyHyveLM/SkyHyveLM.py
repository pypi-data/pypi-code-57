class LM:

    def __init__(self, socket_connection, header_size=16, b64=False):

        self.socket_connection = socket_connection

    def send(self, data):

        data_length = len(data)
        message_length = data_length + self.HEADER_SIZE

        message_length_length = len(str(message_length))
        preceeding_zeros_count = self.HEADER_SIZE - message_length_length
        header = ((preceeding_zeros_count * '0') + str(message_length)).encode()

        message = header + data

        self.socket_connection.send(message)

    def recv(self, buffer_size):

        message_length = 0
        message = b''

        message_segment = self.socket_connection.recv(buffer_size)
        message_segment_length = len(message_segment)
        message_length = message_length + message_segment_length

        header = message_segment[:self.HEADER_SIZE]
        data = message_segment[self.HEADER_SIZE:]
        header = header.decode()
        expected_message_length = int(header)

        message = message + data
        while message_length < expected_message_length:
            message_segment = self.socket_connection.recv(buffer_size)
            message_segment_length = len(message_segment)
            message_length = message_length + message_segment_length
            message = message + message_segment

        return message
