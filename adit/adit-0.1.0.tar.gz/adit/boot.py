import logging
import logging.config
from adit.config import ConfigManager
from adit import constants as const


def _init_config(args):
    pass


def _init_logging(log_config):
    if log_config is None:
        logging.config.fileConfig(const.DEFAULT_LOG_CONFIG)
    else:
        try:
            logging.config.fileConfig(log_config)
        except:
            logging.config.fileConfig(const.DEFAULT_LOG_CONFIG)


def _init_dask_controller(mode, args):
    pass


def _init_dfs_controller(mode, args):
    pass


def _init_dashboard():
    pass


def boot(mode, args):
    _init_config(args= args)
    _init_dask_controller(mode=mode, args=args)
    _init_dfs_controller(mode=mode, args=args)
    _init_dashboard()
