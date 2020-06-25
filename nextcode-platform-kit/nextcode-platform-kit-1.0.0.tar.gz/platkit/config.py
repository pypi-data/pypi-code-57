#!/usr/bin/env python


class Config:
    # and whatever else you want in your class -- that's all!

    """
    Borg pattern Config class see:
    http://code.activestate.com/recipes/66531-singleton-we-dont-need-no-stinkin-singleton-the-bo/

    example usage:
        config = Config({'my': 'config'})
    """

    shared_state = {}
    data = {}

    def __init__(self, data=None):
        self.__dict__ = self.shared_state
        self.set(data)

    def dict(self):
        return self.data

    def set(self, data):
        if data is None:
            data = {}
        self.data.update(data)

    def get(self, key, default=None):
        return self.data.get(key, default)
