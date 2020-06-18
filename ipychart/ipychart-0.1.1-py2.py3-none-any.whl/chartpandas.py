import pandas as pd
from pandas.api.types import is_numeric_dtype
from .chart import Chart


class ChartPandas(Chart):
    """
    A Jupyter - Chart.js bridge enabling interactive data visualization in the Jupyter notebook.

    Official documentation : https://nicohlr.gitlab.io/ipychart/
    Pandas Integration section : https://nicohlr.gitlab.io/ipychart/user_guide/advanced.html#pandas-integration

    This class is a daughter class of the main Chart class of ipychart. It is the ipychart Pandas API, allowing you to draw numerous charts directly from your dataframe or series.

    Args:
        data ([pd.DataFrame, pd.Series]): Your pandas data that will be used to draw the chart.
        kind (str): Type of chart. This string corresponds to the "type" argument of Chart.js.
        x (str, optional): The column of the data dataframe used as datapoints for x Axis. This argument is not used if data is of type pd.Series. Defaults to None.
        y (str, optional): The column of the data dataframe used as datapoints for y Axis. This argument is not used if data is of type pd.Series. Defaults to None.
        agg (str, optional): The aggregator used to gather data (ex: 'median' or 'mean'). This argument is not used if data is of type pd.Series. Defaults to None.
        dataset_options (dict, optional): These are options directly related to the dataset object (i.e. options concerning your data). Defaults to None.
        options (dict, optional): All options to configure the chart. This dictionary corresponds to the "options" argument of Chart.js. Defaults to None.
    """

    def __init__(self, data: (pd.DataFrame, pd.Series), kind: str, x: str = None, y: str = None,
                 agg: str = None, dataset_options: dict = None, options: dict = None):

        self.data = data
        self.kind = kind
        self.x = x
        self.y = y
        self.agg = agg
        self.dataset_options = dataset_options if dataset_options else {}
        self.options = options if options else {}

        # Check user input
        self._validate_input()

        # Transform pandas input into Chart.js input
        self._create_chart_inputs()

        # Use Chart class to create widget
        super().__init__(self.data, self.kind, self.options)

    def _validate_input(self):
        pass

    def _create_chart_inputs(self):
        """
        This function will prepare all the arguments to create a chart from the input of the user.
        Data are automatically aggregated before being send to the Chart.
        """

        data = {}

        if isinstance(self.data, pd.Series):
            data['labels'] = self.data.value_counts(ascending=True, sort=False).index.tolist()
            data['datasets'] = [{'data': self.data.value_counts(ascending=True, sort=False).round(4).tolist(), **self.dataset_options}]

        elif isinstance(self.data, pd.DataFrame):
            if is_numeric_dtype(self.data[self.y]):
                data['labels'] = self.data[self.x].value_counts(ascending=True, sort=False).index.tolist()
                if self.kind not in ['scatter', 'bubble']:
                    data['datasets'] = [{'data': self.data.groupby(self.x).agg(self.agg)[self.y].round(4).tolist(), **self.dataset_options}]
                    # TODO: Add axis names corresponding to cols
                else:
                    # TODO: Create dict with data points
                    pass
            else:
                raise AttributeError('Please select a numeric col as y')

        else:
            raise AttributeError('Wrong input format')

        self.data = data
