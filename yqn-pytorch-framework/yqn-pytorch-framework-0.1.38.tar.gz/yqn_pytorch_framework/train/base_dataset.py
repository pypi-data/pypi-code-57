from abc import abstractmethod

from torch.utils import data

from yqn_config.base_config import BaseConfig


class BaseDataset(data.Dataset):
    def __init__(self, config: BaseConfig):
        self.config = config
        super(BaseDataset, self).__init__()

    @abstractmethod
    def get_item_size(self):
        pass

    @abstractmethod
    def get_item(self, index):
        pass

    def __len__(self):
        return self.get_item_size() * self.config.repeat_count

    def __getitem__(self, index):
        real_index = index % (self.get_item_size())
        data = self.get_item(real_index)
        return data
