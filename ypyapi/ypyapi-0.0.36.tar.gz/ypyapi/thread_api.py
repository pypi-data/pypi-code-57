#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2020/5/13 0:20
# @Author : yangpingyan@gmail.com
import threading
import heapq
import queue
from time import sleep


class PriorityQueue:
    '''
    put() higher priority get() earlier. default priority is 5.

    '''
    def __init__(self):
        self._queue = []
        self._count = 0
        self._cv = threading.Condition()
    def put(self, item, priority=5):
        with self._cv:
            heapq.heappush(self._queue, (-priority, self._count, item))
            self._count += 1
            self._cv.notify()

    def get(self, timeout=None):
        with self._cv:
            while len(self._queue) == 0:
                self._cv.wait(timeout=timeout)
                raise Exception("empty")
            return heapq.heappop(self._queue)[-1]

    def len(self):
        return len(self._queue)


if __name__ == '__main__':
    print("Mission start!")
    q = PriorityQueue()
    q.put(7)
    print(q.len())

    print(q.get())
    print(q.len())

    print("Mission complete!")

