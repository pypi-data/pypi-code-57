#!/usr/bin/env python3

import enum

from ..apis.base_api import BaseApi, DEFAULT_TIMEOUT
from ..apis.cmdid import PCProgramCmdId
from ..pb2.codemao_faceanalyze_pb2 import FaceAnalyzeRequest, FaceAnalyzeResponse
from ..pb2.codemao_facedetect_pb2 import FaceDetectRequest, FaceDetectResponse
from ..pb2.codemao_facerecognise_pb2 import FaceRecogniseRequest, FaceRecogniseResponse
from ..pb2.codemao_getinfrareddistance_pb2 import GetInfraredDistanceRequest, GetInfraredDistanceResponse
from ..pb2.codemao_getregisterfaces_pb2 import GetRegisterFacesRequest, GetRegisterFacesResponse
from ..pb2.codemao_recogniseobject_pb2 import RecogniseObjectRequest, RecogniseObjectResponse
from ..pb2.codemao_takepicture_pb2 import TakePictureRequest, TakePictureResponse
from ..pb2.pccodemao_message_pb2 import Message


class FaceDetect(BaseApi):
    """
    人脸检测（个数）
    """

    def __init__(self, is_serial: bool = True, timeout: int = 0):
        assert timeout > 0, 'FaceDetect timeout should be positive'
        self.__isSerial = is_serial
        self.__timeout = timeout

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = FaceDetectRequest()
        request.timeout = self.__timeout

        cmd_id = PCProgramCmdId.FACE_DETECT_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = FaceDetectResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class FaceAnalysis(BaseApi):
    """
    人脸分析（性别）
    """

    def __init__(self, is_serial: bool = True, timeout: int = 0):
        assert timeout > 0, 'FaceAnalysis timeout should be positive'
        self.__isSerial = is_serial
        self.__timeout = timeout

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT
        request = FaceAnalyzeRequest()
        request.timeout = self.__timeout

        cmd_id = PCProgramCmdId.FACE_ANALYSIS_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = FaceAnalyzeResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


@enum.unique
class ObjectRecogniseType(enum.Enum):
    FRUIT = 1  # 水果
    GESTURE = 2  # 手势
    FLOWER = 3  # 花


class ObjectRecognise(BaseApi):
    """
    物体识别
    object_type: 物体识别类型，默认水果
    timeout：超时时间，默认10s
    """

    def __init__(self, is_serial: bool = True, object_type: ObjectRecogniseType = ObjectRecogniseType.FRUIT,
                 timeout: int = 10):
        assert timeout > 0, 'ObjectRecognise timeout should be positive'
        assert object_type is not None and object_type.value > 0, 'objectType should not be None,and should be positive'
        self.__isSerial = is_serial
        self.__objectType = object_type.value
        self.__timeout = timeout

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = RecogniseObjectRequest()
        request.objectType = self.__objectType
        request.timeout = self.__timeout

        cmd_id = PCProgramCmdId.RECOGNISE_OBJECT_REQUEST.value

        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = RecogniseObjectResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class FaceRecognise(BaseApi):
    """
    人脸识别
    timeout:超时时间，默认10s
    """

    def __init__(self, is_serial: bool = True, timeout: int = 10):
        assert timeout > 0, 'ObjectRecognise timeout should be positive'
        self.__isSerial = is_serial
        self.__timeout = timeout

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT
        request = FaceRecogniseRequest()
        request.timeout = self.__timeout

        cmd_id = PCProgramCmdId.FACE_RECOGNISE_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = FaceRecogniseResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


@enum.unique
class TakePictureType(enum.Enum):
    IMMEDIATELY = 0  # 立即拍照
    FINDFACE = 1  # 寻找人脸拍照


class TakePicture(BaseApi):
    """
    拍照
    takePictureType:拍照类型，默认立即拍照
    """

    def __init__(self, is_serial: bool = True, take_picture_type: TakePictureType = TakePictureType.IMMEDIATELY):
        self.__isSerial = is_serial
        self.__type = take_picture_type.value

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT
        request = TakePictureRequest()
        request.type = self.__type

        cmd_id = PCProgramCmdId.TAKE_PICTURE_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = TakePictureResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class GetInfraredDistance(BaseApi):
    """
    获取红外距离
    """

    def __init__(self, is_serial: bool = True):
        self.__isSerial = is_serial

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT
        request = GetInfraredDistanceRequest()

        cmd_id = PCProgramCmdId.GET_INFRARED_DISTANCE_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = GetInfraredDistanceResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class GetRegisterFaces(BaseApi):
    """
    获取已注册的人脸列表
    """

    def __init__(self, is_serial: bool = True):
        self.__isSerial = is_serial

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT
        request = GetRegisterFacesRequest()

        cmd_id = PCProgramCmdId.GET_REGISTER_FACES_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = GetRegisterFacesResponse()
            response.ParseFromString(data)
            return response
        else:
            return None
