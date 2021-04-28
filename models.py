"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

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

    def __repr__(self):
        """Show info about pet."""

        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url}>"

    @classmethod
    def get_users(cls):
        cls.query.get(id)
    
    


