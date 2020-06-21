from cleo import Command
from tinydb import TinyDB, Query
from blc.handlers.project import Project, ProjectManager
from rich.console import Console


class ProjectCommand(Command):
    """
    Projects actions

    blc:projects
        {--s|sync : Syncronizes with the remote server}
        {--r|remove : Removes all entries from db}
        {--l|list : Lists all available projects}
        {--c|create : Creates a new project}
    """

    def __init__(self):
        Command.__init__(self)
        self.db = TinyDB('data/projects.json')
        self.q = Query()
        self.console = Console()

    def _create(self):
        name = self.ask('Please insert project name', 'Task')
        color = self.ask(f'Please insert a color for {name}', 'f4f4f4')
        self.line(f'You are about to create {name} with color {color}')
        if self.confirm('Are you sure?', True):
            c = Project({'name': name, 'color': color}).save()
            if c.__class__ is not Project:
                self.line(f'<error>{c}</error>')

    def _sync(self):
        ProjectManager().sync()

    def _list(self):
        for pro in ProjectManager().list():
            self.console.print(f"{pro.name}", style=f"#{pro.color}")

    def _remove(self):
        ProjectManager().delete_all()

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
