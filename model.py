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
    default_amount = db.Column(db.Integer,
                               nullable=False,
                               default=1)

    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.datetime.utcnow)
    #do I want this?
    last_log_in = db.Column(db.Datetime, nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s fname=%s lname=%s>" % (self.user_id,
                                           self.fname, self.lname)


###COPIED AND PASTED FROM RATINGS
class Org(db.Model): #Should I call it org or Organization? It's a long word to type?
    """Org receiving donations"""

    __tablename__ = "orgs"
    #the seed data has id on it already; will incriment fuck up
    org_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    logo_url = db.Column(db.String(200), nullable=True)
    mission_statement = db.Column(db.String(500), nullable=True)
    website_url = db.Column(db.String(200), nullable=True)
    payee_email = db.Column(db.String(50), nullable=False)
    has_chapters = db.Column(db.Boolean, nullable=False)

    released_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Org name=%s>" % (self.name)


class Transaction(db.Model):
    """Transactions made by users"""

    __tablename__ = "transactions"

    transaction_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
   #define user_id and org_id as foreign keys from the Primary keys of
   #Org and User
    org_id = db.Column(db.Integer,
                         db.ForeignKey('orgs.org_id'))
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'))

    # Define relationship to user (self.user = User object)
    user = db.relationship("User",
                           backref=db.backref("transactions",
                                              order_by=transaction_id))

    # Define relationship to Org (self.org = Org object)
    org = db.relationship("Org",
                            backref=db.backref("transactions",

                                               order_by=transaction_id))
    amount = db.Column(db.Integer, nullable=False) ##Do I want this to be a float?

    time = db.Column(db.DateTime, nullable=True)

    # status  = #figure out how to work this



    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Transaction user=%s  org=%org>" % (self.user, self.org)


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
