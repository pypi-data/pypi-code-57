from ..commander import QueueCommand
from ..commander import Commander
from ..ui.add_task_ui import AddTaskUi


class AddCommand(QueueCommand):

    command = 'add'

    @classmethod
    def register(self, parser):
        super().register(parser)
        parser.add_argument('item', nargs='?')
        parser.add_argument('--interactive', action='store_true')

    def execute_on_queue(self, parsed, queue):
        if parsed.interactive:  # pragma: no cover
            frame = AddTaskUi(lambda task: queue.add(task))
        else:
            if hasattr(parsed, 'item') and parsed.item:
                item = parsed.item
            else:
                item = input('Item: ')
            queue.add(item)


Commander.register(AddCommand)
