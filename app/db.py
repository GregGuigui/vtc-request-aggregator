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
    lyft_access_token = db.Column(db.String(120), unique=True)
    lyft_refresh_token = db.Column(db.String(120), unique=True)
    lyft_client_id = db.Column(db.String(120), unique=True)

    def __init__(self):
        return

    def __repr__(self):
        return '<User %r>' % self.uber_access_token
        
    @staticmethod
    def create_or_update(vtc_name, oauth2credentials):
        existing_user = User.query.filter_by(uber_client_id=oauth2credentials.client_id).first()
        if(existing_user is None):
            existing_user = User()
            db.session.add(existing_user)
            
        setattr(existing_user, vtc_name + '_access_token', oauth2credentials.access_token)
        setattr(existing_user, vtc_name + '_refresh_token', oauth2credentials.refresh_token)
        setattr(existing_user, vtc_name + '_expires_in_seconds', oauth2credentials.expires_in_seconds)
        setattr(existing_user, vtc_name + '_grant_type', oauth2credentials.grant_type)
        
        db.session.commit()
        
        return existing_user