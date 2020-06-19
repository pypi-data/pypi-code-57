import shutil
import os
import subprocess
import sys
import time

import requests
import platform
import json

from remo_app.cmd.log import Log
from remo_app.cmd.viewer import electron
from remo_app.config import REMO_HOME
from remo_app.remo.stores.version_store import Version
from remo_app.config.config import Config


class ProgressBar:
    def __init__(self, text='Progress', total=100, response=None, full_bar_width=50):
        self.text = f'{text}:'
        self.total = total
        if response:
            content_size = self.content_size(response.headers)
            if content_size != -1:
                self.total = content_size
        self.full_bar_width = full_bar_width
        self.current_progress = 0

    def progress(self, progress=1):
        self.current_progress += progress
        self.show_progress(int(self.current_progress / self.total))

    def bar(self, percent: int):
        done = int((percent / 100) * self.full_bar_width)
        rest = self.full_bar_width - done
        return f"[{'#' * done}{' ' * rest}]"

    def show_progress(self, percent: int):
        end = '\n' if percent == 100 else '\r'
        print(f'{self.text} {self.bar(percent)} {percent}%  ', end=end)

    def done(self):
        self.show_progress(100)

    @staticmethod
    def content_size(headers):
        try:
            return int(headers.get('content-length'))
        except (KeyError, TypeError):
            return -1


class Download:
    def __init__(self, url, path, text, retries=3):
        if self.is_file_exists(path):
            return
        Log.msg(text)
        self.download(url, path, retries)

    def download(self, url, path, retries):
        self.makedir(path)

        for _ in range(retries):
            if not self.download_with_aria(url, path):
                self.download_fallback(url, path)
            if self.is_file_exists(path):
                break

        if not self.is_file_exists(path):
            Log.installation_aborted(f'failed to download file from URL {url} to location {path}')

    def makedir(self, path):
        dir_path, filename = os.path.split(path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def is_file_exists(self, path) -> bool:
        return os.path.exists(path)

    def download_with_aria(self, url, path) -> bool:
        if not self.is_tool_exists('aria2c'):
            return False

        dir_path, filename = os.path.split(path)
        cmd = f'aria2c -d "{dir_path}" -o "{filename}" "{url}"'
        Shell.run(cmd, show_output=False)

        return self.is_file_exists(path)

    def download_fallback(self, url, path, chunk_size=1024 * 1024):
        with open(path, 'wb') as f:
            with requests.get(url, stream=True) as resp:
                bar = ProgressBar('Progress', total=60 * 1024 * 1024, response=resp)
                for chunk in resp.iter_content(chunk_size):
                    if chunk:
                        f.write(chunk)
                        bar.progress(len(chunk))

    @staticmethod
    def is_tool_exists(tool):
        return bool(shutil.which(tool))


class Shell:
    @staticmethod
    def ok(cmd: str, show_command=True, show_output=True) -> bool:
        """
        Runs command in shell

        Args:
            cmd: command to run
            show_command: print out command to console
            show_output: print out command output to console

        Returns:
            True if succeeded
        """
        return Shell.run(cmd, show_command=show_command, show_output=show_output) == 0

    @staticmethod
    def run(cmd: str, show_command=True, show_output=True) -> int:
        """
        Runs command in shell

        Args:
            cmd: command to run
            show_command: print out command to console
            show_output: print out command output to console

        Returns:
            status code
        """
        if show_command:
            Log.msg(f"$ {cmd}")
        kwargs = {'shell': True}
        if not show_output:
            kwargs['stdout'] = subprocess.DEVNULL
            kwargs['stderr'] = subprocess.DEVNULL
        return subprocess.call(cmd, **kwargs)

    @staticmethod
    def output(cmd: str, show_command=True) -> str:
        """
        Runs command in shell and return back result

        Args:

            cmd: command to run
            show_command:  print out command to console

        Returns:
            command result as string
        """

        if show_command:
            Log.msg(f"$ {cmd}")
        output = subprocess.check_output(cmd.split())
        return output.decode("utf-8").strip()


def _get_pip_executable():
    python_dir = os.path.dirname(sys.executable)
    files = os.listdir(python_dir)
    for pip in ('pip', 'pip.exe', 'pip3', 'pip3.exe'):
        if pip in files:
            return os.path.join(python_dir, pip)

    if 'Scripts' in files:
        scripts_dir = os.path.join(python_dir, 'Scripts')
        for pip in ('pip.exe', 'pip3.exe'):
            if pip in os.listdir(scripts_dir):
                return os.path.join(scripts_dir, pip)

    Log.exit('pip was not found')


class Pip:
    executable = _get_pip_executable()

    @staticmethod
    def run(command, package):
        if not Shell.ok(f'"{Pip.executable}" {command} {package}', show_output=False):
            Log.exit(f'pip failed to {command} {package}')

    @staticmethod
    def install(package):
        Pip.run('install', package)

    @staticmethod
    def uninstall(package):
        Pip.run('uninstall', package)


class PostgresInstaller:
    username = 'remo'
    dbname = 'remo'
    userpass = 'remo'

    @staticmethod
    def _install_psycopg2():
        Pip.install('psycopg2')

    @staticmethod
    def _is_installed_psycopg2():
        try:
            import psycopg2
        except Exception:
            return False
        return True

    def install(self):
        if not self._is_installed():
            self._install()
        if not self._is_installed():
            Log.run_again('failed to install postgres, try to install it manually')

        if not self._is_installed_psycopg2():
            self._install_psycopg2()
        if not self._is_installed_psycopg2():
            Log.run_again("""failed to install psycopg2 pip package.
You can try to install it manually with `pip install psycopg2`""")

        if not self._is_running():
            self._launch()

        db = self._create_db_and_user(self.dbname, self.username, self.userpass)
        db_params = json.dumps(db, indent=2, sort_keys=True)
        if not self.can_connect(self.dbname, self.username, self.userpass):
            Log.exit(f"""
Failed connect to database:
{db_params}
""")

        Log.msg(f"""
Postgres database connection parameters:
{db_params}
""")
        return db

    def on_start_check(self, db_params):
        if self.can_connect(**db_params):
            return

        if not self._is_installed():
            Log.exit(
                """postgres not installed

Please run: python -m remo_app init
""")

        if not self._is_running():
            self._launch()

        if not self._is_installed_psycopg2():
            self._install_psycopg2()

        if not self.can_connect(**db_params):
            Log.exit(f"""failed connect to database.
Please check `db_url` value in config file: {Config.path()}.""")

    @staticmethod
    def db_params(database='', user='', password='', host='localhost', port='5432'):
        return {
            'engine': 'postgres',
            'user': user,
            'password': password,
            'host': host,
            'port': port,
            'name': database,
        }

    @staticmethod
    def can_connect(database='', user='', password='', host='localhost', port='5432', **kwargs):
        try:
            import psycopg2
            conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
        except Exception:
            return False
        conn.close()
        return True

    def _is_installed(self):
        raise NotImplementedError()

    def _is_running(self):
        raise NotImplementedError()

    def _launch(self):
        raise NotImplementedError()

    def _install(self):
        raise NotImplementedError()

    def _create_db_and_user(self, dbname, username, password):
        raise NotImplementedError()

    def _drop_db(self, database: str):
        raise NotImplementedError()

    def restart(self) -> bool:
        raise NotImplementedError()

    def drop_database(self, db_params):
        if not self.restart():
            Log.exit('failed to drop remo database, unable to restart postgres')

        for _ in range(5):
            if self.can_connect(**db_params):
                break
            time.sleep(1)

        if self.can_connect(**db_params):
            self._drop_db(db_params.get('database'))
        else:
            Log.exit(f"""failed connect to database.
Please check that `db_url` value in the config file {Config.path()} is correct.""")


class OSInstaller:
    sqlite_url = ''
    sqlite_exe = ''

    def install(self, postgres: PostgresInstaller):
        self.install_os_specific_tools()

        self.drop_electron_files()
        self.setup_remo_home()

        Log.stage('Installing vips lib')
        self.install_vips()

        Log.stage('Installing postgres')
        return postgres.install()

    def uninstall(self, postgres: PostgresInstaller, db_params):
        Log.stage('Deleting database')
        postgres.drop_database(db_params)

        Log.stage('Deleting remo folder')
        self.delete_remo_home_folder()

    def install_os_specific_tools(self):
        pass

    def install_vips(self):
        if not Shell.ok("vips -v", show_command=False, show_output=False):
            Shell.run(self.vips_install_cmd, show_output=False)
        if not Shell.ok("vips -v", show_command=False, show_output=False):
            Log.run_again(f"""failed to install vips library

You can try to install vips manually with the following command:
{self.vips_install_cmd}""")

    def install_sqlite(self):
        if self.is_tool_exists('sqlite3'):
            return

        path = str(os.path.join(REMO_HOME, 'sqlite'))
        if not os.path.exists(path):
            os.makedirs(path)

        archive_path = os.path.join(path, 'sqlite.zip')
        if not os.path.exists(archive_path):
            Download(self.sqlite_url, archive_path, '* Downloading sqlite:')

            bin_path = str(os.path.join(path, 'bin'))
            if not os.path.exists(bin_path):
                os.makedirs(bin_path)
            Log.msg('* Extract sqlite')
            self.unzip(archive_path, bin_path)

        if os.path.exists(self.sqlite_exe):
            os.environ["PATH"] = os.path.dirname(self.sqlite_exe) + os.pathsep + os.environ["PATH"]
        else:
            Log.exit_warn("""automatic installation for SQLite failed. Please try to install it manually.
See instructions here https://www.sqlitetutorial.net/download-install-sqlite/""")

    def unzip(self, archive_path: str, extract_path: str, retries: int = 3):
        if os.path.exists(extract_path):
            shutil.rmtree(extract_path, ignore_errors=True)
        if not os.path.exists(extract_path):
            os.makedirs(extract_path)

        for _ in range(retries):
            if self._unzip(archive_path, extract_path):
                break

        if not os.listdir(extract_path):
            Log.run_again(f"""failed to unzip {archive_path} into {extract_path}.
You can try to do it manually""")

    def _unzip(self, archive_path: str, extract_path: str) -> bool:
        return Shell.ok(f'unzip -q "{archive_path}" -d "{extract_path}"', show_output=False)

    @staticmethod
    def is_tool_exists(tool):
        return bool(shutil.which(tool))

    @staticmethod
    def get_latest_available_electron_app_version():
        try:
            resp = requests.get(f'https://app.remo.ai/version?electron-app-platform={platform.system()}').json()
            return resp.get('version')
        except Exception:
            pass

    @staticmethod
    def get_electron_app_version() -> str:
        path = electron.get_executable_path()
        if os.path.exists(path):
            return Shell.output(f'"{path}" --version', show_command=False)

    def is_new_electron_app_available(self) -> bool:
        latest = self.get_latest_available_electron_app_version()
        current = self.get_electron_app_version()
        return Version.to_num(latest) > Version.to_num(current)

    def download_electron_app(self):
        app_path = str(os.path.join(REMO_HOME, 'app'))
        if os.path.exists(app_path) and os.listdir(app_path):
            # skip if dir not empty
            return

        Log.stage('Installing electron app')

        archive_path = os.path.join(REMO_HOME, 'app.zip')
        if not os.path.exists(archive_path):
            url = 'https://app.remo.ai/download/latest?platform={}'.format(platform.system())
            Download(url, archive_path, '* Downloading remo app:')

        Log.msg('* Extract remo app')
        self.unzip(archive_path, app_path)

    def drop_electron_files(self):
        if not self.is_new_electron_app_available():
            return

        app_path = str(os.path.join(REMO_HOME, 'app'))
        if os.path.exists(app_path):
            shutil.rmtree(app_path, ignore_errors=True)

        archive_path = os.path.join(REMO_HOME, 'app.zip')
        if os.path.exists(archive_path):
            os.remove(archive_path)

    @staticmethod
    def setup_remo_home():
        if not os.path.exists(REMO_HOME):
            Log.msg(f'Installing Remo to dir: {REMO_HOME}')
            os.makedirs(REMO_HOME)

    def dependencies(self) -> list:
        return []

    def delete_remo_home_folder(self):
        if os.path.exists(REMO_HOME):
            shutil.rmtree(REMO_HOME, ignore_errors=True)
        if os.path.exists(REMO_HOME):
            self.delete_folder(REMO_HOME)
        if os.path.exists(REMO_HOME):
            Log.warn(f'Remo dir {REMO_HOME} was not fully deleted, you can delete it manually')

    @staticmethod
    def delete_folder(path: str):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                try:
                    os.remove(os.path.join(root, name))
                except Exception as err:
                    Log.error(f'failed to delete file: {err}')
            for name in dirs:
                try:
                    os.rmdir(os.path.join(root, name))
                except Exception as err:
                    Log.error(f'failed to delete dir: {err}')


class WindowsInstaller(OSInstaller):
    sqlite_url = 'https://www.sqlite.org/2020/sqlite-tools-win32-x86-3310100.zip'
    sqlite_exe = str(
        os.path.join(REMO_HOME, 'sqlite', 'bin', 'sqlite-tools-win32-x86-3310100', 'sqlite3.exe')
    )

    def dependencies(self) -> list:
        return ['vips', 'postgres', 'scoop', 'git', 'unzip', 'aria2']

    def install_os_specific_tools(self):
        self._add_scoop_to_path()
        self.install_scoop()
        self.install_tool_with_scoop('git', 'scoop install git')
        self.install_tool_with_scoop('aria2c', 'scoop install aria2')
        self.install_tool_with_scoop('unzip', 'scoop install unzip')

    def install_scoop(self):
        if not self.is_tool_exists('scoop'):
            Log.stage('Installing scoop')

            Shell.run("""powershell.exe -Command "iwr -useb get.scoop.sh | iex" """, show_output=False)
            self._add_scoop_to_path()

        if not self.is_tool_exists('scoop'):
            Log.run_again("""failed to install scoop - package manager.
You can try to install scoop manually.

Launch PowerShell and run the following command:
Set-ExecutionPolicy RemoteSigned -scope CurrentUser
iex (new-object net.webclient).downloadstring('https://get.scoop.sh')

See: https://scoop.sh/
https://www.onmsft.com/how-to/how-to-install-the-scoop-package-manager-in-windows-10""")

    def install_tool_with_scoop(self, tool_name, install_cmd):
        if not self.is_tool_exists(tool_name):
            Shell.run(install_cmd, show_output=False)
        if not self.is_tool_exists(tool_name):
            Log.run_again(f"""failed to install {tool_name}.
You can try to install {tool_name} manually.

Launch PowerShell and run the following command:
{install_cmd}""")

    @staticmethod
    def _add_scoop_to_path():
        scoop_dir = os.path.expandvars('%userprofile%\\scoop\\shims')
        if os.path.exists(scoop_dir) and scoop_dir not in os.environ["PATH"]:
            os.environ["PATH"] = scoop_dir + os.pathsep + os.environ["PATH"]

    def install_vips(self):
        vips_bin_dir = str(os.path.join(REMO_HOME, 'libs', 'vips', 'vips-dev-8.8', 'bin'))
        vips_bin_executable = os.path.join(vips_bin_dir, 'vips.exe')
        if not os.path.exists(vips_bin_executable):
            self.download_vips()
        if not os.path.exists(vips_bin_executable):
            Log.run_again(f"""failed to install vips library.
You can try to download vips archive and unpack it manually.

Do the following steps:
1. Download zip file: https://github.com/libvips/libvips/releases/download/v8.8.4/vips-dev-w64-web-8.8.4.zip
2. Unpack it to location: {str(os.path.join(REMO_HOME, 'libs', 'vips'))}
3. Check that you have binaries in: {vips_bin_dir}""")
        os.environ["PATH"] = vips_bin_dir + os.pathsep + os.environ["PATH"]

    def download_vips(self):
        libs_path = str(os.path.join(REMO_HOME, 'libs'))
        archive_path = os.path.join(libs_path, 'vips.zip')
        url = 'https://github.com/libvips/libvips/releases/download/v8.8.4/vips-dev-w64-web-8.8.4.zip'
        Download(url, archive_path, '* Downloading vips lib:')

        vips_lib_path = str(os.path.join(libs_path, 'vips'))
        vips_bin_executable = os.path.join(vips_lib_path, 'vips-dev-8.8', 'bin', 'vips.exe')
        if not os.path.exists(vips_bin_executable):
            Log.msg('* Extract vips lib')
            self.unzip(archive_path, vips_lib_path)

    def _unzip(self, archive_path, extract_path) -> bool:
        if not self._unzip_with_7z(archive_path, extract_path):
            if not self._unzip_with_unzip(archive_path, extract_path):
                return self._unzip_fallback(archive_path, extract_path)
        return True

    def _unzip_with_7z(self, archive_path, extract_path) -> bool:
        if not self.is_tool_exists('7z'):
            return False
        return Shell.ok(f'7z x "{archive_path}" -o"{extract_path}"', show_output=False)

    def _unzip_with_unzip(self, archive_path, extract_path) -> bool:
        if not self.is_tool_exists('unzip'):
            return False
        return Shell.ok(f'unzip -q "{archive_path}" -d "{extract_path}"', show_output=False)

    def _unzip_fallback(self, archive_path, extract_path) -> bool:
        return Shell.ok(
            """powershell.exe -Command "Expand-Archive '{}' '{}'" """.format(archive_path, extract_path),
            show_output=False
        )


class MacInstaller(OSInstaller):
    sqlite_url = 'https://www.sqlite.org/2020/sqlite-tools-osx-x86-3310100.zip'
    sqlite_exe = str(os.path.join(REMO_HOME, 'sqlite', 'bin', 'sqlite-tools-osx-x86-3310100', 'sqlite3'))
    vips_install_cmd = 'brew install vips'

    def dependencies(self) -> list:
        return ['vips', 'postgres', 'brew', 'git', 'unzip']

    def install_os_specific_tools(self):
        if not Shell.ok("brew --version", show_command=False, show_output=False):
            Log.run_again("""brew was not found.
Please install homebrew - package manager for macOS. See: https://brew.sh

Paste that in a macOS Terminal:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
""")


class LinuxInstaller(OSInstaller):
    sqlite_url = 'https://www.sqlite.org/2020/sqlite-tools-linux-x86-3310100.zip'
    sqlite_exe = str(os.path.join(REMO_HOME, 'sqlite', 'bin', 'sqlite-tools-linux-x86-3310100', 'sqlite3'))
    vips_install_cmd = 'sudo apt-get install -y -qq libvips-dev'

    def dependencies(self) -> list:
        return ['vips', 'postgres', 'openssl', 'apt-transport-https', 'ca-certificates', 'unzip', 'libpq-dev', 'python3-dev', 'unzip']

    def install_os_specific_tools(self):
        Shell.run("sudo apt-get update -qq", show_output=False)
        Shell.run("sudo apt-get install -y -qq openssl", show_output=False)
        Shell.run(
            "sudo apt-get install -y -qq apt-transport-https ca-certificates unzip libpq-dev python3-dev",
            show_output=False
        )


def get_instance() -> OSInstaller:
    installer = {'Windows': WindowsInstaller, 'Linux': LinuxInstaller, 'Darwin': MacInstaller}.get(
        platform.system()
    )

    if not installer:
        Log.exit_warn(f'current operation system - {platform.system()}, is not supported.')

    arch, _ = platform.architecture()
    if arch != '64bit':
        Log.exit_warn(f'current system architecture {arch}, is not supported.')

    return installer()
