"""
chart.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

from .base import Base

import numpy as np
import pandas as pd
import string
import sys

# Reference to this module
this = sys.modules[__name__]

# Cache to store data in session
this.cache = []


# TODO add method to create from dataframe
# TODO handle when x is a date (needs to be new Date(...))
# TODO https://stackoverflow.com/questions/8950761/google-chart-redraw-scale-on-window-resize
class Chart(Base):
    """
    Generate the HTML for charts with Google Visualization API
    """

    # Initialize class instance
    def __init__(self, kind='line'):
        """
        Initialize instance of Chart class

        Parameters
        ----------
        kind : str
            Kind of chart to create (e.g., line, ...)
        """

        # Kind of chart
        self.kind = kind

        # Generate _id randomly
        self._id = _generate_id()

        # Data for plotting
        self._data = pd.DataFrame({'x': []})
        self._labels = []
        self._colors = []
        self._styles = []

        # Chart style
        self._x_title = None
        self._y_title = None
        self._legend = None

    # Legend
    def legend(self, position='bottom'):
        self._legend = position

    # Plot
    def plot(self, x, y, label=None, color=None, style=None):
        # Create label for y if necessary
        if label is None:
            label = 'y' + str(len(self._data.columns) - 1)

        # Create DataFrame for x, y and combine with class data
        _data = pd.DataFrame({'x': x, label: y})
        self._data = self._data.merge(_data, how='outer', on='x').fillna(0)

        # Save information
        self._labels.append(label)
        self._colors.append(color)
        self._styles.append(style)

    # Show the Google Chart
    def show(self, render_loader=True, width='100%', height='500px'):
        # Render loader if necessary
        output = '' if not render_loader else """
            <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        """

        # Open script section
        output += """
            <script type="text/javascript">
        """

        # Script preamble
        output += """
            google.charts.load("current", {{packages: ["corechart", "{kind}"]}});
            google.charts.setOnLoadCallback(drawChart_{id});
            function drawChart_{id}() {{
        """.format(kind=self.kind, id=self._id)

        # Specify data, initialize options
        output += """
            var data = google.visualization.arrayToDataTable({data});
            var options = {{
        """.format(data=repr(np.vstack([self._data.columns, self._data.values]).tolist()))

        # Formatting for x axis
        output += """
            hAxis: {{title: "{x_title}"}},
        """.format(x_title=self._x_title if self._x_title is not None else '')

        # Formatting for y axis
        output += """
            vAxis: {{title: "{y_title}"}},
        """.format(y_title=self._y_title if self._y_title is not None else '')

        # Legend
        output += """
            legend: {{position: "{legend}"}},
        """.format(legend=self._legend if self._legend is not None else 'none')

        # Close out script
        output += """
            }};
            var chart = new google.visualization.LineChart(document.getElementById("{id}"));
            chart.draw(data, options);
            }}
            </script>
            <div id="{id}" style="width: {width}; height: {height};"></div>
        """.format(id=self._id, width=width, height=height)

        # Return
        return output

    # Set x title
    def xtitle(self, title):
        self._x_title = title

    # Set y title
    def ytitle(self, title):
        self._y_title = title


class GoogleTable:
    def __init__(self, data, row_numbers=True):
        self._data = data
        self._id = _generate_id()

        self.row_numbers = row_numbers

    # Show the Google Table
    def show(self, render_loader=True):
        # Render loader if necessary
        output = '' if not render_loader else """
            <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        """

        # Open script section
        output += """
            <script type="text/javascript">
        """

        # Script preamble
        output += """
            google.charts.load("current", {{packages: ["table"]}});
            google.charts.setOnLoadCallback(drawTable_{id});
            function drawTable_{id}() {{
        """.format(id=self._id)

        # Specify data (reset index to get row names), initialize options
        _data = self._data.reset_index().fillna(0)
        output += """
            var data = google.visualization.arrayToDataTable({data});
            var options = {{
        """.format(data=repr(np.vstack([_data.columns, _data.values]).tolist()))

        # Options
        # TODO add ability to adjust width, height
        output += """
            showRowNumber: {row_numbers},
            width: "100%",
        """.format(row_numbers='true' if self.row_numbers else 'false')

        # Close out script
        output += """
            }};
            var table = new google.visualization.Table(document.getElementById("{id}"));
            table.draw(data, options);
            }}
            </script>
            <div id="{id}"></div>
        """.format(id=self._id)

        # Return
        return output


# Helper function to generate a unique ID
def _generate_id(n=10):
    while True:
        _id = ''.join(np.random.choice(list(string.ascii_lowercase), n))
        if _id not in this.cache:
            break
    this.cache.append(_id)
    return _id
