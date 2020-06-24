import datetime
import json
import os
from unittest import TestCase

from airflow import DAG
from airflow.models import BaseOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

from awehflow.config import Config
from awehflow.core import ConfigCache, DagLoader, SubDag, DependencySensors
from tests.helpers import prepare_clean_tmp_dir, tmp_dir_path, ensure_dir_exists, dict_to_yml


class TestConfigCache(TestCase):

    def setUp(self):
        self.configs = [
            {
                'name': 'pipeline_1',
                'start_date': '2020-03-29',
                'schedule': '30 23 * * *',
                'catchup': True,
                'engineers': [
                    {
                        'name': 'Engineer 1',
                        'slack': 'engineer_1'
                    }
                ]
            },
            {
                'name': 'pipeline_2',
                'start_date': '2020-03-30',
                'engineers': [
                    {
                        'name': 'Engineer 2',
                        'slack': 'engineer_2'
                    }
                ]
            }
        ]

        prepare_clean_tmp_dir(folder_name='config_cache')
        self.configs_path = os.path.join(tmp_dir_path(), 'config_cache')
        ensure_dir_exists(self.configs_path)

        for config in self.configs:
            config_path = os.path.join(self.configs_path, '{}.yml'.format(config['name']))
            dict_to_yml(config, config_path)

        self.config_cache = ConfigCache(self.configs_path)

    def test_cache_directory_path(self):
        self.assertEqual(self.config_cache.cache_directory_path, '{}/.cache'.format(self.configs_path))

    def test_bundle_path(self):
        self.assertEqual(self.config_cache.bundle_path, '{}/.cache/configs_bundle.json'.format(self.configs_path))

    def test_config_files_glob(self):
        self.assertEqual(len(self.config_cache.config_files_glob), 2)
        self.assertCountEqual([file.split('/')[-1] for file in self.config_cache.config_files_glob],
                              ['pipeline_1.yml', 'pipeline_2.yml'])

    def test_refresh_cache(self):
        self.config_cache.refresh_cache()
        self.assertTrue(os.path.exists(self.config_cache.bundle_path))

        with open(self.config_cache.bundle_path) as json_file:
            configs_read_from_bundle = json.load(json_file)

        self.assertCountEqual(self.configs, configs_read_from_bundle)

    def test_read_cache(self):
        with self.assertRaises(FileNotFoundError):
            self.config_cache.read_cache()

        self.config_cache.refresh_cache()
        configs = self.config_cache.read_cache(environment='prod')
        self.assertCountEqual([Config(config, environment='prod') for config in self.configs], configs)


class TestDagLoader(TestCase):
    def setUp(self):
        self.configs = [
            {
                'name': 'pipeline_a',
                'start_date': '2020-03-29',
                'schedule': '30 23 * * *',
                'catchup': True,
                'engineers': [
                    {
                        'name': 'Engineer 1',
                        'slack': 'engineer_1'
                    }
                ],
                'tasks': [
                    {
                        'id': 'stage_1',
                        'operator': 'airflow.operators.bash_operator.BashOperator',
                        'params': {
                            'bash_command': 'echo "hello world"'
                        }
                    },
                    {
                        'id': 'stage_2',
                        'operator': 'airflow.operators.bash_operator.BashOperator',
                        'params': {
                            'bash_command': 'echo "hello universe"'
                        },
                        'upstream': ['stage_1']
                    },
                    {
                        'id': 'stage_2b',
                        'operator': 'airflow.operators.bash_operator.BashOperator',
                        'params': {
                            'bash_command': 'echo "hello universe in parallel"'
                        },
                        'upstream': ['stage_1']
                    }
                ]
            },
            {
                'name': 'pipeline_b',
                'start_date': '2020-03-30',
                'engineers': [
                    {
                        'name': 'Engineer 2',
                        'slack': 'engineer_2'
                    }
                ],
                'dependencies': [
                    {
                        'id': 'sensor_1',
                        'operator': 'airflow.sensors.time_sensor.TimeSensor',
                        'params': {
                            'target_time': '2020-03-29 00:00:00'
                        }
                    },
                    {
                        'id': 'sensor_2',
                        'operator': 'airflow.sensors.time_sensor.TimeSensor',
                        'params': {
                            'target_time': '2020-03-29 00:00:00'
                        }
                    },
                ],
                'tasks': [
                    {
                        'id': 'stage_1b',
                        'operator': 'airflow.operators.bash_operator.BashOperator',
                        'params': {
                            'bash_command': 'echo "hello world"'
                        }
                    },
                    {
                        'id': 'stage_2c',
                        'operator': 'airflow.operators.bash_operator.BashOperator',
                        'params': {
                            'bash_command': 'echo "hello world"'
                        }
                    }
                ]
            }
        ]

        prepare_clean_tmp_dir(folder_name='config_cache')
        self.configs_path = os.path.join(tmp_dir_path(), 'config_cache')
        ensure_dir_exists(self.configs_path)

        for config in self.configs:
            config_path = os.path.join(self.configs_path, '{}.yml'.format(config['name']))
            dict_to_yml(config, config_path)

        configs_cache = ConfigCache(configs_path=self.configs_path)
        configs_cache.refresh_cache()

        self.dag_loader = DagLoader(
            project="test_project",
            configs_path=self.configs_path,
            event_handlers=[]
        )

    def test_load(self):
        dags = self.dag_loader.load(global_symbol_table=globals())
        for variable_name, dag in dags:
            self.assertEqual(globals()[variable_name], dag)

    def test_load_dag_dependencies(self):
        dags = self.dag_loader.load(global_symbol_table=globals())

        # Pipeline A
        # ==========
        dag = next(dag for var_name, dag in dags if dag.dag_id == 'pipeline_a_v1')

        task_ids = list(map(lambda task: task.task_id, dag.tasks))
        self.assertCountEqual(task_ids, ['start', 'stage_1', 'stage_2', 'stage_2b', 'success', 'failure'])

        start = dag.get_task('start')
        stage_1 = dag.get_task('stage_1')
        stage_2 = dag.get_task('stage_2')
        stage_2b = dag.get_task('stage_2b')
        success = dag.get_task('success')
        failure = dag.get_task('failure')

        self.assertCountEqual(list(map(lambda task: task.task_id, start.upstream_list)), [])
        self.assertCountEqual(list(map(lambda task: task.task_id, stage_1.upstream_list)), ['start'])
        self.assertCountEqual(list(map(lambda task: task.task_id, stage_2.upstream_list)), ['stage_1'])
        self.assertCountEqual(list(map(lambda task: task.task_id, stage_2b.upstream_list)), ['stage_1'])
        self.assertCountEqual(list(map(lambda task: task.task_id, success.upstream_list)), ['stage_2', 'stage_2b'])
        self.assertCountEqual(list(map(lambda task: task.task_id, failure.upstream_list)), ['stage_2', 'stage_2b'])

        # Pipeline B
        # ==========
        dag = next(dag for var_name, dag in dags if dag.dag_id == 'pipeline_b_v1')

        task_ids = list(map(lambda task: task.task_id, dag.tasks))
        self.assertCountEqual(task_ids, ['start', 'sensor_1', 'sensor_2', 'stage_1b', 'stage_2c', 'success', 'failure'])

        start = dag.get_task('start')
        sensor_1 = dag.get_task('sensor_1')
        sensor_2 = dag.get_task('sensor_2')
        stage_1b = dag.get_task('stage_1b')
        stage_2c = dag.get_task('stage_2c')
        success = dag.get_task('success')
        failure = dag.get_task('failure')

        self.assertCountEqual(list(map(lambda task: task.task_id, start.upstream_list)), [])
        self.assertCountEqual(list(map(lambda task: task.task_id, sensor_1.upstream_list)), ['start'])
        self.assertCountEqual(list(map(lambda task: task.task_id, sensor_2.upstream_list)), ['start'])
        self.assertCountEqual(list(map(lambda task: task.task_id, stage_1b.upstream_list)), ['sensor_1', 'sensor_2'])
        self.assertCountEqual(list(map(lambda task: task.task_id, stage_2c.upstream_list)), ['sensor_1', 'sensor_2'])
        self.assertCountEqual(list(map(lambda task: task.task_id, success.upstream_list)), ['stage_1b', 'stage_2c'])
        self.assertCountEqual(list(map(lambda task: task.task_id, failure.upstream_list)), ['stage_1b', 'stage_2c'])

    def test_build_task(self):
        task = DagLoader.build_task(task_id='some_task__id',
                                    dag=DAG(dag_id='some_dag', default_args={'start_date': datetime.datetime.now()}),
                                    operator='airflow.operators.bash_operator.BashOperator',
                                    bash_command='echo "hello world"')

        self.assertIsInstance(task, BashOperator)
        self.assertEqual(task.task_id, 'some_task__id')
        self.assertEqual(task.bash_command, 'echo "hello world"')

    def test_build_task_with_expected_class(self):
        task = DagLoader.build_task(task_id='some_task__id',
                                    dag=DAG(dag_id='some_dag', default_args={'start_date': datetime.datetime.now()}),
                                    operator='airflow.operators.bash_operator.BashOperator',
                                    expected_class=BashOperator,
                                    bash_command='echo "hello world"')
        self.assertIsInstance(task, BashOperator)

        task = DagLoader.build_task(task_id='some_task__id',
                                    dag=DAG(dag_id='some_dag', default_args={'start_date': datetime.datetime.now()}),
                                    operator='airflow.operators.bash_operator.BashOperator',
                                    expected_class=BaseOperator,
                                    bash_command='echo "hello world"')
        self.assertIsInstance(task, BashOperator)

        with self.assertRaises(Exception):
            task = DagLoader.build_task(task_id='some_task__id',
                                        dag=DAG(dag_id='some_dag',
                                                default_args={'start_date': datetime.datetime.now()}),
                                        operator='airflow.operators.bash_operator.BashOperator',
                                        expected_class=PythonOperator,
                                        bash_command='echo "hello world"')


class TestSubDag(TestCase):

    def setUp(self):
        self.task_configs = [
            {
                'id': 'stage_1',
                'operator': 'airflow.operators.bash_operator.BashOperator',
                'params': {
                    'bash_command': 'echo "hello world"'
                }
            },
            {
                'id': 'stage_2',
                'operator': 'airflow.operators.bash_operator.BashOperator',
                'params': {
                    'bash_command': 'echo "hello universe"'
                },
                'upstream': ['stage_1']
            },
            {
                'id': 'stage_2b',
                'operator': 'airflow.operators.bash_operator.BashOperator',
                'params': {
                    'bash_command': 'echo "hello universe in parallel"'
                },
                'upstream': ['stage_1']
            }
        ]

        self.dag = DAG(dag_id='some_dag', default_args={'start_date': datetime.datetime.now()})

        self.sub_dag = SubDag(
            task_configs=self.task_configs,
            dag=self.dag,
            params={}
        )

    def test_leaves(self):
        leaf_ids = [leaf.task_id for leaf in self.sub_dag.leaves]

        self.assertCountEqual(leaf_ids, ['stage_2', 'stage_2b'])

    def test_roots(self):
        root_ids = [root.task_id for root in self.sub_dag.roots]

        self.assertCountEqual(root_ids, ['stage_1'])


class TestDependencySensors(TestCase):

    def setUp(self):
        self.sensor_configs = [
            {
                'id': 'sensor_1',
                'operator': 'airflow.sensors.time_sensor.TimeSensor',
                'params': {
                    'target_time': datetime.time(0, 0, 0)
                }
            },
            {
                'id': 'sensor_2',
                'operator': 'airflow.sensors.time_sensor.TimeSensor',
                'params': {
                    'target_time': datetime.time(0, 0, 0)
                }
            },
            {
                'id': 'sensor_3',
                'operator': 'airflow.sensors.time_sensor.TimeSensor',
                'params': {
                    'target_time': datetime.time(0, 0, 0)
                }
            }
        ]

        self.dag = DAG(dag_id='some_dag', default_args={'start_date': datetime.datetime.now()})

        self.dependency_sensors = DependencySensors(
            sensor_configs=self.sensor_configs,
            dag=self.dag,
            params={}
        )

    def test_leaves(self):
        task_ids = [task.task_id for task in self.dependency_sensors.leaves]
        self.assertCountEqual(task_ids, ['sensor_1', 'sensor_2', 'sensor_3'])

    def test_roots(self):
        task_ids = [task.task_id for task in self.dependency_sensors.roots]
        self.assertCountEqual(task_ids, ['sensor_1', 'sensor_2', 'sensor_3'])
