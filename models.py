from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class NewsFilms(db.Model):
    __tablename__ = 'NewsFilms'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), unique=True, nullable=False)
    summary = db.Column(db.String(250), unique=True, nullable=False)
    description = db.Column(db.Text(), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    img_url = db.Column(db.Text(), unique=True, nullable=False)


class Users(UserMixin, db.Model):
    __tablename__ = 'Users_blog'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    role = db.Column(db.String(30), default="User")