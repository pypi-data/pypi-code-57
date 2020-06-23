#  Copyright (c) 2020 Chris Stranex
#  See LICENSE for licencing information.
#
#  There is NO WARRANTY, to the extent permitted by law.
#
import time
from logging import basicConfig
from proto.helloworld_pb2 import HelloWorldRequest, HelloWorldResponse
from alicorn import Alicorn, GrpcContext

basicConfig()

app = Alicorn()
app.debug = True


@app.rpc_service("HelloWorldService")
class HelloWorldService:

    @app.rpc_method_unary(HelloWorldRequest, HelloWorldResponse)
    def SayHello(self, request: HelloWorldRequest, context: GrpcContext):
        return HelloWorldResponse(message=f"Hello {request.name}")

    @app.rpc_method_stream(HelloWorldRequest, HelloWorldResponse)
    def StreamHello(self, request_iterator: HelloWorldRequest, context: GrpcContext):
        for request in request_iterator:
            time.sleep(1)
            yield HelloWorldResponse(message=f"Hello {request.name}")


if __name__ == '__main__':
    app.run()
