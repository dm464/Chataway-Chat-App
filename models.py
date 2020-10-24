# models.py
import flask_sqlalchemy
from app import db
from enum import Enum
from datetime import datetime


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50))
    message = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __init__(self, user, message):
        self.user = user
        self.message = message
        
    def __repr__(self):
        return '<Username: %s\tMessage: %s>' % (self.user, self.message)

class AuthUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auth_type = db.Column(db.String(120))
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    picture = db.Column(db.String(300))
    
    
    def __init__(self, auth_type, name, email, picture):
        assert type(auth_type) is AuthUserType
        self.auth_type = auth_type.value
        self.name = name
        self.email = email
        self.picture = picture
        
    def __repr__(self):
        return "<User name: {}\ntype: {}".format(self.name, self.auth_type)

class AuthUserType(Enum):
    GOOGLE = "google"
    FACEBOOK = "facebook"