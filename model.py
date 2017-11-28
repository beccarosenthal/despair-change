"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import datetime
import os

SAMPLE_PASSWORD = os.environ.get("SAMPLE_PASSWORD")
BUYER_EMAIL = os.environ.get("BUYER_EMAIL")
ORG_APP_EMAIL = os.environ.get("ORG_APP_EMAIL")
BUYER_EMAIL1 = os.environ.get("BUYER_EMAIL1")
RENT_A_SWAG = os.environ.get("RENT_A_SWAG")
SAMPLE_PHONE = os.environ.get("SAMPLE_PHONE")
ALT_NPS_EMAIL = os.environ.get("ALT_NPS")
READING_CENTER = os.environ.get("READING_CENTER")


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
    password = db.Column(db.String(150), nullable=True)
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


    ##########REFERRALS EXPLANATION######################
    #I am User1.  I referred User2 and User3. User3 referred User4.
    #User1.referrer is null, because no user referred me.
    #User2.referrer == User1
    #User1.referred == [User2, User3]
    #User2.referrer == User1
    #User2.referred == null
    #User3.referrer == User1
    #User3.referred == User4
    #User1's total donation impact amount includes User2, User3, AND User4
    referred = db.relationship("User",
                               secondary="referrals",
                               primaryjoin="User.user_id==Referral.referrer_id",
                               secondaryjoin="User.user_id==Referral.referred_id")
    referrer = db.relationship("User",
                               secondary="referrals",
                               primaryjoin="User.user_id==Referral.referred_id",
                               secondaryjoin="User.user_id==Referral.referrer_id",
                               uselist=False)  #don't wrap this in a list--there will only be one or zero


#     def user_orgs()

# #TODO uncomment line below and figure out how to query for list of user's fave orgs
# #in order
#     user_orgs = db.relationship("User",
#     #                             secondary="user_orgs",
#     #                             primaryjoin="User.user_id==UserOrg.user_id")
    def get_ranked_orgs(self):
        """get list of users ranked orgs; if not, return list of all orgs"""

        ranked_orgs = self.user_org
        orgs = [user_org.org for user_org in ranked_orgs]

        #TODO
        #there is a better way to get the remaining orgs than this. What is it? also, this is where that weird error message is coming from
        org_ids = [org.org_id for org in orgs]
        other_orgs = Organization.query.filter(~Organization.org_id.in_(org_ids)).all()
        ranked_orgs = orgs + other_orgs
        return ranked_orgs

    def referral_link(self):
        """Generate a referral link for user; if not, return False"""
        #for now, my domain is local host; if this changes, so too will this method
        domain = "localhost:5000"

        url_string = "/donated/referred?org_id={org}&referrer_id={user}"
        org_id = self.get_ranked_orgs()[0].org_id
        return domain + url_string.format(org=org_id, user=self.user_id)
        #TODO Make this work
    # def get_referred_chain(self):
    #     """returns list of referred users and all people who have been referred by those users
    #      from self

    #     #HYPOTHETICAL EXAMPLE:
    #     #User1 referred User2 and User3. User3 referred User4.

    #     >>>get_all_referred_by_user(User1)
    #     >>>[User2, User3, User4]
    #     """
    #     ##recursive function
    #     chain = []
    #     for user in self.referred:
    #         chain += [user] + self.get_referred_chain()
    #     return chain

    def __repr__(self):
        """Provide helpful representation when printed."""
        repr_string = "<User user_id={id} fname={first} lname={last} email={email}>"

        return repr_string.format(id=self.user_id,
                                  first=self.fname,
                                  last=self.lname,
                                  email=self.user_email)


class Organization(db.Model):
    """Org receiving donations"""

    __tablename__ = "organizations"
    #the seed data has id on it already; will increment fuck up
    org_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    payee_email = db.Column(db.String(100), nullable=False)
    logo_url = db.Column(db.String(200), nullable=True)
    mission_statement = db.Column(db.Text, nullable=True)
    website_url = db.Column(db.String(200), nullable=True)
    has_chapters = db.Column(db.Boolean, nullable=True)

    #todo write way to query with timestamp included
    def amount_raised(self, start_date=None, end_date=None):
        """calculate amount of money raised by particular org"""
        total = 0
        for transaction in self.transactions:
            total += transaction.amount

        return total

        #or

        # total = (db.session.query(
        #     db.func.sum(Transaction.amount)
        #            .filter(Transaction.org_id == self.org_id))
        #            .one()[0])
    def num_transactions(self):
        """get number of donations"""

        return len(self.transactions)

    def num_unique_donors(self):
      """get number of unique donors"""

      num_users = len(db.session.query(Transaction.user_id).filter(Transaction.org_id == self.org_id).all())
      return num_users

    def unique_donors(self):
        """get details of donations sorted by donors"""

        #gets tuple of (user_Id, $ donated to org, # donations by org)
        donations_by_user = (db.session.query(
            Transaction.user_id,
            db.func.sum(Transaction.amount),
            db.func.count(Transaction.transaction_id))
                                       .filter(Transaction.org_id == self.org_id)
                                       .group_by(Transaction.user_id)
                                       .all())

        return donations_by_user

    def average_donation(self):
        """get average donation amount"""

        average = self.amount_raised()/float(len(self.transactions))
        average = '${:,.2f}'.format(average)
        return average


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

    def get_transactions_by_org(org_id):

        pass


    # # #TODO add this to transactions already in db, figure out logic for how to change transaction if referred makes donation and then signs up
    # referrer_id = db.Column(db.Integer,
    #                         db.ForeignKey('users.user_id'),
    #                         nullable=True)

    # via_referral = db.Column(db.Boolean,
    #                          nullable=True,
    #                          default=False)
    #TODO figure out if I can make
    # referrer_email = db.Column(db.String,
    #                      db.ForeignKey('users.user_email'),
    #                      nullable=True)

    ##TODO: Change status of all pending delivery to org transactions to delivered to org

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

    # referrer = db.relationship("User",
    #                        backref=db.backref("referred_transactions",
    #                                           order_by=timestamp),
    #                        foreign_keys=[referrer_id])



    # Define relationship to user (self.user = User object)
    user = db.relationship("User",
                           backref=db.backref("transactions",
                                              order_by=timestamp),
                           foreign_keys=[user_id])



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

class Referral(db.Model):
    """Table connecting referred to referring users

      ######RELATIONSHIP BETWEEN REFERRER AND REFERRED#########
    #I am User1.  I referred User2 and User3. User3 referred User4.
    # User1.referrer is null, because no user referred me.
    #User2.referrer == User1
    # User1.referred == [User2, User3]
    # User2.referrer == User1.
    #User2.referred == null
    #User3.referrer == User1
    #User3.referred == User4
    #User1's total impact amount includes User2, User3, AND User4"""

    __tablename__ = "referrals"

    ref_id = db.Column(db.Integer,
                       primary_key=True,
                       autoincrement=True)
    referrer_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    referred_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)


    def __repr__(self):
        """Provide helpful representation when printed."""

        repr_string ="<Referral ref_id={id} referrer={referrer} referred={referred}>"
        return repr_string.format(id=self.ref_id,
                                  referrer=self.referrer_id,
                                  referred=self.referred_id)


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

    pink, glen, chinandler = example_users()

    print "Added Users"
    org1, org2, org3, org4, org5 = example_orgs()

    #add users and org to DB
    db.session.add_all([pink, glen, chinandler, org1, org2, org3, org4, org5])
    db.session.commit()

    # import pdb; pdb.set_trace()

    transaction = example_transaction()

    # import pdb; pdb.set_trace()

    user_org = example_user_org()

    referral1, referral2, referral3 = example_referral()


    #add transaction after users/org has been created for referential integrity
    db.session.add_all([transaction, user_org, referral1, referral2, referral3])
    db.session.commit()



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

    logo_url1 = "https://media.makeameme.org/created/how-about-getting.jpg"
    mission1 = "At the Institute of Finishing Projects, we finish proje"

    org = Organization(
                       name="Institute of Finishing Projects",
                       payee_email=ORG_APP_EMAIL,
                       logo_url=logo_url1,
                       mission_statement=mission1,
                       website_url="http://Iwastesomuchtime.com",
                       has_chapters=False
                       )

    logo_url2 = "https://ih1.redbubble.net/image.294685880.6679/flat,800x800,075,f.jpg"
    mission2 = "At Rent-A-Swag, we bring you the dopest shirts, the swankiest jackets, the slickest cardigans, the flashiest fedoras, the hottest ties, the snazziest canes and more!"
    org2 = Organization(
                       name="Rent-A-Swag",
                       payee_email=RENT_A_SWAG,
                       logo_url=logo_url2,
                       mission_statement=mission2,
                       website_url="http://www.pawneeindiana.com/",
                       has_chapters=False
                       )

    logo_url3 = "https://pbs.twimg.com/profile_images/887766984745775104/_YfeP9WT_400x400.jpg"
    mission3 = "45 messed with the wrong set of vested park rangers."

    org3 = Organization(
                       name="Alternative US National Parks Service",
                       payee_email=ALT_NPS_EMAIL,
                       logo_url=logo_url3,
                       mission_statement=mission3,
                       website_url="https://twitter.com/altnatparkser?lang=en",
                       has_chapters=False
                       )

    logo_url4 = "http://cdn.hexjam.com/editorial_service/bases/images/000/009/138/xlarge/zoolander-for-blog.jpg?1427992126"
    mission4 = "We teach you that there's more to life than being really, really good looking"
    org4 = Organization(
        name="The Derek Zoolander Center For Kids Who Can't Read Good And Wanna Learn To Do Other Stuff Good Too",
        payee_email=READING_CENTER,
        logo_url=logo_url4,
        mission_statement=mission4,
        website_url="https://dzssite.wordpress.com/",
        has_chapters=False
        )
    logo_url5="https://upload.wikimedia.org/wikipedia/en/thumb/f/f3/American_Civil_Liberties_Union_logo.svg/1280px-American_Civil_Liberties_Union_logo.svg.png"
    mission5="An organization that strives to achieve all of the goals of the ACLU with none of the resources."
    org5 = Organization(
                        name="Alt ACLU",
                        payee_email="altaclu@gmail.com",
                        logo_url=logo_url5,
                        mission_statement=mission5,
                        website_url="https://www.aclu.org/about-aclu",
                        has_chapters=True)


    return org, org2, org3, org4, org5


def example_transaction():
    """Create transaction by user 1 for org 1"""

    user = User.query.filter(User.user_email == BUYER_EMAIL).first()

    org = Organization.query.filter(Organization.payee_email == ORG_APP_EMAIL)\
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

    org = Organization.query.filter(Organization.payee_email == ORG_APP_EMAIL)\
                            .first()

    user_org = UserOrg(user_id=user.user_id,
                       org_id=org.org_id,
                       rank=1)

    return user_org

def example_referral():
    """create sample referrals"""

    referral1 = Referral(referrer_id=16, referred_id=17)
    referral2 = Referral(referrer_id=16, referred_id=22)
    referral3 = Referral(referrer_id=22, referred_id=15)

    return referral1, referral2, referral3


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
    from flask_bcrypt import Bcrypt
    connect_to_db(app)
    bcrypt = Bcrypt(app)
    # db.create_all()
    # create_example_data()

    #When you're ready to start auto-incrementing for real, uncomment this
    # set_val_table_id()

    print "Connected to DB."
