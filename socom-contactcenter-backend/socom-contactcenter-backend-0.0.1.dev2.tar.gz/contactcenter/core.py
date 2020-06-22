#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging


class Service:

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def count_all(self):
        raise NotImplementedError()

    def list(self, skip=0, limit=10, sort_key='_id', sort_dir='1'):
        raise NotImplementedError()

    def get_one_by_id(self, uid):
        raise NotImplementedError()

    def delete_one_by_id(self, uid):
        raise NotImplementedError()
