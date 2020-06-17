import os

from aos.managers import misc

try:
    import sqlite3 as sqlite
except ImportError:
    import sqlite

def executeSQL(cursor, query, params=None):
    """ Execute a sqlite3 query """
    if params is None:
        return cursor.execute(query)

    return cursor.execute(query, params)


class SqliteDB():
    """ """
    def __init__(self, sqlitefile):
        self._conn = sqlite.connect(sqlitefile)
        self.cursor = self._conn.cursor()

    def close(self):
        self.cursor.close()
        self._conn.close()


class PrimaryDB(SqliteDB):
    def __init__(self, sqlitefile):
        SqliteDB.__init__(self, sqlitefile)
        self.pkglist = {}

    def getPackages(self, names=[]):
        """ Search pkgs with names.
        The columns from packages table:
        pkgKey, pkgId, name, arch, version, epoch, release, summary, description, location_href
        """
        pkglist = []
        properties = ["pkgId", "pkgKey", "name", "epoch", "version", "release", "arch", "location_href"]
        query = "select %s from packages " % ",".join(properties)

        tmp = []
        for name in names:
            tmp.append("name = '%s'" % name)

        if names:
            query += "where %s" % " OR ".join(tmp)

        rows = executeSQL(self.cursor, query)
        for row in rows:
            tmp = dict(zip(properties, row))
            pkglist.append(tmp)

        return pkglist

    def getPackagesWithSpecificNameAndColumn(self, names=[], columns=[]):
        """ Search specified columns of pkgs with specified names.
        The columns from pakcages table:
        pkgKey, pkgId, name, arch, version, epoch, release, summary, description, location_href
        """
        pkglist = []
        query = "SELECT %s " % ",".join(columns) # select columns
        query += "from packages " # table name

        tmp = []
        for name in names:
            tmp.append("name = '%s'" % name)

        if names:
            query += "WHERE %s" % " OR ".join(tmp) # specific pkg names

        rows = executeSQL(self.cursor, query)
        for row in rows:
            tmp = dict(zip(columns, row))
            pkglist.append(tmp)

        return pkglist

    def getPackages2(self, names=[]):
        columns = ["pkgId", "pkgKey", "name", "epoch", "version", "release", "arch", "location_href"]
        return self.getPackagesWithSpecificNameAndColumn(names, columns)

    def getPackagesWithVersion(self, names=[]):
        columns = ["name", "version", "pkgKey"]
        return self.getPackagesWithSpecificNameAndColumn(names, columns)

class FilelistsDB(SqliteDB):
    def __init__(self, sqlitefile):
        SqliteDB.__init__(self, sqlitefile)

    def getFiles(self, pkgKey):
        filelist = []
        properties = ["pkgKey", "dirname", "filenames"]

        if not pkgKey:
            return filelist
        else:
            query = "select %s from filelist where pkgKey = '%s'" % (",".join(properties), pkgKey)

        rows = executeSQL(self.cursor, query)
        for row in rows:
            tmp = dict(zip(properties, row))
            filelist.append(tmp)

        return filelist

class OtherDB(SqliteDB):
    def __init__(self, sqlitefile):
        SqliteDB.__init__(self, sqlitefile)

    def test(self):
        pass
