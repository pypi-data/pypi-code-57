import numpy
import numpy.random


class OnceThrough(object):
    def __init__(self, values, batch_size, max_examples):
        self._values = values
        self._batch_size = batch_size
        self._length = len(values[0]) if max_examples == -1 else min(len(values[0]), max_examples)
        self._position = 0

    def __iter__(self):
        return self

    def __next__(self):
        if (self._position == self._length):
            raise StopIteration

        position = self._position
        self._position = min(self._length, position + self._batch_size)
        return [val[position:self._position] for val in self._values]


class DataSets(object):
    def __init__(self, row_handler, data, labels, ids, weights, test_fraction, shuffle_data=True, is_control = None):
        """

        :param row_handler:
        :param data:
        :param labels:
        :param ids:
        :param weights:
        :param test_fraction:
        :param shuffle_data:  If set to false, data is not shuffled before being chunked into train/test folds.
        This is useful if you want to partition data is a specific way.
        """
        self._row_handler = row_handler
        self.width = row_handler.width
        self._test_len = int(len(data) * test_fraction)
        self._test_fraction = test_fraction
        if is_control is None:
            is_control = numpy.zeros([len(data)])

        if shuffle_data:
            self._data, self._labels, self._ids, self._weights, self._is_control = \
                shuffle([data, labels, ids, weights, is_control])
        else:
            self._data = data
            self._labels = labels
            self._ids = ids
            self._weights = weights
            self._is_control = is_control

        self._partition_count = 0
        self._partition()

    def get_num_examples(self):
        """
        :return: The number of training and eval examples.
        """
        return len(self._data)

    def get_row_by_id(self, row_id):
        index = numpy.nonzero(self._ids == row_id)

        if len(index) == 0:
            return None
        else:
            return self._data[index[0]]

    def _slice_arrays(self, datas, test_start, test_end):
        """ Takes array of all-data arrays and slices each input array into test & train numpy arrays
        """
        all_test = []
        all_train = []
        for data in datas:
            test = data[test_start: test_end]
            if test_start > 0:
                train_start = data[0: test_start]
                train_end = data[test_end:]
                train = numpy.concatenate((train_start, train_end))
            else:
                train = data[test_end:]
            all_test.append(test)
            all_train.append(train)

        return all_train, all_test

    def _partition(self):
        test_start = self._partition_count * self._test_len
        test_end = (self._partition_count + 1) * self._test_len
        train, test = self._slice_arrays([self._data, self._labels, self._ids, self._weights, self._is_control], test_start, test_end)
        self.test = DataSet(test[0], test[1], test[2], test[3], test[4], self.width)
        self.train = DataSet(train[0], train[1], train[2], train[3], test[4], self.width)

    def repartition(self):
        self._partition_count += 1
        if (self._partition_count + 0.9) * self._test_fraction > 1.0:
            self._partition_count = 0
        self._partition()

    def get_test_control(self):
        data = []
        weights=[]
        labels = []
        ids = []
        for i, entry in enumerate(self.test._is_control):
            if entry:
                data.append(self.test._data[i])
                weights.append(self.test._weights[i])
                labels.append(self.test._labels[i])
                ids.append(self.test._ids[i])

        return DataSet(data, labels, ids, weights, numpy.ones([len(data)]), self.width)

def shuffle(arrays):
    vals = []
    perm = numpy.random.permutation(len(arrays[0]))

    for val in arrays:
        vals.append(val[perm])

    return vals


class DataSet(object):
    def __init__(self, data, labels, ids, weights, is_control, width):
        """Construct a DataSet.
        """
        self._width = width
        self._data = data
        self._labels = labels
        self._is_control = is_control
        self._weights = weights
        self._ids = ids
        self._num_examples = len(data)
        self._epochs_completed = 0
        self._index_in_epoch = 0

    def once_through(self, batch_size, max_examples=-1):
        return OnceThrough([self._data, self._labels, self._ids], batch_size, max_examples)

    def copy(self):
        return DataSet(numpy.copy(self._data), numpy.copy(self._labels), numpy.copy(self._ids),
                       numpy.copy(self._weights) if self._weights is not None else None, self._width)

    @property
    def data(self):
        return self._data

    @property
    def labels(self):
        return self._labels

    @property
    def ids(self):
        return self._ids

    @property
    def num_examples(self):
        return self._num_examples

    @property
    def epochs_completed(self):
        return self._epochs_completed

    def next_batch(self, batch_size):
        """Return the next `batch_size` examples from this data set."""
        start = self._index_in_epoch
        self._index_in_epoch += batch_size
        if self._index_in_epoch > self._num_examples:
            # Finished epoch
            self._epochs_completed += 1
            # Shuffle the data
            self._data, self._labels, self._ids = shuffle([self._data, self._labels, self._ids])

            # Start next epoch
            start = 0
            self._index_in_epoch = batch_size
            assert batch_size <= self._num_examples
        end = self._index_in_epoch
        return self._data[start:end], self._labels[start:end]
