import sqlite3


class SqliteConnect(object):
    def __init__(self, path=':memory:'):
        if not hasattr(self, 'cursor'):
            self.connection = sqlite3.connect(path)
            self.cursor = self.connection.cursor()
            self.path = path

    def __new__(cls, path=':memory:'):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SqliteConnect, cls).__new__(cls)
        return cls.instance

    def __str__(self):
        return f'<Connection to sqlite file {self.path} singleton-unit #{id(self)}>'

    def __repr__(self):
        return f'{self.__class__.__name__}(path="{self.path}")'
