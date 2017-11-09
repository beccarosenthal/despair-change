"""TESTS FOR DESPAIR CHANGE"""
import os
from unittest import TestCase
# from faker import faker
from flask import session

from model import (User, Organization, Transaction, State,
                   UserOrg, connect_to_db, db, create_example_data)
from seed import load_states
from server import app

SAMPLE_PASSWORD = os.environ.get("SAMPLE_PASSWORD")
BUYER_EMAIL = os.environ.get("BUYER_EMAIL")
FACILITATOR_EMAIL = os.environ.get("FACILITATOR_EMAIL")


class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index_route(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn("Welcome to Despair Change", result.data)


    def test_about_route(self): ##NOTE: TEST WILL BREAK IF DOUCHEBAG JAR VID REMOVED
        """Test about page."""

        result = self.client.get("/about")
        self.assertIn("/www.youtube.com/embed/fWSKU3-52pk", result.data)

    def test_login_route(self):
        """Test login page."""
        route = self.client.get('/login')
        self.assertIn('Email Address:', route.data)

    def test_register_route(self):
        """Test register page."""
        route = self.client.get('/register')
        self.assertIn('Age:', route.data)


class DespairChangeTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        load_states()

        create_example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def login(self):
        """Helper function to allow self.client to see site as logged in"""
        return self.client.post("/login",
                                data={"email": BUYER_EMAIL,
                                      "password": SAMPLE_PASSWORD},
                                follow_redirects=True)

    def test_login_correct_password(self): #NOTE: if you get rid of "DONATION" on /donate, test will fail
        """Test login page."""

        result = self.login()
        self.assertIn("donation", result.data.lower())
        self.assertNotIn("That is an incorrect password", result.data)


    def test_login_incorrect_password(self):
        """Test unsuccessful login page."""

        result = self.client.post("/login",
                                  data={"email": BUYER_EMAIL,
                                        "password": "Pa$$word124"},
                                  follow_redirects=True)

        self.assertNotIn("donation", result.data.lower())
        self.assertIn("That is an incorrect password", result.data)

    def test_login_no_account(self):
        """Test login attempt for nonexistent account."""

        result = self.client.post("/login",
                                  data={"email": "privacy4lyfe@EdSnowden.com",
                                        "password": "Password1!"},
                                  follow_redirects=True)

        self.assertNotIn("donation", result.data.lower())
        self.assertIn("You need to register first!", result.data)

    def test_register(self):
        """Test register new User"""

        result = self.client.post('/register',
                                  data={"email": "NothingButKnope@pawnee.gov",
                                        "password": "Eagleton$UX",
                                        'fname': "Leslie",
                                        "lname": "Knope",
                                        "age": 37,
                                        "zipcode": "46001",
                                        "state": "IN",
        #FOR THE RECORD: the phone number listed here is the actual phone number
        #for the department of Parks and Rec at the most obese city in Indiana
                                        "phone": "8124356141"},
                                        follow_redirects=True)
        self.assertIn("donation", result.data.lower())
        self.assertNotIn('login', result.data)






    #TODO

    # /register
        #     user input added correct
        #     user input added incorrectly
                #bad phone, zip, email, etc
        #     user email already in there
        #         *****TODO fix server.py logic so that user registering with
        #         wrong password redirects them to login page


####################################################################################
class DespairChangeLoggedIn(TestCase):
    """Despair Change tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['current_user'] = 1

    # #goal is to make sure what pages you can and cannot see
    # def test_donate_while_logged_in(self):
    #     """Test donate page."""
    #     route = self.client.get('/donate')
    #     self.assertIn('DONATION', route.data)

    # def test_important_page(self):
    #     """Test important page."""

    #     result = self.client.get("/important")
    #     self.assertIn("You are a valued user", result.data)



    ##Right now buttons fails because it's not connected to db
    # def test_buttons(self): ##NOTE: This page will likely not be in final project
    #     """Test buttons page."""

    #     ##NOTE: Test will break if monkey gif removed
    #     result = self.client.get("/buttons")
    #     self.assertIn("giphy.com/embed/5Zesu5VPNGJlm", result.data)

    #TODO Write Tests for:
        # / - basically a question of what they can see on the nav bar
            # if logged in
            # if not logged in

        # /register
        #     user input added correct
        #     user input added incorrectly
        #     user email already in there
        #         *****TODO fix server.py logic so that user registering with
        #         wrong password redirects them to login page
        #     user
        # /dashboard
        #     logged in
        #     logged out
        # register






# ###COME BACK TO THIS IF IT BECOMES NECESSARY TO MAKE FAKE USERS

# class TestUser(unittest.TestCase):
#     def setUp(self):
#         self.fake = Faker()
#         self.user = User(
#             fname=self.fake.first_name(),
#             lname=self.fake.last_name(),
#             user_email=self.fake.ascii_email(),
#             state=self.fake.state_abbr(),
#             zipcode=self.fake.zipcode()
#         )

#     def test_user_creation(self):
#         self.assertIsInstance(self.user, User)

#     def test_user_name(self):
#         expected_username = self.user.first_name + " " + self.user.last_name
#         self.assertEqual(expected_username, self.user.user_name)


# class TestOrganization(unittest.TestCase):
#     def setUp(self):
#         self.fake = Faker()
#         self.organization = Organization(
#             name=self.fake.company(),
#             payee_email=self.fake.company_email(),
#             logo_url=self.fake.image_url(),
#             mission_statement=self.fake.catch_phrase(),
#             website_url=self.fake.url(),
#             has_chapters=self.fake.boolean()
#             )

#     def test_organization_creation(self):
#         self.assertIsInstance(self.organization, Organzation)


if __name__ == "__main__":
    import unittest

    unittest.main()
