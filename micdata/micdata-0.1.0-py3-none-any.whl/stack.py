import os
import numpy as np
import micdata


class Stack():
    def __init__(self, file_name, data=None, dtype=np.float32):
        self._io = micdata.io.IOFactory(file_name)
        self.data = data
        self.formatter = None
        self.formatted = False
        if self.data is None:
            self.load()

    def load(self):
        if self.data is None:
            self.data = self._io.load()
        else:
            import warnings
            warnings.warn('Refusing to overwrite existing data. Call the reset method before loading new data.')

    def save(self):
        self._io.write(self.data)

    def change_file_name(self, file_name):
        self._io = micdata.io.IOFactory(file_name)

    def format(self, formatter):
        assert isinstance(formatter, micdata.formatting.ImageFormatter), 'formatter must be an ImageFormatter'
        if self.data is None:
            raise ValueError('Cannot format stack before loading data.')
        self.formatter = formatter
        self.data = self.formatter.apply(self.data)
        self.formatted = True

    def revert_format(self):
        assert self.formatted, 'Cannot revert the format of a stack that has not been formatted.'
        self.data = self.formatter.revert(self.data)
        self.formatted = False

    def reset(self):
        self.data = None
        self.formatted = False
        del(self.formatter)
