#  Copyright (c) 2020 Chris Stranex
#  See LICENSE for licencing information.
#
#  There is NO WARRANTY, to the extent permitted by law.
#

import logging
import grpc
from proto import helloworld_pb2_grpc, helloworld_pb2

logging.basicConfig()
logger = logging.getLogger(None)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    with grpc.insecure_channel('localhost:9000') as channel:
        service = helloworld_pb2_grpc.HelloWorldServiceStub(channel)

        print(service.SayHello(helloworld_pb2.HelloWorldRequest(name="Chris")))

        for response in service.StreamHello(iter([
            helloworld_pb2.HelloWorldRequest(name="Chris"),
            helloworld_pb2.HelloWorldRequest(name="David"),
            helloworld_pb2.HelloWorldRequest(name="Bradley"),
            helloworld_pb2.HelloWorldRequest(name="Ted"),
            helloworld_pb2.HelloWorldRequest(name="Jane"),
        ])):
            print(response.message)
