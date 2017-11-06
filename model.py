"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy
import datetime


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
    state = db.Column(db.String(2), nullable=True)
    phone = db.Column(db.String(15), nullable=True)
    #QUESTION could this be a float, or should it be int
    default_amount = db.Column(db.Float,
                               nullable=False,
                               default=1.00)

    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.datetime.utcnow)

    last_login = db.Column(db.DateTime, nullable=False,
                           default=datetime.datetime.utcnow)

    def __repr__(self):
        """Provide helpful representation when printed."""
        repr_string = "<User user_id={id} fname={first}} lname={last}>"
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
        return repr_string.format(self.name, self.org_id)


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
        return repr_string.format(self.transaction_id,
                                  self.user.user_id,
                                  self.org.org_id)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
