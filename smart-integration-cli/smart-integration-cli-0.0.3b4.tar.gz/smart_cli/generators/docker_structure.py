import os
import sys
from typing import Optional

from .filemanager import FileGenerator
from .utils import get_random_string
from .structure import Structure


class DockerAPPStructure(Structure):
    def generate_docker_compose_file(self):
        lib_path = self.get_lib_path()
        for filename in ('docker-compose.tpl', 'docker-compose-prod.tpl'):
            templates_path = lib_path + '/smart_cli/templates/docker_files'
            file_path = f'{templates_path}/{filename}'
            generator = FileGenerator(
                file_path,
                f'{filename.replace(".tpl", ".yml")}',
                {'project_name': self.project_name},
            )
            generator.write_file()
        self.generate_ignore_files()

    def generate_ignore_files(self):
        lib_path = self.get_lib_path()
        for filename in ('gitignore.tpl', 'dockerignore.tpl'):
            templates_path = lib_path + '/smart_cli/templates/docker_files'
            file_path = f'{templates_path}/{filename}'
            generator = FileGenerator(
                file_path,
                f'.{filename.replace(".tpl", "")}',
                {'project_name': self.project_name},
            )
            generator.write_file()

    def generate_docker_folder(self):
        os.mkdir('docker')
        os.chdir('docker')
        self._genereate_dev_docker_files()
        self._genereate_prod_docker_files()
        os.chdir('..')

    def _genereate_dev_docker_files(self):
        os.mkdir('local')
        os.chdir('local')
        os.mkdir('python')
        os.chdir('python')
        self.__gen_file_by_list(['Dockerfile_dev.tpl', 'entrypoint.sh.tpl'])
        os.chdir('..')
        os.chdir('..')

    def _genereate_prod_docker_files(self):
        os.mkdir('prod')
        os.chdir('prod')
        os.mkdir('python')
        os.chdir('python')
        self.__gen_file_by_list(['Dockerfile_prod.tpl', 'entrypoint.sh.tpl'])
        os.chdir('..')

        os.chdir('..')

    def __gen_file_by_list(self, list_of_file_names: list):
        lib_path = self.get_lib_path()
        templates_path = lib_path + '/smart_cli/templates/docker_files/docker'
        for filename in list_of_file_names:
            file_path = f'{templates_path}/{filename}'
            new_file_name = (
                filename.replace("_prod.tpl", "")
                .replace("_dev.tpl", "")
                .replace(".tpl", "")
                .replace("_nginx", "")
            )
            generator = FileGenerator(
                file_path, new_file_name, {'project_name': self.project_name}
            )
            generator.write_file()

    def install_dependencies(self):
        dependencies = [
            'requests>=2.18.1',
            'Django',
            'djangorestframework',
            'pytz>=2018.4',
            'boto',
            'boto3',
            'django-storages',
            'django-cors-headers',
            'celery==4.4.2',
        ]
        with open('.req.txt', 'a') as f:
            for d in dependencies:
                f.write(d + '\n')
        os.system('pip install -r .req.txt')
        os.remove('.req.txt')

    def generate_requirements_files(self):
        os.mkdir('requirements')
        os.chdir('requirements')

        dependencies = [
            'asgiref==3.2.7',
            'boto==2.49.0',
            'boto3==1.7.54',
            'botocore==1.10.84',
            'config-field',
            'Click==7.0',
            'django-cors-headers',
            'django-storages',
            'drf-dynamicfieldserializer',
            'Django==3.0.4',
            'pytz==2019.3',
            'sqlparse==0.3.1',
            'psycopg2-binary==2.8.4',
            'smart-integration-utils',
            'Jinja2',
            'celery==4.4.2',
            'requests',
            'validators',
        ]

        with open('requirements.txt', 'a') as f:
            for d in dependencies:
                f.write(d + '\n')

        local_dep = [
            '-r requirements.txt',
            'django-debug-toolbar',
        ]
        with open('local_requirements.txt', 'a') as f:
            for d in local_dep:
                f.write(d + '\n')

        local_dep = [
            '-r requirements.txt',
            'django-debug-toolbar',
        ]
        with open('local_requirements.txt', 'a') as f:
            for d in local_dep:
                f.write(d + '\n')

        prod_dep = [
            '-r requirements.txt',
            'gunicorn',
        ]
        with open('prod_requirements.txt', 'a') as f:
            for d in prod_dep:
                f.write(d + '\n')
        os.chdir('..')

    def generate_api_apps_files(self):
        return self._generate_app('api', 'core')

    def generate_settings_folder(self):
        os.mkdir('settings')
        os.chdir('settings')
        with open('__init__.py', 'w') as f:
            f.write('')
        lib_path = self.get_lib_path()
        templates_path = lib_path + '/smart_cli/templates/docker_files/settings'
        params = {'project_name': self.project_name, 'secret_key': get_random_string()}
        for name in os.listdir(templates_path):
            if name.endswith('.tpl'):
                self._gen_file(templates_path, name, params)
        os.chdir('..')

    def init_django_app(self):
        os.system(f'django-admin startproject {self.project_name}')

    def _rewrite_manage_py_file(self):
        lib_path = self.get_lib_path()
        templates_path = lib_path + '/smart_cli/templates/docker_files'
        params = {'project_name': self.project_name}
        self._gen_file(templates_path, 'manage.py.tpl', params)

    def install_dependencies(self):
        dependencies = ['django==2.2.7']
        with open('.req.txt', 'a') as f:
            for d in dependencies:
                f.write(d + '\n')
        os.system('pip install -r .req.txt')
        os.remove('.req.txt')

    def rewrite_basic_files(self, default: bool = True):
        super().rewrite_basic_files(False)
        self._rewrite_manage_py_file()
        os.chdir(self.project_name)
        self._rewrite_init_file_for_celery()
        os.system('rm settings.py')
        self.generate_settings_folder()
        os.chdir('..')

    def _rewrite_init_file_for_celery(self):
        lib_path = self.get_lib_path()
        template_path = lib_path + '/smart_cli/templates/docker_files/celery_init.tpl'
        params = {'project_name': self.project_name}
        generator = FileGenerator(template_path, '__init__.py', params)
        generator.write_file()
