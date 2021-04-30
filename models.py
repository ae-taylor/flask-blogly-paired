"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User model"""
    __tablename__ = "users"


    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(25),
                           nullable=False)
    last_name = db.Column(db.String(25),
                           nullable=False)
    image_url = db.Column(db.Text,
                          nullable=True)  
    posts = db.relationship('Post', backref="user")

    def __repr__(self):
        """Show info about pet."""

        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url}>"


class Post(db.Model):
    """ Post model """
    __tablename__ = "posts"


    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(100),
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    created_at = db.Column(db.DateTime,
                           nullable=False, 
                           default=datetime.utcnow)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)

    def __repr__(self):
        """Show info about blog post."""

        b = self
        return f"<Blog {b.id} {b.title} {b.created_at} {b.user_id}>"


    



