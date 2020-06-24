import typing

from aws_cdk.aws_ec2 import InstanceType, InstanceSize, InstanceClass, IVpc, Port, IConnectable
from aws_cdk.aws_kms import IKey
from aws_cdk.aws_rds import DatabaseInstance, DatabaseInstanceEngine, StorageType, ParameterGroup, OptionGroup
from aws_cdk.core import Construct, Duration

INSTANCE_CLASS_MEMEORY_MULTIPLIER_MAPPING = {
    InstanceClass.STANDARD4: 1,
    InstanceClass.STANDARD5: 1,
    InstanceClass.BURSTABLE2: 1,
    InstanceClass.BURSTABLE3: 1,
    InstanceClass.MEMORY4: 2,
    InstanceClass.MEMORY5: 2,
}

INSTANCE_SIZE_TO_MEMORY_MAPPING = {
    InstanceSize.SMALL: 2,
    InstanceSize.MEDIUM: 4,
    InstanceSize.LARGE: 8,
    InstanceSize.XLARGE: 16,
    InstanceSize.XLARGE2: 32,
    InstanceSize.XLARGE4: 64,
    InstanceSize.XLARGE10: 160,
    InstanceSize.XLARGE12: 192,
    InstanceSize.XLARGE16: 256,
    InstanceSize.XLARGE24: 384,
}


class Postgres(Construct):
    def __init__(self, scope: Construct, id: str, *, master_username: str, vpc: IVpc, database_name: str,
                 instance_class: InstanceClass, instance_size: InstanceSize, instance_identifier: str = None,
                 version: str = '10.11', encryption_key: typing.Optional[IKey] = None) -> None:
        super().__init__(scope, id)
        db_memory_gb = INSTANCE_SIZE_TO_MEMORY_MAPPING[instance_size] * INSTANCE_CLASS_MEMEORY_MULTIPLIER_MAPPING[
            instance_class]
        if db_memory_gb <= 4:
            work_mem = '1024'
        elif db_memory_gb <= 8:
            work_mem = '2048'
        else:
            work_mem = '3072'
        parameters = {
            # 'archive_timeout': '900',
            'authentication_timeout': '60',
            'autovacuum': 'on',
            'autovacuum_analyze_threshold': '50',
            'autovacuum_freeze_max_age': '200000000',
            'autovacuum_max_workers': '2',
            'autovacuum_multixact_freeze_max_age': '400000000',
            'autovacuum_naptime': '60',
            'autovacuum_vacuum_scale_factor': '0.2',
            'autovacuum_vacuum_threshold': '50',
            'autovacuum_work_mem': '-1' if db_memory_gb <= 8 else f'{512 * 1024}',
            'bgwriter_delay': '150',
            'checkpoint_completion_target': '0.7',
            'checkpoint_timeout': '900',
            'effective_cache_size': f'{int(db_memory_gb * 0.5 * 1024 * 1024 / 8)}',
            'lc_messages': 'en_US.UTF-8',
            'lc_monetary': 'en_US.UTF-8',
            'lc_numeric': 'en_US.UTF-8',
            'lc_time': 'en_US.UTF-8',
            # 'listen_addresses': '*',
            'log_autovacuum_min_duration': '0',
            'log_checkpoints': 'on',
            'log_connections': 'on',
            'log_destination': 'stderr',
            'log_disconnections': 'on',
            'log_duration': '0',
            'log_error_verbosity': 'verbose',
            'log_executor_stats': '0',
            # 'log_file_mode': '0600 or above',
            'log_hostname': 'off',
            # 'log_line_prefix': 'at %t - from Application [%a] on server [%r] using user [%u] for dbname [%d] process id [%p] returned SQLSTATE [%e]:',
            'log_lock_waits': 'on',
            'log_min_duration_statement': '15000',
            'log_min_error_statement': 'error',
            'log_min_messages': 'warning',
            'log_rotation_age': '1440',
            'log_rotation_size': '10240',
            'log_statement': 'ddl',
            'log_statement_stats': '0',
            'log_temp_files': '-1',
            # 'log_truncate_on_rotation': 'off',
            'maintenance_work_mem': '262144',
            'max_files_per_process': '1000',
            'max_locks_per_transaction': '64',
            # 'max_parallel_maintenance_workers': '8',
            'max_parallel_workers': '8',
            'max_parallel_workers_per_gather': '2',
            'max_pred_locks_per_page': '2',
            'max_pred_locks_per_relation': '2',
            # 'max_replication_slots': 'match with the no.of replication servers available ',
            # 'max_wal_senders': 'match with the no.of replication servers available ',
            'rds.force_admin_logging_level': 'Warning',
            'rds.force_autovacuum_logging_level': 'error',
            'rds.log_retention_period': '10080',
            'rds.rds_superuser_reserved_connections': '3',
            'rds.restrict_password_commands': '1',
            'search_path': '$user,public',
            'shared_buffers': f'{int(0.1 * 1024 * 1024 * db_memory_gb / 8)}' if db_memory_gb <= 8 else f'{int(.25 * 1024 * 1024 * db_memory_gb / 8)}',
            'shared_preload_libraries': 'pg_stat_statements,pgaudit',
            # 'superuser_reserved_connections': '3',
            'track_functions': 'all',
            'wal_buffers': str(int(128 * 1024 / 8)) if db_memory_gb <= 8 else str(int(512 * 1024 / 8)),
            'wal_keep_segments': '32',
            'work_mem': work_mem
        }
        parameter_group = ParameterGroup(scope, 'rds-parameter-group', family='postgres10', parameters=parameters)
        option_group = OptionGroup(scope, 'rds-option-group', engine=DatabaseInstanceEngine.POSTGRES,
                                   major_engine_version='10', configurations=[])
        self.instance = DatabaseInstance(scope, "db-instance",
                                         engine=DatabaseInstanceEngine.POSTGRES,
                                         engine_version=version,
                                         instance_class=InstanceType.of(instance_class, instance_size),
                                         multi_az=True,
                                         storage_type=StorageType.IO1,
                                         allocated_storage=120,
                                         master_username=master_username,
                                         kms_key=encryption_key,
                                         vpc=vpc,
                                         database_name=database_name,
                                         storage_encrypted=True,
                                         backup_retention=Duration.days(7),
                                         monitoring_interval=Duration.seconds(60),
                                         enable_performance_insights=True,
                                         auto_minor_version_upgrade=True,
                                         parameter_group=parameter_group,
                                         option_group=option_group,
                                         deletion_protection=False,
                                         instance_identifier=instance_identifier
                                         )

    @property
    def endpoint(self):
        return self.instance.instance_endpoint.hostname

    def allow_connection_from(self, other: IConnectable, port: Port = None):
        connection_port = port or Port.tcp(5432)
        return self.instance.connections.allow_from(other, connection_port)
