import os
import platform

import time

from .installer import PostgresInstaller, Shell
from remo_app.remo.stores.version_store import Version
from .log import Log


class WindowsPostgresInstaller(PostgresInstaller):
    def restart(self) -> bool:
        self._set_env_vars()
        if not Shell.ok("pg_ctl --version", show_command=False, show_output=False):
            Log.exit('failed to restart postgres, pg_ctl was not found in the PATH')

        return Shell.ok("pg_ctl restart")

    def _is_running(self):
        return Shell.ok("psql -U postgres -l", show_command=False, show_output=False)

    def _launch(self):
        Log.msg("Launching postgres ...")

        for _ in range(3):
            if Shell.ok("pg_ctl start", show_output=False):
                break
            time.sleep(2)

        if not Shell.ok("pg_ctl status", show_command=False, show_output=False):
            Log.exit('failed to launch postgres')

        Log.msg("""
You can stop Postgres server with following command:
$ pg_ctl stop
""")

    def _install(self):
        Shell.run("scoop install postgresql@12.2", show_output=False)
        self._set_env_vars()

    def _create_db_and_user(self, dbname, username, password):
        Shell.run(f"""psql -U postgres -c "create user {username} with encrypted password '{password}';" """, show_output=False)
        Shell.run(f"""psql -U postgres -c "create database {dbname};" """, show_output=False)
        Shell.run(f"""psql -U postgres -c "grant all privileges on database {dbname} to {username};" """, show_output=False)
        return self.db_params(database=dbname, user=username, password=password)

    def _drop_db(self, database: str):
        Shell.run(f"""psql -U postgres -c "drop database {database};" """, show_output=True)

    def _is_installed(self) -> bool:
        if self._is_psql_in_path():
            return True

        self._set_env_vars()
        return self._is_psql_in_path()

    def _is_psql_in_path(self) -> bool:
        return Shell.ok("psql --version", show_command=False, show_output=False)

    def _get_postgres_dir(self) -> str:
        for path in ('%PROGRAMFILES%\\PostgreSQL',
                     '%PROGRAMFILES(x86)%\\PostgreSQL',
                     '%USERPROFILE%\\scoop\\apps\\postgresql'):
            full_path = os.path.expandvars(path)
            if os.path.exists(full_path):
                return full_path

    def _get_postgres_version_dir(self, postgres_dir: str) -> str:
        current = os.path.join(postgres_dir, 'current')
        if os.path.exists(current):
            return current

        versions = os.listdir(postgres_dir)
        if len(versions) > 1:
            versions.sort(key=Version.to_num, reverse=True)
        return os.path.join(postgres_dir, versions[0])

    def _set_env_vars(self):
        path = self._get_postgres_dir()
        if not path:
            return

        postgres = self._get_postgres_version_dir(path)

        bin = os.path.join(postgres, 'bin')
        if os.path.exists(bin) and bin not in os.environ["PATH"]:
            os.environ["PATH"] = bin + os.pathsep + os.environ["PATH"]

        data = os.path.join(postgres, 'data')
        if not os.path.exists(os.getenv('PGDATA')):
            os.environ.pop('PGDATA')
        if os.path.exists(data) and not os.getenv('PGDATA'):
            os.environ['PGDATA'] = data


class LinuxPostgresInstaller(PostgresInstaller):

    def restart(self) -> bool:
        return Shell.ok('sudo systemctl restart postgresql')

    def _is_installed(self):
        return Shell.ok("psql --version", show_command=False, show_output=False)

    def _install(self):
        Shell.run('sudo apt-get install -y -qq postgresql-10', show_output=False)

    def _is_running(self):
        return Shell.ok("service postgresql status", show_command=False, show_output=False)

    def _launch(self):
        Log.msg("Launching postgres ...")
        Shell.run('sudo systemctl start postgresql')

        Log.msg("""
You can stop it later with following command:
$ sudo systemctl stop postgresql
""")

    def _drop_db(self, database: str):
        Shell.run(f"""sudo -u postgres psql -c "drop database {database};" """, show_output=True)

    def _create_db_and_user(self, dbname, username, password):
        Shell.run(
            f"""sudo -u postgres psql -c "create user {username} with encrypted password '{password}';" """,
            show_output=False
        )
        Shell.run(f"""sudo -u postgres psql -c "create database {dbname};" """, show_output=False)
        Shell.run(
            f"""sudo -u postgres psql -c "grant all privileges on database {dbname} to {username};" """,
            show_output=False
        )
        return self.db_params(database=dbname, user=username, password=password)


class MacPostgresInstaller(PostgresInstaller):

    def restart(self) -> bool:
        return Shell.ok('brew services restart postgresql@10')

    def _is_installed(self):
        if Shell.ok("postgres --version", show_command=False, show_output=False):
            return True
        self._add_postgres_to_path()
        return Shell.ok("postgres --version", show_command=False, show_output=False)

    def _add_postgres_to_path(self):
        if os.path.exists("/usr/local/opt/postgresql@10/bin"):
            os.environ['PATH'] = f"/usr/local/opt/postgresql@10/bin:{os.getenv('PATH')}"

    def _is_running(self):
        if Shell.ok("psql -l", show_command=False, show_output=False):
            return True
        self._add_postgres_to_path()
        return Shell.ok("psql -l", show_command=False, show_output=False)

    def _install(self):
        Shell.run('brew install postgresql@10', show_output=False)
        shell_exe_path = os.getenv('SHELL')
        shell_name = os.path.basename(shell_exe_path)
        shell_rc_path = os.path.expanduser(f'~/.{shell_name}rc')
        Shell.run(f"""echo 'export PATH="/usr/local/opt/postgresql@10/bin:$PATH"' >> {shell_rc_path}""")
        self._add_postgres_to_path()

    def _launch(self):
        postgres_exe_path = Shell.output("which postgres", show_command=False)
        postgres_dir = os.path.dirname(os.path.dirname(postgres_exe_path))
        files = list(filter(lambda name: name.startswith('homebrew'), os.listdir(postgres_dir)))
        if not files:
            Log.exit_msg("Failed to launch postgres server, please start it manually.")

        homebrew_mxcl = os.path.join(postgres_dir, files[0])
        Log.msg("Launching postgres ...")
        Shell.run(f'launchctl load {homebrew_mxcl}')

        Log.msg(f"""
You can stop it later with following command:
$ launchctl unload {homebrew_mxcl}
""")

        tries = 5
        while not self._is_running() and tries > 0:
            time.sleep(1)
            tries -= 1
        if not self._is_running():
            Log.exit("Failed to launch postgres")

    def _drop_db(self, database: str):
        Shell.run(f'dropdb {database}', show_output=True)

    def _create_db_and_user(self, dbname, username, password):
        Shell.run('createdb $USER', show_output=False)
        Shell.run(f"""psql -c "create user {username} with encrypted password '{password}';" """, show_output=False)
        Shell.run(f'createdb {dbname} -O {username}', show_output=False)
        return self.db_params(database=dbname, user=username, password=password)


def get_instance() -> PostgresInstaller:
    installer = {
        'Windows': WindowsPostgresInstaller,
        'Linux': LinuxPostgresInstaller,
        'Darwin': MacPostgresInstaller,
    }.get(platform.system())

    if not installer:
        Log.exit_warn(f'current operation system - {platform.system()}, is not supported.')

    return installer()
