from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def init_db(app):
    db.init_app(app=app)
    migrate = Migrate(app, db)
    return migrate

class User(db.Model):
    token = db.Column(db.String(100), primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    token_generated_date = db.Column(db.DateTime, nullable=False)
    # User can comment out this line out to test the database migration result
    # added_col = db.Column(db.String(100), nullable=False)

