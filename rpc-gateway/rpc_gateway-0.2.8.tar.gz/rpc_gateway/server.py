from typing import Optional, Dict, Any, List, Union, ClassVar
import logging
import websockets
from inspect import isclass
from concurrent.futures import ThreadPoolExecutor
from rpc_gateway import errors, messages, gateway
from rpc_gateway.utils import await_sync

logger = logging.getLogger(__name__)


class Server(gateway.GatewayClient):
    def __init__(self, gateway_url: str = 'ws://localhost:8888', max_workers: int = 5, instances: Optional[Dict[str, Any]] = None):
        super().__init__(gateway_url)
        self.instances = {} if instances is None else instances
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    async def _on_start(self):
        await self._register_gateway_instances(list(self.instances.keys()))

    async def _register_gateway_instances(self, instances: List[str]):
        await self.websocket_connection.send_request(messages.Method.REGISTER, instances)

    def register(self, name: str, instance: Any) -> Any:
        if name in self.instances:
            raise errors.InstanceAlreadyRegisteredError(f'Instance already registered with name: {name}')

        self.instances[name] = instance

        return instance

    def _get_instance(self, instance_name: Union[type, str]):
        try:
            if isclass(instance_name):
                return self.instances[instance_name.__name__]

            return self.instances[instance_name]
        except KeyError:
            raise errors.InstanceNotFoundError(f'Instance not found: {instance_name}')

    def _get(self, instance_name: str, attribute_name: str) -> messages.Response:
        try:
            instance = self._get_instance(instance_name)
            data = getattr(instance, attribute_name)

            if callable(data):
                return messages.Response(status=messages.Status.METHOD)

            return messages.Response(data=data)
        except Exception as err:
            return messages.Response(status=messages.Status.ERROR, data=err)

    def _set(self, instance_name: str, attribute_name: str, value: Any) -> messages.Response:
        try:
            instance = self._get_instance(instance_name)
            setattr(instance, attribute_name, value)
            return messages.Response()
        except Exception as err:
            return messages.Response(status=messages.Status.ERROR, data=err)

    def _call(self, instance_name: str, attribute_name: str, args: List[Any], kwargs: Dict[str, Any]) -> messages.Response:
        try:
            instance = self._get_instance(instance_name)
            method = getattr(instance, attribute_name)
            data = method(*args, **kwargs)
            return messages.Response(data=data)
        except Exception as err:
            return messages.Response(status=messages.Status.ERROR, data=err)

    async def _run(self, *args: Any) -> Any:
        return await self.event_loop.run_in_executor(self.executor, *args)

    async def _handle_request(self, websocket_connection: websockets.WebSocketCommonProtocol, request: messages.Request) -> messages.Response:
        if request.method == 'get':
            return await self._run(self._get, request.data['instance'], request.data['attribute'])

        if request.method == 'set':
            return await self._run(self._set, request.data['instance'], request.data['attribute'], request.data['value'])

        if request.method == 'call':
            return await self._run(self._call, request.data['instance'], request.data['attribute'], request.data['args'], request.data['kwargs'])

        return messages.Response(status=messages.Status.ERROR, data=errors.InvalidMethodError(f'Invalid method: {request.method}'))


if __name__ == '__main__':
    import time
    logging.basicConfig(level=logging.INFO)

    class TestClass:
        foo = 'bar'

        def method(self):
            return 'baz'

        def sleep(self, duration):
            time.sleep(duration)

    server = Server()
    server.register('test', TestClass())
    server.start()