#!/usr/bin/env python3

from ..apis.base_api import BaseApi, DEFAULT_TIMEOUT
from ..apis.cmdid import PCProgramCmdId
from ..pb2.codemao_revertorigin_pb2 import RevertOriginRequest, RevertOriginResponse
from ..pb2.pccodemao_disconnection_pb2 import DisconnectionRequest, DisconnectionResponse
from ..pb2.pccodemao_getappversion_pb2 import GetAppVersionRequest, GetAppVersionResponse
from ..pb2.pccodemao_message_pb2 import Message


class StartRunProgram(BaseApi):
    """
    进入编程模式
    """

    def __init__(self, is_serial: bool = True, ):
        self.__isSerial = is_serial

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = GetAppVersionRequest()

        cmd_id = PCProgramCmdId.GET_ROBOT_VERSION_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = GetAppVersionResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class StopRunProgram(BaseApi):
    """
    退出编程模式
    """

    def __init__(self, is_serial: bool = True, ):
        self.__isSerial = is_serial

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = DisconnectionRequest()

        cmd_id = PCProgramCmdId.DISCONNECTION_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = DisconnectionResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class RevertOrigin(BaseApi):
    """
    复位
    """

    def __init__(self, is_serial: bool = True):
        self.__isSerial = is_serial

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = RevertOriginRequest()

        cmd_id = PCProgramCmdId.REVERT_ORIGIN_REQUEST.value

        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = RevertOriginResponse()
            response.ParseFromString(data)
            return response
        else:
            return None
