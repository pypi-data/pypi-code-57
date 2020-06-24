from airflow.contrib.hooks.bigquery_hook import BigQueryHook
from airflow.operators.sensors import BaseSensorOperator
from airflow.utils.decorators import apply_defaults


class BigQueryDataSensor(BaseSensorOperator):
    """
    Does a data check in Google Bigquery. It requires a select statement that
    returns 0 records for a successful check

        :param sql: The BigQuery SQL select statement returning 0 records for success, more
            than 0 records for failure
        :type sql: string
        :param bigquery_conn_id: The connection ID to use when connecting to
            Google BigQuery.
        :type bigquery_conn_id: string
    """
    template_fields = ('sql',)
    ui_color = '#f0eee4'

    @apply_defaults
    def __init__(self,
                 sql,
                 bigquery_conn_id='bigquery_default_conn',
                 *args, **kwargs):

        super(BigQueryDataSensor, self).__init__(*args, **kwargs)
        self.sql = sql
        self.bigquery_conn_id = bigquery_conn_id

    def poke(self, context):
        self.log.info('BigQuery sensor data check:\n%s', self.sql)
        hook = BigQueryHook(bigquery_conn_id=self.bigquery_conn_id)
        result = hook.get_first(sql=self.sql)
        return result is None
