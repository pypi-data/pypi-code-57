# Copyright (C) 2011 by Dr. Dieter Maurer, Illtalstr. 25, D-66571 Bubach, Germany
# see "LICENSE.txt" for details
"""Pass persistent objects across threads.

The ZODB forbids to pass persistent objects across thread boundaries.
To be more precise: in the standard ZODB execution model, connections
are (indirectly, via transactions) associated with threads and a thread must
only access persistent objects loaded via connections associated with itself.
Failure to observe this restriction can lead to non deterministic
(`ConnectionStateError`) errors or even persistent data corruption.

This module defines the class `PersistentContext` which helps
to handle this limitation. One thread can construct an instance with
persistent objects and then pass the instance to a different thread.
This can then get access to the persistent objects.

`PersistentContext` does not directly manage the persistent objects
but instead identifies them by their ZODB and their oid. On access,
they are loaded from the ZODB properly via a connection associated
with the accessing thread, newly opened if necessary.

The function is not without risk: it is dangerous to access a
given ZODB via several connections in the same transaction (this may lead
to deadlock during `commit`).
`PersistentContext` prevents this for the connections it opens itself.
However, it does not have any knowledge about connections opened
independently by the target thread. Usually, only the root database
is opened independently; all other databases are opened indirectly
via the root connection. In this case, `PersistentContext` knows about
the dependently opened connections and the problem is limited to
the root database. `PersistentContext.get_root_connection()` can be used
to get a proper root connection avoiding the need for the target
thread to open its own connection.
If a ``PersistentContext`` is used to return the result of an asynchronous
operation, it is likely that the receiving target already has a root connection
opened. For this use case, ``PersistentContext`` has the method
``set_root_connection`` to inform ``PersistentContext`` about the root connection to use. Note that the root connection is stored on the current transaction
and lost at transaction boundaries.

`PersistentContext` is an abstract class. Derived classes must
define the method `_get_root_database`, used by the class
to access the ZODB root connection.

The persistent objects passed in a `PersistentContext` across
thread boundaries are reloaded in the destination thread.
This implies that modifications to those objects in the source thread
may not be seen in the destination thread as they become visible only
after a successful commit. `scheduler.TransactionalScheduler` can
be used (in some cases) to ensure that modifications are seen
(it delays a thread start until a successful transaction commit).

When a `PersistentContext` instance is constructed, it must be able
to determine for each persistent object its associated ZODB and oid.
If necessary, it performs a `transaction.savepoint` to get those information.
This will work for persistent objects
which are already part of the graph of persistent objects.
It will fail for persistent objects which do not yet form part of this
graph; a `ValueError` is raised in this case.

Note: It is dangerous to access the persistent objects encapsulated
in a `PersistentContext` in the creating thread without
having previously called `set_root_connection`. The reason is that
in such a case, a new root database connection is opened
and opening the same database in the same thread multiple times
can lead to deadlock during commit.
"""
import transaction

from ZODB.DB import DB

from .pycompat import iterkeys, iteritems


class PersistentContext(object):
  """see module docstring."""

  # To be defined by derived classes
  def _get_root_database(self):
    """return the ZODB root database.
    The need for this method is a bit akward: modern ZODB versions do not
    have this concept but instead use the `multidatabase` notion
    where multiple databases are at the same level.
    However, `PersistentContext` needs this concept
    to reduce the risk of multiple connections to the same database.
    It opens all database connections via a connection to the root
    database and assumes that the destination thread does this too.
    """
    raise NotImplementedError("`_get_root_database` must be implemented by derived classes.")

  def __init__(self, *objs, **kwobjs):
    """create a persistent context for persistent objects from *objs* and *kwobjs*.

    Subscription syntax (`[...]`) can be used to access
    the managed persistent objects.
    `int` keys access *objs*, `str` keys *kwobjs*.

    All objects must be persistent objects (otherwise `AttributeError` occurs)
    and must be part of the graph of persistent objects (otherwise
    """
    # backward compatibilty -- will not work
    #  when used with `PersistentTransactionalScheduler` or
    #  other `pickle` based persistency.
    if objs and isinstance(objs[0], DB):
      self._db = objs[0]; objs = objs[1:]
    savepoint_called = False

    known_dbs = self._get_root_database_().databases

    def identify(obj):
      """determine database and oid for *obj*.

      return pair *savepoint_called*, *id*.
      """
      sc = savepoint_called
      jar, oid = obj._p_jar, obj._p_oid # `AttributeError` if not persistent
      if oid is None:
        # this is a new object
        if not sc:
          transaction.savepoint(True) # try to associate a database
          sc = True
      jar, oid = obj._p_jar, obj._p_oid # `AttributeError` if not persistent
      if jar is None or oid is None:
        raise ValueError("obj %r not part of the graph of persistent objects" % obj)
      dbn = jar.db().database_name
      assert dbn in known_dbs, "object must be in a database known by the root database -- not the case for %s" % dbn
      return sc, (dbn, oid)

    self._objs = oids = []
    for o in objs:
      savepoint_called, oid = identify(o)
      oids.append(oid)

    self._kwobjs = kwids = {}
    for k, o in iteritems(kwobjs):
      savepoint_called, oid = identify(o)
      kwids[k] = oid


  def __getitem__(self, k):
    """access persistent object -- reload from proper connection."""
    if isinstance(k, int): i = self._objs
    else: i = self._kwobjs
    return self.__resolve(i[k]) # may raise `IndexError` or `KeyError`.

  # length information for positional objects
  def __len__(self): return len(self._objs)

  # mapping access for keyword objects
  def get(self, k, default=None):
    i = self._kwobjs.get(k)
    if i is None: return default
    return self.__resolve(i)

  def keys(self): return self._kwobjs.keys() # this may return an interator
  def iterkeys(self): return iterkeys(self._kwobjs)


  def get_root_connection(self):
    T = transaction.get() # current transaction
    root_connection = getattr(T, self.__tag, None)
    if root_connection is None:
      root_connection = self._get_root_database_().open()
      self.set_root_connection(root_connection, True)
    return root_connection

  def set_root_connection(self, root_connection, close=False):
    T = transaction.get() # current transaction
    rc = getattr(T, self.__tag, None)
    if rc is not None:
      if rc != root_connection:
        raise ValueError("root connection already set up")
      else: return
    setattr(T, self.__tag, root_connection)
    if close:
      T.addAfterCommitHook(self.__close_root_connection, (T,))
      T.addAfterAbortHook(self.__close_root_connection, (False, T,))



  # internal -- do not touch
  __tag = __name__ + '_tag'

  def __resolve(self, ref):
    """return the persistent object identified by *ref* (a pair *db_name* and *oid*).

    The object is properly loaded from a connection associated with
    the current thread (indirectly via the current transaction).
    """
    db_name, oid = ref
    rc = self.get_root_connection()
    c = rc.get_connection(db_name)
    return c[oid] # may raise `POSKeyError` or old state


  def __close_root_connection(self, status, T):
    root_connection = getattr(T, self.__tag)
    root_connection.close()
    delattr(T, self.__tag)


  def _get_root_database_(self):
    # backward compatibilty
    if hasattr(self, "_db"): return self._db
    return self._get_root_database()
      
