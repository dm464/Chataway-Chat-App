# models.py
import flask_sqlalchemy
from app import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50))
    message = db.Column(db.String(350))
    
    def __init__(self, u, m):
        self.user = u
        self.message = m
        
    def __repr__(self):
        return '<Username: %s\tMessage: %s>' % (self.user, self.message)

