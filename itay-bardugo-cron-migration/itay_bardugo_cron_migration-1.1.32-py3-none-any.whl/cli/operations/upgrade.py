from cron_migration.cli.models.command import BaseCommand
from cron_migration.cli.manager import CommandsManager
from cron_migration.revisions.services.revision_apply import RevisionApply


@CommandsManager.bind("upgrade")
class Upgrade(BaseCommand):
    def __init__(self, service: RevisionApply):
        self._service = service

    def run(self):
        for revision in self._service.get_upgrades_list():
            log = BaseCommand._output.printed_task(
                BaseCommand._output.blue,
                f"upgrading file: {revision.path}, revision id: {revision.get_revision_id()}",
                BaseCommand._output.green,
                "Done",
                BaseCommand._output.red,
                "Failed!",
                success_indicator=None
            )(lambda: self._service.upgrade(revision))
            log()

        return 0
