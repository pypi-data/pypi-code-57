from Session import Session

import unittest
import argparse
import sqlalchemy

class tests(unittest.TestCase):

    def setUp(self, host):
        self.sess = Session('test', 'test', host, 'Test')

    def test_connect(self):
        assert(not self.sess.conn.closed)

    def test_insert(self):
        try:
            self.sess.insert('test_table', ['column1', 'column2'], [['6/19/2020', 'test']])
        except sqlalchemy.exc.SQLAlchemyError as e:
            print('Insert Error: ', e)
            quit()

    def test_insert_CSV(self):
        try:
            self.sess.insert_from_CSV('./TestDocs/test.csv', 'test_table')
        except sqlalchemy.exc.SQLAlchemyError as e:
            print('CSV Error: ', e)
            quit()

    def test_execute_SQL(self):
        try:
            self.sess.execute_SQL('./queries/test.sql')
        except sqlalchemy.exc.SQLAlchemyError as e:
            print('SQL Error: ', e)
            quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('host', help='Host IP for test')
    args = parser.parse_args()

    test = tests()

    test.setUp(args.host)
    test.test_connect()
    test.test_insert()
    test.test_insert_CSV()
    test.test_execute_SQL()
    print('Test SUCCESS')