"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__='users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name=db.Column(db.Text, nullable=False)
    last_name=db.Column(db.Text, nullable=False)
    image_url=db.Column(db.Text, nullable=False, default='')

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    full_name = property(
        fget=get_full_name
    )

    def __repr__(self):
        return f"<User {self.full_name}.>"

class Post(db.Model):

    __tablename__="posts"

    now = datetime.now()

    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.Text, nullable=False, default=now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    users = db.relationship('User', backref='posts')

    def __repr__(self):
        return f"<Post {self.title}, Created At {self.created_at}, by {self.users.first_name}.>"
    
class Tag(db.Model):

    __tablename__='tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)

    posts = db.relationship('Post', secondary='post_tags', backref='tags')


class PostTag(db.Model):

    __tablename__='post_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False, primary_key=True)


    

