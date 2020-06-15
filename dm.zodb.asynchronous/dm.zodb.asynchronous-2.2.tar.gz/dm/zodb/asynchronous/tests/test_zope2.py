"""Tests for Zope adaptations of `PersistentContext` and `PersistentTransactionalScheduler`.

Those tests also verify the abstract base classes.
"""
from __future__ import print_function

from unittest import makeSuite, TestSuite
from transaction import commit, abort, get as get_transaction

from ZODB.DemoStorage import DemoStorage
from ZODB.DB import DB
from ZODB.POSException import ConflictError
from persistent import Persistent

import Zope2

from ..zope2 import PersistentTransactionalScheduler, PersistentContext

from . import TestCase, print, get_and_reset_output
from . test_scheduler import TestSchedulerMixin


class ZopeLayer(object):
  """Sets up a minimal mock Zope environment with a ZODB."""
  @classmethod
  def setUp(cls):
    cls._db = Zope2.DB
    db = Zope2.DB = DB(DemoStorage())
    root = db.open().root()
    root["s"] = PersistentTransactionalScheduler()
    for i in range(3): root[i] = _PO(i)
    commit()
    root._p_jar.close()

  @classmethod
  def tearDown(cls):
    abort()
    Zope2.DB.close()
    Zope2.DB = cls._db


class TestBase(TestCase):
  layer = ZopeLayer

  def setUp(self):
    root = self.root = Zope2.DB.open().root()
    self.s = root["s"]

  def tearDown(self):
    abort()
    self.root._p_jar.close()


class TestPersistentContext(TestBase):
  def setUp(self):
    TestBase.setUp(self)
    # to avoid the need for a separate thread
    #  the case with a separate thread is implicitely tested in
    #  `TestPersistentTransactionalScheduler`
    PersistentContext().set_root_connection(self.root._p_jar)

  def test_elementary(self):
    root = self.root
    c = PersistentContext(root[0], root[1], a=root[2])
    self.assertEqual(len(c), 2)
    self.assertEqual(list(c.keys()), ["a"])
    self.assertIs(c[0], root[0])
    self.assertIs(c["a"], root[2])

  def test_uncommited(self):
    root = self.root
    root[3] = _PO(3)
    c = PersistentContext(root[3])
    self.assertIs(c[0], root[3])

  def test_unplaced(self):
    self.assertRaises(ValueError, PersistentContext, _PO(4))

  def test_not_persistent(self):
    self.assertRaises(AttributeError, PersistentContext, 1)


class _PO(Persistent):
  """Auxiliary persistent class."""
  def __init__(self, i): self.i = i

  
##########################################################################
## Tests for `PersistentTransactionalScheduler`

class TestPersistentTransactionalScheduler(TestBase, TestSchedulerMixin):
  """Note: these tests have (harmless) side effects."""
  def setUp(self):
    TestBase.setUp(self)
    get_and_reset_output()

  def tearDown(self):
    get_and_reset_output()
    TestBase.tearDown(self)

  def test_simple(self):
    s = self.s
    sid = s.schedule(_tpts_return_1)
    commit()
    self.assertEqual(self.wait(sid), (1, None))
    abort()
    self.assertEqual(s.get_result(sid), (1, None))
    commit()
    self.assertIs(s.get_result(sid), None)

  def test_retry_unsuccessful(self):
    s = self.s
    sid = s.schedule(_tpts_conflict)
    commit()
    r = self.wait(sid)
    self.assertIs(r[0], None)
    self.assertIsInstance(r[1], ConflictError)
    self.assertEqual(get_and_reset_output(), "conflict\n" * 4)

  def test_retry_successful(self):
    s = self.s
    sid = s.schedule(_tpts_Retry())
    commit()
    self.assertEqual(self.wait(sid), (1, None))
    self.assertEqual(get_and_reset_output(), "conflict\n")

   # we cannot test that even the schedule state cannot be
   #   updated (in this case, a critical log message should be
   #   generated and `get_result` would always return `False`.

# Helpers
def _tpts_return_1(): return 1

def _tpts_conflict():
  print("conflict")
  raise ConflictError()

class _tpts_Retry(object):
      retried = False
      def __call__(self):
        if self.retried: return 1
        else: print("conflict"); self.retried = True; raise ConflictError



  
##########################################################################
## Boilerplate for `zope.testrunner`

def test_suite():
  return TestSuite([makeSuite(c) for 
    c in (TestPersistentContext, TestPersistentTransactionalScheduler)
                    ])
