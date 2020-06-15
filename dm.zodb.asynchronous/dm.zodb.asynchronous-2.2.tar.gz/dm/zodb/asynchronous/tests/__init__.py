"""Test code.

This is a test suite for `zope.testing` and its test runner.
"""
from __future__ import print_function

from unittest import TestCase


# Auxiliaries to catch and compare output
class _Output(object):
  def __init__(self): self.data = []
#
  def write(self, s): self.data.append(s)
#
  def get_and_reset_output(self):
    r = "".join(self.data)
    self.__init__()
    return r

_output = _Output()

py_print = print
def print(*args, **kw): py_print(*args, file=_output, **kw)

get_and_reset_output = _output.get_and_reset_output
    


# Python version compatibility
class TestCase(TestCase):
  if not hasattr(TestCase, "assertIs"):
    def assertIs(self, a, b, *args): self.assertTrue(a is b, *args)
  if not hasattr(TestCase, "assertIsInstance"):
    def assertIsInstance(self, a, b, *args):
      self.assertTrue(isinstance(a, b), *args)
  



