from . import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id                = db.Column(db.Integer, primary_key=True)
    name              = db.Column(db.String(100), nullable=False)
    email             = db.Column(db.String(150), unique=True, nullable=False)
    password_hash     = db.Column(db.String(255), nullable=False)
    created_at        = db.Column(db.DateTime, default=datetime.utcnow)

    todos = db.relationship("Todo", backref="owner", lazy=True)


class Category(db.Model):
    __tablename__ = "categories"

    id      = db.Column(db.Integer, primary_key=True)
    name    = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

  
    todos = db.relationship("Todo", backref="category", lazy=True)


class Todo(db.Model):
    __tablename__ = "todos"

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(200), nullable=False)
    done        = db.Column(db.Boolean, default=False)
    due_at      = db.Column(db.DateTime, nullable=True)
    reminded    = db.Column(db.Boolean, default=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    user_id     = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
