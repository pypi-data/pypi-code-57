from __future__ import print_function
import semver
from swimlane_platform.lib import Configuration, BaseWithLog, info_function_start_finish
from swimlane_platform.lib.mongo_manager import MongoManager


class DatabaseVersionSynch(BaseWithLog):

    def __init__(self, config, current_version):
        # type: (Configuration, semver.VersionInfo) -> DatabaseVersionSynch
        super(DatabaseVersionSynch, self).__init__(config)
        self.current_version = current_version
        self.mongo_manager = MongoManager(self.config)

    @info_function_start_finish('Synchronize versions db and assembly.')
    def run(self):
        # type: () -> None
        """
        If version of db stored in database is out of synch with assembly version.
        """
        settings = self.mongo_manager.get_swimlane_settings()
        database_version = settings.get('DatabaseVersion')
        self.logger.debug("Current database version ${version}".format(version=database_version))
        self.logger.debug("Current assembly version ${version}".format(version=self.current_version))
        db_version = semver.VersionInfo.parse(database_version)
        if db_version < self.current_version:
            settings['DatabaseVersion'] = str(self.current_version)
            self.mongo_manager.set_swimlane_settings(settings)
            self.logger.debug("Settings saved with ${version}".format(version=self.current_version))


def run(config, current_version):
    # type: (Configuration, semver.VersionInfo) -> None
    """
    The script run method, that can be called by other script or from file run method.
    :param current_version: The assembly version.
    :param config: Configuration information collected by parent script.
    """
    DatabaseVersionSynch(config, current_version).run()
