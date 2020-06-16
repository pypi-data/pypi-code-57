import queue
from threading import Thread
import time
import numpy

"""
Returns a batch of data from dataset.  Maybe shorter if not enough available data
"""
def get_batch(dataset, width, size):
    values = [[] for i in range(width)]
    start_time = time.time()
    try:
        for x in range(0, size):
            value = next(dataset)
            for i in range(len(value)):
                values[i].append(value[i])
    except StopIteration:
        print("Got stop: " + str(len(values[0])))
        # Only stop if there's no data
        if len(values[0]) == 0:
            raise
    end_time = time.time()
    print("Batch time (%d): %5.6f" % (size, end_time - start_time))
    return values

class BatchIterator(object):
    def __init__(self, source, size, limit = None):
        self._source = source
        self._size = size
        self._done = False
        self._limit = limit
        self._left = limit

    def __iter__(self):
        return self

    def __next__(self):
        if self._done:
            raise StopIteration

        if self._limit is not None:
            if self._left == 0:
                self._done = True
                raise StopIteration

            if self._left < self._size:
                self._done = True
                return get_batch(self._source, 3, self._left)
            else:
                self._left -= self._size

        batch = get_batch(self._source, 3, self._size)
        if len(batch[0]) != self._size:
            self._done = True
        return batch

class Source(object):
    def __init__(self, row_handler, train_function, test_function, width):
        self._train_function = train_function
        self._test_function = test_function
        self._width = width
        self._row_handler = row_handler

    def all_test_data(self, batch_size):
        return self._test_function(batch_size)

    def train_data(self, batch_size):
        return self._train_function(batch_size)

class _background_consumer(Thread):
    """Will fill the queue with content of the source in a separate thread.
    """
    def __init__(self, sentinel, queue, source, batch_size = 1000):
        Thread.__init__(self)
        self._queue = queue
        self._source = source
        self._sentinel = sentinel
        self._stopped = False
        self._batch_size = batch_size

    def _add_to_queue(self, datas, labels, ids):
        datas = numpy.array(datas, dtype = numpy.float)
        # print "Adding queue entry"
        if self._queue.qsize() == self._batch_size:
            print ("Queue Full")
        self._queue.put([datas, labels, ids])

    def run(self):
        count = 0
        datas = []
        labels = []
        ids = []
        for data, label, id in self._source:
            datas.append(data)
            labels.append(label)
            ids.append(id)
            if len(datas) == self._batch_size:
                self._add_to_queue(datas, labels, ids)
                datas = []
                labels = []
                ids = []
            if self._stopped:
                break

        if len(datas) > 0:
            self._add_to_queue(datas, labels, ids)
        # Signal the consumer we are done.
        self._queue.put(self._sentinel)

    def stop(self):
        self._stopped = True
        if not self._queue.empty():
            self._queue.get(False)

class BufferedDataset(object):
    """Buffers content of an iterator polling the contents of the given
    iterator in a separate thread.
    When the consumer is faster than many producers, this kind of
    concurrency and buffering makes sense.

    The size parameter is the number of elements to buffer.

    The source must be threadsafe.
    """
    def __init__(self, queue_size, batch_size, source):
            # Object used by _background_consumer to signal the source is exhausted
            # to the main thread.
        self._sentinel = object()
        self._queue = queue.Queue(queue_size)
        self._poller = _background_consumer(self._sentinel, self._queue, source, batch_size)
        self._poller.daemon = True
        self._poller.start()
        self._count = 0

    def __del__(self):
        self._poller.stop()

    def close(self):
        self._poller.stop()

    def __iter__(self):
        return self

    def __next__(self):
        # if self._queue.qsize() == 0:
        #       print ("Queue is empty")
        item = self._queue.get(True)
        self._count += 1

        if item is self._sentinel:
            raise StopIteration()
        return item
