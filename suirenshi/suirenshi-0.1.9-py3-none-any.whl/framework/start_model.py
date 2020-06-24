#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
# 
# File: start_model.py
# Project: framework
# Created Date: Wednesday, June 10th 2020, 9:52:45 pm
# Author: liruifeng02
# -----
# Last Modified: Wed Jun 24 2020
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
import numpy as np

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
    parser.add_argument("base_path", help="the base path of the relative path", type=str)
    parser.add_argument("model_id", help="find the pipe to read and write", type=int)
    parser.add_argument("cfg_path", help="cfg file to parse parameters", type=str)
    parser.add_argument("port_use", help="which port to use", type=int)
    parser.add_argument("model_use", help="which model to use", type=str)
    parser.add_argument("model_path", help="where model python file", type=str)
    parser.add_argument("model_module", help="model python file name", type=str)
    parser.add_argument("delete_model_file", help="delete model file or not", type=int)

    args = parser.parse_args()
    return args


def start_model(args):
    """
    Start model
    Args:
        args:

    Returns:

    """
    logging.debug(
        'Model ID is {}, Model Use is {}, Port is {}'.format(args.model_id, args.model_use,
                                                             args.port_use))
    sys.path.append(args.model_path)
    model_module = __import__(args.model_module)
    model_class = getattr(model_module, args.model_use)
    delete_model_file = bool(args.delete_model_file)
    model = model_class(args.model_id, args.cfg_path, args.base_path, delete_model_file)
    if model_class is None:
        raise Exception('Unknown Model type: {}'.format(args.model_use))
    options = [('grpc.max_send_message_length', 521310100),
               ('grpc.max_receive_message_length', 521310100)]
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=1), options=options)
    service_pb2_grpc.add_InferenceServicer_to_server(inference.ModelInference(model), grpc_server)
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

    start_model(args)
