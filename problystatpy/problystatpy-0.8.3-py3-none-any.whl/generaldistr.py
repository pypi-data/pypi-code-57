class Distribution:
    """Base class for distribution function classes.

    Use derived class after importing this class,
    in order to read data files.

    """

    def __init__(self, mu=0, sigma=1):
        """ Generic distribution class for calculating and
        visualizing a probability distribution.

        Attributes
        ----------
        mean: float, default=0
            representing the mean value of the distribution

        stdev: float, default=1
            representing the standard deviation of the distribution

        data: list of floats
            a list of floats to be extracted from the data file
        """

        self.mean = mu
        self.stdev = sigma
        self.data = []

    def read_data_file(self, file_name):
        """Function to read in data from a txt file.
        The txt file should have one number (float) per line.
        The numbers are stored in the data attribute.

        Parameters
        ----------
        file_name: string
            name of a file to read from
        """
        with open(file_name) as file:
            data_list = []
            line = file.readline()
            while line:
                data_list.append(int(line))
                line = file.readline()
        file.close()

        self.data = data_list
