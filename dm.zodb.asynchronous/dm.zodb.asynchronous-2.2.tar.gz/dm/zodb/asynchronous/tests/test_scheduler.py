"""Tests for `scheduler.TransactionalScheduler`.

Note: `PersistentTransactionalScheduler` is tested in `test_zope2`.
"""
from __future__ import print_function

from unittest import makeSuite, TestSuite
from time import sleep
from transaction import commit, abort

from ..scheduler import TransactionalScheduler
from . import print, get_and_reset_output, TestCase


def show(*args, **kw):
  print ("show:", args, kw)
  return "ok"

def exc(): raise Exception()

class TestSchedulerMixin(object):
  def wait(self, sid):
    while True:
      r = self.s.get_result(sid)
      if r is not False: break
      sleep(0.01)
      abort() # allow us to see modified state
    return r


class TestTransactionalScheduler(TestCase, TestSchedulerMixin):
  def setUp(self):
    get_and_reset_output()
    self.s = TransactionalScheduler()

  def tearDown(self): get_and_reset_output()

  def test_unfinished_abort(self):
    sid = self.s.schedule(show, 1, 2, a="a")
    self.assertEqual(self.s.get_result(sid), False)
    self.assertEqual("", get_and_reset_output())
    abort()
    self.assertIs(self.s.get_result(sid), None)
    self.assertEqual("", get_and_reset_output())

  def test_commit(self):
    sid = self.s.schedule(show, 1, 2, a="a")
    commit()
    self.assertEqual(self.wait(sid), ("ok", None))
    self.assertEqual("show: (1, 2) {'a': 'a'}\n", get_and_reset_output())
    abort()
    self.assertEqual(self.s.get_result(sid), ("ok", None))
    commit()
    self.assertIs(self.s.get_result(sid), None)

  def test_exception(self):
    sid = self.s.schedule(exc)
    commit()
    # We log something here, but `assertLogs` may not yet be available
    r, e = self.wait(sid)
    self.assertIs(r, None)
    self.assertIsInstance(e, Exception)
    self.assertIs(getattr(e, "__traceback__", None), None)



def test_suite():
  return TestSuite([makeSuite(TestTransactionalScheduler)])


