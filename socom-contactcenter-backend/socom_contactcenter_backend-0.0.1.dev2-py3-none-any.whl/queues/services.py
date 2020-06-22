#!/usr/bin/python
# -*- coding: utf-8 -*-

from contactcenter.core import Service
from contactcenter.queues.persistence import QueueDAO


class QueueService(Service):

    def __init__(self, dao: QueueDAO):
        super().__init__()
        self.dao: QueueDAO = dao

    def count_all(self):
        return self.dao.count()

    def list(self, skip=0, limit=10, sort_key='_id', sort_dir='1'):
        # TODO: Change sort setting
        return self.dao.find_all(skip, limit, [(sort_key, sort_dir)])

    def get_one_by_id(self, uid):
        return self.dao.find_one_by_key(uid)

    def get_one_by_name(self, queue_name):
        return self.dao.find_one_by_name(queue_name)

    def create(self, queue_name, status='LIVE', behaviors=None, default_behavior=None):
        """ Inserts a new contact
        :param queue_name: The name of the queues
        :param status: The status of the queues (default value is 'LIVE')
        :param behaviors: The available behaviors of the queues (as a dict where keys are behavior names)
        :param default_behavior: The default behavior of the queues
        :return: id of the inserted 'queues' record
        """
        inserted_id = self.dao.insert_one(queue_name, status, behaviors, default_behavior)
        return inserted_id

    def bulk_create(self, data):
        return self.dao.insert(data)

    def update(self, **kwargs):
        raise NotImplementedError()

    def delete_one_by_id(self, iud):
        return self.dao.delete(iud)
