import datetime
import random
# from faker import Faker

from model import (db, connect_to_db, State, User,
                   Organization, Transaction, Referral, UserOrg)

from server import app

ORG_IDS = [1, 2, 3, 4, 5]
USER_IDS = [27, 15, 17, 22, 23, 16, 30, 20, 31, 32, 33]


def load_states():
    """seed states into database"""

    #delete rows in state table, because we don't want duplicates
    State.query.delete()

    with open('data/states.txt') as states_file:
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



##This is making everything error out right now because set password field isn't in
# the DB yet
def add_users():
    """takes fake users and adds them to database"""

    with open("data/users.csv") as users_file:
        for row in users_file:
            row = row.rstrip()
            fname, lname, user_email, password, default_amount, state, zipcode, phone, created_at, set_password  = row.split(",")
            created_at = datetime.datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
            user = User(fname=fname,
                        lname=lname,
                        user_email=user_email,
                        set_password=set_password,
                        password=password,
                        default_amount=float(default_amount),
                        state_code=state,
                        zipcode=str(zipcode),
                        phone=phone,
                        created_at=created_at
                        )

            # We need to add to the session or it won't ever be stored
            db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()

    print "users added to database"

def create_transactions():
    """makes fake transactions between users with ids 1-500 and real fake orgs"""

    with open('data/transactions.txt', 'w+') as transactions:
        for i in range(5000):
            rand_num = random.randrange(0, 5)
            #Make sure user_id chosen actually exists
            user_id = random.choice(range(1, 1000))
            while User.query.get(user_id) is None:
                user_id = random.choice(range(1, 1000))

            transactions.write("{}|{}|{}|{}|{}\n".format(
                ORG_IDS[rand_num], #random org ID
                user_id, #random user
                User.query.get(user_id).default_amount,
                "Call this a payment ID",
                fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None),
                 )  )

def add_transactions():
    """add fake transactions to db"""

    with open('data/transactions.txt') as transactions:
        for row in transactions:
            row = row.rstrip()
            org_id, user_id, amount, payment_id, timestamp = row.split('|')
            timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            transaction = Transaction(
                user_id=user_id,
                org_id=org_id,
                amount=float(amount),
                timestamp=timestamp,
                status='pending delivery to org',
                payment_id=payment_id)

            db.session.add(transaction)

        db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()
    load_states()
    # create_users()
    add_users()
    create_transactions()
    add_transactions()
    # # Import different types of data

