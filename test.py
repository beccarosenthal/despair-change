from unittest import TestCase
# from faker import faker
from flask import session

from model import (User, Organization, Transaction, State,
                   UserOrg, connect_to_db, db, create_example_data)
from server import app


class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn("Welcome to Despair Change", result.data)


    def test_about(self): ##NOTE: TEST WILL BREAK IF DOUCHEBAG JAR VID REMOVED
        """Test about page."""

        result = self.client.get("/about")
        self.assertIn("/www.youtube.com/embed/fWSKU3-52pk", result.data)

    #TODO Write Tests for:
        # /about

        # /login
        #     user exists
        #         correct password
        #         incorrect password
        #     user does not exist

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
