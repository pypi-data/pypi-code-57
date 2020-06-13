"""
report.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>

How to Use
----------
>>> df = pd.DataFrame(...)
>>> report = DataReport(path='report.html')
>>> report.add_overview(df)
>>> report.add_correlations(df)
>>> report.add_column_analyzer(df)
>>> report.generate()
>>> report.launch()
"""

from izzy.misc import ArrayLike
from .analyzer import fan1d

import pandas as pd


#
class DataReport:
    """
    Generate a report for all columns in a pandas DataFrame

    The report
    """

    # Initialize class
    def __init__(self, path, name=None, toc=True):
        """
        Initialize class instance

        Parameters
        ----------
        path : str
            Location to save report
        toc : bool
            Should table of contents be generated? (Default: True)
        """

        # Path to save report to
        self.path = path

        # Report name
        self.name = name if name is not None else 'data report'

        # Should table of contents be generated?
        self.toc = toc

        # Report data and sections
        self.report = ''
        self.sections = []

        # Status
        self.is_compiled = False

    # Helper function to add block
    @classmethod
    def _add_block(cls, block, content):
        """

        Parameters
        ----------
        block
        content

        Returns
        -------

        """

        return '{% block ' + block + '%}' + content + '{% endblock %}'

    # Add overview to the report
    def add_overview(self, df, outcome=None):
        """
        Add overview

        Overview includes the following data elements,
          - Number of observations
          - Number of variables
          - Dataset size in memory
          - Number of duplicate rows
          - Number of rows with missing values
          - Details about outcome (if present)

        Parameters
        ----------
        df : pandas.DataFrame
            DataFrame
        outcome : str
            (Optional) Column name in DataFrame that represents some outcome
        """

        pass

    # Compile report
    def compile(self, footer=True):
        """
        Compile report

        Returns
        -------

        """

        # Has the report already been compiled?
        if self.is_compiled:
            raise AttributeError('report has already been compiled; cannot compile again')

        # Extend template
        _report = '{% extends "include/report_template.html" %}'

        # Add title
        _report += self._add_block('title', self.name)

        # Add TOC
        if self.toc:
            for section in self.sections:
                pass

        # Add report
        _report += self.report

        # Add footer
        if footer:
            _report += self._add_block('footer', '<a href="https://github.com/LockhartLab/izzy">built was izzy</a>')

        # Mark as compiled; save
        self.is_compiled = True
        self.report = _report

    # Launch report
    def launch(self):
        pass

    # Save report
    def save(self):
        pass


