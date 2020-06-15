# Copyright (C) 2011-2018 by Dr. Dieter Maurer, Illtalstr. 25, D-66571 Bubach, Germany
# see "LICENSE.txt" for details
"""Scheduling asynchronous operations and managing those schedules.
"""
from time import time
from logging import getLogger
from uuid import uuid4 as uuid

import transaction

from persistent import Persistent
from BTrees.OOBTree import OOBTree
from ZODB.POSException import ConflictError

from .transactional import transactional

# Python 2/3 compatibility
try:
  from _thread import start_new_thread
except:
  from thread import start_new_thread

logger = getLogger(__name__)

  
class _Schedule(object):
  """Auxiliary schedule class."""

  retry_exceptions = ()

  def __init__(self, request):
    self._request = request
    self.id = uuid().hex

  def run(self):
    request = self._request
    r, exc = None, None
    try:
      __traceback_info__ = request # for Zope
      (f, args, kw) = request
      r = f(*args, **kw)
    except self.retry_exceptions: raise
    except Exception as e:
      # provide traceback
      logger.exception("exception in call of %r" % f)
      exc = _cleanup_exception(e)
    self._result = r, exc

  def get_result(self): return self._result


class TransactionalScheduler(object):
  """scheduler for asynchronous operations and their management.

  Note: This scheduler maintains its data in RAM. It cannot be
  safely used, when `schedule` and `completed/get_result` can be
  called in different processes. You might be able to use
  `TransactionalPersistentScheduler` in this case.
  """

  # may be overridden by derived classes or the constructor
  timeout = 3600 # s; delete completions older than this (forgotten requests)

  # may be overridden by dezived classes
  MAPPING_FACTORY = dict
  SCHEDULE_FACTORY = _Schedule

  def __init__(self, timeout=None):
    self._schedules = self.MAPPING_FACTORY()
    self._completed = self.MAPPING_FACTORY()
    if timeout is not None: self.timeout = timeout


  def schedule(self, f, *args, **kw):
    """schedule an asynchronous call for when the transaction commits and return id.
    """
    schedule = self.SCHEDULE_FACTORY((f, args, kw))
    self._schedules[schedule.id] = schedule
    transaction.get().addAfterCommitHook(self._start, (schedule,))
    transaction.get().addAfterAbortHook(self._remove, (True, schedule.id,))
    return schedule.id

  def completed(self, id):
    """`None`, `False` or `True`, if *id* is unknown, not yet completed, completed."""
    if id not in self._schedules: return None
    return id in self._completed

  def remove(self, id):
    """remove schedule *id*, if it exists."""
    self._remove(True, id)

  def get_result(self, id):
    """return the result for *id*.

    It may return `None` (*id* is unknown), `False` (*id* is known
    but not yet completed) or a pair *result*, *exception*.
    In the last case, removal of *id* is scheduled for when the transaction
    commits successfully.
    """
    schedule = self._schedules.get(id)
    if schedule is None: return
    if id not in self._completed: return False
    transaction.get().addAfterCommitHook(self._remove, (id,))
    return schedule.get_result()


  # internal
  def _complete(self, id):
    """mark *id* as completed.

    Also remove "forgotten" completions.
    """
    ct = time()
    # remove outdated schedules
    timeline = ct - self.timeout
    completed = self._completed; schedules = self._schedules
    # we assume that the number is moderate
    #  otherwise, we would need a more efficient data structure (a heap).
    for cid, t in completed.items():
      if t < timeline:
        # outdated -- we are aware that parellel threads may interfere
        try: del schedules[cid]
        except KeyError: pass
        try: del completed[cid]
        except KeyError: pass
    completed[id] = ct


  def _remove(self, status, id):
    """after commit hook to remove *id* in case of a successful transaction."""
    if status:
      # transaction successful
      # we are aware that parallel threads my interfere
      try: del self._schedules[id]
      except KeyError: pass
      try: del self._completed[id]
      except KeyError: pass


  def _start(self, status, schedule):
    """after commit hook to start *schedule* in case of a successfull transaction."""
    if status: start_new_thread(self._run_thread, (schedule,))
    else: self._remove(True, schedule.id)


  def _run_thread(self, schedule):
    """run *schedule* in a new thread."""
    schedule.run() # should not raise an exception
    self._complete(schedule.id)


class _PersistentSchedule(Persistent, _Schedule):
  """Auxiliary schedule class for use with `PersistentTransactionScheduler`."""

  retry_exceptions = (ConflictError,)


class PersistentTransactionalScheduler(Persistent, TransactionalScheduler):
  """like `TransactionalScheduler` but it stores the schedules in the ZODB
  rather than RAM.

  Note that this is an abstract class. Derived classes must
  set `PERSISTENT_CONTEXT_FACTORY` to a concrete subclass
  of `.context.PersistentContext`.
  """

  # Must be defined by derived classes
  PERSISTENT_CONTEXT_FACTORY = None

  # May be overridden by derived classes
  TRANSACTIONAL_DECORATOR = transactional
  SCHEDULE_FACTORY = _PersistentSchedule
  MAPPING_FACTORY = OOBTree

  def schedule(self, f, *args, **kw):
    schedule = self.SCHEDULE_FACTORY((f, args, kw))
    self._schedules[schedule.id] = schedule
    transaction.get().addAfterCommitHook(
      self._start,
      (self.PERSISTENT_CONTEXT_FACTORY(self, schedule),)
      )
    # This happens automatically
    # transaction.get().addAfterAbortHook(self._remove, (True, schedule.id,))
    return schedule.id

  @staticmethod
  def _run_schedule(context):
    context[0]._run_thread(context[1])

  @staticmethod
  def _abort_schedule(context, e):
    self, schedule = context[0], context[1]
    logger.exception("schedule %s(%s) aborted", schedule.id, schedule._request)
    schedule._result = None, _cleanup_exception(e)
    self._complete(schedule.id)

  @classmethod
  def _run_scheduler_thread(cls, context):
    try:
      cls.TRANSACTIONAL_DECORATOR(cls._run_schedule)(context)
    except Exception as e:
      try:
        cls.TRANSACTIONAL_DECORATOR(cls._abort_schedule)(context, e)
      except Exception:
        schedule = context[1]
        logger.critical("schedule %s(%s) will not terminate", schedule.id, schedule._request, exc_info=True)
        raise

  def _start(self, status, context):
    """after commit hook to start *schedule* in case of a successfull transaction."""
    if status: start_new_thread(self._run_scheduler_thread, (context,))
    # automatically
    # else: self._remove(True, schedule.id)
        



def _cleanup_exception(exc):
  """remove tracebacks (under python 3) from *exc*.

  Those tracebacks would (almost surely) be interpreted in a
  foreign thread and contain references which pose problems there.
  """
  if exc is None: return
  if getattr(exc, "__traceback__", None) is not None:
    exc.__traceback__ = None
  if getattr(exc, "__context__", None) is not None:
    exc.__context__ = _cleanup_exception(exc.__context__)
  if getattr(exc, "__cause__", None) is not None:
    exc.__cause__ = _cleanup_exception(exc.__cause__)
  return exc
