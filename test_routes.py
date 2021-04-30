from unittest import TestCase

from app import app
from models import db, User, connect_db, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

connect_db(app)

db.drop_all()
db.create_all()

IMAGE_URL = 'https://previews.123rf.com/images/auremar/auremar1209/auremar120902515/15233744-cool-dude-in-sunglasses.jpg'


class RoutesTestCase(TestCase):
    """ tests for User class """ 

    def setUp(self):
        """Clean up any existing users."""
        Post.query.delete()
        User.query.delete()
        user = User(first_name='test_first', last_name='test_last', 
                    image_url=IMAGE_URL)
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id

       
        post = Post(title="test_title", content="test", user_id=self.user_id)
        db.session.add(post)
        db.session.commit()
        self.post_id=post.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_homepage_redirect(self):
        """successfully the redirect to /users """
        with app.test_client() as client:
            resp = client.get('/')
            self.assertEqual(resp.status_code, 302)
    
    def test_show_users(self):
        """successfully renders homepage """ 
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertIn('User Homepage', html)

    def test_new_user_creation(self):
        """ successfully redirects after new user creation """
        with app.test_client() as client:
            resp = client.post('/users/new', data={'first-name': 'test_name',
                                                   'last-name': 'test_last',
                                                   'img-url': IMAGE_URL})
            self.assertEqual(resp.status_code, 302)

    def test_show_profile(self):
        """successfully renders profile page """ 
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertIn('test_first', html)     

    def test_edit_user(self):
        """should successfully render edit user page """ 
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertIn('test_first', html)  

    def test_show_new_post_form(self):
        """should successfully render new post form """
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/posts/new")
            html = resp.get_data(as_text=True)

            self.assertIn('Add Post for test_first test_last', html)

    def test_show_post_details(self):
        """should succesfully render the post details """
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertIn('test_title', html)
            
    def test_process_post_edit(self):
        """should succesfully redirect to the post details"""
        with app.test_client() as client:
           
            resp = client.post(f"/posts/{self.post_id}/edit",
                               data={'title': 'new_title',
                                     'content': 'new_content'},
                               follow_redirects=True)
            
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('new_title', html)