from logging import Logger
from typing import Callable, Dict, Optional

from sqlalchemy.sql import Select
from twisted.internet.defer import Deferred
from vortex.DeferUtil import deferToThreadWrapWithLogger

from peek_plugin_base.storage.DbConnection import DbSessionCreator
from peek_storage.plpython.LoadPayloadPgUtil import LoadPayloadTupleResult


def getTuplesPayload(logger: Logger,
                     dbSessionCreator: DbSessionCreator,
                     sql: Select,
                     sqlCoreLoadTupleClassmethod: Callable,
                     payloadFilt: Optional[Dict] = None,
                     fetchSize=50) -> Deferred:
    return deferToThreadWrapWithLogger(logger) \
        (getTuplesPayloadBlocking) \
        (dbSessionCreator, sql, sqlCoreLoadTupleClassmethod, payloadFilt, fetchSize)


def getTuplesPayloadBlocking(dbSessionCreator: DbSessionCreator,
                             sql: Select,
                             sqlCoreLoadTupleClassmethod: Callable,
                             payloadFilt: Optional[Dict] = None,
                             fetchSize=50) -> LoadPayloadTupleResult:
    from peek_storage.plpython.LoadPayloadPgUtil import callPGLoadPayloadTuplesBlocking
    return callPGLoadPayloadTuplesBlocking(dbSessionCreator,
                                           sql,
                                           sqlCoreLoadTupleClassmethod,
                                           payloadFilt,
                                           fetchSize)
