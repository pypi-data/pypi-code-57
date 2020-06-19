from remo_app.cmd.log import Log


def manage(argv):
    from django.core.management import execute_from_command_line

    argv = 'manage.py ' + argv
    argv = argv.split()
    execute_from_command_line(argv)


def migrate():
    Log.msg('* Prepare database')
    manage('migrate')


def is_database_uptodate():
    from django.db.migrations.executor import MigrationExecutor
    from django.db import connections, DEFAULT_DB_ALIAS

    connection = connections[DEFAULT_DB_ALIAS]
    connection.prepare_database()
    executor = MigrationExecutor(connection)
    targets = executor.loader.graph.leaf_nodes()
    return not executor.migration_plan(targets)
