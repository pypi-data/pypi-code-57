#  Copyright (c) 2020 Chris Stranex
#  See LICENSE for licencing information.
#
#  There is NO WARRANTY, to the extent permitted by law.
#

import time
from logging import basicConfig

from grpc import StatusCode

from proto.helloworld_pb2_grpc import HelloWorldServiceServicer
from proto.helloworld_pb2 import HelloWorldRequest, HelloWorldResponse
from alicorn import Alicorn, GrpcContext

basicConfig()

app = Alicorn()


@app.service
class HelloWorldService(HelloWorldServiceServicer):

    def SayHello(self, request: HelloWorldRequest, context: GrpcContext) -> HelloWorldResponse:
        return HelloWorldResponse(message=f"Hello {request.name}")

    def StreamHello(self, request_iterator, context):
        for request in request_iterator:
            time.sleep(1)
            yield HelloWorldResponse(message=f"Hello {request.name}")


if __name__ == '__main__':
    app.run()
