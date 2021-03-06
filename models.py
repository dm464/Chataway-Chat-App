"""
models.py
This module is what's used to create the databases for AuthUser and Messages
"""
from datetime import datetime
from enum import Enum
from app import db


class AuthUser(db.Model):
    """Template for AuthUser database"""
    id = db.Column(db.Integer, primary_key=True)
    auth_type = db.Column(db.String(120))
    name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    picture = db.Column(db.String(300))

    def __init__(self, auth_type, name, email, picture):
        assert type(auth_type) is AuthUserType
        self.auth_type = auth_type.value
        self.name = name
        self.email = email
        self.picture = picture

    def __repr__(self):
        return "<User name: {}\ntype: {}".format(self.name, self.auth_type)


class Message(db.Model):
    """Template for Message database"""
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50))
    message = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer, nullable=False, default=0)
    user_pic = db.Column(db.String(300))

    def __init__(self, user, message, timestamp, user_id, user_pic):
        self.user = user
        self.message = message
        self.timestamp = timestamp
        self.user_id = user_id
        self.user_pic = user_pic

    def __repr__(self):
        return "<Username: %s\tMessage: %s>" % (self.user, self.message)


class AuthUserType(Enum):
    """AuthUser Enum for referencing"""
    GOOGLE = "google"
    FACEBOOK = "facebook"
