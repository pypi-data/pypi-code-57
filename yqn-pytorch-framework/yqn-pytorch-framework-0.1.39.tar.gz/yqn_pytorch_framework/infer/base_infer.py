import os
from abc import abstractmethod

import torch
import numpy as np
from yqn_config.base_config import BaseConfig
from yqn_exception.exception import InputSizeException, InferModelException
from yqn_pytorch_framework.device import get_device, tensor_load_device
from yqn_pytorch_framework.train.base_engine import BaseModelEngine


class BaseModelInfer:
    def __init__(self, model_config: BaseConfig):
        self.config = model_config
        self.device = model_config.device
        with torch.no_grad():
            self.model = self.load_model().cpu()
            resume_file = self.get_infer_model_file()
            if os.path.exists(resume_file):
                print("=> loading checkpoint '{}'".format(resume_file))
                checkpoint = torch.load(resume_file, map_location=torch.device('cpu'))
                if hasattr(self.config, "saved_state"):
                    if self.config.saved_state:
                        self.model.load_state_dict(checkpoint, strict=False)
                    else:
                        self.model.load_state_dict(checkpoint['state_dict'])
                else:
                    self.model.load_state_dict(checkpoint['state_dict'])

                self.model = tensor_load_device(self.model, self.device)

                self.model.eval()
                print("=> loaded checkpoint '{}' ".format(resume_file))
            else:
                raise InferModelException("infer model not found " + str(resume_file))

        super(BaseModelInfer, self).__init__()

    def get_infer_model_file(self):
        """
        :return: infer_model 文件路径
        """
        directory = self.config.get_train_model_out_dir(self.config.split_date)
        infer_model_path = os.path.join(directory, 'model_best.pth')
        return infer_model_path

    @abstractmethod
    def load_model(self):
        """
        :return: model
        """
        pass

    @abstractmethod
    def get_input_size_without_batch(self):
        pass

    @abstractmethod
    def format_output(self, outputs, input_features):
        pass

    @abstractmethod
    def pre_handle(self, *input_features):
        pass

    def infer(self, *input_features):
        with torch.no_grad():
            input_features_handled = self.pre_handle(*input_features)
            expect_input_shapes = self.get_input_size_without_batch()
            if type(expect_input_shapes) is list or type(expect_input_shapes) is tuple:
                for expect_input_shape, input_feature in zip(expect_input_shapes, input_features_handled):
                    is_same_size = self.compare_shape(expect_input_shape, input_feature)
                    if not is_same_size:
                        raise InputSizeException("input shape error")
            else:
                is_same_size = self.compare_shape(expect_input_shapes, input_features_handled)
                if not is_same_size:
                    raise InputSizeException("input shape error")
            per_size = self.config.batch_size
            if type(input_features_handled) is list or type(input_features_handled) is tuple:
                input_shape = input_features_handled[0].shape
            else:
                input_shape = input_features_handled.shape
            loop_size = int(input_shape[0] / per_size) + (0 if input_shape[0] % per_size == 0 else 1)
            outputs = []
            multi_outputs = []
            for index in range(loop_size):
                input_tensors = []
                if type(input_features_handled) is list or type(input_features_handled) is tuple:
                    for input_items in input_features_handled:
                        input_converted = input_items[
                                          index * per_size: min(input_shape[0], (index + 1) * per_size), ]
                        input_tensor = tensor_load_device(torch.from_numpy(np.array(input_converted)),
                                                          self.config.device)
                        input_tensors.append(input_tensor)
                else:
                    input_converted = input_features_handled[
                                      index * per_size: min(input_shape[0], (index + 1) * per_size), ]
                    input_tensors = tensor_load_device(torch.from_numpy(np.array(input_converted)), self.config.device)
                result = self.model(*tuple(input_tensors))
                if type(result) is list or type(result) is tuple:
                    if index == 0:
                        for result_index in range(len(result)):
                            multi_outputs.append([])
                    for result_item, result_index in zip(result, range(len(result))):
                        multi_outputs[result_index].append(result_item)
                else:
                    outputs.append(result)
            if len(outputs) > 0:
                outputs_cat = torch.cat(outputs, dim=0)
            else:
                outputs_cat = []
                for multi_output in multi_outputs:
                    outputs_cat.append(torch.cat(multi_output, dim=0))
            dic = {'outputs': outputs_cat, 'input_features': input_features}
            return self.format_output(**dic)

    @staticmethod
    def compare_shape(expect_input_shape, input_feature):
        input_shape = input_feature.shape
        shape_len = len(input_shape)
        is_same_size = True
        for index in range(shape_len - 1):
            is_same_size = is_same_size & (input_shape[index + 1] == expect_input_shape[index])
        return is_same_size
