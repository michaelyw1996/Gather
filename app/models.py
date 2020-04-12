from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    myPosts = db.relationship('ActivityPost', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class ActivityPost(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    activityType = db.Column(db.String(200))
    name = db.Column(db.String(50))
    activityTitle = db.Column(db.String(100))
    activityDescription = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Forum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    author = db.Column(db.String(250), nullable=False)
