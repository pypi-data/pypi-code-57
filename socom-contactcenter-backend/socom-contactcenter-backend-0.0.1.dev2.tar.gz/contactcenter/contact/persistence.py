#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import sys

import pymongo
import pymongo.errors

from monkey.dao.core import PersistenceError, ObjectNotFoundError
from monkey.dao.pymongo.core import PyMongoDAO

__author__ = 'Xavier ROY'


class ContactDAO(PyMongoDAO):
    _COLLECTION_NAME = 'contacts'

    _AUDITABLE = True

    def __init__(self, database):
        super().__init__(database, ContactDAO._COLLECTION_NAME, True)
        self.auditable = ContactDAO._AUDITABLE

    def find_one_by_email_addr(self, email_addr):
        """ Find a contact by its email address
        :param email_addr: The email address
        :return: The first found contact matching the email address
        """
        try:
            contact = self.collection.find_one({'email_addr': email_addr})
            if contact is not None:
                return contact
            else:
                raise ObjectNotFoundError(self.collection.name, {'email_addr': email_addr})
        except pymongo.errors.PyMongoError as e:
            raise PersistenceError('Unexpected error', e)

    def find_one_by_phone_number(self, phone_num):
        """ Find a contact by its email address
        :param phone_num: The email address
        :return: The first found contact matching the phone number
        """
        try:
            contact = self.collection.find_one({'phone_numbers': {'$elemMatch': {'num': phone_num}}})
            if contact is not None:
                return contact
            else:
                raise ObjectNotFoundError(self.collection.name, {'email_addr': phone_num})
        except pymongo.errors.PyMongoError as e:
            raise PersistenceError('Unexpected error', e)

    def find_contacts_by_last_name(self, last_name, skip=0, limit=-1):
        """ Lists entries matching the specified last name
        :param last_name: The last name
        :param skip: The number of skipped records.
        :param limit: The maximum number of returned records
        :return: Contact matching the last name
        """
        try:
            cursor = self.collection.find({'shortName': short_name}).sort('host', direction=1).skip(skip).limit(limit)
            entries = []
            for entry in cursor:
                entries.append(entry)
            return entries
        except pymongo.errors.PyMongoError as e:
            raise PersistenceError('Unexpected error', e)

    def insert_one(self, first_name, last_name, phone_numbers, email_addr):
        """ Inserts a new contact
        :param first_name: The first name of the contact
        :param last_name: The last name of the contact
        :param phone_numbers: The phone numbers to reach the contact
        :param email_addr: The email address of the contact
        :return: id of the inserted record
        """
        # Build a new contact
        data_set = {'first_name': first_name,
                    'last_name': last_name,
                    'phone_numbers': phone_numbers,
                    'email_addr': email_addr}
        return self.insert(data_set)
