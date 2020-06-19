# data/controller.py

# TODO: add logger for database logging
# TODO: add documentation sphinx

import pprint
import xmlrpc.client
from .query import Query

class Controller:
    
    # constructor
    def __init__(self):
        # credentials of the server and database
        self.server_credentials = {
            'url': '',
            'db': '',
            'timezone': ''
        }
        # credentials of the user
        self.user_credentials = {
            'username': '',
            'password': ''
        }
        # protected authentication variables
        self._common = None
        self._db = None
        self._uid = None

    # method to configure the server credentials
    def configure_server(self, url, db, timezone="UTC"):
        self.server_credentials['url'] = url
        self.server_credentials['db'] = db
        self.server_credentials['timezone'] = timezone

    # method to configure the user credentials
    def configure_user(self, username, password):
        self.user_credentials['username'] = username
        self.user_credentials['password'] = password

    # method to connect and authenticate to the database
    def connect(self):
        try:
            self._common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.server_credentials['url']))
            self._uid = self._common.authenticate(self.server_credentials['db'], self.user_credentials['username'], self.user_credentials['password'], {})
            self._db = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.server_credentials['url']))
            self._db.execute_kw(self.server_credentials['db'], self._uid, self.user_credentials['password'],
                                'res.users', 'check_access_rights', ['read'], {'raise_exception': False})
        # TODO: add error handling for connect() method
        except xmlrpc.client.ProtocolError as e:
            print(e)
        except Exception as e:
            print(e)
        else:
            print('Connected succesfully.')

    # method to search by id
    def search_by_id(self, model, id):
        try:
            return self._db.execute_kw(self.server_credentials['db'], self._uid, self.user_credentials['password'],
                                        model, 'search', [[('id', '=', id)]])[0]
        except IndexError as e:
            # no results were found
            return None

    # method to search_read by id
    def search_read_by_id(self, model, id, fields=[]):
        try:
            return self._db.execute_kw(self.server_credentials['db'], self._uid, self.user_credentials['password'],
                                        model, 'search_read', [[('id', '=', id)]], {'fields': fields})[0]
        except IndexError as e:
            # no results were found
            return None
    
    # method to search by query
    def search_by_query(self, model, query):
        return self._db.execute_kw(self.server_credentials['db'], self._uid, self.user_credentials['password'],
                                        model, 'search', [query.search_params], query.modifiers)

    # method to search_read by query
    def search_read_by_query(self, model, query):
        return self._db.execute_kw(self.server_credentials['db'], self._uid, self.user_credentials['password'],
                                        model, 'search_read', [query.search_params], query.modifiers)
    # method to count results from query
    def count_by_query(self, model, query):
        return self._db.execute_kw(self.server_credentials['db'], self._uid, self.user_credentials['password'],
                                        model, 'search_count', [query.search_params])
    
    # method to format results to string
    def format_results(self, results, indentation=2):
        return pprint.pformat(results, indentation)






