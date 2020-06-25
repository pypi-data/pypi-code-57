import datetime
from tempfile import TemporaryFile
from CooHSQL.CooHSQL_Utils import clear_event_type, reverse_delete, check_parm, reverse_insert, \
    reverse_update, dump_update, check_datetime, opinion_time
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import (
    DeleteRowsEvent,
    UpdateRowsEvent,
    WriteRowsEvent
)


class CooHSQL(object):
    def __init__(self, connection_settings, max_filtration=20, start_file=None, start_pos=None, event_schemas=None,
                 event_tables=None, server_id=8023, start_time=None, stop_time=None):
        self.max_filtration_len = max_filtration
        self.coon_settings = connection_settings
        self.server_id = server_id
        self.log_file = start_file
        self.log_pos = start_pos
        self.only_schemas = event_schemas
        self.only_tables = event_tables
        self.resume_stream = True if start_file and start_pos else False
        self.start_time = start_time if check_datetime(start_time) else '1998-01-01 00:00:00'
        self.stop_time = stop_time if check_datetime(stop_time) else '2999-01-01 00:00:00'

    def process_binlog(self, mode='flashback'):
        """
        伪装 slave 获取数据库中的 binlog
        :return:
        """
        check_parm(mode)

        stream = BinLogStreamReader(
            connection_settings=self.coon_settings,
            server_id=self.server_id,
            log_file=self.log_file,
            log_pos=self.log_pos,
            only_schemas=self.only_schemas,
            only_tables=self.only_tables,
            resume_stream=self.resume_stream,
            only_events=[
                DeleteRowsEvent,
                UpdateRowsEvent,
                WriteRowsEvent
            ],
        )

        # 临时文件
        tem_file = TemporaryFile(mode='w+')

        for binlog_event in stream:
            for row in binlog_event.rows:
                # print(binlog_event.extra_data_length)
                # print(binlog_event.packet.log_pos)
                try:
                    event_time = datetime.datetime.fromtimestamp(binlog_event.timestamp)
                except OSError:
                    event_time = datetime.datetime(1980, 1, 1, 0, 0)

                if opinion_time(event_time, self.start_time) and opinion_time(self.stop_time, event_time):

                    event = {"schema": binlog_event.schema, "table": binlog_event.table,
                             "event_time": event_time.strftime("%Y-%m-%d %H:%M:%S")}

                    if isinstance(binlog_event, DeleteRowsEvent):
                        event["action"] = "delete"
                        event["data"] = clear_event_type(row["values"])

                    elif isinstance(binlog_event, UpdateRowsEvent):
                        event["action"] = "update"
                        event["before_data"] = clear_event_type(row["before_values"])
                        event["after_data"] = clear_event_type(row["after_values"])

                    elif isinstance(binlog_event, WriteRowsEvent):
                        event["action"] = "insert"
                        event["data"] = clear_event_type(row["values"])

                    if mode == 'flashback':
                        tem_file.write(self.reverse_sql(event) + '\n')
                    else:
                        print(self.dump_sql(event))

        tem_file.seek(0)
        for event_sql in tem_file.readlines()[::-1]:
            print(event_sql)

    def reverse_sql(self, event):
        """
        逆向 SQL
        :param event:
        :return:
        """
        if event["action"] == 'delete':
            return reverse_delete(event)

        elif event["action"] == 'insert':
            return reverse_insert(event, self.max_filtration_len)

        elif event["action"] == 'update':
            return reverse_update(event, self.max_filtration_len)

    def dump_sql(self, event):
        if event["action"] == 'delete':
            return reverse_insert(event, self.max_filtration_len)

        elif event["action"] == 'insert':

            return reverse_delete(event)

        elif event["action"] == 'update':
            return dump_update(event, self.max_filtration_len)


if __name__ == '__main__':
    mysql_settings = {
        'host': '',
        'port': 3306,
        'user': '',
        'password': ''
    }
    CooHSQL = CooHSQL(mysql_settings)
    CooHSQL.process_binlog()
