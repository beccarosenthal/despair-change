import random
from faker import Faker


from model import (db, connect_to_db, State, User,
                   Organization, Transaction, Referral, UserOrg)


from server import app

fake = Faker()
ORG_IDS = [8, 9, 13, 15, 16]


def load_states():
    """seed states into database"""

    #delete rows in state table, because we don't want duplicates
    State.query.delete()

    with open('seed_data/states.txt') as states_file:
        for row in states_file:
            state = row.rstrip()
            code, name = row.split("|")

            #get rid of quotation marks in the data
            code = code.replace("'", "")
            name = name.replace("'", "")

            state = State(code=code, name=name)

            #add state to session so it gets stored
            db.session.add(state)

    db.session.commit()

    print "States Loaded"


def create_users():
    """Creates users data from Faker."""

    print 'Users'

    with open('data/users.txt', 'w+') as users:
        for i in range(500):
            users.write('{}|{}|{}|{}|{}|{}|{}|{}|{}|{}\n'.format(fake.first_name(),
                                                                 fake.last_name(),
                                                                 fake.free_email(),
                                                                 fake.boolean(
                                                                     chance_of_getting_true=75),
                                                                 fake.password(length=10,
                                                                               special_chars=True,
                                                                               digits=True,
                                                                               upper_case=True,
                                                                               lower_case=True),
                                                                 random.choice(range(1, 6)),
                                                                 fake.state_abbr(),
                                                                 fake.zipcode(),
                                                                 fake.phone_number(),
                                                                 fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None),
                                                                 ))


##This is making everything error out right now because set password field isn't in 
# the DB yet
def add_users():
    """takes fake users and adds them to database"""

    with open("data/users.txt") as users_file:
        for row in users_file:
            row = row.rstrip()
            fname, lname, user_email, set_password, password, default_amount, state, zipcode, phone, created_at = row.split("|")

            user = User(fname=fname, 
                        lname=lname, 
                        user_email=user_email, 
                        # set_password=set_password, 
                        password=password, 
                        default_amount=default_amount,
                        state=state,
                        zipcode=zipcode,
                        phone=phone,
                        created_at=created_at)

            # We need to add to the session or it won't ever be stored
            db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()

    print "users added to database"

def create_transactions():
    """makes fake transactions between users with ids 1-500 and real fake orgs"""

    with open('data/transactions.txt', 'w+') as transactions:
        for i in range(1000):
            rand_num = random.randrange(0, 5)
            user_id = random.choice(range(1, 500))
            transactions.write("{}|{}|{}|{}|{}|\n".format(
                ORG_IDS[rand_num], #random org ID
                user_id, #random user
                User.query.get(user_id).default_amount,
                "Call this a payment ID",
                fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None),
                 )  )
                                


if __name__ == "__main__":
    # connect_to_db(app)

    # In case tables haven't been created, create them
    # db.create_all()
    create_users()
    # add_users() #right now this will error out VERY badly
    create_transactions()
    # # Import different types of data
    # load_states()

