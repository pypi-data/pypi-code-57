#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
"""
# This module provide
# Authors: jiaohanzhe(jiaohanzhe@baidu.com)
# Date: 2020/6/10 3:05 下午
"""

import asyncio
from typing import List

import grpc
import service_pb2
import service_pb2_grpc
from utils import simple_logger
from utils.utils import config_parser
logging = simple_logger.get_simple_logger()


class BasePipeline(object):
    """
    BasePipeline
    """

    def __init__(self, pipeline_id: int, cfg_path: str) -> None:
        """

        Args:
            pipeline_id: 用于区分pipeline的唯一识别符
            cfg_path: 配置文件路径
        """
        self.pipeline_id = pipeline_id
        self.cfg_path = cfg_path
        self.cfg_dic = config_parser(self.cfg_path)
        self.result = None
        self.pipeline_name = 'pipeline_{}'.format(str(pipeline_id))
        self.pipeline_cfg = self.cfg_dic[self.pipeline_name]
        self.ports = eval(self.pipeline_cfg['ports'])
        self.loop = None

    def _send_single_inference_request(self, request: service_pb2.InferenceRequest,
                                       port: int) -> service_pb2.InferenceReply:
        """
        单次的同步阻塞请求
        Args:
            request: 请求
            port: 端口号

        Returns:

        """
        options = [('grpc.max_send_message_length', -1),
                   ('grpc.max_receive_message_length', -1)]
        with grpc.insecure_channel('{}:{}'.format('127.0.0.1', port), options=options) as channel:
            stub = service_pb2_grpc.InferenceStub(channel)
            logging.debug('Sending single inference request')
            return stub.Inference(request, timeout=self.pipeline_cfg.get("timeout", 10000))

    def inference(self, request):
        """
        用户自定义的业务逻辑
        Returns:

        """
        raise Exception('This method must be defined by user')

    def _send_multiple_inference_request(self, requests: List[service_pb2.InferenceRequest],
                                         ports: List[int]):
        """

        Args:
            requests: 请求列表
            ports: 端口列表（需要和请求顺序对应）

        Returns:

        """
        assert len(requests) == len(ports), 'Requests and ports should be of the same length'
        self.loop = asyncio.new_event_loop()
        self.total_result = []
        asyncio.set_event_loop(self.loop)
        try:
            _ = self.loop.run_until_complete(self.gather_tasks(requests, ports))
        except Exception as e:
            logging.error('Fail to send multiple inference requests')
            logging.error(e)
        finally:
            self.loop.close()

    async def gather_tasks(self, requests: List[service_pb2.InferenceRequest], ports: List[int]):
        """

        :param requests:
        :param ports:
        :return:
        """
        tasks = []
        for request, port in zip(requests, ports):
            tasks.append(self.make_future(self._send_single_inference_request, request, port))
        results = await asyncio.gather(*tuple(tasks))
        return results

    async def make_future(self, func, *args):
        """
        异步请求
        Args:
            func: 需要异步的函数
            *args: 函数接受的参数

        Returns:

        """
        future = self.loop.run_in_executor(None, func, *args)
        response = await future
        logging.debug('Response:')
        self.total_result.extend(response.singleInferenceReply)
