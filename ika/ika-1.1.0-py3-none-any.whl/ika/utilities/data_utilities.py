import numpy as np
from typing import List, Union
from datetime import timedelta


class DataUtilities:
    def __init__(self):
        pass

    @staticmethod
    def csv_to_list(csv_path):
        """
        From a path to a csv file,
        :param csv_path:
        :return:
        """
        pass

    @staticmethod
    def subset(data: List[float], subset_size: int) -> List[List[float]]:
        """
        Return a nested list (a list of lists). The inner lists are subgroups of the data, where each subset is of
        length of the sample size

        Example:
        data =  [1, 2, 3, 4, 5, 6]
        sample_size = 2
        return: [[1, 2], [3, 4], [5, 6]]

        :param List[float], data:
        :param int, subset_size: size of the subset of data to pass through to get a measurement
        :return:  List[List[float]]
        """
        m = len(data)
        subgroups = []
        for index in range(0, m, subset_size):
            subset = data[index:index + subset_size]
            subgroups.append(subset)
        return subgroups

    @staticmethod
    def subset_and_reduce(data: Union[List[float], List[timedelta]] = None,
                          subset_size: int = None
                          ) -> Union[List[float], List[timedelta]]:
        """
        Given a list of data, split the data into subgroups of subset_size, and return a list of only
        the first value of each subset. The point of this is the reduce the length of the some data by skipping over
        it at specific steps of subset_size

        :param Union[List[float], List[timedelta]], data: a 1D array of data
        :param int, subset_size: size of the subgroups for the data to be split into
        :return:
        """
        new_data: Union[List[float], List[timedelta]] = []
        subgroups: List[List[float]] = DataUtilities.subset(data=data, subset_size=subset_size)
        for subgroup in subgroups:
            first_value = subgroup[0]
            new_data.append(first_value)
        return new_data

    @staticmethod
    def subset_means(data: List[float], subset_size: int) -> List[float]:
        """
        For some data set, split it into subgroups based on the sample size, and return a list consisting of the
        mean of each subset

        :param List[float], data:
        :param int, subset_size: size of the subset of data to pass through to get a measurement
        :return:
        """
        means: List[float] = []
        subgroups: List[List[float]] = DataUtilities.subset(data=data, subset_size=subset_size)
        for subgroup in subgroups:
            subgroup_mean = np.mean(subgroup)
            means.append(subgroup_mean)
        return means

    @staticmethod
    def subset_ranges(data: List[float], subset_size: int) -> List[float]:
        """
        For some data set, split it into subgroups based on the sample size, and return a list consisting of
        the range of each subset

        :param List[float], data:
        :param int, subset_size: size of the subset of data to pass through to get a measurement
        :return:
        """
        ranges: List[float] = []
        subgroups: List[List[float]] = DataUtilities.subset(data=data, subset_size=subset_size)
        for subgroup in subgroups:
            subgroup_range = DataUtilities.range(data=subgroup)
            ranges.append(subgroup_range)
        return ranges

    @staticmethod
    def range(data: List[float],
              ) -> float:
        """
        Calculate the range for a list of float values.

        Equation:
        range = max(x_j) - min(x_j)
        where:
            x_j is the max value in some data
            x_j is the min value in some data

        :param List[float], data:
        :return: List[float], a list of the moving ranges
        """
        x_max = max(data)
        x_min = min(data)
        range = x_max - x_min
        return range

    @staticmethod
    def grand_average(data: List[float], subset_size: int) -> float:
        """
        Calculate the grand average for some data. Within this function, the data gets split up into subsets based
        on the subset size.

        A grand average is the average of all the subset of the data.

        Equation:
        grand_average = sum (X_bar_i) / k
        where:
            X_bar_i is the mean for the subset i in the data
            k is the number of data subsets

        :param List[float], data:
        :param int, subset_size: size of the subset of data to pass through to get a measurement
        :return: float, the average range of the data
        """
        k = len(data) / subset_size
        grand_average = 0
        subset_means = DataUtilities.subset_means(data=data, subset_size=subset_size)
        for subset_mean in subset_means:
            grand_average += subset_mean
        # actual grand average needs to be divided by the number of subsets
        grand_average = grand_average / k
        return grand_average

    @staticmethod
    def moving_range(data: List[float],
                     ) -> List[float]:
        """
        Calculate the moving range for a list of float values.

        Equation:
        MR_i = |x_i - x_x-1|
        where:
            MR_i is the moving range for some data at index i
            x_i is the value in some data at index i
            x_i-1 is the value in some data at index i-1

        A moving range for index i in data is: abs(data_i - data_i-1)
        For m values in data, there will be m-1 ranges

        :param List[float], data:
        :return: List[float], a list of the moving ranges
        """
        moving_ranges = [abs(data[index + 1] - data[index]) for index in range(len(data) - 1)]
        return moving_ranges