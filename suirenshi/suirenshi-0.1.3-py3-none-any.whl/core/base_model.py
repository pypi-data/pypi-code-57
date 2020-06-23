#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
"""
# This module provide
# Authors: suye(suye02@baidu.com)
# Date: 2020/6/11 3:05 下午
"""
import os
import json
import time
from abc import abstractmethod
from collections import namedtuple

from logging import simple_logger
from utils.utils import config_parser

logging = simple_logger.get_simple_logger()


class BaseModel(object):
    """
    模型预测服务
    解析模型对应的配置文件
    包含了模型初始化、及启动物体检测
    """

    def __init__(self, model_id, cfg_path, base_path):
        """
        Args:
            model_id: 模型ID
            cfg_path: 模型config路径
        """
        # 基本meta信息
        self.model_id = model_id
        self.cfg_path = cfg_path
        self.base_path = base_path
        # 加载配置文件
        self.cfg_dic = config_parser(self.cfg_path)
        self.model_name = 'model_{}'.format(str(model_id))
        self.model_cfg = self.cfg_dic[self.model_name]
        self.model_path = os.path.join(base_path, self.model_cfg['model_path'])
        self.config_path = os.path.join(base_path, self.model_cfg['config_path'])
        self.class_mapper = json.loads(self.model_cfg['class_mapper'])
        self.thresh_values = [float(x) for x in self.model_cfg['thresh_values'].split(',')]
        self.num_classes = int(self.model_cfg['num_classes'])
        self.result = None
        # runtime 初始化
        self.error_code = 0
        self.image_np = None
        # 启动模型
        self.model = None
        self._env_check()
        self._start_model()

    @abstractmethod
    def _start_model(self):
        """
        启动模型（抽象方法，必须改写）
        """

    @abstractmethod
    def _env_check(self):
        """
        启动模型前检查环境中是否有正在占用gpu的程序或已启动的预测服务等，避免重复启动模型等误操作
        """

    @abstractmethod
    def _inference(self, x_offset=0, y_offset=0):
        """
        Args:
            x_offset: 切图inference的小图的左上角x坐标
            y_offset: 切图inference的小图的左上角y坐标
            Returns:
        """

    @abstractmethod
    def inference(self, image_np):
        """
        传入图片numpy（此处删除了不必要字段model id，offset等，这些都可以抽到cfg中）
        调用_inference接口进行预测，结果写入类属性self.results
        Args:
            image_np: 图片numpy数组

        Returns:
        """
        self.image_np = image_np
        self._preprocess()
        Result = namedtuple('Result', ['masks', 'bboxes', 'labels'])
        self.result = Result(masks=[], bboxes=[], labels=[])
        inference_start = time.time()
        self._inference()
        logging.debug('Inference Time: {:.3f}'.format(time.time() - inference_start))
        post_start = time.time()
        self._postprocess()
        logging.debug('Post Time: {:.3f}'.format(time.time() - post_start))

    @abstractmethod
    def results_parser(self):
        """
        根据框架类型(paddle or mmdet)编写结果处理代码，统一存入 namedtuple('Result', ['masks', 'bboxes', 'labels'])
        """

    def _preprocess(self):
        """
        前处理
        Returns:

        """
        pass

    def _postprocess(self):
        """
        后处理
        Returns:
        """
        pass
