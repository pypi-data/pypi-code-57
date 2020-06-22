#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import sys

import pymongo
import pymongo.errors

from monkey.dao.core import PersistenceError, ObjectNotFoundError
from monkey.dao.pymongo.core import PyMongoDAO

__author__ = 'Xavier ROY'


class TraceDAO(PyMongoDAO):
    _COLLECTION_NAME = 'trace'

    _AUDITABLE = True

    def __init__(self, database):
        super().__init__(database, TraceDAO._COLLECTION_NAME, True)
        self.auditable = TraceDAO._AUDITABLE

