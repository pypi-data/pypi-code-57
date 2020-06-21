from blc.api import Call
from blc.handlers.exceptions import NotFound, MultipleObjectsFound
from blc.handlers.exceptions import WrongParameters
from tinydb import TinyDB, Query


class ProjectManager():

    def __init__(self):
        self.db = TinyDB('data/projects.json')
        self.q = Query()

    def find(self, id=None, name=None):
        """Finds a record based on its id"""
        if id:
            q = self.db.search(self.q.id == id)
        if name:
            q = self.db.search(self.q.name == name)
        if not (name or id):
            raise WrongParameters
        if len(q) == 0:
            raise NotFound
        if len(q) > 1:
            raise MultipleObjectsFound
        return Project(q[0])

    def list(self):
        """Returns a list of projects available."""
        return [Project(pro) for pro in self.db.all()]

    def sync(self):
        """Syncs local db with the cloud."""
        pros = Call().do(extra='projects/').json()
        for pro in pros:
            if not self.db.search(self.q.name == pro['name']):
                self.db.insert(pro)

    def delete_all(self):
        """Drops the projects database. """
        self.db.truncate()


class Project():

    def __init__(self, initial_data):
        self.name = initial_data['name']
        self.color = initial_data['color'].replace("#", "")
        try:
            self.id = initial_data['id']
        except KeyError:
            self.id = None

    def save(self):
        """Saves project to the cloud and resyncs the local db."""
        Call().do(
            extra='projects/',
            pay={self.__dict__},
            method='POST'
        )
        ProjectManager().sync()
        return self
