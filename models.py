from datetime import datetime
from annotation import db


class Tweet(db.Model):
    __tablename__ = "tweets"
    id = db.Column('id', db.Integer, primary_key=True)
    id_str = db.Column('id_str',db.Unicode)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    text = db.Column('text', db.Unicode)
    created_at = db.Column('created_at', db.Date, default=datetime.utcnow)
    verified = db.Column('verified', db.Boolean, default=False)
    category = db.Column('category',db.Unicode)

    users = db.relationship('User', foreign_keys=user_id, backref="tweets")


class User(db.Model):
    __tablename__ = "users"
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Unicode)
    screen_name = db.Column('screen_name',db.Unicode)
    created_at = db.Column('created_at',db.Date,default=datetime.utcnow)
    location = db.Column('location',db.Unicode)


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Unicode)

