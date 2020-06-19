import os
import json

from remo_app.config import REMO_HOME


class Config:
    default_port = "8123"
    local_server = 'http://localhost'
    default_viewer = 'electron'
    __slots__ = ['db_url', 'port', 'server', 'user_name', 'user_email', 'user_password', 'conda_env', 'viewer', 'debug']

    def __init__(self, **kwargs):
        for name in self.__slots__:
            setattr(self, name, kwargs.get(name, ''))
        self.validate()

    def validate(self):
        if not isinstance(self.debug, bool):
            self.debug = False

        if not self.server:
            self.server = self.local_server

        if not self.port:
            self.port = self.default_port

        if not self.viewer:
            self.viewer = self.default_viewer

        self.conda_env = os.getenv('CONDA_PREFIX', '')

    def update(self, **kwargs):
        for name, value in kwargs.items():
            if name in self.__slots__:
                setattr(self, name, value)
        self.validate()

    @staticmethod
    def from_dict(values: dict):
        config = Config()
        config.update(**values)
        return config

    def is_local_server(self):
        return self.server == self.local_server

    def get_host_address(self):
        skip_port = ((self.server.startswith('http://') and self.port == "80")
                     or (self.server.startswith('https://') and self.port == "443"))
        if skip_port:
            return self.server
        else:
            return '{}:{}'.format(self.server, self.port)

    def parse_db_params(self, url=None):
        if not url:
            url = self.db_url
        if not url:
            return

        params = {
            'engine': 'postgres',
            'database': '',
            'user': '',
            'password': '',
            'host': 'localhost',
            'port': '5432'
        }

        pos = url.find("://")
        if pos == -1:
            return
        params['engine'] = url[:pos]
        url = url[pos + len('://'):]
        pos = url.rfind('/')
        if pos == -1:
            return

        params['database'] = url[pos + 1:]
        url = url[:pos]
        pos = url.rfind('@')
        if pos != -1:
            user_pass = url[:pos]
            host_port = url[pos + 1:]
            pos = host_port.rfind(':')
            if pos == -1:
                params['host'] = host_port
            else:
                params['host'] = host_port[:pos]
                params['port'] = host_port[pos + 1:]

            pos = user_pass.find(':')
            if pos == -1:
                params['user'] = user_pass
            else:
                params['user'] = user_pass[:pos]
                params['password'] = user_pass[pos + 1:]
        return params


    @staticmethod
    def path():
        return str(os.path.join(REMO_HOME, 'remo.json'))

    @staticmethod
    def is_exists():
        return os.path.exists(Config.path())

    @staticmethod
    def load():
        return Config.load_from_path(Config.path())

    @staticmethod
    def load_from_path(config_path):
        if not os.path.exists(config_path):
            return None

        with open(config_path) as cfg_file:
            config = json.load(cfg_file)

        return Config.from_dict(config)

    def to_dict(self):
        return {
            name: getattr(self, name)
            for name in self.__slots__
        }

    def save(self):
        remo_dir = os.path.dirname(self.path())
        if not os.path.exists(remo_dir):
            os.makedirs(remo_dir)

        with open(self.path(), 'w') as cfg:
            json.dump(self.to_dict(), cfg, indent=2, sort_keys=True)
