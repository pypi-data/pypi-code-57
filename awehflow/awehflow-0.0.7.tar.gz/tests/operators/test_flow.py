import datetime
from unittest import TestCase
from unittest.mock import MagicMock, patch, call

import pytz
from airflow import DAG
from airflow.models import TaskInstance

from awehflow.operators.flow import EventEmittingOperator, StartOperator, SuccessOperator, FailureOperator


class TestEventEmittingOperatorOperator(TestCase):
    def setUp(self):
        self.dag = DAG(dag_id='some_dag', start_date=datetime.datetime.now())
        self.handler1 = MagicMock()
        self.handler2 = MagicMock()
        self.task = EventEmittingOperator(
            dag=self.dag,
            task_id='task',
            event_handlers=[self.handler1, self.handler2]
        )

        self.task_instance = TaskInstance(task=self.task, execution_date=datetime.datetime(1985, 3, 29))
        self.task_instance_context = self.task_instance.get_template_context()

    def test_execute(self):
        with self.assertRaises(Exception):
            self.task.execute(self.task_instance_context)

    def test_emit_event(self):
        self.task.emit_event('some_event_name', body={'field': 'val'})
        self.handler1.handle.assert_called_once_with({
            'name': 'some_event_name',
            'body': {'field': 'val'}
        })
        self.handler2.handle.assert_called_once_with({
            'name': 'some_event_name',
            'body': {'field': 'val'}
        })


class TestStartOperator(TestCase):
    def setUp(self):
        self.dag = DAG(dag_id='some_dag', start_date=datetime.datetime.now())
        self.task = StartOperator(
            dag=self.dag,
            task_id='task',
            project='some_project',
            event_handlers=[],
            job_name='some_job_name',
            engineers=[{'name': 'Batman'}]
        )

        self.task_instance = TaskInstance(task=self.task, execution_date=datetime.datetime(1985, 3, 29, tzinfo=pytz.UTC))
        self.task_instance_context = self.task_instance.get_template_context()

    @patch('awehflow.operators.flow.utc_now')
    def test_execute(self, mock_utc_now):
        self.task.emit_event = MagicMock()
        mock_utc_now.return_value = datetime.datetime(1985, 3, 29)
        self.task_instance_context['dag_run'] = MagicMock()
        self.task_instance_context['dag_run'].run_id = 'some_dag_run_id'
        self.task.execute(self.task_instance_context)

        self.task.emit_event.assert_called_once_with('start', {
            'run_id': 'some_dag_run_id',
            'dag_id': 'some_dag',
            'name': 'some_job_name',
            'project': 'some_project',
            'engineers': [{'name': 'Batman'}],
            'status': 'running',
            'start_time': datetime.datetime(1985, 3, 29),
            'reference_time': datetime.datetime(1985, 3, 30, tzinfo=pytz.UTC)
        })


class TestSuccessOperator(TestCase):
    def setUp(self):
        self.dag = DAG(dag_id='some_dag', start_date=datetime.datetime.now())
        self.task = SuccessOperator(
            dag=self.dag,
            task_id='task',
            project='some_project',
            event_handlers=[],
            job_name='some_job_name',
            engineers=[{'name': 'Batman'}]
        )

        self.task_instance = TaskInstance(task=self.task, execution_date=datetime.datetime(1985, 3, 29))
        self.task_instance_context = self.task_instance.get_template_context()

    @patch('awehflow.operators.flow.utc_now')
    def test_execute(self, mock_utc_now):
        self.task.emit_event = MagicMock()
        mock_utc_now.return_value = datetime.datetime(1985, 3, 29)
        self.task_instance_context['dag_run'] = MagicMock()
        self.task_instance_context['dag_run'].run_id = 'some_dag_run_id'
        self.task.execute(self.task_instance_context)

        self.task.emit_event.assert_called_once_with('success', {
            'run_id': 'some_dag_run_id',
            'dag_id': 'some_dag',
            'name': 'some_job_name',
            'project': 'some_project',
            'engineers': [{'name': 'Batman'}],
            'status': 'success',
            'end_time': datetime.datetime(1985, 3, 29)
        })


class TestFailureOperator(TestCase):
    def setUp(self):
        self.dag = DAG(dag_id='some_dag', start_date=datetime.datetime.now())
        self.task = FailureOperator(
            dag=self.dag,
            task_id='task',
            project='some_project',
            event_handlers=[],
            job_name='some_job_name',
            engineers=[{'name': 'Batman'}]
        )

        self.task_instance = TaskInstance(task=self.task, execution_date=datetime.datetime(1985, 3, 29))
        self.task_instance_context = self.task_instance.get_template_context()

    @patch('awehflow.operators.flow.utc_now')
    def test_execute(self, mock_utc_now):
        self.task.emit_event = MagicMock()
        mock_utc_now.return_value = datetime.datetime(1985, 3, 29)
        self.task_instance_context['dag_run'] = MagicMock()
        self.task_instance_context['dag_run'].run_id = 'some_dag_run_id'
        self.task_instance_context['task_instance'] = MagicMock()
        self.task_instance_context['task_instance'].log_url = 'example.com'
        self.task_instance_context['task_instance'].task_id = 'task'
        self.task_instance_context['exception'] = 'Exception message'
        self.task.execute(self.task_instance_context)

        self.task.emit_event.assert_called_once_with('failure', {
            'run_id': 'some_dag_run_id',
            'dag_id': 'some_dag',
            'name': 'some_job_name',
            'project': 'some_project',
            'engineers': [{'name': 'Batman'}],
            'status': 'failure',
            'error': {
                'task_id': 'task',
                'message': 'Exception message',
                'log_url': 'example.com'
            },
            'end_time': datetime.datetime(1985, 3, 29)
        })
