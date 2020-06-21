from pathlib import Path
import toml

class Config:
    '''Holds configuration for the etcetera'''
    def __init__(self, url:str, home=None, **conf):
        '''Creates new configuration from url and (optionally) other values

        Args:
            url (str): repository URL, for example "s3://my-datasets"
            home (str): directory to be used as local dataset cache. If not specified,
                ``~/.etc/`` is used. If directory does not exist, it will be created.
            conf (str): other parameters, specific to the cloud provider.
        '''
        self.url  = url
        self.home = home or Path.home() / '.etc'
        self.conf = conf

    @classmethod
    def load(cls, filename=None):
        '''Loads configuration from a TOML file'''
        if filename is None:
            filename = Path.home() / '.etc.toml'
        else:
            filename = Path(filename)

        if not filename.is_file():
            raise RuntimeError(f'Can not find configuration file {filename}')

        with open(filename) as f:
            conf = toml.loads(f.read())

        url = conf.pop('url', None)
        if url is None:
            raise RuntimeError(f'Profile {profile} in {filename} does not have "url" key')
        home = conf.pop('home', None)
        if home is None:
            home = Path.home() / '.etc'

        return Config(url, home, **conf)
