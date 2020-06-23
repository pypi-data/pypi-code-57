from adminlte_base.contrib import ponyorm
from flask_login import UserMixin
from pony.orm import Database, Required, Optional, Set, LongStr

db = Database()


MenuItem = ponyorm.create_entity_menu_item(db)


Menu = ponyorm.create_entity_menu(db)


class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.email = 'trash@kyzima-spb.com'

    def __str__(self):
        return 'Kirill Vercetti'

    def is_authenticated(self):
        return True
