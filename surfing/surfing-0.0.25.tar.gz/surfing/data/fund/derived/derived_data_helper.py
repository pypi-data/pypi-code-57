from collections import defaultdict
from ...wrapper.mysql import DerivedDatabaseConnector


class DerivedDataHelper(object):
    def __init__(self):
        self._updated_count = defaultdict(int)

    def _upload_derived(self, df, table_name):
        print(table_name)
        # print(df)
        df.to_sql(table_name, DerivedDatabaseConnector().get_engine(), index=False, if_exists='append')

        self._updated_count[table_name] += df.shape[0]
