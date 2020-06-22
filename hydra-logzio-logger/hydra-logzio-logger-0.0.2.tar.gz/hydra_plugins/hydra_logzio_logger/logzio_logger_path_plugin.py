from hydra.plugins import SearchPathPlugin
from hydra._internal.config_search_path import ConfigSearchPath


class LogzioLoggerPathPlugin(SearchPathPlugin):
    def manipulate_search_path(self, search_path):
        assert isinstance(search_path, ConfigSearchPath)
        search_path.append("logzio-logger", "pkg://hydra_plugins.hydra_logzio_logger.conf")
