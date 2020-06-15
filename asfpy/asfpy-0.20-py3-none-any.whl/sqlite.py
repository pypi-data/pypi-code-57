#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
 #the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"SQLite document-store wrapper for ASF."

import sqlite3


class asfpyDBError(Exception):
    pass


class db:
    def __init__(self, fp):
        self.connector = sqlite3.connect(fp)
        self.connector.row_factory = sqlite3.Row
        self.cursor = self.connector.cursor()
        # Need sqlite 3.25.x or higher for upserts
        self.upserts_supported = (sqlite3.sqlite_version >= "3.25.0")

    def run(self, cmd, *args):
        self.cursor.execute(cmd, args)

    def runc(self, cmd, *args):
        self.cursor.execute(cmd, args)
        self.connector.commit()

    def delete(self, table, **target):
        "Delete a row where ..."
        if not target:
            raise asfpyDBError("DELETE must have at least one defined target value for locating where to delete from")
        ### more than ONE key/value are silently ignored, and the
        ### selection of one-of-many is arbitrary.
        k, v = next(iter(target.items()))
        statement = f'DELETE FROM {table} WHERE {k} = ?;'
        self.runc(statement, v)

    def update(self, table, document, **target):
        "Update a row where ..."
        if not target:
            raise asfpyDBError("UPDATE must have at one defined target to specify the row to update")
        k, v = next(iter(target.items()))
        items = document.items()  # Use the same ordering for keys/values
        columns = ", ".join("%s = ?" % uk for uk, uv in items)
        statement = f'UPDATE {table} SET {columns} WHERE {k} = ?;'
        values = [uv for uk, uv in items]
        values.append(v)  # unique constraint
        self.runc(statement, *values)

    def insert(self, table, document):
        "Standard insert, document -> sql."
        items = document.items()  # Use the same ordering for keys/values
        columns = ", ".join(uk for uk, uv in items)
        questionmarks = ", ".join(['?'] * len(items))
        statement = f'INSERT INTO {table} ({columns}) VALUES ({questionmarks});'
        values = [uv for uk, uv in items]
        self.runc(statement, *values)

    def upsert(self, table, document, **target):
        "Performs an upsert in a table with unique constraints. Insert if not present, update otherwise."
        # Always have the target identifier as part of the row
        if not target:
            raise asfpyDBError("UPSERTs must have at least one defined target value for locating where to upsert")
        k, v = next(iter(target.items()))
        document[k] = v

        # table: foo
        # bar: 1
        # baz: 2
        # INSERT INTO foo (bar,baz) VALUES (?,?) ON CONFLICT (bar) DO UPDATE SET (bar=?, foo=?) WHERE bar=?,(1,2,1,2,1,)
        if self.upserts_supported:
            items = document.items()  # Use the same ordering for keys/values
            variables = ", ".join(uk for uk, uv in items)
            questionmarks = ", ".join(['?'] * len(items))
            upserts = ", ".join("%s = ?" % uk for uk, uv in items)

            statement = f'INSERT INTO {table} ({variables}) VALUES ({questionmarks}) ON CONFLICT({k}) DO UPDATE SET {upserts} WHERE {k} = ?;'
            # insert values, update values, and the unique constraint value
            values = ([uv for uk, uv in items] * 2) + [v]
            self.runc(statement, *values)
        # Older versions of sqlite do not support 'ON CONFLICT', so we'll have to work around that...
        else:
            try:  # Try to insert
                self.insert(table, document)
            except sqlite3.IntegrityError: # Conflict, update instead
                self.update(table, document, **target)

    def fetch(self, table, limit=1, **params):
        "Searches a table for matching params, returns up to $limit items that match, as dicts."
        if params:
            items = params.items()  # Use the same ordering for keys/values
            search = " AND ".join("%s = ?" % uk for uk, uv in items)
            values = [uv for uk, uv in items]
        else:
            search = "1"
            values = ()
        statement = f'SELECT * FROM {table} WHERE {search}'
        if limit:
            statement += f' LIMIT {limit}'
            rows_left = limit
        self.cursor.execute(statement, values)
        saw_row = False
        while True:
            rowset = self.cursor.fetchmany()
            if not rowset:
                if not saw_row:
                    yield None  # no rows found
                return  # break iteration
            for row in rowset:
                yield dict(row)
            if limit:
                rows_left -= len(rowset)
                assert rows_left >= 0
                if rows_left == 0:
                    return  # break iteration
            saw_row = True

    def fetchone(self, table_name, **params):
        return next(self.fetch(table_name, **params))

    def table_exists(self, table):
        "Simple check to see if a table exists or not."
        return self.fetchone('sqlite_master', type='table', name=table) and True or False


def test(dbname=':memory:'):
    testdb = db(dbname)
    cstatement = '''CREATE TABLE test (
                      foo   varchar unique,
                      bar   varchar,
                      baz   real
                      )'''

    # Create if not already here
    try:
        testdb.runc(cstatement)
    except sqlite3.OperationalError as e:  # Table exists
        assert str(e) == "table test already exists"

    # Insert (may fail if already tested)
    try:
        testdb.insert('test', {'foo': 'foo1234', 'bar': 'blorgh', 'baz': 5})
    except sqlite3.IntegrityError as e:
        assert str(e) == "UNIQUE constraint failed: test.foo"

    # This must fail
    try:
        testdb.insert('test', {'foo': 'foo1234', 'bar': 'blorgh', 'baz': 2})
    except sqlite3.IntegrityError as e:
        assert str(e) == "UNIQUE constraint failed: test.foo"

    # This must pass
    testdb.upsert('test', {'foo': 'foo1234', 'bar': 'blorgssh', 'baz': 8}, foo='foo1234')

    # This should fail with no target specified
    try:
        testdb.upsert('test', {'foo': 'foo1234', 'bar': 'blorgssh', 'baz': 8})
    except asfpyDBError as e:
        assert str(e) == "UPSERTs must have at least one defined target value for locating where to upsert"

    # This should all pass
    testdb.update('test', {'foo': 'foo4321'}, foo='foo1234')
    obj = testdb.fetchone('test', foo='foo4321')
    assert type(obj) is dict and obj.get('foo') == 'foo4321'
    obj = testdb.fetch('test', limit=5, foo = 'foo4321')
    assert str(type(obj)) == "<class 'generator'>"
    assert next(obj).get('foo') == 'foo4321'
    obj = testdb.fetchone('test', foo='foo9999')
    assert obj is None
    testdb.delete('test', foo='foo4321')
    assert testdb.table_exists('test')
    assert not testdb.table_exists('test2')

    # Let's insert 1000 rows, and perform a repeated fetch.
    for i in range(1000):
        testdb.insert('test', {'foo': str(i), 'bar': str(i), 'baz': i})
    count = 0
    for row in testdb.fetch('test', limit=None):
        assert int(row['foo']) == count
        count += 1
    assert count == 1000

    # Change the arraysize, and run it again.
    testdb.cursor.arraysize = 97  # ensure last fetch is short
    count = 0
    for row in testdb.fetch('test', limit=None):
        assert int(row['foo']) == count
        count += 1
    assert count == 1000

    # One more run, with a limit. Leave the arraysize.
    count = 0
    for row in testdb.fetch('test', limit=30):
        assert int(row['foo']) == count
        count += 1
    assert count == 30


if __name__ == '__main__':
    test()
