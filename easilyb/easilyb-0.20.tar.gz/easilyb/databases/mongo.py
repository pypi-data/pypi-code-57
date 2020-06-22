from threading import RLock
from easilyb.docker import mongo_instance, stop_container
KEY_ID = '_key_id'
import atexit


class MongoDB:
    def __init__(self, database_name="default_db", collection_name="default_collection", server_url=None,
                 auto_commit=True, docker_server=False, container_name="default", stop_at_exit=True, data_path=None):
        import pymongo
        if docker_server:
            self.container_name = "easylib_mongo_" + container_name
            self.container, self.server_url = mongo_instance(self.container_name, data_path=data_path)
            if stop_at_exit:
                atexit.register(stop_container, self.container)
        else:
            self.server_url = server_url
        self.client = pymongo.MongoClient(self.server_url)
        self.database_name = database_name
        self.database = self.client[database_name]
        self.collection_name = collection_name
        if self.collection_name not in self.database.collection_names():
            # Create collection
            self.collection = self.database[collection_name]
            self.collection.create_index(KEY_ID, unique=True)
        else:
            self.collection = self.database[collection_name]
        self.auto_commit = auto_commit
        self.lock = RLock()
        self.session, self.transaction = None, None

    def commit(self):
        self.session.commit_transaction()
        self.session.end_session()
        self.session, self.transaction = None, None

    def save(self):
        self.commit()

    def rollback(self):
        self.session.abort_transaction()
        self.session.end_session()
        self.session, self.transaction = None, None

    def start_transaction(self):
        if self.session is not None or self.transaction is not None:
            raise ValueError("Transaction already started")
        self.session = self.client.start_session()
        self.transaction = self.session.start_transaction()

    def __getitem__(self, key):
        return self.collection.find_one({KEY_ID: key})

    def __setitem__(self, key, value):
        doc = dict(value)
        doc[KEY_ID] = key
        self.collection.replace_one({KEY_ID: key}, doc, upsert=True, session=self.session)

    def __delitem__(self, key):
        self.collection.delete_one({KEY_ID: key}, session=self.session)

    def __contains__(self, key):
        return self.collection.find_one({KEY_ID: key}) is not None

    def __iter__(self):
        for doc in self.collection.find():
            yield doc[KEY_ID], doc

    def __enter__(self):
        self.lock.acquire()
        self.start_transaction()

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is None:
                self.commit()
            else:
                self.rollback()
        finally:
            self.lock.release()
