"""
Feature.py
----------
"""

import izzy as iz
import pandas as pd


class Feature:
    def __init__(self, data):
        # The raw data
        self.data = data

        # Pipe for data transformation
        # iz.granulate defaults
        self.bins = 10
        self.mode = 'equal'

        # iz.clip defaults
        self.left = None
        self.right = None
        self.cut = False

    def transform(self, pipe=('clip', 'granulate')):
        for step in pipe:
            self.data = step()
