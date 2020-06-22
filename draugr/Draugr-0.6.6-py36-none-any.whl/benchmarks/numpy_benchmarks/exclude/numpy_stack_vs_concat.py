#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Christian Heider Nielsen'
__doc__ = r'''

           Created on 03/04/2020
           '''

import numpy
import time

def test_perf_stack_vs_concat():
  samples = 10
  for _ in range(samples):
    a = numpy.zeros((1000,1000))
    b = numpy.zeros((1000,1000))
    s1 = time.time()
    c = numpy.stack((a,b))
    s2 = time.time()
    d = numpy.concatenate((a,b),axis=0)
    s3 = time.time()

    print(f"view: {s2 - s1}")
    print(f"delete: {s3 - s2}")


def test_perf_stack_vs_concat2():
  samples = 10
  for _ in range(samples):
    a = numpy.zeros((1000,1000))
    s1 = time.time()
    c = numpy.delete(a,0,0)
    s2 = time.time()
    b = a[1:]
    s3 = time.time()

    print(f"delete: {s2 - s1}")
    print(f"view: {s3 - s2}")

  #assert b == c
