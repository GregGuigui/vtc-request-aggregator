import os

from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'dev.sqlite')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uber_access_token = db.Column(db.String(120), unique=True)
    uber_refresh_token = db.Column(db.String(120), unique=True)
    uber_client_id = db.Column(db.String(120), unique=True)

    def __init__(self, uber_access_token, uber_refresh_token, uber_client_id):
        self.uber_access_token = uber_access_token
        self.uber_access_token = uber_access_token
        self.uber_client_id = uber_client_id

    def __repr__(self):
        return '<User %r>' % self.uber_access_token