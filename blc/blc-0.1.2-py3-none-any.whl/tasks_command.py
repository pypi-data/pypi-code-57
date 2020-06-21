from cleo import Command
from blc.handlers.task import TaskManager, Task
from blc.handlers.category import CategoryManager
from blc.handlers.project import ProjectManager
from rich.console import Console


class TasksCommand(Command):
    """
    Tasks actions

    blc:tasks
        {--s|sync : Syncronizes with the remote server}
        {--r|remove : Removes all entries from db}
        {--l|list : Lists all available projects}
        {--c|create : Creates a new project}
        {--t|today :  List the tasks that have been done today}
        {--w|week :  List the tasks that have been done this week}
    """

    def __init__(self):
        Command.__init__(self)
        self.console = Console()
        self.tasks = TaskManager()
        self.categories = CategoryManager()
        self.projects = ProjectManager()

    def _create(self):
        task = self.ask('Please insert project name', 'Today I did something awesome!')
        cat = self.choice('Please select a category, defaults to task',
                          [c.name for c in self.categories.list()], 1)
        cat = self.categories.find(name=cat)
        pro = self.choice('Please select a project, defaults to certh',
                          [p.name for p in self.projects.list()], 1)
        pro = self.projects.find(name=pro)
        if self.confirm(f'You are about to create {cat.emoji} - {task} for #{pro.name}\nAre you sure?', True):
            return Task({'task': task, 'category': cat.id, 'project': pro.id}).save()

    def handle(self):
        if self.option('today'):
            self.console.print(self.tasks.table(tasks=self.tasks.today()))
        if self.option('week'):
            self.console.print(self.tasks.table(tasks=self.tasks.week()))
        if self.option('create'):
            self._create()
        if self.option('remove'):
            self.tasks.delete_all()
        if self.option('sync'):
            self.tasks.sync()
        if self.option('list'):
            self.console.print(self.tasks.table(tasks=self.tasks.list()))
        self.line('<info>Done 👋</info>')
