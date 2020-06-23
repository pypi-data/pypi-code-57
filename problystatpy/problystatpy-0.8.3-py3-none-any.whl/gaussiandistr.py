import math
import matplotlib.pyplot as plt
from .generaldistr import Distribution


class Gaussian(Distribution):
    """ Gaussian distribution class for calculating and
    visualizing a Gaussian distribution.

    Attributes
    ----------
    mean: float, default=0
        representing the mean value of the distribution

    stdev: float, default=1
        representing the standard deviation of the distribution

    data: list of floats
        a list of floats to be extracted from the data file
    """
    def __init__(self, mu=0, sigma=1):

        Distribution.__init__(self, mu, sigma)

    def calculate_mean(self):
        """Method to calculate the mean of the data set.

        Returns
        -------
        self.mean: float
            mean of the data set
        """
        avg = 1.0 * sum(self.data) / len(self.data)

        self.mean = avg

        return self.mean

    def calculate_stdev(self, sample=True):
        """Method to calculate the standard deviation
        of the data set.

        Parameters
        -------
        sample: bool, default=True
            whether the data represents a sample or population

        Returns
        -------
        self.stdev: float
            standard deviation of the data set
        """
        if sample:
            n = len(self.data) - 1
        else:
            n = len(self.data)

        mean = self.calculate_mean()

        sigma = 0

        for d in self.data:
            sigma += (d - mean) ** 2

        sigma = math.sqrt(sigma / n)

        self.stdev = sigma

        return self.stdev

    def plot_histogram(self):
        """Method to output a histogram of the instance variable data using
        matplotlib pyplot library.
        """
        plt.hist(self.data)
        plt.title("Histogram of Data",
                  fontweight ="bold")
        plt.xlabel("data")
        plt.ylabel("count")

    def pdf(self, x):
        """Probability density function calculator
        for the gaussian distribution.

        Parameters
        -------
        x: float
            point for calculating the probability density function

        Returns
        -------
        float, probability density function output
        """
        return (1.0 / (self.stdev * math.sqrt(2*math.pi))) * math.exp(-0.5*((x - self.mean) / self.stdev) ** 2)

    def plot_histogram_pdf(self, n_spaces = 50):
        """Method to plot the normalized histogram of the
        data and a plot of the probability density function
        along the same range.

        Parameters
        -------
        n_spaces: int, default=50
            number of data points

        Returns
        -------
        x: list
            x values for the pdf plot
        y: list
            y values for the pdf plot
        """
        mu = self.mean
        sigma = self.stdev

        min_range = min(self.data)
        max_range = max(self.data)

        interval = 1.0 * (max_range - min_range) / n_spaces

        x = []
        y = []

        for i in range(n_spaces):
            tmp = min_range + interval*i
            x.append(tmp)
            y.append(self.pdf(tmp))

        fig, axes = plt.subplots(2,sharex=True)
        fig.subplots_adjust(hspace=.5)
        axes[0].hist(self.data, density=True)
        axes[0].set_title('Normed Histogram of Data')
        axes[0].set_ylabel('Density')

        axes[1].plot(x, y)
        axes[1].set_title('Normal Distribution for \n Sample Mean and Sample Standard Deviation')
        axes[0].set_ylabel('Density')
        plt.show()

        return x, y

    def __add__(self, other):
        """Magic method to add together two Gaussian distributions.

        Parameters
        -------
        other: 2nd Gaussian instance

        Returns
        -------
        result: 3rd Gaussian instance
            sum of two Gaussian distribution instances
        """
        result = Gaussian()

        result.mean = self.mean + other.mean
        result.stdev = math.sqrt(self.stdev**2 + other.stdev**2)

        return result

    def __repr__(self):
        """Magic method to output the characteristics
        of the Gaussian instance.

        Returns
        -------
        string, Gaussian object characteristics
        """
        return "mean {}, standard deviation {}".format(self.mean, self.stdev)
