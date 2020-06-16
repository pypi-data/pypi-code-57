#!/usr/bin/env python3

import enum

from ..apis.base_api import BaseApi, DEFAULT_TIMEOUT
from ..apis.cmdid import PCProgramCmdId
from ..pb2.codemao_controlbehavior_pb2 import ControlBehaviorRequest, ControlBehaviorResponse
from ..pb2.codemao_controlmouthlamp_pb2 import ControlMouthRequest, ControlMouthResponse
from ..pb2.codemao_playexpression_pb2 import PlayExpressionRequest, PlayExpressionResponse
from ..pb2.codemao_setmouthlamp_pb2 import SetMouthLampRequest, SetMouthLampResponse
from ..pb2.pccodemao_message_pb2 import Message


@enum.unique
class RobotExpressionType(enum.Enum):
    INNER = 0  # 内置表情
    CUSTOM = 1  # 自定义表情


class PlayExpression(BaseApi):
    """
    播放表情
    express_name:表情名称
    express_type: 表情类型，默认内置表情
    """

    def __init__(self, is_serial: bool = True, express_name: str = None,
                 express_type: RobotExpressionType = RobotExpressionType.INNER):
        assert express_name is not None, 'PlayExpression expressName could not be None'
        self.__isSerial = is_serial
        self.__expressName = express_name
        self.__dirType = express_type.value

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = PlayExpressionRequest()
        request.expressName = self.__expressName
        request.dirType = self.__dirType

        cmd_id: int = PCProgramCmdId.PLAY_EXPRESSION_REQUEST.value

        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = PlayExpressionResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


@enum.unique
class RobotBehaviorControlType(enum.Enum):
    START = 1  # 开始
    STOP = 0  # 停止


class ControlBehavior(BaseApi):
    """
    控制表现力
    name:表现力名称
    control_type: 控制类型，默认为开始
    """

    def __init__(self, is_serial: bool = True, name: str = None,
                 control_type: RobotBehaviorControlType = RobotBehaviorControlType.START):
        assert name is not None and len(name), 'ControlBehavior name should be available'
        self.__isSerial = is_serial
        self.__name = name
        self.__eventType = control_type.value

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = ControlBehaviorRequest()
        request.name = self.__name
        request.eventType = self.__eventType

        cmd_id = PCProgramCmdId.CONTROL_BEHAVIOR_REQUEST.value

        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = ControlBehaviorResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


@enum.unique
class MouthLampColor(enum.Enum):
    RED = 1  # 红色
    GREEN = 2  # 绿色
    BLUE = 3  # 蓝色


class SetMouthLamp(BaseApi):
    """
    设置嘴巴灯
    TODO:各参数的范围和意义
    color：嘴巴灯颜色
    """

    def __init__(self, is_serial: bool = True, model: int = 0, color: MouthLampColor = MouthLampColor.RED,
                 duration: int = 0,
                 breath_duration: int = 0):

        self.__isSerial = is_serial
        self.__model = model
        self.__color = color.value
        self.__duration = duration
        self.__breathDuration = breath_duration

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = SetMouthLampRequest()
        request.model = self.__model
        request.color = self.__color
        request.duration = self.__duration
        request.breathDuration = self.__breathDuration

        cmd_id = PCProgramCmdId.SET_MOUTH_LAMP_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = SetMouthLampResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class ControlMouthLamp(BaseApi):
    """
    控制嘴巴灯开关
    is_open：默认true，开启嘴巴灯
    """

    def __init__(self, is_serial: bool = True, is_open: bool = True):

        self.__isSerial = is_serial
        self.__isOpen = is_open

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = ControlMouthRequest()
        request.isOpen = self.__isOpen

        cmd_id = PCProgramCmdId.SWITCH_MOUTH_LAMP_REQUEST.value

        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = ControlMouthResponse()
            response.ParseFromString(data)
            return response
        else:
            return None
