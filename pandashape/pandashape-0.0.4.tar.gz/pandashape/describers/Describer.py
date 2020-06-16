import pandas as pd


class Describer:
    def describe(self, df):
        raise NotImplementedError()

    def get_section_header(self):
        raise NotImplementedError()
