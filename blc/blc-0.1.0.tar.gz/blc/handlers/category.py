from blc.api import Call
from blc.handlers.exceptions import NotFound, MultipleObjectsFound
from blc.handlers.exceptions import WrongParameters
from tinydb import TinyDB, Query


class CategoryManager():

    def __init__(self):
        self.db = TinyDB('data/categories.json')
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
        return Category(q[0])

    def list(self):
        """Returns a list of all categories."""
        return [Category(cat) for cat in self.db.all()]

    def sync(self):
        """Fetches entries to the local db with the cloud."""
        cats = Call().do(extra='categories/').json()
        for cat in cats:
            if not self.db.search(self.q.name == cat['name']):
                self.db.insert(cat)

    def delete_all(self):
        """Drops the categories database."""
        self.db.truncate()


class Category():

    def __init__(self, initial_data):
        self.name = initial_data['name']
        self.emoji = initial_data['emoji']
        try:
            self.id = initial_data['id']
        except KeyError:
            self.id = None

    def save(self):
        """Creates a new category to the cloud and resyncs the db."""
        Call().do(
            extra='categories/',
            pay={self.__dict__},
            method='POST'
        )
        CategoryManager().sync()
        return self
