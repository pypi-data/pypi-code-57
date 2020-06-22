#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
# 
# File: start_serve.py
# Project: framework
# Created Date: Wednesday, June 10th 2020, 10:00:08 pm
# Author: liruifeng02
# -----
# Last Modified: Mon Jun 22 2020
# Modified By: liruifeng02
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	----------------------------------------------------------
"""
import logging
import configparser
import multiprocessing
import os
import subprocess
import sys

from six.moves import shlex_quote

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from utils import authentication, utils
import codecs


class ParseConf(object):
    """
    Class to store config info.
    Attributes:
        cfg: model configure file
        activate_pipes: which model to use
        script_path: serve script
        pipe_gpu_map: a dict to map pipe to gpu
    """

    def __init__(self, conf):
        """

        Args:
            conf:
        """
        self.conf = conf

    def conf_parse(self):
        """

        Returns:

        """
        conf_parser = configparser.ConfigParser()
        try:
            conf_parser.readfp(codecs.open(self.conf, "r", "utf-8-sig"))
            self.cfg = conf_parser.get("config", "cfg")

            self.activate_models = eval(conf_parser.get("model", "activate_models"))
            self.model_gpu_map = eval(conf_parser.get("model", "model_gpu_map"))
            self.model_port_map = eval(conf_parser.get("model", "model_port_map"))
            self.model_use = eval(conf_parser.get("model", "model_use"))
            self.model_path = eval(conf_parser.get("model", "model_path"))
            self.model_module = eval(conf_parser.get("model", "model_module"))

            self.activate_pipelines = eval(conf_parser.get("pipeline", "activate_pipelines"))
            self.pipeline_port_map = eval(conf_parser.get("pipeline", "pipeline_port_map"))
            self.pipeline_use = eval(conf_parser.get("pipeline", "pipeline_use"))
            self.pipeline_path = eval(conf_parser.get("pipeline", "pipeline_path"))
            self.pipeline_module = eval(
                conf_parser.get("pipeline", "pipeline_module"))

            self.is_auth = eval(conf_parser.get("auth", "is_auth"))
            self.auth_path = eval(conf_parser.get("auth", "auth_path"))
            self.auth_module = eval(conf_parser.get("auth", "auth_module"))
            self.auth_method = eval(conf_parser.get("auth", "auth_method"))

        except Exception as e:
            logging.fatal("Fail to parse conf as Exception: {}".format(e))


def model_popen(jobs_pid, script_path, base_path, model_id=-1, gpu_use=-1, port_use=0, model_use=None, cfg=None,
                model_path=None, model_module=None):
    """
    Popen to start process
    Args:
        script_path:
        model_id:
        gpu_use:
        port_use:
        model_use:
        cfg:

    Returns:

    """
    os.environ['CUDA_VISIBLE_DEVICES'] = str(gpu_use)
    cmd_pattern = '{python} {script_path} {base_path} {model_id} {cfg} {port_use} ' \
                  '{model_use} {model_path} {model_module} '
    cmd = cmd_pattern.format(python=shlex_quote('python'),
                             script_path=script_path,
                             base_path=base_path,
                             gpu_use=gpu_use,
                             model_id=model_id,
                             cfg=cfg,
                             port_use=port_use,
                             model_use=model_use,
                             model_path=model_path,
                             model_module=model_module)
    p = subprocess.Popen(cmd, shell=True)
    jobs_pid.append(p.pid)
    logging.info("Run cmd: {}".format(cmd))


def pipeline_popen(jobs_pid, script_path, pipeline_id=-1, port_use=0, pipeline_use=None, cfg=None,
                   pipeline_path=None, pipeline_module=None):
    """
    Popen to start process
    Args:
        script_path:
        pipeline_id:
        port_use:
        pipeline_use:
        cfg:

    Returns:

    """
    cmd_pattern = '{python} {script_path} {pipeline_id} {cfg} {port_use} {pipeline_use} {pipeline_path} ' \
                  '{pipeline_module}'
    cmd = cmd_pattern.format(python=shlex_quote('python'),
                             script_path=script_path,
                             pipeline_id=pipeline_id,
                             cfg=cfg,
                             port_use=port_use,
                             pipeline_use=pipeline_use,
                             pipeline_path=pipeline_path,
                             pipeline_module=pipeline_module)
    p = subprocess.Popen(cmd, shell=True)
    jobs_pid.append(p.pid)
    logging.info("Run cmd: {}".format(cmd))


def start_task(conf):
    """

    Args:
        conf: config file path.

    Returns:

    """
    conf = utils.get_abspath(conf)
    args = ParseConf(conf)
    args.conf_parse()
    logging.info("Active models: {}".format(args.activate_models))
    logging.info("Model GPU mapper: {}".format(args.model_gpu_map))
    logging.info("Model Port mapper: {}".format(args.model_port_map))
    logging.info("Model use: {}".format(args.model_use))

    logging.info("Active pipelines: {}".format(args.activate_pipelines))
    logging.info("Pipeline Port mapper: {}".format(args.pipeline_port_map))
    logging.info("Pipeline use: {}".format(args.pipeline_use))

    logging.info("Auth: {}".format(args.is_auth))

    base_path = sys.path[0]
    model_script_path = os.path.join(os.path.dirname(__file__), "start_model.py")
    pipeline_script_path = os.path.join(os.path.dirname(__file__), "start_pipeline.py")

    if args.is_auth:
        sys.path.append(utils.get_abspath(args.auth_path))
        auth_module = __import__(args.auth_module)
        authenticate = getattr(auth_module, args.auth_method)
        authentication.authenticate = authenticate
        if not authenticate():
            sys.exit(-1)

    # 鉴权通过，启动模型、pipline
    jobs_pid = multiprocessing.Manager().list()
    config_path = utils.get_abspath(args.cfg)
    # start models
    model_path = utils.get_abspath(args.model_path)
    for model_id in args.activate_models:
        logging.info("Model {} start a subprocess".format(model_id))
        gpu_use = args.model_gpu_map[str(model_id)]
        port_use = args.model_port_map[str(model_id)]
        model_use = args.model_use[str(model_id)]
        logging.info(
            "Model {} using GPU: {}, PORT: {}, MODEL: {}".format(model_id, gpu_use, port_use,
                                                                 model_use))
        p = multiprocessing.Process(target=model_popen,
                                    args=(jobs_pid, model_script_path, base_path, model_id, gpu_use, port_use,
                                          model_use, config_path, model_path, args.model_module))
        p.start()

    # start pipelines
    pipeline_path = utils.get_abspath(args.pipeline_path)
    for pipeline_id in args.activate_pipelines:
        logging.info("Pipeline {} start a subprocess".format(pipeline_id))
        port_use = args.pipeline_port_map[str(pipeline_id)]
        pipeline_use = args.pipeline_use[str(pipeline_id)]
        logging.info(
            "Pipeline {} using PORT: {}, PIPELINE: {}".format(pipeline_id, port_use, pipeline_use))
        p = multiprocessing.Process(target=pipeline_popen,
                                    args=(jobs_pid, pipeline_script_path, pipeline_id, port_use, 
                                          pipeline_use, config_path, pipeline_path, args.pipeline_module))
        p.start()
    return jobs_pid


def stop_task(jobs_pid):
    """
    stop stask
    """
    for pid in jobs_pid:
        utils.kill(pid)


if __name__ == "__main__":
    """
    main
    """
    config = "/home/liruifeng02/baidu/bce-themis/grpc-service/src/framework/config.conf"
    start_task(config)
