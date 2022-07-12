from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for the model for Users"""

    def setUp(self):
        """Add a sample user"""
        User.query.delete()

        user = User(first_name="TestUser", last_name="Last", image_url="https://images.unsplash.com/photo-1511367461989-f85a21fda167?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MXx8cHJvZmlsZXxlbnwwfHwwfHw%3D&w=1000&q=80")
        db.session.add(user)
        db.session.commit()

        self.user_id=user.id
        self.user=user

    def tearDown(self):
        """Clean up everything at the end"""

        db.session.rollback()

    def test_list_users(self):
        """Test redirect of homepage and if the users page lists all users"""

        with app.test_client() as client:
            res = client.get('/', follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('TestUser', html)

    def test_show_user_details(self):
        """Shows the users detail page"""
        with app.test_client() as client:
            res = client.get(f"/users/{self.user_id}")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>TestUser Last</h1>', html)
            self.assertIn(self.user.first_name, html)

    def test_add_user(self):
        """Tests adding a user to the list of users"""
        with app.test_client() as client:
            d = {"first_name": "TestUser2", "last_name": "LastName", "image_url": "none"}
            res = client.post('/users/new', data=d, follow_redirects=True)
            html=res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("TestUser2 LastName", html)
    
    def test_delete_user(self):
        """Tests deleting a user"""
        with app.test_client() as client:
            res = client.post(f'/users/{self.user_id}/delete', follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertNotIn("TestUser", html)