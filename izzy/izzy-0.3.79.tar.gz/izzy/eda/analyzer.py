"""
analyzer.py
"""

from izzy.viz import plot

from izzy.features import granulate
from izzy.misc import flag_numeric, Refunction, get_name, pivot
from izzy.classification import create_engine_from_string, is_model_instance

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typelike import ListLike


# FeatureAnalyzer class
# TODO create a pipe ... and ability to run a pipe
class FeatureAnalyzer:
    """
    Analyze a model feature with outcome.
    """

    # Initialize class instance
    def __init__(self, x, y, z=None, clean=True, engine='LR', verbose=False):
        """
        Initialize FeatureAnalyzer

        Parameters
        ----------
        x : ListLike
            An independent variable to analyze
        y : ListLike
            The outcome to analyze against
        z : ListLike
            (Optional) A secondary feature for interaction analysis
        clean : bool
            Automatically clean the data by removing nulls and non-numeric values. (Default: True)
        engine : str or GenericModel
            String identifier for izzy model instance or engine of existing instance. (Default = 'LR')
        verbose : bool
            (Default: False)
        """

        # Get the names of feature, interaction, and outcome
        self.columns = [
            get_name(y, default='y'),
            get_name(x, default='x'),
        ]

        # Create data set
        self.data = pd.DataFrame({self.columns[0]: y,
                                  self.columns[1]: x}, columns=self.columns)

        # Define bins
        self.bins = {self.columns[1]: Refunction(granulate, bins=10, mode='equal')}

        # Add interaction z if necessary
        if z is not None:
            # Append z name to columns
            self.columns.append(get_name(z, default='z'))

            # Add z to data set
            self.data[self.columns[2]] = z

            # Add bin for z
            self.bins[self.columns[2]] = Refunction(granulate, bins=10, mode='equal')

        # Verbose flag
        self.verbose = verbose

        # Clean data by removing nulls and non-numeric values?
        if clean:
            self.clean()

        # Create model engine from string if necessary
        if isinstance(engine, str):
            engine = create_engine_from_string(engine)

        # Verify that engine has all the appropriate methods
        # assert is_model_instance(engine), 'must be instance of izzy model engine (instance of %s)' % type(engine)

        # Set the engine
        self.engine = engine

    # Include z?
    def _include_z(self):
        return True if len(self.columns) == 3 else False

        # Clip the data
    def clip(self, lower=None, upper=None, cut=False, axis=0):
        """
        Clip the data. If cut = False, we set any values < lower to lower and any values > upper to upper. If cut =
        True, values < lower or > upper are discarded.

        Parameters
        ----------
        lower : int or float
            Minimum value to set.
        upper : int or float
            Maximum value to set.
        cut : bool
            Should we cap/floor or cut?
        axis : int
            Which data-element should be clip?
                0 - outcome
                1 - feature
                2 - interaction
        """

        # Clip
        if not cut:
            self.data[self.columns[axis]].clip(lower=lower, upper=upper, inplace=True)

        # Cut
        else:
            x = self.data[self.columns[axis]] >= lower
            y = self.data[self.columns[axis]] <= upper
            self.data = self.data[x & y]

    # Clean the data
    def clean(self):
        """
        Clean the data. This removes any nulls and non-numeric records.
        """

        # Flag the numeric records
        is_numeric = flag_numeric(self.data, logical_and=True)

        # If verbose, talk about the number of non-numeric records
        if self.verbose:
            n = np.sum(is_numeric)
            d = len(is_numeric)
            p = np.round(100.*n/d)
            print('{0}% ({1} out of {2}) records are numeric'.format(p, n, d))

        # Produce filtered data set by flag and make sure data is float
        self.data = self.data[is_numeric].astype(float)

    # Return granulated (binned) data
    def granulate(self, include_z=True):
        # Include z?
        if include_z:
            include_z = self._include_z()

        # Create copy of data
        data = self.data.copy()

        # Loop over columns and bin
        end = 2 if not include_z else 3
        for column in self.columns[1:end]:
            data[column] = self.bins[column](data[column])

        # Return
        return data

    # Impute
    # TODO add impute logic
    def impute(self):
        pass

    # Report the performance of our feature vs. the outcome
    def performance(self, include_z=True):
        """
        Returns
        -------
        result :
        """

        # First, train model without interactions
        x = self.data[[self.columns[1]]]
        y = self.data[self.columns[0]]
        self.engine.fit(x, y)
        result = self.engine.performance(x, y)

        # Second if we have an interaction term, add it to the report
        if include_z and len(self.columns) == 3:
            x = self.data[self.columns[1:2]]
            self.engine.fit(x, y)
            result = (result, self.engine.performance(x, y))

        # Return
        return result

    # Pivot table
    def pivot(self, aggfunc='mean', include_z=False):
        # Granulate (this checks if we should actually include z)
        data = self.granulate(include_z=include_z)

        # Pivot arguments
        kwargs = {'data': data, 'index': self.columns[1], 'values': self.columns[0], 'aggfunc': aggfunc}
        if include_z:
            kwargs['columns'] = self.columns[2]

        # Return table
        return pivot(**kwargs)

    # Pivot, x vs y
    def pivot1d(self, aggfunc='mean'):
        return self.pivot(aggfunc=aggfunc, include_z=False)

    # Pivot, x vs z vs y
    def pivot2d(self, aggfunc='mean'):
        return self.pivot(aggfunc=aggfunc, include_z=True)

    # Plot
    def plot(self, aggfunc='mean'):
        fviz(fan=self, include_z=True, aggfunc=aggfunc)

    # Plot 1D
    def plot1d(self, aggfunc='mean'):
        fviz1d(fan=self, aggfunc=aggfunc)

    # Plot 2D
    def plot2d(self, aggfunc='mean'):
        fviz2d(fan=self, aggfunc=aggfunc)


# Plot feature vs. outcome (wrapper for FeatureAnalyzer)
def fan1d(x, y, clean=True, xlower=None, xupper=None, xcut=False, xbins=10, xmode='equal', **kwargs):
    """
    PLot feature vs. outcome. Recommended to use FeatureAnalyzer directly instead of this function.

    mode quantile, equal, distinct

    Parameters
    ----------
    x : array-like
        The independent variable
    y : array-like
        The dependent variable. Must be same length as `feature`.
    xlower : float
        The left boundary
    xupper : float
        The right boundary
    xcut : bool
        Turns clip from capping / flooring to firm exclusionary boundaries.
    xbins : int or array-like
        If int, number of quantiles to split the data into. If array-like, specify the break points.
    xmode : str


    Returns
    -------
    FeatureAnalyzer
    """

    # Launch FeatureAnalyzer
    fan = FeatureAnalyzer(x=x, y=y, clean=clean, verbose=False)

    # Clip feature
    fan.clip(lower=xlower, upper=xupper, cut=xcut, axis=1)

    # Set bins (otherwise FeatureAnalyzer automatically does this)
    if xbins is not None:
        fan.bins[fan.columns[1]] = Refunction(granulate, bins=xbins, mode=xmode)

    # Return
    return fan


# 2D plot, feature vs interaction vs outcome
# Can I finagle this to call fan1d first? Not super important at the moment.
def fan2d(x, z, y,
          xlower=None, xupper=None, xcut=False, xbins=10, xmode='equal',
          zlower=None, zupper=None, zcut=False, zbins=10, zmode='equal'):

    # Launch FeatureAnalyzer
    fan = FeatureAnalyzer(x=x, z=z, y=y, clean=True, verbose=False)

    # Clip
    fan.clip(lower=xlower, upper=xupper, cut=xcut, axis=1)
    fan.clip(lower=zlower, upper=zupper, cut=zcut, axis=2)

    # Set bins
    if xbins is not None:
        fan.bins[fan.columns[1]] = Refunction(granulate, bins=xbins, mode=xmode)
    if zbins is not None:
        fan.bins[fan.columns[2]] = Refunction(granulate, bins=zbins, mode=zmode)

    # Return
    return fan


# Visualize FeatureAnalyzer
def fviz(**kwargs):
    """

    Parameters
    ----------
    kwargs

    Returns
    -------

    """

    # Parse fviz-specific parameters
    # TODO move these to definition
    aggfunc = kwargs.get('aggfunc', 'mean')
    include_z = kwargs.get('include_z', False)
    figsize = kwargs.get('figsize', (20, 10))
    savefig = kwargs.get('savefig', None)

    # If fan is provided in kwargs, set
    if 'fan' in kwargs.keys():
        fan = kwargs['fan']
        assert isinstance(fan, FeatureAnalyzer), 'fan must be FeatureAnalyzer instance'

    # Otherwise, create FeatureAnalyzer
    else:
        function = fan1d
        if 'z' in kwargs.keys():
            function = fan2d
        fan = function(**kwargs)

    # Produce pivot table
    table = fan.pivot(aggfunc=aggfunc, include_z=include_z)

    # Build plot
    if len(table.columns) == 1:
        plot(table.index, table.iloc[:, 0])
    else:
        pass


# Call fviz to get x vs y plot
def fviz1d(**kwargs):
    kwargs['include_z'] = False
    fviz(**kwargs)


# Calls fviz to get x vs z vs y plot
def fviz2d(**kwargs):
    kwargs['include_z'] = True
    fviz(**kwargs)


# To be deprecated, alias of fviz1d
# TODO specify arguments
# def risk1d(**kwargs):
    # return fviz1d(**kwargs)
def risk1d(x, y, bins=10):
    # TODO is granulate a dumb name? This could just be called bin or bucket
    df = pd.DataFrame({
        'x': granulate(x, bins=bins, mode='equal'),
        'y': y
    })
    xy = df.pivot_table(index='x', values='y', aggfunc='mean')
    plt.figure()
    plt.plot(xy.index.values, xy['y'].values)
    plt.show()

# To be deprecated, alias of fviz2d
def risk2d(**kwargs):
    return fviz2d(**kwargs)

# TODO create function to run feature analyzer on DataFrame
