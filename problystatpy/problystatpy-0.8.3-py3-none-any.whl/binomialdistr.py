from .generaldistr import Distribution
import math
import matplotlib.pyplot as plt


class Binomial(Distribution):
    """ Binomial distribution class for calculating and
    visualizing a Binomial distribution.

    Attributes
    ----------
    mean: float, default=0
        representing the mean value of the distribution

    stdev: float, default=1
        representing the standard deviation of the distribution

    data: list of floats
        a list of floats to be extracted from the data file

    p: float, default=0.5
        representing the probability of an event occurring

    n: float, default=20
        representing the size of data set
    """
    def __init__(self, prob=0.5, size=20):

        self.p = prob
        self.n = size

        Distribution.__init__(
            self,
            self.calculate_mean(),
            self.calculate_stdev()
        )

    def calculate_mean(self):
        """Function to calculate the mean from p and n

        Returns
        -------
        self.mean: float
            mean of the data set
        """
        self.mean = self.p * self.n

        return self.mean

    def calculate_stdev(self):
        """Function to calculate the standard deviation from p and n.

        Returns
        -------
        self.stdev: float
            standard deviation of the data set
        """
        self.stdev = math.sqrt(self.n * self.p * (1 - self.p))

        return self.stdev

    def replace_stats_with_data(self):
        """Function to calculate p and n from the data set.
        The function updates the p and n variables of the object.

        Returns
        -------
        self.p: float
            the p value
        self.n: float
            the n value
        """
        self.n = len(self.data)
        self.p = 1.0 * sum(self.data)/len(self.data)
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()

        return self.p, self.n

    def plot_bar(self):
        """Function to output a histogram of the
        instance variable data using matplotlib pyplot library.
        """
        plt.bar(x = ['0', '1'], height = [(1 - self.p) * self.n,self.p * self.n])
        plt.title('Bar Chart of Data')
        plt.xlabel('outcome')
        plt.ylabel('frequency')

    def pdf(self, k):
        """Probability density function calculator
        for the binomial distribution.

        Parameters
        -------
        k: float
            point for calculating the probability
            density function.

        Returns
        -------
        float, probability density function output
        """
        first = (math.factorial(self.n) / (math.factorial(k) * math.factorial(self.n-k)))
        second = (self.p**k) * (1 - self.p)**(self.n - k)

        return first * second

    def plot_binomial_pdf(self):
        """Function to plot the pdf of the binomial distribution.

        Returns
        -------
        float, probability density function output

        Returns:
        x: list
            x values for the pdf plot
        y: list
            y values for the pdf plot
        """
        x = []
        y = []

        for i in range(self.n+1):
            x.append(i)
            y.append(self.pdf(i))

        plt.bar(x, y)
        plt.title('Distribution of Outcomes')
        plt.xlabel('probability')
        plt.ylabel('outcome')
        plt.show()

        return x, y

    def __add__(self, other):
        """Function to add together two Binomial
        distributions with equal p.

        Parameters
        -------
        other: 2nd Binomial instance

        Returns
        -------
        result: 3rd Binomial instance
            sum of two Binomial distribution instances
        """
        try:
            assert self.p == other.p, 'p values are not equal'
        except AssertionError as error:
            raise

        result = Binomial()
        result.p = self.p
        result.n = self.n + other.n
        result.calculate_mean()
        result.calculate_stdev()

        return result

    def __repr__(self):
        """Function to output the characteristics
        of the Binomial instance.

        Returns
        -------
        string, Gaussian object characteristics
        """
        return "mean {}, standard deviation {}, p {}, n {}".format(self.mean, self.stdev, self.p, self.n)
