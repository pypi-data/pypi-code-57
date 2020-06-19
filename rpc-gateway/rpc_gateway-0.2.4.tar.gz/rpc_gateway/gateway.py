from typing import Optional, List, Dict
import logging
import time
import asyncio
import websockets
from rpc_gateway import messages, errors
from rpc_gateway.websocket_connection import WebsocketConnection
from rpc_gateway.utils import await_sync

logger = logging.getLogger(__name__)


class GatewayConnection:
    def __init__(self, gateway: 'Gateway', connection: websockets.WebSocketServerProtocol):
        self.gateway = gateway
        self.connection = connection
        self.message_pump = WebsocketConnection(connection, lambda message: gateway.handle_request(self, message))
        self.instances: List[str] = []

    async def start(self):
        await self.message_pump.start()

    async def stop(self):
        await self.message_pump.stop()

    def register_instances(self, instances):
        self.instances = list(set(*self.instances, *instances))


class Gateway:
    SERVER_MESSAGES = (messages.Method.GET, messages.Method.SET, messages.Method.CALL)

    def __init__(self, host: str = 'localhost', port: int = 8888):
        self.host = host
        self.port = port
        self.logger = logger.getChild(self.__class__.__name__)
        self.websocket_connections: List[WebsocketConnection] = []
        self.websocket: Optional[websockets.WebSocketServer] = None
        self.event_loop = asyncio.get_event_loop()
        self.instances: Dict[str, WebsocketConnection] = {}
        self.websocket_instances: Dict[WebsocketConnection, List[str]] = {}

    def start(self, wait = True):
        await_sync(self._start(wait), self.event_loop)

    async def _start(self, wait = True):
        self.logger.info(f'Starting on ws://{self.host}:{self.port}')
        self.websocket = await websockets.serve(self.on_connection, self.host, self.port)

        if wait:
            await self._wait()

    def wait(self):
        await_sync(self._wait(), self.event_loop)

    async def _wait(self):
        if self.websocket is not None:
            await self.websocket.wait_closed()

        self.logger.info(f'Done')

    def stop(self):
        await_sync(self._stop(), self.event_loop)

    async def _stop(self):
        await asyncio.gather(*[websocket_connection.stop() for w, websocket_connection in self.websocket_connections.items()])
        self.websocket.close()

    async def on_connection(self, connection: websockets.WebSocketServerProtocol, path: str):
        self.logger.info(f'New connection from {connection.remote_address} path: {path}')
        websocket_connection = WebsocketConnection(connection, request_handler=self.handle_request, close_handler=self.handle_close)
        self.websocket_connections.append(websocket_connection)

        await websocket_connection.start()

        for instance in self.websocket_instances[websocket_connection]:
            self.instances.pop(instance)
        self.websocket_connections.remove(websocket_connection)

        self.logger.info(f'Connection from {connection.remote_address} closed')

    #
    # Request Handlers
    #

    async def handle_forward_request(self, websocket_connection: WebsocketConnection, request: messages.Request) -> messages.Response:
        self.logger.info(f'Forwarding request to server: {request}')
        instance = request.data['instance']

        if instance not in self.instances:
            return messages.Response(status=messages.Status.ERROR, data=errors.InstanceNotFoundError(f'Instance not found: {instance}'))

        server = self.instances[request.data['instance']]
        response = await server.request(request, raise_error=False)
        self.logger.info(f'Forwarding response to client: {response}')

        return response

    async def handle_available_request(self, websocket_connection: WebsocketConnection, request: messages.Request) -> messages.Response:
        available = request.data in self.instances
        return messages.Response(data=available)

    async def handle_register_request(self, websocket_connection: WebsocketConnection, request: messages.Request) -> messages.Response:
        self.logger.info(f'Registering instances: {request.data}')
        self.websocket_instances[websocket_connection] = self.websocket_instances.get(websocket_connection, []) + request.data
        for instance_name in request.data:
            self.instances[instance_name] = websocket_connection

        return messages.Response()

    # this is called by the GatewayConnection MessagePump when a new request is received
    async def handle_request(self, websocket_connection: WebsocketConnection, request: messages.Request) -> messages.Response:
        if request.method in self.SERVER_MESSAGES:
            return await self.handle_forward_request(websocket_connection, request)

        if request.method == messages.Method.AVAILABLE:
            return await self.handle_available_request(websocket_connection, request)

        if request.method == messages.Method.REGISTER:
            return await self.handle_register_request(websocket_connection, request)

        return messages.Response(status=messages.Status.ERROR, data=errors.InvalidMethodError(f'Invalid method: {request.method}'))

    async def handle_close(self, websocket_connection: WebsocketConnection):
        if websocket_connection in self.websocket_instances:
            # remove registered instances
            for instance_name in self.websocket_instances[websocket_connection]:
                self.instances.pop(instance_name)

            self.websocket_instances.pop(websocket_connection)

        # send an error response for any in-progress requests
        for request_id, response_queue in websocket_connection.receive_queues.items():
            await response_queue.put(messages.Response(status=messages.Status.ERROR, data=errors.ServerConnectionLostError(f'Server connection lost')))


class GatewayClient:
    def __init__(self, gateway_url: str = 'ws://localhost:8888'):
        self.logger = logger.getChild(self.__class__.__name__)
        self.gateway_url = gateway_url
        self.websocket_connection = WebsocketConnection(request_handler=self._handle_request, close_handler=self._handle_close)
        self.event_loop = asyncio.get_event_loop()
        self.connect_retry_timeout = 2.0

    @property
    def connected(self) -> bool:
        return self.websocket_connection.connection is not None

    async def _connect(self):
        while True:
            try:
                self.logger.info(f'Connecting to {self.gateway_url}')
                self.connection = await websockets.connect(self.gateway_url)
                return
            except OSError:
                self.logger.warning(f'Error connecting to {self.gateway_url}, retrying in {self.connect_retry_timeout} seconds')
                time.sleep(self.connect_retry_timeout)

    def start(self, wait=True):
        await_sync(self._start(wait), self.event_loop)

    async def _start(self, wait=True):
        await self._connect()
        await self.websocket_connection.start(wait=False, connection=self.connection)
        await self._on_start()

        if wait:
            await self._wait()

    def wait(self):
        await_sync(self._wait(), self.event_loop)

    async def _wait(self):
        await self.websocket_connection.wait()

    async def _on_start(self):
        pass

    def stop(self):
        await_sync(self._stop(), self.event_loop)

    async def _stop(self):
        await self.websocket_connection.stop()

    async def _handle_request(self, websocket_connection: WebsocketConnection, request: messages.Request) -> messages.Response:
        pass

    async def _handle_close(self, websocket_connection: WebsocketConnection):
        await self._connect()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    gateway = Gateway()
    gateway.start()