from flask import Flask
from ..database_util import init_db
from ..routes import init_api
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand






def create_app(appname,blueprint,config):
    app = Flask(appname)
    app.register_blueprint(blueprint)
    app.config.from_object(config)
    migrate = init_db(app)
    init_api(app)
    manager = Manager(app=app)
    manager.add_command('db', MigrateCommand)
    return app, migrate, manager