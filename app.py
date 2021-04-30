"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User, Post


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
# db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)


@app.route('/')
def show_homepage():
    """redirects to /users """
    return redirect('/users')


@app.route('/users')
def show_users():
    """renders template that shows all users """
    users = User.query.all()

    return render_template('users.html',
                           users=users)


@app.route('/users/new')
def show_user_add_form():
    """renders new user form page """
    return render_template('new_user.html')


@app.route('/users/new', methods=['POST'])
def process_new_user():
    """handles the post request from new user form """
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['img-url']

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    flash('Successfully Created User')
    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_profile(user_id):
    """render profile page for user """
    user = User.query.get_or_404(user_id)
    posts = user.posts
    return render_template('user_detail.html', user=user, posts=posts)


@app.route('/users/<int:user_id>/edit')
def show_edit_user_page(user_id):
    """show edit page for the user """
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def process_user_edit(user_id):
    """handles form for editing user profile """
    user = User.query.get(user_id)

    user.first_name = request.form['first-name']
    user.last_name = request.form['last-name']
    user.image_url = request.form.get('img-url')

    db.session.commit()
    flash('Successfully Edited Profile')
    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """handle delete user post """
    user = User.query.get(user_id)

    # Post.query.filter_by(user_id=user_id).delete()

    for post in user.posts:
        db.session.delete(post)

    db.session.delete(user)
    db.session.commit()
    flash('Successfully Deleted Profile')
    return redirect('/users')


# ---------- routes for blog_posts start here --------------

@app.route('/users/<int:user_id>/posts/new')
def show_add_post_form(user_id):
    """ shows form to add a post for user """
    user = User.query.get(user_id)
    return render_template('new_post.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def process_new_post(user_id):
    """ processes form for adding new post and redirects to user page """
    title = request.form['title']
    content = request.form['content']
    
    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    flash('Successfully Added Post')
    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """shows post details and content """

    post = Post.query.get(post_id)
    user = post.user

    return render_template('post_detail.html', post=post, user=user)


@app.route('/posts/<int:post_id>/edit')
def show_edit_post_page(post_id):
    """renders template for form to edit a post """

    post = Post.query.get(post_id)
    user = post.user

    return render_template('edit_post.html', post=post, user=user)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def process_post_edit(post_id):
    """processes edit form post and redirects to post details """

    post = Post.query.get(post_id)

    post.title = request.form['title']
    post.content = request.form['content']

    db.session.commit()
    flash('Successfully Edited Post')
    return redirect(f"/posts/{post.id}")


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def process_post_delete(post_id):
    """processes delete post and redirects to user profile page """

    post = Post.query.get(post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()

    flash('Successfully Deleted Post')
    return redirect(f"/users/{user_id}")
