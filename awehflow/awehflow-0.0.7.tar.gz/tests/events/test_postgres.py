import datetime
from unittest import TestCase
from unittest.mock import patch, MagicMock

from awehflow.events.postgres import PostgresMetricsEventHandler


class TestPostgresMetricsEventHandler(TestCase):
    @patch('awehflow.events.postgres.PostgresHook')
    def setUp(self, _):
        self.handler = PostgresMetricsEventHandler(
            jobs_table='some_jobs_table',
            task_metrics_table='some_task_metrics_table'
        )

    def test_handle(self):
        """All events should literally just pass the event the event along to pubsub"""
        self.handler._PostgresMetricsEventHandler__upsert_job = MagicMock()
        event = {'name': 'start'}
        self.handler.handle(event)
        self.handler._PostgresMetricsEventHandler__upsert_job.assert_called_once_with(event)

        self.handler._PostgresMetricsEventHandler__upsert_job = MagicMock()
        event = {'name': 'success'}
        self.handler.handle(event)
        self.handler._PostgresMetricsEventHandler__upsert_job.assert_called_once_with(event)

        self.handler._PostgresMetricsEventHandler__upsert_job = MagicMock()
        event = {'name': 'failure'}
        self.handler.handle(event)
        self.handler._PostgresMetricsEventHandler__upsert_job.assert_called_once_with(event)

        self.handler._PostgresMetricsEventHandler__insert_task_metric = MagicMock()
        event = {'name': 'task_metric'}
        self.handler.handle(event)
        self.handler._PostgresMetricsEventHandler__insert_task_metric.assert_called_once_with(event)

        self.handler._PostgresMetricsEventHandler__upsert_job = MagicMock()
        event = {'name': 'woot'}
        self.handler.handle(event)
        self.handler._PostgresMetricsEventHandler__upsert_job.assert_not_called()

    def test_upsert_job(self):
        self.handler.hook = MagicMock()

        self.handler._PostgresMetricsEventHandler__upsert_job({
            'name': 'something',
            'body': {
                'run_id': 'some_run_id',
                'dag_id': 'some_dag_id',
                'name': 'some_name',
                'engineers': [
                    {
                        'name': 'Batman'
                    }
                ],
                'start_time': datetime.datetime(1985, 3, 29),
                'reference_time': datetime.datetime(1986, 3, 29)
            }
        })
        self.handler.hook.run.assert_called_once_with(
            sql="""
            INSERT INTO some_jobs_table (run_id,dag_id,name,engineers,start_time,reference_time)
            VALUES (%s,%s,%s,%s,%s,%s)
            ON CONFLICT ON CONSTRAINT run_id_dag_id_unique DO UPDATE SET (name,engineers,start_time,reference_time) = (EXCLUDED.name,EXCLUDED.engineers,EXCLUDED.start_time,EXCLUDED.reference_time)
        """,
            parameters=('some_run_id', 'some_dag_id', 'some_name', '[{"name": "Batman"}]', '1985-03-29 00:00:00', '1986-03-29 00:00:00')
        )

    def test_insert_task_metric(self):
        self.handler.hook = MagicMock()

        self.handler._PostgresMetricsEventHandler__insert_task_metric({
            'name': 'something',
            'body': {
                'run_id': 'some_run_id',
                'dag_id': 'some_dag_id',
                'job_name': 'some_job_name',
                'task_id': 'some_task_id',
                'value': {
                    'name': 'Batman'
                },
                'created_time': datetime.datetime(1985, 3, 29),
                'reference_time': datetime.datetime(1986, 3, 29)
            }
        })
        self.handler.hook.run.assert_called_once_with(
            sql="""
            INSERT INTO some_task_metrics_table (run_id,dag_id,job_name,task_id,value,created_time,reference_time)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """,
            parameters=('some_run_id', 'some_dag_id', 'some_job_name', 'some_task_id', '{"name": "Batman"}', '1985-03-29 00:00:00', '1986-03-29 00:00:00')
        )