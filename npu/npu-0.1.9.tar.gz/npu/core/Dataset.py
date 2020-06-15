"""
:synopsis: Datasets class wrapper
.. moduleauthor:: Naval Bhandari <naval@neuro-ai.co.uk>
"""


class Dataset(object):

    def __init__(self, id, train_end, val_end, test_end):
        self.id = id
        self.__train_end = train_end
        self.__val_end = val_end
        self.__test_end = test_end

    def __str__(self):
        return self.id

    def __getitem__(self, item):
        return {"id": self, "indexes": item}

    @property
    def train(self):
        """
        Property for training subset
        :return: slice
        """
        return self[0:self.__train_end]

    @property
    def val(self):
        """
        Property for validation subset
        :return: slice
        """
        return self[self.__train_end:self.__val_end]

    @property
    def test(self):
        """
        Property for test subset
        :return: slice
        """
        return self[self.__val_end:self.__train_end]
