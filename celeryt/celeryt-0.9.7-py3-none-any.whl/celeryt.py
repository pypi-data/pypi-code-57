"""celery-t"""
import json
import os
import subprocess
import time
from typing import List, Any, Dict

from jinja2 import Environment, BaseLoader, Template


class CeleryT:
    CELERY_FIlE: str = 'ressources/celery.json'
    SKINOS_FILE: str = 'ressources/skinos.json'
    COMMON_FILE: str = 'ressources/common.json'
    COMMIT_MESSAGE: str = ':tata: Initial commit'

    @staticmethod
    def run():
        cmd: List[str] = [
            'celery',
            '-A',
            'super_project',
            'worker',
            '-l',
            'INFO',
            '-B'
        ]
        print(f'\033[31;1m/!\\ This is for test purposes only /!\\\033[0m')
        time.sleep(1)
        try:
            subprocess.run(cmd)
        except KeyboardInterrupt:
            pass

    def __init__(self, name: str, skinos: bool, flow: bool, verbose: bool):
        self.name: str = name
        self.skinos: bool = skinos
        self.flow: bool = flow
        self.verbose: bool = verbose
        self.project_path = os.path.join(os.getcwd(), self.name)
        self.env: Environment = Environment(loader=BaseLoader)

        self.current_file_dir: str = os.path.dirname(os.path.abspath(__file__))

    def new(self) -> None:
        # generate project path
        self.generate_project_path(path=self.project_path)
        resources: Dict[str, Any] = self.load_all_resources_files()

        if self.skinos:
            print(f'Generate skinos project "{self.name}"')
        else:
            print(f'Generate celery project "{self.name}"')

        # common dirs
        self.generate_dirs(resources['common']['dirs'])
        self.generate_files(resources['common']['files'])

        if self.skinos:
            self.generate_dirs(resources['skinos']['dirs'])
            self.generate_files(resources['skinos']['files'])
        else:
            self.generate_dirs(resources['celery']['dirs'])
            self.generate_files(resources['celery']['files'])

        self.git_init()
        if self.flow:
            self.git_flow_init()

    def build_path(self, path: str) -> str:
        return os.path.join(self.current_file_dir, path)

    def load_all_resources_files(self) -> Dict[str, Any]:
        return {
            'celery': self.load_resources_file(self.build_path(self.CELERY_FIlE)),
            'skinos': self.load_resources_file(self.build_path(self.SKINOS_FILE)),
            'common': self.load_resources_file(self.build_path(self.COMMON_FILE)),
        }

    @staticmethod
    def load_resources_file(path: str) -> Dict[str, Any]:
        with open(path) as f:
            resources: Dict[str, Any] = json.load(f)

        if 'dirs' not in resources \
                or 'files' not in resources\
                or isinstance(resources['dirs'], list)\
                or isinstance(resources['files'], dict):
            return resources

    def generate_path(self, path: str) -> str:
        return os.path.join(self.project_path, path)

    @staticmethod
    def generate_project_path(path: str) -> None:
        if os.path.exists(path):
            exit(f'A file or a directory already with this name - "{path}"')
        else:
            os.mkdir(path)

    def generate_dirs(self, dirs: List[str]) -> None:
        for d in dirs:
            path: str = self.generate_path(d).format(__app_name__celeryt__=self.name)
            os.mkdir(path)
            self.print(f'- {path}')

    def generate_files(self, files: Dict[str, str]) -> None:
        for file_name, content_template in files.items():
            path: str = self.generate_path(file_name).format(__app_name__celeryt__=self.name)

            context: Dict[str, str] = {"__app_name__celeryt__": self.name}
            template: Template = self.env.from_string(content_template)
            content: str = template.render(**context)

            with open(path, 'w') as f:
                f.write(content)
                self.print(f'- {path}')

    def __run_cmd(self, cmd: List[str]) -> bool:
        return subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=self.project_path
        ).returncode == 0

    def git_init(self) -> None:
        init_cmd: List[str] = ['git', 'init']
        add_cmd: List[str] = ['git', 'add', '-A']
        commit_cmd: List[str] = ['git', 'commit', '-m', '":tada: Initial commit"']

        init_return: bool = self.__run_cmd(init_cmd)
        add_return: bool = self.__run_cmd(add_cmd)
        commit_return: bool = self.__run_cmd(commit_cmd)
        print('Git init')
        # TODO: check bool return

    def git_flow_init(self):
        init_cmd: List[str] = ['git', 'flow', 'init', '-d']

        init_return: bool = self.__run_cmd(init_cmd)
        # TODO: check bool return
        print('Git flow init')

    def print(self, msg: Any):
        if self.verbose:
            print(msg)
