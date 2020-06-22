#!/usr/bin/python
# -*- coding: utf-8 -*-

from contactcenter.core import Service

from contactcenter.contact.data import build_name_key, OrganizationContact, PersonContact
from contactcenter.contact.persistence import ContactDAO

PERSON_CONTACT = 'user'
SERVICE_CONTACT = 'service'
ORGANIZATION_CONTACT = 'organization'

_NAME_KEY_FIELD_NAME = 'name_key'
_TYPE_FIELD_NAME = 'type'
_ID_FIELD_NAME = '_id'


class ContactService(Service):

    def __init__(self, dao: ContactDAO):
        super().__init__()
        self.dao: ContactDAO = dao

    def count_all(self):
        return self.dao.count()

    def list(self, skip=0, limit=10, sort_key='_id', sort_dir='1'):
        # TODO: Change sort setting
        return self.dao.find_all(skip, limit, [(sort_key, sort_dir)])

    def get_one_by_id(self, uid):
        return self.dao.find_one_by_key(uid)

    def create_personal_contact(self, contact: PersonContact):
        """ Create a new personal contact
        :param contact: The contact details
        :return: id of the created contact
        """
        data_set = {'name': contact.name,
                    'name_key': contact.name_key,
                    'type': contact.type,
                    'first_name': contact.first_name,
                    'last_name': contact.last_name,
                    'usual_first_name': contact.usual_first_name,
                    'usual_last_name': contact.usaul_last_name,
                    'birth_last_name': contact.birth_last_name,
                    'organization': contact.organization,
                    'phone_numbers': contact.phone_numbers,
                    'email_addr': contact.email_addr,
                    'key_set': contact.key_set,
                    'bulk_data': contact.bulk_data
                    }

        inserted_id = self.dao.insert(data_set)
        return inserted_id

    def create_organization_contact(self, contact: OrganizationContact):
        """ Create a new organization contact
        :param contact: The contact details
        :return: id of the created contact
        """
        data_set = {'name': contact.name,
                    'type': contact.type,
                    'organization': contact.name,
                    'phone_numbers': contact.phone_numbers,
                    'email_addr': contact.email_addr}
        # TODO: merge with props
        inserted_id = self.dao.insert(data_set)
        return inserted_id

    def update_organization_contact(self, uid, contact: OrganizationContact):
        # TODO: Review change set construction
        change_set = {'name': contact.name,
                      _TYPE_FIELD_NAME: contact.type,
                      'organization': contact.name,
                      'phone_numbers': contact.phone_numbers,
                      'email_addr': contact.email_addr}
        self.dao.update_from_dict(uid, change_set)

    def update_person_contact(self, uid, contact: PersonContact):
        # TODO: Review change set construction
        change_set = {'name': contact.name,
                      _TYPE_FIELD_NAME: contact.type,
                      'organization': contact.name,
                      'phone_numbers': contact.phone_numbers,
                      'email_addr': contact.email_addr}
        self.dao.update_from_dict(uid, change_set)

    def delete_one_by_id(self, iud):
        return self.dao.delete(iud)

    def get_one_by_email_addr(self, email_addr):
        contact = self.dao.find_one_by_email_addr(email_addr)
        return contact

    def get_one_by_phone_number(self, phone_num):
        contact = self.dao.find_one_by_phone_number(phone_num)
        return contact

    def lookup_by_type_and_name(self, contact_type, contact_name):
        """
        Look for documents that match the propvided contact name and type.
        :param contact_type: The contact type
        :param contact_name: The contact name
        :return: The id list of documents that matchthe contact name and type
        """
        # TODO: Utiliser la notion de full_name_key pour éliminer les caractères blanc, les signes diacritiques et les différences de casse.
        query = {
            _NAME_KEY_FIELD_NAME: build_name_key(contact_name),
            _TYPE_FIELD_NAME: contact_type
        }
        contacts = self.dao.find(query)
        contact_ids = map(ContactService._get_doc_uid, contacts)
        return contact_ids

    def _get_doc_uid(doc):
        return doc[_ID_FIELD_NAME]

    # Obsolete functions

    def _create(self, first_name, last_name, phone_numbers, email_addr):
        # DELETE_ME
        self.create_personal_contact(first_name, last_name, phone_numbers, email_addr)

    def _create_personal_contact(self, first_name, last_name, phone_numbers, email_addr, organization=None):
        # DELETE_ME
        """ Create a new contact
        :param first_name: The first name of the contact
        :param last_name: The last name of the contact
        :param phone_numbers: The phone numbers to reach the contact
        :param email_addr: The email address of the contact
        :param organization: The name of the organization
        :return: id of the created contact
        """
        data_set = {'name': '{} {}'.format(first_name, last_name),

                    'type': PERSON_CONTACT,
                    'first_name': first_name,
                    'last_name': last_name,
                    'organization': organization,
                    'phone_numbers': phone_numbers,
                    'email_addr': email_addr}
        inserted_id = self.dao.insert(data_set)
        return inserted_id

    def _create_service_contact(self, name, phone_numbers, email_addr, organization=None):
        # DELETE_ME
        """ Create a new service contact
        :param name: The name of the contact
        :param phone_numbers: The phone numbers to reach the contact
        :param email_addr: The email address of the contact
        :param organization: The name of the organization
        :return: id of the created contact
        """
        data_set = {'name': name,
                    'type': SERVICE_CONTACT,
                    'organization': organization,
                    'phone_numbers': phone_numbers,
                    'email_addr': email_addr}
        inserted_id = self.dao.insert(data_set)
        return inserted_id

    def _create_organization_contact(self, name, phone_numbers, email_addr):
        # DELETE_ME
        """ Create a new service contact
        :param name: The name of the contact
        :param phone_numbers: The phone numbers to reach the contact
        :param email_addr: The email address of the contact
        :return: id of the created contact
        """
        data_set = {'name': name,
                    'type': ORGANIZATION_CONTACT,
                    'organization': name,
                    'phone_numbers': phone_numbers,
                    'email_addr': email_addr}
        inserted_id = self.dao.insert(data_set)
        return inserted_id
