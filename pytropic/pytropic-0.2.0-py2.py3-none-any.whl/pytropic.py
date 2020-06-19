# -*- coding: utf-8 -*-
import collections
import math
import warnings

"""Main module."""


def sliding(string, n):
    for i in range(len(string) - n + 1):
        yield string[i: i+n]


class Model(object):
    """A counter for ngrams"""

    def __init__(self, size=2.0):
        self.size = size
        self.default_count = 0.5  # make a parameter?
        self.counter = collections.Counter()
        self.total = 0

    def update(self, string, muliplier=1):
        """
        Public: update a counter with a string, and a multiplier

        Examples

        counter = NGramCounter(2)
        counter.update_with_multiplier('01234', 1)

        string: The String to update with
        multiplier: The Integer describing how much weight (will often be 1)
        """
        for substr in sliding(string, self.size):
            self.counter[substr] += muliplier
            self.total += muliplier

    def count(self, ngram):
        """
        Public: get count for string, with default

         Examples

         counter = NGramCounter.new(2)
         counter.update('01234')
         counter.count('01')
         #=> 1
         counter.count('bob')
         #=> 0.5

         ngram: The String to check

        """
        return self.counter.get(ngram, self.default_count)

    def log_prob(self, key):
        if self.total == 0 or not key:
            return -math.inf
        count = self.count(key)
        return math.log(count, 2.0) - math.log(self.total, 2.0)

    def dump(self, io):
        for key, value in self.counter.items():
            io.write("{}\t{}\t{}\n".format(self.size, key, value))

    def predict(self, string):
        n_ngrams = 0
        log_prob_total = 0.0
        for ngram in sliding(string, self.size):
            n_ngrams += 1
            log_prob_total += self.log_prob(ngram)
        log_prob_average = log_prob_total / n_ngrams
        return {'log_prob_total': log_prob_total,
                'log_prob_average': log_prob_average,
                'size': int(n_ngrams)}

    def entropy(self, string):
        return -self.predict(string)['log_prob_average']

    def read(self, io):
        n = 0
        for line in io:
            n += 1
            try:
                _, ngram, count = line.strip().split("\t")
                count = float(count)
                self.counter[ngram] += count
                self.total += count
            except ValueError as err:
                warnings.warn("Invalid line at {}. Error: {}".format(n, err))

    def read_from_string(self, string):
        n = 0
        for line in string.split('\n'):
            n += 1
            try:
                _, ngram, count = line.strip().split("\t")
                count = float(count)
                self.counter[ngram] += count
                self.total += count
            except ValueError as err:
                warnings.warn("Invalid line at {}. Error: {}".format(n, err))


    def train(self, io):
        for line in io:
            self.update(line.strip())

    def train_with_multiplier(self, io):
        n = 0
        for line in io:
            n += 1
            try:
                text, count = line.strip().split("\t")
                count = float(count)
                self.update(text, count)
            except ValueError as err:
                warnings.warn("Invalid line at {}. Error: {}".format(n, err))
