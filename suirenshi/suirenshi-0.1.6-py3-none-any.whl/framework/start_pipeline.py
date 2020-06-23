#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
# 
# File: start_pipeline.py
# Project: framework
# Created Date: Wednesday, June 10th 2020, 9:54:54 pm
# Author: liruifeng02
# -----
# Last Modified: Tue Jun 23 2020
# Modified By: liruifeng02
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	----------------------------------------------------------
"""
import argparse
import time
import os
import sys
from concurrent import futures
import grpc

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import framework.inference as inference
import logging
from pb import service_pb2, service_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def parse():
    """
    parse params
    Returns:

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("pipeline_id", help="find the pipe to read and write", type=int)
    parser.add_argument("cfg_path", help="cfg file to parse parameters", type=str)
    parser.add_argument("port_use", help="which port to use", type=int)
    parser.add_argument("pipeline_use", help="which pipeline to use", type=str)
    parser.add_argument("pipline_path", help="where pipline python file", type=str)
    parser.add_argument("pipline_module", help="pipline python file name", type=str)

    args = parser.parse_args()
    return args


def start_pipeline(args):
    """
    Start model
    Args:
        args:

    Returns:

    """
    logging.debug(
        'Pipeline ID is {}, Pipeline Use is {}, Port is {}'.format(args.pipeline_id,
                                                                   args.pipeline_use,
                                                                   args.port_use))
    sys.path.append(args.pipline_path)
    pipline_module = __import__(args.pipline_module)
    pipline_class = getattr(pipline_module, args.pipeline_use)
    if pipline_class is None:
        raise Exception('Unknown pipeline type: {}'.format(args.pipeline_use))
    pipeline = pipline_class(args.pipeline_id, args.cfg_path)
    options = [('grpc.max_send_message_length', 521310100),
               ('grpc.max_receive_message_length', 521310100)]
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=1), options=options)
    service_pb2_grpc.add_InferenceServicer_to_server(inference.PiplineInference(pipeline), grpc_server)
    grpc_server.add_insecure_port('127.0.0.1:{}'.format(args.port_use))
    grpc_server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS * 24)
    except KeyboardInterrupt:
        grpc_server.stop(0)


if __name__ == "__main__":
    """
    Call and save logs
    """
    args = parse()
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='pipeline_{}.log'.format(args.pipeline_id),
                        filemode='w')
    start_pipeline(args)
