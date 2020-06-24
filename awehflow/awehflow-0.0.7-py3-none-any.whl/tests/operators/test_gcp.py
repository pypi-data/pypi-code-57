import datetime
from unittest import TestCase
from unittest.mock import MagicMock, patch, call

from airflow import DAG
from airflow.models import TaskInstance

from awehflow.operators.gcp import BigQueryJobOperator, BigQueryJobTaskMetricOperator


class TestBigQueryJobOperator(TestCase):
    def setUp(self):
        self.dag = DAG(dag_id='some_dag', start_date=datetime.datetime.now())

        self.task = BigQueryJobOperator(
            dag=self.dag,
            task_id='task',
            sql='select 1;'
        )

        self.task_instance = TaskInstance(task=self.task, execution_date=datetime.datetime(1985, 3, 29))
        self.task_instance_context = self.task_instance.get_template_context()

    @patch('awehflow.operators.gcp.BigQueryHook')
    def test_execute(self, _):
        self.task.bq_cursor = MagicMock()
        self.task.bq_cursor.run_query.return_value = 'some_job_id'
        job_id = self.task.execute(self.task_instance_context)
        self.assertEqual(job_id, 'some_job_id')


class TestBigQueryJobTaskMetricOperator(TestCase):
    def setUp(self):
        self.dag = DAG(dag_id='some_dag', start_date=datetime.datetime.now())

        self.task = BigQueryJobTaskMetricOperator(
            dag=self.dag,
            task_id='task',
            task_ids=['task_id_1', 'task_id_2']
        )

        self.task_instance = TaskInstance(task=self.task, execution_date=datetime.datetime(1985, 3, 29))
        self.task_instance_context = self.task_instance.get_template_context()

    # @patch('awehflow.operators.flow.utc_now')
    # def test_execute(self, mock_utc_now):
    #     self.task.emit_event = MagicMock()
    #     mock_utc_now.return_value = datetime.datetime(1985, 3, 29)

    @patch('awehflow.operators.gcp.BigQueryHook')
    @patch('awehflow.operators.gcp.utc_now')
    def test_execute(self, mock_utc_now, MockBigQueryHook):
        self.task.emit_event = MagicMock()
        mock_utc_now.return_value = datetime.datetime(1985, 3, 29)
        jobs = MockBigQueryHook.return_value.get_service.return_value.jobs.return_value
        jobs.get.return_value.execute.return_value = 'some_metric'
        ti = MagicMock()
        ti.xcom_pull.return_value = 'some_job_id'
        self.task_instance_context['task_instance'] = ti
        self.task_instance_context['dag_run'] = MagicMock()
        self.task_instance_context['dag_run'].run_id = 'some_dag_run_id'

        self.task.execute(self.task_instance_context)

        self.task.emit_event.assert_has_calls([
            call('task_metric', {
                'run_id': 'some_dag_run_id',
                'task_id': 'task_id_1',
                'value': 'some_metric',
                'created_time': datetime.datetime(1985, 3, 29)
            }),
            call('task_metric', {
                'run_id': 'some_dag_run_id',
                'task_id': 'task_id_2',
                'value': 'some_metric',
                'created_time': datetime.datetime(1985, 3, 29)
            })
        ], any_order=True)
