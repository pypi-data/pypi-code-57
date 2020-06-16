import numpy
import csv
import time
from bytegain.custom.model_data.dataset import OnceThrough

class LstmField(object):
    def __init__(self, width):
        self._width = width

    def is_sparse(self):
        return self._width > 0

class LstmCsvSpec(object):
    def __init__(self, fields, max_events):
        self._fields = fields
        self._max_events = max_events
        self._width = 0
        for field in self._fields:
            if field.is_sparse():
                self._width += field._width
            else:
                self._width += 1

    def max_events(self):
        return self._max_events

    def max_width(self):
        return self._width * self._max_events

    def sparse_width(self):
        return len(self._fields) * self._max_events

    def field_widths(self):
        return [x._width for x in self._fields]

    def create_batch_data(self, batch):
        batch_size = len(batch)
        output = numpy.zeros([batch_size, self._max_events, self._width], numpy.int)

        for row_index, row in enumerate(batch):
            for i in range (self._max_events):
                input_offset = i * len(self._fields)
                output_offset = 0
                for field_index, field in enumerate(self._fields):
                    value = row[input_offset + field_index]
                    if field.is_sparse():
                        output[row_index][i][value + output_offset] = 1
                        output_offset += field._width
                else:
                    output[row_index][i][output_offset] = value
                    output_offset += 1

        return output

    def parse_csv_row(self, row):
        id = int(row[0])
        leased = int(row[1])
        events = numpy.zeros(self._max_events * len(self._fields))
        offset = 0
        event_count = 0
        for event in row[2:][-self._max_events:]:
            event_count += 1
            event_fields = event.split(",")
            for bucket, field in zip(self._fields, event_fields):
                int_value = int(field)
                # We use -1 & -2 to indicate null, or unknown, but for sparse need all >=0
                if bucket.is_sparse():
                    int_value += 2
                    if int_value > bucket._width or int_value < 0:
                        raise Exception("Invalid sparse value %d. Max width: %d" % (int_value, bucket._width))
                events[offset] = int_value
                offset += 1

        return id, leased, events, event_count

AL_SPEC = LstmCsvSpec([LstmField(16), LstmField(5), LstmField(0)], 20)

class LstmDataset(object):
    def __init__(self, filename, lstm_spec, test_fraction = 0.1, random_seed=83243312):
        """
        Datset for LSTM data
        """
        start_time = time.time()
        self._spec = lstm_spec

        self._data = []
        self._ids = []
        self._labels = []
        self._event_counts = []
        with open(filename, "r") as f:
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                id, label, events, event_count = lstm_spec.parse_csv_row(row)
                self._ids.append(id)
                self._labels.append(label)
                self._event_counts.append(event_count)
                self._data.append(events)

        self._ids = numpy.array(self._ids, dtype = numpy.int)
        self._labels = numpy.array(self._labels, dtype = numpy.float)
        self._data = numpy.array(self._data, dtype = numpy.int)
        self._event_counts = numpy.array(self._event_counts, dtype = numpy.int)
        self._ids, self._labels, self._data, self._event_counts = shuffle([self._ids, self._labels, self._data, self._event_counts])
        self._test_len = int(len(self._ids) * test_fraction)
        self._partition_count = 0
        numpy.random.seed(random_seed)
        self._partition()
        print("Loaded %d rows in %ds" % (len(self._ids), time.time() - start_time))

    def event_width(self):
        return self._spec._width

    def max_events(self):
        return self._spec._max_events

    def _partition(self):
        test_start = self._partition_count * self._test_len
        test_end = (self._partition_count + 1) * self._test_len
        self.test = LstmSet(self._spec, self._data[test_start : test_end], self._event_counts[test_start : test_end], self._labels[test_start : test_end], self._ids[test_start : test_end],
                self.event_width(), self.max_events())
        if self._partition_count != 0:
            data_start, counts_start, label_start, ids_start = self._data[0:test_start], self._event_counts[0:test_start], self._labels[0:test_start], self._ids[0:test_start]
            data_end, counts_end, label_end, ids_end = self._data[test_end:], self._event_counts[test_end:], self._labels[test_end:], self._ids[test_end:]

            self.train = LstmSet(self._spec, numpy.concatenate((data_start, data_end)), numpy.concatenate((counts_start, counts_end)), numpy.concatenate((label_start, label_end)), numpy.concatenate((ids_start, ids_end)),
             self.event_width(), self.max_events())
        else:
            self.train = LstmSet(self._spec, self._data[test_end:], self._event_counts[test_end:], self._labels[test_end:], self._ids[test_end:],
             self.event_width(), self.max_events())

    def repartition(self):
        self._partition_count += 1
        if (self._partition_count + 0.9) * self._test_fraction > 1.0:
            self._partition_count = 0
        self._partition()

def shuffle(arrays):
    vals = []
    perm = numpy.random.permutation(len(arrays[0]))

    for val in arrays:
        vals.append(val[perm])

    return vals

class LstmSet(object):
    def __init__(self, lstm_spec, data, event_counts, labels, ids, event_width, max_events):
        """Construct a DataSet.
        """
        self._lstm_spec = lstm_spec
        self._event_width = event_width
        self._max_events = max_events
        self._data = data
        self._event_counts = event_counts
        self._labels = labels
        self._ids = ids
        self._num_examples = len(data)
        self._epochs_completed = 0
        self._index_in_epoch = 0

    def once_through(self, batch_size, max_examples = -1):
        # if max_examples > 0:
        #       expanded = self._lstm_spec.create_batch_data(self._data[0:max_examples])
        # else:
        #       expanded = self._lstm_spec.create_batch_data(self._data)

        return OnceThrough([self._data, self._event_counts, self._labels, self._ids], batch_size, max_examples)

    @property
    def data(self):
        return self._data

    @property
    def event_counts(self):
        return self._event_counts

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
            self._data, self._labels
            # Shuffle the data
            self._data, self._event_counts, self._labels, self._ids = shuffle([self._data, self._event_counts, self._labels, self._ids])

            # Start next epoch
            start = 0
            self._index_in_epoch = batch_size
            assert batch_size <= self._num_examples
        end = self._index_in_epoch
        # batch_data = self._lstm_spec.create_batch_data(self._data[start:end])
        return self._data[start:end], self._event_counts[start:end], self._labels[start:end]
