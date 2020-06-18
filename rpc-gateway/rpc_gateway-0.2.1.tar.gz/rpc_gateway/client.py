from typing import Any, Iterable, Optional, List, Dict, Callable
import time
import logging
import asyncio
from rpc_gateway import errors, messages, gateway


class Client(gateway.GatewayClient):
    def get_instance(self, instance_name) -> Any:
        if not self.connected:
            self.start(wait=False)
            time.sleep(1)

        if not self.instance_available(instance_name):
            raise errors.InstanceNotFoundError(f'Instance not found: {instance_name}')

        client = self

        class _Proxy:
            def __dir__(self) -> Iterable[str]:
                return client.call(instance_name, '__dir__')

            def __getattr__(self, item):
                return client.get(instance_name, item)

            def __setattr__(self, key, value):
                return client.set(instance_name, key, value)

            def __repr__(self):
                return client.call(instance_name, '__repr__')

            def __str__(self):
                return client.call(instance_name, '__str__')

        return _Proxy()

    def proxy_method(self, instance_name: str, method_name: str) -> Callable:
        def _proxy_method(*args, **kwargs):
            return self.call(instance_name, method_name, args, kwargs)

        return _proxy_method

    def instance_available(self, instance_name: str) -> bool:
        response = self.websocket_connection.send_request_sync(messages.Method.AVAILABLE, instance_name)
        return response.data

    def call(self, instance_name: str, method_name: str, args: Optional[Iterable[Any]] = None, kwargs: Optional[Dict[str, Any]] = None) -> Any:
        response = self.websocket_connection.send_request_sync(messages.Method.CALL, {
            'instance': instance_name,
            'attribute': method_name,
            'args': args or [],
            'kwargs': kwargs or {}
        })

        return response.data

    def get(self, instance_name: str, attribute_name: str) -> Any:
        response = self.websocket_connection.send_request_sync(messages.Method.GET, {
            'instance': instance_name,
            'attribute': attribute_name
        })

        if response.status == messages.Status.METHOD:
            return self.proxy_method(instance_name, attribute_name)

        return response.data

    def set(self, instance_name: str, attribute_name: str, value: Any) -> Any:
        self.websocket_connection.send_request_sync(messages.Method.SET, {
            'instance': instance_name,
            'attribute': attribute_name,
            'value': value
        })

        return value


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    class TestClass:
        foo = 'bar'

        def method(self):
            return 'baz'

    client = Client()
    test: TestClass = client.get_instance('test')
    print(test.foo)
    # print(test.method())
    # print(test)
