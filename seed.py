import random
from faker import Faker


from model import (db, connect_to_db, State, User,
                   Organization, Transaction, Referral, UserOrg)


from server import app

fake = Faker()


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
                                                                 random.choice(range(1, 5)),
                                                                 fake.state_abbr(),
                                                                 fake.zipcode(),
                                                                 fake.phone_number(),
                                                                 fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None),
                                                                 ))



def add_users():
    """takes fake users and adds them to database"""

    with open("data/users.txt") as users_file:
        for row in users_file:
            row = row.rstrip()
            fname, lname, user_email, set_password, password, default_amount, state, zipcode, phone, created_at = row.split("|")

            user = User(fname=fname, 
                        lname=lname, 
                        user_email=user_email, 
                        set_password=set_password, 
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

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    # db.create_all()
    create_users()
    # # Import different types of data
    # load_states()

