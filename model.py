"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import datetime
import os

SAMPLE_PASSWORD = os.environ.get("SAMPLE_PASSWORD")
BUYER_EMAIL = os.environ.get("BUYER_EMAIL")
BUYER_EMAIL1 = os.environ.get("BUYER_EMAIL1")
FACILITATOR_EMAIL = os.environ.get("FACILITATOR_EMAIL")
FACILITATOR_EMAIL1 = os.environ.get("FACILITATOR_EMAIL1")
SAMPLE_PHONE = os.environ.get("SAMPLE_PHONE")



# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of Despair Change website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    fname = db.Column(db.String(15), nullable=False)
    lname = db.Column(db.String(30), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(5), nullable=True)
    state_code = db.Column(db.String(4),
                           db.ForeignKey('states.code'),
                                         nullable=True)

    default_amount = db.Column(db.Float,
                               nullable=False,
                               default=1.00)

    phone = db.Column(db.String(15), nullable=True)

    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.datetime.utcnow)

    last_login = db.Column(db.DateTime, nullable=False,
                           default=datetime.datetime.utcnow)

    #in case I want to reference state data through the User
    state = db.relationship("State", backref="users")

    def __repr__(self):
        """Provide helpful representation when printed."""
        repr_string = "<User user_id={id} fname={first} lname={last}>"

        return repr_string.format(id=self.user_id,
                                  first=self.fname,
                                  last=self.lname)



class Organization(db.Model):
    """Org receiving donations"""

    __tablename__ = "organizations"
    #the seed data has id on it already; will incriment fuck up
    org_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    payee_email = db.Column(db.String(100), nullable=False)
    logo_url = db.Column(db.String(200), nullable=True)
    mission_statement = db.Column(db.Text, nullable=True)
    website_url = db.Column(db.String(200), nullable=True)
    has_chapters = db.Column(db.Boolean, nullable=True)


    def __repr__(self):
        """Provide helpful representation when printed."""

        repr_string = "<Org name={name} org_id={id}>"
        return repr_string.format(name=self.name,
                                  id=self.org_id)


class Transaction(db.Model):
    """Transactions made by users"""

    __tablename__ = "transactions"

    transaction_id = db.Column(db.Integer,
                               autoincrement=True,
                               primary_key=True)
    #define user_id and org_id as foreign keys from the Primary keys of
    #Org and User - may turn into origin and destination
    org_id = db.Column(db.Integer,
                       db.ForeignKey('organizations.org_id'),
                       nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)

    #payment_id generated from paypal payment
    payment_id = db.Column(db.String(40), nullable=False)

    amount = db.Column(db.Float, nullable=False)

    timestamp = db.Column(db.DateTime,
                          nullable=False,
                          default=datetime.datetime.utcnow)

    #TODO figure out how to work this
    # status = db.Column(db.String(25), nullable=True)
    status = db.Column(db.Enum('pending_delivery',
                               'delivered_to_org',
                               name='statuses'),
                       nullable=False)

    ##DEFINING RELATIONSHIPS

    # Define relationship to user (self.user = User object)
    user = db.relationship("User",
                           backref=db.backref("transactions",
                                              order_by=timestamp))

    # Define relationship to Org (self.org = Org object)
    org = db.relationship("Organization",
                          backref=db.backref("transactions",
                                             order_by=timestamp))


    def __repr__(self):
        """Provide helpful representation when printed."""
        repr_string ="<Transaction id={trans_id} user_id={user} org_id={org}>"
        return repr_string.format(trans_id=self.transaction_id,
                                  user=self.user_id,
                                  org=self.org_id)

#calling it user_org instead of favorite to make it clear that this
#table defines the relationship between a user and the orgs to which
#they donate. It won't be used until phase 2, if I add more organizations as
#options to which users can donate. This table will allow them to choose
#their favorites.
class User_Org(db.Model):
    """Favorite orgs identified by a user."""

    __tablename__ = 'user_orgs'

    user_org_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    org_id = db.Column(db.Integer,
                        db.ForeignKey('organizations.org_id'),
                        nullable=False)

    rank = db.Column(db.Integer, nullable=True)

    org = db.relationship("Organization", backref="user_org")
    user = db.relationship("User", backref="user_org")


    def __repr__(self):
        """Provide helpful representation when printed."""
        repr_string ="<User_Org id={id} user_id={user} org_id={org}>"
        return repr_string.format(id=self.user_org_id,
                                  user=self.user_id,
                                  org=self.org_id)


class State(db.Model):
    """States/territories with state codes for use in registration"""

    __tablename__ = "states"

    code = db.Column(db.String(4), primary_key=True, nullable=False)
    name = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        repr_string ="<State name={name}>"
        return repr_string.format(name=self.name)

##Class for regional chapters if/when I decide to do that in stage 2
# class Chapters(db.Model):
#     """Information about local chapters of national organizations"""

#     # chapter_id = primary_key
#     # org_id = foreign keys
#     # chapter payee user_email
    # state
    # zip code
    # pass

##############################################################################
# Making Fake Data

def create_example_data():
    """generates objects for example data"""

    #Clear out DB before running this to make sure no duplicates
    User_Org.query.delete()
    Transaction.query.delete()
    User.query.delete()
    Organization.query.delete()

    print 'Deleted tables'

    users = example_users()
    pink = users[0]
    glen = users[1]

    org = example_orgs()

    transaction = example_transaction()

    user_org = example_user_org()

    #add users and org to DB
    db.session.add_all([pink, glen, org])
    db.session.commit()

    #add transaction after users/org has been created for referential integrity
    db.session.add_all([transaction, user_org])
    db.session.commit()

    print pink, glen, org, transaction, user_org


def example_users():
    """create fake user data"""

    pink = User(user_email="fuckingperfect@iampink.com",
                password=SAMPLE_PASSWORD,
                fname="Alicia",
                lname="Moore",
                age=27,
                zipcode="94611",
                state_code="CA",
                phone="3108008135")

    glen = User(user_email=BUYER_EMAIL,
                password=SAMPLE_PASSWORD,
                fname="Glen",
                lname="Coco",
                age=27,
                zipcode="94611",
                state_code="CA",
                phone=SAMPLE_PHONE)

    return [pink, glen]


def example_orgs():
    """Create org data"""

    org = Organization(name="Institute of Finishing Projects",
                       payee_email="FACILITATOR_EMAIL",
                       logo_url="https://media.makeameme.org/created/how-about-getting.jpg",
                       mission_statement="At the Institute of Finishing Projects, we finish projects.",
                       website_url="http://www.incredibox.com/",
                       has_chapters=False)

    return org

def example_transaction():
    """Create transaction by user 1 for org 1"""
    transaction = Transaction(org_id=1,
                          user_id=1,
                          payment_id='insert valid payment_id here',
                          amount=1.00,
                          status='pending_delivery')

    return transaction


def example_user_org():
    """create sample user_org"""

    user_org = User_Org(user_id=2,
                         org_id=1,
                         rank=1)

    return user_org

def set_val_table_id():
    """Set value for the incrementing table ids after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})

    #Get max org_id in database
    result = db.session.query(func.max(Organization.org_id)).one()
    max_id = int(result[0])

    # Set the value for the next org_id to be max_id + 1
    query = "SELECT setval('organizations_org_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})


    #Get max transaction_id in database
    result = db.session.query(func.max(Transaction.
                                       transaction_id)).one()
    max_id = int(result[0])

    # Set the value for the next org_id to be max_id + 1
    query = "SELECT setval('transactions.transaction_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})


    db.session.commit()



def connect_to_db(app, db_uri='postgresql:///despair_change'):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    db.create_all()
    create_example_data()

    #When you're ready to start auto-incrementing for real, uncomment this
    # set_val_table_id()

    print "Connected to DB."
