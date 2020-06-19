# app.py

from odoo_controller.data.controller import Controller
from odoo_controller.data.query import Query

def run():
    db = Controller()
    db.configure_server('', '', '')
    db.configure_user('', '')
    db.connect()

if __name__ == '__main__':
    run()