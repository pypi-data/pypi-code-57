from flask import Flask
from ..database_util import init_db

def create_app(appname,blueprint,config):
    app = Flask(appname)
    app.register_blueprint(blueprint)
    app.config.from_object(config)
    init_db(app)
    return app