import asyncio
import json

class db(object):
    def __init__(self, nw):
        self.nw = nw

    async def get(self, table, query, projection=None, options=None):
        """ahmad = await db.get('test', {'age', 20})"""
        queue = asyncio.Queue()
        if projection is None:
            projection = {}
        if options is None:
            options = {}

        def db_result(msg):
            queue.put_nowait(msg.Value)

        if projection == {} and options == {}:
            self.nw.send('db','get', table, json.dumps(query))
        else:
            self.nw.send('db','get', table, json.dumps(query), json.dumps(projection), json.dumps(options))
        self.nw.when('db.'+ table, db_result)
        return await queue.get()

    async def first(self, table, query, projection=None, options=None):
        result = await self.get(table, query, projection, options)
        if result:
            return result[0]
        else:
            return None

    def index(self, table, keys, options = None):
        if options:
            self.nw.send('db', 'set', table, 'index', keys, options)
        else:
            self.nw.send('db', 'set', table, 'index', keys)

    def drop(self, table):
        """db.drop('test')"""
        self.nw.send('db','set', table, 'drop')

    def remove(self, table, query):
        """db.remove('test', {'age',40})"""
        self.nw.send('db', 'set', table, 'remove', json.dumps(query))

    def set(self, table, value):
        """db.set('test', {'name':'ahmad', 'age': 40})"""
        return self.nw.send('db', 'set', table, json.dumps(value))

    async def set_wait(self, table, value):
        """db.set('test', {'name':'ahmad', 'age': 40})"""
        queue = asyncio.Queue()

        def db_result(msg):
            queue.put_nowait(msg.Value)

        self.nw.send('db', 'set', table, json.dumps(value))
        self.nw.when('db.' + table, db_result)
        return await queue.get()

    async def aggregate(self, table, query):
        """oldest = await db.aggregate('test', [{"$group" : {"_id" : 1, "oldest" : {"$max" : "$age"}}}])"""
        queue = asyncio.Queue()

        def db_result(msg):
            queue.put_nowait(msg.Value)

        self.nw.send('db', 'get', table, 'aggregate', json.dumps(query))
        self.nw.when('db.' + table, db_result)
        return await queue.get()


if __name__ == '__main__':
    from nodewire.control import control
    async def myloop():
        await asyncio.sleep(10)
        mydb = db(ctrl.nw)
        ahmad = await mydb.get('test', {})
        print(ahmad)

    def connected():
        mydb = db(ctrl.nw)
        mydb.set('test', {'name':'ahmad sadiq', 'age': 43})

    ctrl = control()
    ctrl.nw.on_connected = connected
    ctrl.nw.run(myloop())