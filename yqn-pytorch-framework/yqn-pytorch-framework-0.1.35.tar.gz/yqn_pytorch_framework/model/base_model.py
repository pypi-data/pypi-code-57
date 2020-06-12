from abc import abstractmethod

from torch import nn


class BaseModel(nn.Module):

    def __init__(self, config):
        super(BaseModel, self).__init__()
        self.config = config

    @abstractmethod
    def get_default_input(self):
        """
        获取input shape 大小
        :return:
        """
        pass
