from cleo import Command
from tinydb import TinyDB, Query
from blc.handlers.category import CategoryManager, Category


class CategoryCommand(Command):
    """
    Categories actions

    categories
        {--s|sync : Syncronizes with the remote server}
        {--r|remove : Removes all entries from db}
        {--l|list : Lists all available categories}
        {--c|create : Creates a new category}
    """

    def __init__(self):
        Command.__init__(self)
        self.db = TinyDB('data/categories.json')
        self.q = Query()

    def _create(self):
        name = self.ask('Please insert category name', 'Task')
        emoji = self.ask(f'Please insert a emoji for {name}', '💩')
        self.line(f'You are about to create {name} with emoji {emoji}')
        if self.confirm('Are you sure?', True):
            c = Category({'name': name, 'emoji': emoji}).save()
            if c.__class__ is not Category:
                self.line(f'<error>{c}</error>')

    def _sync(self):
        CategoryManager().sync()

    def _list(self):
        for cat in CategoryManager().list():
            self.line(f"{cat.emoji} - {cat.name}")

    def _remove(self):
        CategoryManager().delete_all()

    def handle(self):
        if self.option('create'):
            self._create()
        if self.option('remove'):
            self._remove()
        if self.option('sync'):
            self._sync()
        if self.option('list'):
            self._list()
        self.line('<info>Done 👋</info>')
