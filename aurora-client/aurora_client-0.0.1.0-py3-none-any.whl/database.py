import grpc

from aurora_client.aurora import Aurora_pb2, Aurora_pb2_grpc, AuroraDB_pb2, AuroraDB_pb2_grpc

#from framework.config.settings import AthenaConfig


class Database(object):
    """
    Aurora stub
    """

    DT_Double = 0
    DT_Int = 1
    DT_Long = 2
    DT_String = 6

    def __init__(self, ip, port):
        channel = grpc.insecure_channel('{0}:{1}'.format(ip, port))
        self.stub_login = Aurora_pb2_grpc.AuroraLoginServiceStub(channel)
        self.stub_db = AuroraDB_pb2_grpc.AuroraDatabaseServiceStub(channel)

        try:
            self.stub_login.Login(
                Aurora_pb2.ClientPeer(
                    clientName="StockAI",
                    version=Aurora_pb2.Version(
                        major=1,
                        minor=0
                    )
                )
            )
            # print("Connected to Aurora")
            self._connected = True
        except Exception as e:
            print("Failed to connect to Aurora: {}".format(e))
            self._connected = False

    def release(self):
        if self._connected:
            self.stub_login.Logout(Aurora_pb2.Empty())

    def is_connected(self):
        return self._connected

    def execute_db_update(self, query, userlevel):

        request = AuroraDB_pb2.DbQuery(sql=query, userLevel=userlevel)
        response = self.stub_db.ExecuteUpdate(request)
        if response.success:
            return 1
        else:
            print('execute_db_update failed: {0}'.format(response.errorString))
            return 0

    def execute_db_updates(self, queries, userlevel):

        request = AuroraDB_pb2.DbQueries(sqls=queries, userLevel=userlevel)
        response = self.stub_db.ExecuteUpdates(request)
        if response.success:
            return 1
        else:
            print('execute_db_updates failed: {0}'.format(response.errorString))
            return 0

    def execute_db_query(self, query, userlevel):

        request = AuroraDB_pb2.DbQuery(sql=query, userLevel=userlevel)
        response = self.stub_db.ExecuteQuery(request)
        data = []
        for row in response.results:
            rdata = {}
            for k in row.kvMap:
                rdata[k] = row.kvMap[k]
            data.append(rdata)

        return data

    def execute_db_query_long(self, query, userlevel):
        index = 1
        limit = 500
        query = AuroraDB_pb2.DbQuery(sql=query, userLevel=userlevel)
        last_size = 1
        data = []
        while last_size != 0:
            pagination = AuroraDB_pb2.Pagination(pageCtrl=True, pageIndex=index, limit=limit)
            index = index + 1
            request = AuroraDB_pb2.DbPaginatedQuery(query=query, pagination=pagination)
            response = self.stub_db.ExecutePaginatedQuery(request)
            last_size = len(response.results)
            for row in response.results:
                rdata = {}
                for k in row.kvMap:
                    rdata[k] = row.kvMap[k]
                data.append(rdata)

        return data

    def is_table_exist(self, table_name):
        request = AuroraDB_pb2.DbIsTableExistRequest(userLevel=1, tableName=table_name)
        return self.stub_db.IsTableExist(request).rtnVal

    def create_table(self, table_name, fields):
        fields_ = []
        for k, v in fields.items():
            fields_.append(AuroraDB_pb2.DbTableField(fieldName=k, fieldType=v))
        request = AuroraDB_pb2.DbCreateTableRequest(userLevel=1, tableName=table_name, fields=fields_)
        self.stub_db.CreateTable(request)
