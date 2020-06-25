from collections import defaultdict
from ...wrapper.mysql import RawDatabaseConnector


class RawDataHelper(object):
    def __init__(self):
        self._updated_count = defaultdict(int)

    def _upload_raw(self, df, table_name, to_truncate=False):
        print(table_name)
        # print(df)
        if to_truncate:
            with RawDatabaseConnector().managed_session() as mn_session:
                try:
                    mn_session.execute(f'TRUNCATE TABLE {table_name}')
                    mn_session.commit()
                except Exception as e:
                    print(f'Failed to truncate table {table_name} <err_msg> {e}')
        df.to_sql(table_name, RawDatabaseConnector().get_engine(), index=False, if_exists='append')

        self._updated_count[table_name] += df.shape[0]

