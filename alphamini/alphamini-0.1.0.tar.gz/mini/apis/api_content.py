#!/usr/bin/env python3

from ..apis.base_api import BaseApi, DEFAULT_TIMEOUT
from ..apis.cmdid import PCProgramCmdId
from ..pb2.cloudtranslate_pb2 import Platform, Translate
from ..pb2.cloudwiki_pb2 import WiKi
from ..pb2.codemao_translate_pb2 import TranslateResponse, TranslateRequest
from ..pb2.codemao_wiki_pb2 import WikiRequest, WikiResponse
from ..pb2.pccodemao_message_pb2 import Message


class QueryWiKi(BaseApi):
    """
    百科
    默认腾讯百科
    """

    def __init__(self, is_serial: bool = True, query: str = None):
        assert query is not None and len(query), 'QueryWiKi query should be available'
        self.__isSerial = is_serial
        self.__query = query
        self.__platform = Platform.TENCENT

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        wiki = WiKi()
        wiki.query = self.__query
        wiki.platform = self.__platform

        request = WikiRequest()
        request.wiki.CopyFrom(wiki)

        cmd_id = PCProgramCmdId.WIKI_REQUEST.value

        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = WikiResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class StartTranslate(BaseApi):
    """
    翻译
    默认百度翻译
    """

    def __init__(self, is_serial: bool = True, query: str = None, prefix: str = '', suffix: str = '',
                 from_lan: Platform = None, to_lan: Platform = None, platform: Platform = Platform.BAIDU):
        assert query is not None, 'Translate query could not be None'
        assert from_lan is not None, 'Translate from_lan could not be None'
        assert to_lan is not None, 'Translate to_lan could not be None'
        self.__isSerial = is_serial
        self.__query = query
        self.__prefix = prefix
        self.__suffix = suffix
        self.__fromLan = from_lan
        self.__toLan = to_lan
        self.__platform = platform

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        translate = Translate()
        translate.query = self.__query
        translate.prefix = self.__prefix
        translate.suffix = self.__suffix
        translate.platform = self.__platform
        # translate.from = self.__fromLan
        setattr(translate, "from", self.__fromLan)
        translate.to = self.__toLan

        request = TranslateRequest()
        request.translate.CopyFrom(translate)

        cmd_id = PCProgramCmdId.TRANSLATE_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = TranslateResponse()
            response.ParseFromString(data)
            return response
        else:
            return None
