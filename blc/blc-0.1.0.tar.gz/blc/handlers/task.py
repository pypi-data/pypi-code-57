from blc.api import Call
from blc.handlers.exceptions import NotFound, MultipleObjectsFound
from blc.handlers.exceptions import WrongParameters
from blc.handlers.category import CategoryManager
from blc.handlers.project import ProjectManager
from rich.table import Table
from tinydb import TinyDB, Query
import pendulum


class TaskManager():

    def __init__(self):
        self.db = TinyDB('data/tasks.json')
        self.q = Query()
        self.tasks = self.db.all()

    def find(self, id=None):
        """Finds a task based on its id."""
        if id:
            q = self.db.search(self.q.id == id)
        else:
            raise WrongParameters
        if len(q) == 0:
            raise NotFound
        if len(q) > 1:
            raise MultipleObjectsFound
        return Task(q[0])

    def list(self):
        """Returns a list of tasks available."""
        return [Task(task) for task in self.tasks]

    def today(self):
        """Returns the list of tasks done today."""
        tasks = []
        for task in self.list():
            if pendulum.parse(task.created_at).date() == pendulum.now().date():
                tasks.append(task)
        return tasks

    def week(self):
        """Returns the list of tasks done this week."""
        tasks = []
        for task in self.list():
            if (pendulum.parse(task.created_at).week_of_year == pendulum.now().week_of_year and
                    pendulum.parse(task.created_at).year == pendulum.now().year):
                tasks.append(task)
        return tasks

    def table(self, tasks=None):
        """Returns the tasks in a tabular view."""
        table = Table()
        table.add_column('emoji')
        table.add_column('task', style='green')
        table.add_column('done at', style='magenta')
        table.add_column('project', style='blue')
        for task in tasks:
            emoji = task.category.emoji
            pro = task.project.name
            dts = pendulum.parse(task.created_at).diff_for_humans()
            table.add_row(emoji, task.task, dts, pro)
        return table

    def sync(self):
        """Syncs local db with the cloud."""
        tasks = Call().do().json()
        for task in tasks:
            if not self.db.search(self.q.id == task['id']):
                self.db.insert(task)

    def delete_all(self):
        """Drops the tasks database. """
        self.db.truncate()


class Task():

    def __init__(self, initial_data):
        if "id" in initial_data:
            self.id = initial_data['id']
        self.task = initial_data['task']
        if 'created_at' in initial_data:
            self.created_at = initial_data['created_at']
        self.category_id = initial_data['category']
        self.project_id = initial_data['project']
        self.category = self._find_category()
        self.project = self._find_project()

    def _find_project(self):
        """Locates the project object."""
        try:
            pro = ProjectManager().find(id=self.project_id)
        except (NotFound, MultipleObjectsFound):
            pro = None
        return pro

    def _find_category(self):
        """Locates the category object."""
        try:
            cat = CategoryManager().find(id=self.category_id)
        except (NotFound, MultipleObjectsFound):
            cat = None
        return cat

    def save(self):
        """Saves task to the cloud and resyncs the local db."""
        Call().do(
            pay={'task': self.task, 'category': self.category_id, 'project': self.project_id},
            method='POST'
        )
        TaskManager().sync()
        return self
