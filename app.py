"""Blogly application."""

from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db,  connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  =  False
app.config['SQLALCHEMY_ECHO'] =  True
app.config['SECRET_KEY'] = "secretthings"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def home_page():
    """Redirects to the /users page"""
    return redirect('/users')
    

@app.route('/users')
def users_page():
    """Shows a list of all the users with links to their information page"""
    users = User.query.all()
    return render_template('homepage.html', users=users)

@app.route('/users/new')
def new_users():
    """Form to add new users"""
    return render_template('new_users.html')

@app.route('/users/new', methods=["POST"])
def process_new_users():
    """Route to process a new user, redirects to the /users page"""
    first_name = request.form['first_name']
    last_name=request.form['last_name']
    image_url=request.form['image_url']

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Shows details about a single user"""
    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Shows the edit page for a user"""
    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def process_edit_user(user_id):
    """Processes the edits submitted for the user"""
    first_name = request.form['first_name']
    last_name=request.form['last_name']
    image_url=request.form['image_url']

    user = User.query.get(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url if image_url else None

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Deletes a selected user"""
    
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')




