#!/usr/bin/env python3

import enum

from ..apis.base_api import BaseApi, DEFAULT_TIMEOUT
from ..apis.cmdid import PCProgramCmdId
from ..pb2 import cloudstorageurls_pb2
from ..pb2.cloudtranslate_pb2 import Platform
from ..pb2.codemao_controltts_pb2 import ControlTTSRequest, ControlTTSResponse
from ..pb2.codemao_getaudiolist_pb2 import GetAudioListRequest, GetAudioListResponse
from ..pb2.codemao_playaudio_pb2 import PlayAudioRequest, PlayAudioResponse
from ..pb2.codemao_playonlinemusic_pb2 import MusicRequest, MusicResponse
from ..pb2.codemao_stopaudio_pb2 import StopAudioRequest, StopAudioResponse
from ..pb2.pccodemao_message_pb2 import Message


@enum.unique
class TTSControlType(enum.Enum):
    START = 1  # 播放
    STOP = 0  # 停止


class PlayTTS(BaseApi):
    """
    播放TTS
    controlType:控制类型，默认播放
    """

    def __init__(self, is_serial: bool = True, text: str = None, control_type: TTSControlType = TTSControlType.START):
        assert text is not None and len(text), 'tts text should be available'
        self.__isSerial = is_serial
        self.__text = text
        self.__type = control_type.value

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = ControlTTSRequest()
        request.text = self.__text
        request.type = self.__type

        cmd_id = PCProgramCmdId.PLAY_TTS_REQUEST.value

        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = ControlTTSResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class PlayAudio(BaseApi):
    """
    播放音效
    url:音效地址，阿里私有云
    volume：音量，[0.0，1.0]，默认1.0
    默认音效存储类型为阿里私有云
    """

    def __init__(self, is_serial: bool = True, url: list = None, volume: float = 1.0):
        assert url is not None and len(url), 'PlayAudio url should be available'
        assert 0 <= volume <= 1.0, 'PlayAudio volume should be in range[0,1]'
        self.__isSerial = is_serial
        self.__url = url
        self.__volume = volume
        self.__cloudStorageType = cloudstorageurls_pb2.ALIYUN_PRIVATE

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        cloud = cloudstorageurls_pb2.CloudStorage()
        cloud.type = self.__cloudStorageType
        cloud.url.extend(list(self.__url))

        request = PlayAudioRequest()

        request.cloud.CopyFrom(cloud)
        request.volume = self.__volume

        cmd_id = PCProgramCmdId.PLAY_AUDIO_REQUEST.value

        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = PlayAudioResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class StopAllAudio(BaseApi):
    """
    停止所有音效
    """

    def __init__(self, is_serial: bool = True):
        self.__isSerial = is_serial

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = StopAudioRequest()

        cmd_id = PCProgramCmdId.STOP_AUDIO_REQUEST.value

        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = StopAudioResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


@enum.unique
class AudioType(enum.Enum):
    INNER = 0  # 内置
    CUSTOM = 1  # 自定义


class FetchAudioList(BaseApi):
    """
    获取机器人的音效列表
    //查询类型 0:预置，1：sdcard
    """

    def __init__(self, is_serial: bool = True, audio_type: AudioType = AudioType.INNER):
        self.__isSerial = is_serial
        self.__searchType = audio_type.value

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = GetAudioListRequest()

        request.searchType = self.__searchType

        cmd_id = PCProgramCmdId.GET_AUDIO_LIST_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = GetAudioListResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class PlayOnlineMusic(BaseApi):
    """
    播放在线歌曲
    默认腾讯平台
    """

    def __init__(self, is_serial: bool = True, name: str = None):
        assert name is not None and len(name), 'PlayOnlineMusic name should be available'
        self.__isSerial = is_serial
        self.__name = name
        self.__platform = Platform.TENCENT

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = MusicRequest()

        request.platform = self.__platform
        request.name = self.__name

        cmd_id = PCProgramCmdId.PLAY_ONLINE_MUSIC_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = MusicResponse()
            response.ParseFromString(data)
            return response
        else:
            return None
