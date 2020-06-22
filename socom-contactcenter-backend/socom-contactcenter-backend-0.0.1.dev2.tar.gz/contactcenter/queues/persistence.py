#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymongo
import pymongo.errors

from monkey.dao.core import PersistenceError, ObjectNotFoundError
from monkey.dao.pymongo.core import PyMongoDAO

__author__ = 'Xavier ROY'


class QueueDAO(PyMongoDAO):
    _COLLECTION_NAME = 'queues'

    def __init__(self, database):
        super().__init__(database, QueueDAO._COLLECTION_NAME, True)

    def find_one_by_name(self, queue_name):
        """ Find a queues by its name
        :param queue_name: The queues name
        :return: The first found queues matching the name
        """
        try:
            contact = self.collection.find_one({'name': queue_name})
            if contact is not None:
                return contact
            else:
                raise ObjectNotFoundError(self.collection.name, {'name': queue_name})
        except pymongo.errors.PyMongoError as e:
            raise PersistenceError('Unexpected error', e)

    def insert_one(self, queue_name, status='LIVE', behaviors=None, default_behavior=None):
        """ Inserts a new contact
        :param queue_name: The name of the queues
        :param status: The status of the queues (default value is 'LIVE')
        :param behaviors: The available behaviors of the queues (as a dict where keys are behavior names)
        :param default_behavior: The default behavior of the queues
        :return: id of the inserted 'queues' record
        """
        # Build a new contact
        data_set = {'name': queue_name,
                    'status': status,
                    'behaviors': behaviors,
                    'default_behavior': default_behavior}
        return self.insert(data_set)
