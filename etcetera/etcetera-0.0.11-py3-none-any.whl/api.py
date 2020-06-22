from typing import Optional
from .config import Config
from .engine import Engine
from .repo import Repo


def dataset(name:str, auto_pull=False, config=None):
    '''Returns :class:`etcetera.Dataset` object, given a dataset name.

    Args:
        name (str):               the name of the dataset
        auto_pull(bool):          if set, automatically pulls the dataset from the cloud
        config (etcetera.Config): configuration to use
    '''
    if config is None:
        config = Config.load()

    engine = Engine(config.home)
    if not engine.is_local_dataset(name):
        if not auto_pull:
            raise RuntimeError(f'Local dataset {name} not found. Please pull it.')

        pull(name, config=config)

    return engine.dataset(name)


def pull(name:str, force=False, config=None):
    '''Pull dataset from cloud storage.

    Args:
        name (str):               dataset name
        force (bool):             if True, overrides the existing local dataset
        config (etcetera.Config): configuration to use
    '''
    if config is None:
        config = Config.load()

    repo = Repo.load(config.url, **config.conf)

    engine = Engine(config.home)
    engine.pull(name, repo, force=force)


def push(name:str, force=False, config=None):
    '''Pushes dataset to the cloud.

    Args:
        name (str):      dataset name
        force (bool):    if true, overrides remote dataset
        config (etcetera.Config):  configuration to use
    '''
    if config is None:
        config = Config.load()

    repo = Repo.load(config.url, **config.conf)

    engine = Engine(config.home)
    engine.push(name, repo, force=force)


def register(dirname:str, name:Optional[str]=None, force=False, config=None):
    '''Register local directory as a dataset.

    Args:
        dirname (str):     path to the local directory with data
        name (str):        dataset name (if not specified, directory name is used)
        force (bool):      allows overriding existing dataset
        config (etcetera.Config): configuration to use
    '''
    if config is None:
        config = Config.load()

    engine = Engine(config.home)
    engine.register(dirname, name, force=force)


def purge(name:str, config=None):
    '''Deletes local dataset.

    Args:
        name (str): dataset name
        config (etcetera.Config): configuration to use
    '''
    if config is None:
        config = Config.load()

    engine = Engine(config.home)
    engine.purge(name)


def create(name:str, partitions=('train', 'test'), force=False, config=None):
    '''Create an empty local dataset.

    Args:
        name (str): dataset name
        partitions (List[str]): list of partitions to create
        force (bool): allow overriding the existing dataset
        config (etcetera.Config):  configuration to use
    '''
    if config is None:
        config = Config.load()
    engine = Engine(config.home)
    engine.create(name, partitions, force=force)


def ls(remote=False, config=None):
    '''Lists datasets.

    By the default, local datasets are listed.

    Args:
        remote (bool): if True, list remote datasets
        config (etcetera.Config): configuration to use
    '''
    if config is None:
        config = Config.load()

    if remote:
        repo = Repo.load(config.url, **config.conf)
        for x in repo.ls():
            if x.endswith('.tgz'):
                yield x[:-4]
    else:
        engine = Engine(config.home)
        yield from engine.ls()
