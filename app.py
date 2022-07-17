"""Blogly application."""

from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db,  connect_db, User, Post, Tag, PostTag
from sqlalchemy import func
from sqlalchemy import desc


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
    users = User.query.order_by('last_name').all()
    # print(users)
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
    posts = Post.query.filter_by(user_id=user.id)
    return render_template('details.html', user=user, posts=posts)

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
    user.image_url = image_url if image_url else ''

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

@app.route('/users/<user_id>/posts/new')
def add_post(user_id):
    """Form to add a post made by that user"""
    user = User.query.get(user_id)
    tags=Tag.query.all()
    return render_template('post_form.html', user=user, tags=tags)

@app.route('/users/<user_id>/posts/new', methods=['POST'])
def handle_add_post(user_id):
    """Route to process the add post form"""
    user = User.query.get(user_id)
    title = request.form['title']
    content = request.form['content']
    tags = request.form.getlist('tag')
    
    new_post = Post(title = title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    for tag in tags:
        db.session.add(PostTag(post_id=new_post.id, tag_id=tag))
        db.session.commit()

    return redirect (f'/users/{user.id}')

@app.route('/posts/<post_id>')
def show_users_posts(post_id):
    """Shows the post a user has made"""

    post = Post.query.get(post_id)
    return render_template('post_details.html', post=post)

@app.route('/posts/<post_id>/edit')
def edit_post(post_id):
    """Shows edit post form"""
    post = Post.query.get(post_id)
    tags = Tag.query.all()
    return render_template('edit_post_form.html', post=post, tags=tags)

@app.route('/posts/<post_id>/edit', methods=['POST'])
def handle_edit_post(post_id):
    """Edits the post"""
    post = Post.query.get(post_id)
    title = request.form['title']
    content=request.form['content']
    new_tags = request.form.getlist('tag')
    existing  = PostTag.query.filter_by(post_id=post.id).all()
    

    post.title = title
    post.content=content

    db.session.add(post)
    db.session.commit()

    for tag in new_tags:
        new_PostTag = PostTag(post_id=post.id, tag_id=tag)
        db.session.add(new_PostTag)
        db.session.commit()

    return redirect(f'/posts/{post.id}')

@app.route('/posts/<post_id>/delete')
def delete_post(post_id):
    """Deletes a user's post"""
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')

@app.route('/tags')
def list_tags():
    """Lists all tags available to use on a post"""
    tags = Tag.query.all()
    return render_template('list_tag.html', tags=tags)
    
@app.route('/tags/<tag_id>')
def tag_detail(tag_id):
    """gives details about a tag"""
    tag = Tag.query.get(tag_id)
    return render_template('show_tag.html', tag=tag)

@app.route('/tags/new')
def new_tag_form():
    """form for making a new tag"""
    return render_template('create_tag.html')

@app.route('/tags/new', methods=['POST'])
def handle_tag_form():
    """handles the tag form and creates a new tag"""

    name = request.form['name']
    new_tag = Tag(name=name)

    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")

@app.route('/tags/<tag_id>/edit')
def show_edit_form(tag_id):
    """shows the tag editing form"""
    tag=Tag.query.get(tag_id)
    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<tag_id>/edit', methods=['POST'])
def handle_edit_form(tag_id):
    tag = Tag.query.get(tag_id)
    name = request.form['name']

    tag.name=name
    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<tag_id>/delete')
def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')




