import json
import os
import pathlib
import re
from abc import abstractmethod
from datetime import datetime

import yaml

from yqn_config.conf_parser import CommonConf
from yqn_exception.exception import *
from yqn_pytorch_framework.device import get_device

BOOLEAN_STATES = {'yes': True, 'true': True, 'on': True,
                  'no': False, 'false': False, 'off': False}
REQUIRE_CONFIG = ["config_name",
                  "device",
                  "repeat_count",
                  "shuffle_batch",
                  "num_epochs",
                  "epochs_shuffle",
                  "batch_size",
                  "optimizer",
                  "learning_rate",
                  "retrain",
                  "write_image",
                  "write_scalar",
                  "summary_freq",
                  "save_freq",
                  "progress_freq",
                  "split_date", ]


class BaseConfig:

    def __init__(self, project_path,
                 resource_path,
                 output_path,
                 switch_flag):
        self.project_path = project_path
        self.resource_path = resource_path
        self.output_path = output_path
        self.switch_flag = switch_flag
        self.load_config()
        super(BaseConfig, self).__init__()
        self.device = get_device()
        self.modify_config()
        self.check_config()
        self.make_dirs()

    @abstractmethod
    def get_config_file(self):
        pass

    def modify_config(self):
        pass

    def check_config(self):
        for name in REQUIRE_CONFIG:
            try:
                attr = getattr(self, name)
            except AttributeError:
                raise ConfigMissException("配置文件必须包含:", name)

    def load_config(self):
        config_parser = CommonConf()
        assert os.path.exists(self.get_config_file())
        config_parser.read(self.get_config_file())
        loader = yaml.FullLoader
        loader.add_implicit_resolver(
            u'tag:yaml.org,2002:float',
            re.compile(u'''^(?:
             [-+]?(?:[0-9][0-9_]*)\\.[0-9_]*(?:[eE][-+]?[0-9]+)?
            |[-+]?(?:[0-9][0-9_]*)(?:[eE][-+]?[0-9]+)
            |\\.[0-9_]+(?:[eE][-+][0-9]+)?
            |[-+]?[0-9][0-9_]*(?::[0-5]?[0-9])+\\.[0-9_]*
            |[-+]?\\.(?:inf|Inf|INF)
            |\\.(?:nan|NaN|NAN))$''', re.X),
            list(u'-+0123456789.'))

        lines = []
        lines.append("*" * 150)
        lines.append(" {:<40} Config File Path {:<90} ".format("", self.get_config_file()))
        for section in config_parser.sections():
            lines.append("=" * 150)
            lines.append(" Section {:<140} ".format("[" + str(section) + "]"))
            lines.append("=" * 150)
            for k, v in config_parser.items(section):
                if v.lower() in BOOLEAN_STATES:
                    v = BOOLEAN_STATES[v.lower()]
                else:
                    v = yaml.load(v, Loader=loader)
                setattr(self, k, v)
                lines.append(" {:<40} | {:<105} ".format(k, json.dumps(v)))
        # lines.append("=" * 150)
        # print("|" + "|\n|".join(lines) + "|\n")

    def make_dirs(self):
        model_dir = os.path.join(self.resource_path, "models", self.config_name)
        files_dir = os.path.join(self.resource_path, "files", self.config_name)
        train_model_out_dir = os.path.join(self.output_path, "train_model", self.config_name)
        train_log_dir = os.path.join(self.output_path, "train_log", self.config_name)
        pathlib.Path(model_dir).mkdir(parents=True, exist_ok=True)
        pathlib.Path(files_dir).mkdir(parents=True, exist_ok=True)
        pathlib.Path(train_model_out_dir).mkdir(parents=True, exist_ok=True)
        pathlib.Path(train_log_dir).mkdir(parents=True, exist_ok=True)

    def get_infer_model_path(self, model_name):
        """
            获取推断模型文件路径 {resource_path}/models/{config_name}/model_name
            #:param model_name 模型文件名
        """
        pathlib.Path(os.path.join(self.resource_path, "models", self.config_name)).mkdir(parents=True, exist_ok=True)
        model_path = os.path.join(self.resource_path, "models", self.config_name, model_name)
        return model_path

    def get_file_path(self, file_name):
        """
            获取资源文件路径 如字典文件等 {resource_path}/files/{config_name}/file_name
            #:param file_name 资源文件名
        """
        pathlib.Path(os.path.join(self.resource_path,
                                  "files",
                                  self.config_name)).mkdir(parents=True, exist_ok=True)
        file_path = os.path.join(self.resource_path,
                                 "files",
                                 self.config_name,
                                 file_name)
        return file_path

    def get_tmp_file_dir(self, split_date=False):
        """
            获取零时文件路径  {output_path}/tmp_file/{config_name}
        """
        pathlib.Path(os.path.join(self.output_path, "tmp_file", self.config_name)).mkdir(parents=True, exist_ok=True)
        if split_date:
            timestamp = "{0:%Y_%m_%d/}".format(datetime.now())
            pathlib.Path(os.path.join(self.output_path,
                                      "tmp_file",
                                      self.config_name,
                                      timestamp)).mkdir(parents=True,
                                                        exist_ok=True)
            file_path = os.path.join(self.output_path, "tmp_file", self.config_name, timestamp)
        else:
            file_path = os.path.join(self.output_path, "tmp_file", self.config_name)
        return file_path

    def get_train_model_out_dir(self, split_date=False):
        """
            获取训练模型文件保存路径 {output_path}/train_model/{config_name}/
        """
        pathlib.Path(os.path.join(self.output_path, "train_model", self.config_name)).mkdir(parents=True, exist_ok=True)
        if split_date:
            timestamp = "{0:%Y_%m_%d/}".format(datetime.now())
            pathlib.Path(os.path.join(self.output_path, "train_model", self.config_name, timestamp)).mkdir(parents=True,
                                                                                                           exist_ok=True)
            file_path = os.path.join(self.output_path, "train_model", self.config_name, timestamp)
        else:
            file_path = os.path.join(self.output_path, "train_model", self.config_name)
        return file_path

    def get_train_log_dir(self):
        """
            获取训练Tensorboard日志保存路径 {output_path}/train_log/{config_name}/timestamp
        """
        timestamp = "{0:%Y-%m-%d_%H-%M-%S/}".format(datetime.now())
        train_log_dir = os.path.join(self.output_path, "train_log", self.config_name, timestamp)
        return train_log_dir

    #
    # def get_train_data_dir(self):
    #     file_path = os.path.join(self.output_path, "train_model", self.config_name)
    #     return file_path
