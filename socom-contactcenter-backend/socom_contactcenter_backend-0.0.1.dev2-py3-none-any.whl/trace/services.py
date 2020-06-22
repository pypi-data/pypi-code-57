#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from contactcenter.core import Service

from contactcenter.trace.persistence import TraceDAO


class TraceService(Service):

    def __init__(self, dao: TraceDAO):
        super().__init__()
        self.dao: TraceDAO = dao

    def count_all(self):
        return self.dao.count()

    def list(self, skip=0, limit=10, sort_key='_id', sort_dir='1'):
        # TODO: Change sort setting
        return self.dao.find_all(skip, limit, [(sort_key, sort_dir)])

    def get_one_by_id(self, uid):
        return self.dao.find_one_by_key(uid)

    def create(self, dataset):
        """ Create a new trace entry
        :param dataset:
        :return: id of the created entry
        """
        dataset['timestamp'] = datetime.datetime.utcnow()
        inserted_id = self.dao.insert(dataset)
        return inserted_id

    def bulk_create(self, data):
        return self.dao.insert(data)

    def update(self, **kwargs):
        raise NotImplementedError()

    def delete_one_by_id(self, iud):
        return self.dao.delete(iud)
