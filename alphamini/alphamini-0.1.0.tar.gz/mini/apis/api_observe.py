#!/usr/bin/env python3

# 每种传感器做一个单例对象进行监听

import enum
import asyncio

from ..apis.base_api import BaseEventApi, BaseApiNoNeedResponse
from ..apis.cmdid import PCProgramCmdId
from ..pb2.codemao_facedetecttask_pb2 import FaceDetectTaskRequest, FaceDetectTaskResponse
from ..pb2.codemao_facerecognisetask_pb2 import FaceRecogniseTaskRequest, FaceRecogniseTaskResponse
from ..pb2.codemao_observefallclimb_pb2 import ObserveFallClimbRequest, ObserveFallClimbResponse
from ..pb2.codemao_observeheadracket_pb2 import ObserveHeadRacketRequest, ObserveHeadRacketResponse
from ..pb2.codemao_observeinfrareddistance_pb2 import ObserveInfraredDistanceRequest, ObserveInfraredDistanceResponse
from ..pb2.codemao_speechrecognise_pb2 import SpeechRecogniseRequest, SpeechRecogniseResponse
from ..pb2.codemao_stopspeechrecognise_pb2 import StopSpeechRecogniseRequest, StopSpeechRecogniseResponse
from ..pb2.pccodemao_message_pb2 import Message


class ObserveSpeechRecognise(BaseEventApi):
    """
    监听语音识别
    """

    async def execute(self):
        pass

    def __init__(self):

        cmd_id = PCProgramCmdId.SPEECH_RECOGNISE.value

        message = SpeechRecogniseRequest()

        BaseEventApi.__init__(self, cmd_id=cmd_id, message=message)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = SpeechRecogniseResponse()
            response.ParseFromString(data)
            return response
        else:
            return None

    def stop(self):

        asyncio.create_task(StopSpeechRecognise().execute())

        super().stop()


class StopSpeechRecognise(BaseApiNoNeedResponse):
    """
    停止语音识别
    """

    async def execute(self):

        request = StopSpeechRecogniseRequest()

        cmd_id = PCProgramCmdId.STOP_SPEECH_RECOGNISE_REQUEST.value

        return await self.send(cmd_id, request)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = StopSpeechRecogniseResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class ObserveFaceDetect(BaseEventApi):
    """
    监听人脸检测（个数）
    """

    async def execute(self):
        pass

    def __init__(self):

        cmd_id = PCProgramCmdId.FACE_DETECT_TASK_REQUEST.value

        request = FaceDetectTaskRequest()

        # 单次侦测超时时间
        request.timeout = 1000

        # 侦测间隔时间
        request.period = 1000

        # 任务延时时间
        request.delay = 0

        # 检测开关
        request.switch = True

        BaseEventApi.__init__(self, cmd_id=cmd_id, message=request)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = FaceDetectTaskResponse()
            response.ParseFromString(data)
            return response
        else:
            return None

    def stop(self):

        asyncio.create_task(StopFaceDetect().execute())

        super().stop()


class StopFaceDetect(BaseApiNoNeedResponse):
    """
    停止人脸检测（个数）
    """

    async def execute(self):

        request = FaceDetectTaskRequest()

        # 检测开关
        request.switch = False

        cmd_id = PCProgramCmdId.FACE_DETECT_TASK_REQUEST.value

        return await self.send(cmd_id, request)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = FaceDetectTaskResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class ObserveFaceRecognise(BaseEventApi):
    """
    监听人脸识别
    """

    async def execute(self):
        pass

    def __init__(self):

        cmd_id = PCProgramCmdId.FACE_RECOGNISE_TASK_REQUEST.value

        request = FaceRecogniseTaskRequest()

        # 单次侦测超时时间
        request.timeout = 1000

        # 侦测间隔时间
        request.period = 1000

        # 任务延时时间
        request.delay = 0

        # 检测开关
        request.switch = True

        BaseEventApi.__init__(self, cmd_id=cmd_id, message=request)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = FaceRecogniseTaskResponse()
            response.ParseFromString(data)
            return response
        else:
            return None

    def stop(self):

        asyncio.create_task(StopFaceRecognise().execute())

        super().stop()


class StopFaceRecognise(BaseApiNoNeedResponse):
    """
    停止人脸识别
    """

    async def execute(self):

        request = FaceRecogniseTaskRequest()

        # 检测开关
        request.switch = False

        cmd_id = PCProgramCmdId.FACE_RECOGNISE_TASK_REQUEST.value

        return await self.send(cmd_id, request)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = FaceRecogniseTaskResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class ObserveInfraredDistance(BaseEventApi):
    """
    监听红外距离
    """

    async def execute(self):
        pass

    def __init__(self):

        cmd_id = PCProgramCmdId.SUBSCRIBE_INFRARED_DISTANCE_REQUEST.value

        request = ObserveInfraredDistanceRequest()

        # 检测周期
        request.samplingPeriod = 1000

        # 检测开关
        request.isSubscribe = True

        BaseEventApi.__init__(self, cmd_id=cmd_id, message=request)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = ObserveInfraredDistanceResponse()
            response.ParseFromString(data)
            return response
        else:
            return None

    def stop(self):

        asyncio.create_task(StopObserveInfraredDistance().execute())

        super().stop()


class StopObserveInfraredDistance(BaseApiNoNeedResponse):
    """
    停止监听红外距离
    """

    async def execute(self):

        request = ObserveInfraredDistanceRequest()

        # 检测开关
        request.isSubscribe = False

        cmd_id = PCProgramCmdId.FACE_RECOGNISE_TASK_REQUEST.value

        return await self.send(cmd_id, request)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = ObserveInfraredDistanceResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


@enum.unique
class RobotPosture(enum.Enum):
    STAND = 1  # 站立
    SPLITS_LEFT = 2  # 左劈叉
    SPLITS_RIGHT = 3  # 右劈叉
    SIT_DOWN = 4  # 坐下
    SQUAT_DOWN = 5  # 蹲下
    KNEELING = 6  # 跪下
    LYING = 7  # 侧躺
    LYING_DOWN = 8  # 平躺
    SPLITS_LEFT_1 = 9  # 左劈叉1
    SPLITS_RIGHT_2 = 10  # 右劈叉2
    BEND = 11  # 弯腰


class ObserveRobotPosture(BaseEventApi):
    """
    监听机器人姿态
    姿态值对应：
    STAND = 1; //站立
    SPLITS_LEFT = 2; //左劈叉
    SPLITS_RIGHT = 3; //右劈叉
    SITDOWN = 4; //坐下
    SQUATDOWN = 5; //蹲下
    KNEELING = 6; //跪下
    LYING = 7; //侧躺
    LYINGDOWN = 8; //平躺
    SPLITS_LEFT_1 = 9; //左劈叉1
    SPLITS_RIGHT_2 = 10;//右劈叉2
    BEND = 11;//弯腰
    """

    async def execute(self):
        pass

    def __init__(self):

        cmd_id = PCProgramCmdId.SUBSCRIBE_ROBOT_POSTURE_REQUEST.value

        request = ObserveFallClimbRequest()

        # 检测开关
        request.isSubscribe = True

        BaseEventApi.__init__(self, cmd_id=cmd_id, message=request)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = ObserveFallClimbResponse()
            response.ParseFromString(data)
            return response
        else:
            return None

    def stop(self):

        asyncio.create_task(StopObserveRobotPosture().execute())

        super().stop()


class StopObserveRobotPosture(BaseApiNoNeedResponse):
    """
    停止监听机器人姿态
    """

    async def execute(self):

        request = ObserveFallClimbRequest()

        # 检测开关
        request.isSubscribe = False

        cmd_id = PCProgramCmdId.SUBSCRIBE_ROBOT_POSTURE_REQUEST.value

        return await self.send(cmd_id, request)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = ObserveFallClimbResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


@enum.unique
class HeadRacketType(enum.Enum):
    SINGLE_CLICK = 1  # 单击
    LONG_PRESS = 2  # 长按
    DOUBLE_CLICK = 3  # 双击


class ObserveHeadRacket(BaseEventApi):
    """
    监听拍头事件
    """

    async def execute(self):
        pass

    def __init__(self):

        cmd_id = PCProgramCmdId.SUBSCRIBE_HEAD_RACKET_REQUEST.value

        message = ObserveHeadRacketRequest()

        # 检测开关
        message.isSubscribe = True

        BaseEventApi.__init__(self, cmd_id=cmd_id, message=message)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = ObserveHeadRacketResponse()
            response.ParseFromString(data)
            return response
        else:
            return None

    def stop(self):

        asyncio.create_task(StopObserveHeadRacket().execute())

        super().stop()


class StopObserveHeadRacket(BaseApiNoNeedResponse):
    """
    停止监听拍头事件
    """

    async def execute(self):

        request = ObserveHeadRacketRequest()

        # 检测开关
        request.isSubscribe = False

        cmd_id = PCProgramCmdId.SUBSCRIBE_ROBOT_POSTURE_REQUEST.value

        return await self.send(cmd_id, request)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = ObserveHeadRacketResponse()
            response.ParseFromString(data)
            return response
        else:
            return None
