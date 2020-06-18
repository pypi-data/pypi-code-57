# file: ezmongo.py
# Author: eamonn

import pymongo


class Mongodb(object):
    def __init__(self, host, database, table, username="", password=""):
        self.username = username
        self.password = password

        self.conn_mgo = pymongo.MongoClient(host, 27017)
        self.db = self.conn_mgo[database]
        self.collection = self.db[table]

    def get(self, Chart=True):
        if Chart:
            if self.username and self.password:
                self.db.authenticate("account", "password")
            return self.collection
        return self.db

    def insert(self, arr):
        self.collection.insert(arr)

    def insert_many(self, arr):
        self.collection.insert_many(arr)
