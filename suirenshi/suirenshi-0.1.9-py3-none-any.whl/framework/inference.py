#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
# 
# File: inference.py
# Project: framework
# Created Date: Wednesday, June 10th 2020, 9:54:21 pm
# Author: liruifeng02
# -----
# Last Modified: Tue Jun 23 2020
# Modified By: liruifeng02
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	----------------------------------------------------------
"""
import time
import numpy as np
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import logging
from utils.authentication import auth
from pb import service_pb2, service_pb2_grpc


class ModelInference(service_pb2_grpc.InferenceServicer):
    """
    Model Inference Class
    """

    def __init__(self, model):
        self.model = model

    @auth
    def Inference(self, request, context):
        """
        Args:
            request:
            context:
        Returns:
        """
        start = time.time()
        try:
            self.model.inference(request)
        except Exception as e:
            logging.error(e)
            logging.error('Error in model inference')

        reply = service_pb2.InferenceReply()
        try:
            reply.photo_id = request.photo_id
            reply.product_id = request.product_id
            reply.channel_id = request.channel_id
            self.write_result(reply)
        except Exception as e:
            logging.error(e)
            logging.error('Error in write_result')
        logging.debug('Total time: {:.3f}'.format(time.time() - start))
        return reply

    def write_result(self, reply):
        """
        Args:
            reply:
        Returns:
        """
        num_detections = 0
        logging.debug('Result length is: {}'.format(
            len(self.model.result.labels)))
        for bbox, label, mask in zip(self.model.result.bboxes, self.model.result.labels,
                                     self.model.result.masks):
            if bbox[-1] < self.model.thresh_values[label]:
                continue
            num_detections += 1
            label = self.model.class_mapper[str(label)]
            single_reply = service_pb2.SingleInferenceReply(class_name=label,
                                                            xmin=bbox[0],
                                                            ymin=bbox[1],
                                                            bb_width=bbox[2] -
                                                            bbox[0],
                                                            bb_height=bbox[3] -
                                                            bbox[1],
                                                            score=bbox[4],
                                                            mask=mask.tobytes(),
                                                            mask_height=int(
                                                                mask.shape[0]),
                                                            mask_width=int(
                                                                mask.shape[1])
                                                            )
            reply.singleInferenceReply.append(single_reply)
        reply.num_detections = num_detections


class PiplineInference(service_pb2_grpc.InferenceServicer):
    """
    Pipline Inference Class
    """

    def __init__(self, pipeline):
        self.pipeline = pipeline

    @auth
    def Inference(self, request, context):
        """
        Args:
            request:
            context:
        Returns:
        """
        start = time.time()
        try:
            self.pipeline.inference(request)
        except Exception as e:
            logging.error(e)
            logging.error('Error in model inference')

        reply = service_pb2.InferenceReply()
        try:
            reply.photo_id = request.photo_id
            reply.product_id = request.product_id
            reply.channel_id = request.channel_id
            self.write_result(reply)
        except Exception as e:
            logging.error(e)
            logging.error('Error in write_result')
        logging.debug('Total time: {:.3f}'.format(time.time() - start))
        return reply

    def write_result(self, reply):
        """
        Args:
            reply:
        Returns:
        """
        num_detections = 0
        logging.debug('Result length is: {}'.format(
            len(self.pipeline.result.labels)))
        for bbox, label, feature in zip(self.pipeline.result.bboxes,
                                        self.pipeline.result.labels,
                                        self.pipeline.result.features):
            num_detections += 1
            single_reply = service_pb2.SingleInferenceReply(class_name=label,
                                                            xmin=bbox[0],
                                                            ymin=bbox[1],
                                                            bb_width=bbox[2] -
                                                            bbox[0],
                                                            bb_height=bbox[3] -
                                                            bbox[1],
                                                            score=bbox[4],
                                                            length=feature['length'],
                                                            width=feature['width'],
                                                            pixel_area=feature['pixel_area'],
                                                            gradients=feature['gradients'],
                                                            contrast=feature['contrast'],
                                                            brightness=feature['brightness'],
                                                            top_brightness=feature[
                                                                'top_brightness'],
                                                            low_brightness=feature['low_brightness']
                                                            )
            reply.singleInferenceReply.append(single_reply)
        reply.num_detections = num_detections
