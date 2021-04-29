"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

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
    users = User.get_all_users()
    # users = User.query.all()

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

    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_profile(user_id):
    """render profile page for user """
    user = User.query.get_or_404(user_id)
    return render_template('user_detail.html', user=user)


@app.route('/users/<int:user_id>/edit')
def show_edit_page(user_id):
    """show edit page for the user """
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def process_edit(user_id):
    """handles form for editing user profile """
    user = User.query.get(user_id)

    user.first_name = request.form['first-name']
    user.last_name = request.form['last-name']
    user.image_url = request.form['img-url']

    db.session.commit()
    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """handle delete user post """
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')
