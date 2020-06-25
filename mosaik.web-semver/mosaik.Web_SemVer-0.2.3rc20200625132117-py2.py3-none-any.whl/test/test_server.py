from mosaik_web.server import Server


class MockEnvironment(object):
    @staticmethod
    def event():
        pass

    @staticmethod
    def process(update):
        pass


def test_server():
    # Mock
    environment = MockEnvironment()
    server_sock = 0

    # Test
    server = Server(
        env=environment,
        server_sock=server_sock,
    )

    # Assert
    assert server
