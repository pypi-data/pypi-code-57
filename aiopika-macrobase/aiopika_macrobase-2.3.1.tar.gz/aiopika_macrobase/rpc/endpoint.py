from sentry_sdk import capture_exception

from .request import RPCRequest, RPCResponse, RPCMessageType
from ..endpoint import AiopikaEndpoint
from ..result import AiopikaResult

from aio_pika import IncomingMessage

from structlog import get_logger
log = get_logger('AiopikaRPCEndpoint')


class AiopikaRPCEndpoint(AiopikaEndpoint):
    """
    RPC implementation for RPC processing
    """

    async def handle(self, driver, message: IncomingMessage, data, *args, **kwargs) -> AiopikaResult:
        """
        Handle method for process incoming message

        Args:
            driver: Aiopika Macrobase driver
            message (IncomingMessage): Incoming message from driver processing
            data: Deserialized payload from Incoming Message
            *args: Additional arguments
            **kwargs: Additional arguments with keys

        Returns:
            AiopikaResult: Aiopika result action or None  (if return None then driver ack message).
        """
        identifier = kwargs.get('identifier', None)
        request = RPCRequest(message, identifier, payload=data)

        try:
            response = await self.method(driver, request, request.payload, *args, **kwargs)
        except Exception as e:
            capture_exception(e)
            response = RPCResponse(e, type=RPCMessageType.error)

        return response.get_result(message.correlation_id, identifier, message.expiration)

    async def method(self, driver, request: RPCRequest, data, *args, **kwargs) -> RPCResponse:
        return RPCResponse()


class HealthEndpoint(AiopikaRPCEndpoint):

    async def method(self, driver, request: RPCRequest, data, *args, **kwargs) -> RPCResponse:
        log.info('Health')
        return RPCResponse(payload={'status': 'health', 'value': 'ok'})
