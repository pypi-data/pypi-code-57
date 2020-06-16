#!/usr/bin/env python3
import abc
import asyncio
import enum
from abc import ABC
from typing import Callable, Union

from ..channels.websocket_client import ubt_websocket as _UBTWebSocket, AbstractMsgHandler

DEFAULT_TIMEOUT = 300

socket = _UBTWebSocket()


@enum.unique
class MiniApiResultType(enum.Enum):
    Success = 1
    Timeout = 2


@enum.unique
class MiniEventType(enum.Enum):
    FaceReco = 1
    ASR = 2
    ASROffline = 3


class BaseApi(abc.ABC):
    """
    消息api基类
    向机器人发送消息
    """

    async def send(self, cmd_id: int, message, timeout: int) -> Union[object, bool]:
        """
        消息发送方法
        :param cmd_id: 支持的命令: mini.apis.cmdid
        :param message: 支持的message: mini.pb2.*
        :param timeout: 超时时间, 如果超时时间为0, 表示只需写入socket成功,不需要等机器人命令执行完成; 否则,需要等机器人执行完成再返回,默认等300秒
        :return:  命令执行结果:timeout<=0? bool :(bool, response)
        """
        assert cmd_id >= 0, 'cmdId should not be negative number in BaseApi'
        assert message is not None, 'message should not be none in BaseApi'
        # 通用的发送消息逻辑
        if timeout <= 0:
            return await socket.send_msg0(cmd_id, message)
        else:
            result = await socket.send_msg(cmd_id, message, timeout)
            if result:
                return MiniApiResultType.Success, self.parse_msg(result)
            else:
                return MiniApiResultType.Timeout, None

    async def execute(self):
        """
        子类将支持的message序列化后,写入socket
        由子类实现
        """
        raise NotImplementedError()

    def parse_msg(self, message):
        """
        子类将收到的bytes饭序列化为message
        """
        raise NotImplementedError()


class BaseApiNeedResponse(BaseApi, abc.ABC):
    """
    消息api基类
    向机器人发送消息
    需要回复，timeout不能为空
    """

    async def send(self, cmd_id, data, timeout: int):
        assert timeout > 0, 'timeout should be Positive number in BaseApiNeedResponse'
        return await super().send(cmd_id, data, timeout)


class BaseApiNoNeedResponse(BaseApi, ABC):
    """
    消息api基类
    向机器人发送消息
    不需要需要回复
    """

    async def send(self, cmd_id, message, timeout: int = 0):
        # 默认timeout为0
        return await super().send(cmd_id, message, 0)


class BaseEventApi(BaseApiNoNeedResponse, AbstractMsgHandler, ABC):
    """
    事件类消息api基类, 事件类消息,是由机器人主动推送过来的事件消息, 当注册了事件处理器后
    """

    def __init__(self, cmd_id: int, message, is_repeat: bool = True, timeout: int = 0,
                 handler: 'Callable[..., None]' = None):
        """
        事件类消息,初始化
        :param cmd_id: id
        :param message: response类型
        :param is_repeat: 是否多次监听事件, 默认True
        :param timeout:
        :param handler: 处理器
        """
        super().__init__()
        self.__cmdId = cmd_id
        self.__request = message
        self.__isRepeat = is_repeat
        self.__timeout = timeout
        self.__handler = handler

        if is_repeat:
            self.__repeatCount = -1
        else:
            self.__repeatCount = 1

    def set_handler(self, handler: 'Callable[..., None]' = None):
        self.__handler = handler

    # 开始监听
    def start(self):
        """
         启动监听器
        """
        # 发送消息
        asyncio.create_task(self.send(cmd_id=self.__cmdId, message=self.__request))
        # 注册监听
        socket.register_msg_handler(cmd=self.__cmdId, handler=self)

    # 停止监听
    def stop(self):
        """
        移除监听器,子类需要通知机器人停止事件上报
        """
        # 移除消息监听
        socket.unregister_msg_handler(cmd=self.__cmdId, handler=self)

    # AbstractMsgHandler
    def handle_msg(self, message):
        # 处理监听次数
        if self.__repeatCount > 0:
            # 有监听次数
            self.__handle_msg(message)
            self.__repeatCount -= 1
        elif self.__repeatCount == -1:
            # 无限监听
            self.__handle_msg(message)

    def __handle_msg(self, message):
        if self.__handler is not None:
            self.__handler(self.parse_msg(message))
