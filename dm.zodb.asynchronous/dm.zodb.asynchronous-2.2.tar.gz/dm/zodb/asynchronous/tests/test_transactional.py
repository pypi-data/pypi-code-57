"""Test for module `transactional`."""
from __future__ import print_function

from unittest import TestCase, makeSuite, TestSuite
import transaction

from . import print, get_and_reset_output
from ..transactional import transactional


def register_hooks(text):
   """register transaction hooks such that we can monitor transaction operation"""
   T = transaction.get()
   def show(status, type): print ("transaction %s:" % type, text)
   T = transaction.get() # current transaction
   T.addAfterCommitHook(show, ("commit",))
   T.addAfterAbortHook(show, (False, "abort"))
   

class TestTransactional(TestCase):
  def setUp(self): get_and_reset_output()
  tearDown = setUp

  def test_without_exception(self):
    @transactional
    def f(a=1, b=2):
      register_hooks("f")
      print ("f:", a, b)
      g(2*a)
      print ("after g call")
      return a + b
    
    @transactional
    def g(x):
      register_hooks("g")
      print ("g:", x)
    
    f()
    self.assertEqual("""\
f: 1 2
g: 2
after g call
transaction commit: f
transaction commit: g
""",
                     get_and_reset_output()
                     )

    g(1)
    self.assertEqual("""\
g: 1
transaction commit: g
""",
                     get_and_reset_output()
                     )

  def test_exception(self):
    @transactional
    def raise_exception():
      register_hooks("raise exception")
      print ("raise exception")
      raise ValueError()
    
    self.assertRaises(ValueError, raise_exception)
    self.assertEqual("raise exception\ntransaction abort: raise exception\n",
                     get_and_reset_output()
                     )
                      
  def test_retry(self):
    class ConflictRaiser(object):
      raised = False
      
      @transactional
      def __call__(self):
        register_hooks("conflict raiser")
        if self.raised: print ("conflict raiser returns without exception")
        else:
          print ("conflict raiser raises `ConflictError`")
          self.raised = True
          from ZODB.POSException import ConflictError
          raise ConflictError()
    
    cr = ConflictRaiser()
    cr()
    self.assertEqual("""\
conflict raiser raises `ConflictError`
transaction abort: conflict raiser
conflict raiser returns without exception
transaction commit: conflict raiser
""",
                     get_and_reset_output()
                     )


def test_suite():
  return TestSuite([makeSuite(TestTransactional)])
    
    
    
