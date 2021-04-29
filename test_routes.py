from unittest import TestCase

from app import app
from models import db, User, connect_db

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

connect_db(app)

db.drop_all()
db.create_all()


class RoutesTestCase(TestCase):
    """ tests for User class """ 

    def setUp(self):
        """Clean up any existing users."""
        User.query.delete()
        user = User(first_name='test_first', last_name='test_last', 
                    image_url='https://previews.123rf.com/images/auremar/auremar1209/auremar120902515/15233744-cool-dude-in-sunglasses.jpg')
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id

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

    
    