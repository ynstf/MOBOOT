from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
