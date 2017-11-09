"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import datetime
import os

#TODO for when I want to encrypt passwords
from bcrypt import hashpw, gensalt

SAMPLE_PASSWORD = os.environ.get("SAMPLE_PASSWORD")
BUYER_EMAIL = os.environ.get("BUYER_EMAIL")
FACILITATOR_EMAIL = os.environ.get("FACILITATOR_EMAIL")
BUYER_EMAIL1 = os.environ.get("BUYER_EMAIL1")
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
    password = db.Column(db.String(150), nullable=False)
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
    #TODO Change name to paypal ID
    payment_id = db.Column(db.String(40), nullable=False)

    amount = db.Column(db.Float, nullable=False)

    timestamp = db.Column(db.DateTime,
                          nullable=False,
                          default=datetime.datetime.utcnow)

    status = db.Column(db.Enum("donation attempted",
                               "payment object built",
                               "paypal payment instantiated",
                               "Invalid request", #this one comes from paypal
                               "payment failed",
                               "payment succeeded",
                               "pending delivery to org",
                               "delivered to org",
                               name="statuses"),
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
                                  org=self.org_id,
                                  timestamp=self.timestamp)

#calling it user_org instead of favorite to make it clear that this
#table defines the relationship between a user and the orgs to which
#they donate. It won't be used until phase 2, if I add more organizations as
#options to which users can donate. This table will allow them to choose
#their favorites.
class UserOrg(db.Model):
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
        repr_string ="<UserOrg id={id} user_id={user} org_id={org}>"
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
    UserOrg.query.delete()
    Transaction.query.delete()
    User.query.delete()
    Organization.query.delete()

    print 'Deleted tables'

    users = example_users()
    pink = users[0]
    glen = users[1]
    chinandler = users[2]

    print "Added Users"
    org = example_orgs()

    #add users and org to DB
    db.session.add_all([pink, glen, chinandler, org])
    db.session.commit()

    # import pdb; pdb.set_trace()

    transaction = example_transaction()

    # import pdb; pdb.set_trace()

    user_org = example_user_org()


    #add transaction after users/org has been created for referential integrity
    db.session.add_all([transaction, user_org])
    db.session.commit()

    print pink, glen, chinandler, org, transaction, user_org


def example_users():
    """create fake user data"""

    pink = User(user_email="fuckingperfect@iampink.com",
                password=SAMPLE_PASSWORD,
                fname="Alicia",
                lname="Moore",
                age=38,
                zipcode="90210",
                state_code="CA",
                phone="3108008135")

    glen = User(user_email=BUYER_EMAIL,
                password=SAMPLE_PASSWORD,
                fname="Glen",
                lname="Coco",
                age=17,
                zipcode="94611",
                state_code="CA",
                phone=SAMPLE_PHONE)


    chinandler = User(user_email=BUYER_EMAIL1,
                      password=SAMPLE_PASSWORD,
                      fname="Chinandler",
                      lname="Bong",
                      age=40,
                      zipcode="10012",
                      state_code="NY",
                      phone=SAMPLE_PHONE)


    return [pink, glen, chinandler]


def example_orgs():
    """Create org data"""

    logo_url = "https://media.makeameme.org/created/how-about-getting.jpg"
    mission = "At the Institute of Finishing Projects, we finish proje"

    org = Organization(
                       name="Institute of Finishing Projects",
                       payee_email=FACILITATOR_EMAIL,
                       logo_url=logo_url,
                       mission_statement=mission,
                       website_url="http://www.incredibox.com/",
                       has_chapters=False
                       )

    return org


def example_transaction():
    """Create transaction by user 1 for org 1"""

    user = User.query.filter(User.user_email == BUYER_EMAIL).first()

    org = Organization.query.filter(Organization.payee_email == FACILITATOR_EMAIL)\
                            .first()

    transaction = Transaction(org_id=org.org_id,
                              user_id=user.user_id,
                              payment_id='insert valid payment_id here',
                              amount=1.00,
                              status='pending delivery to org')

    return transaction


def example_user_org():
    """create sample user_org"""

    user = User.query.filter(User.user_email == BUYER_EMAIL).first()

    org = Organization.query.filter(Organization.payee_email == FACILITATOR_EMAIL)\
                            .first()

    user_org = UserOrg(user_id=user.user_id,
                       org_id=org.org_id,
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

    # Set the value for the next transaction_id to be max_id + 1
    query = "SELECT setval('transactions.transaction_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})

    ##TODO do the same thing for UserOrgs

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
