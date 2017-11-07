from model import (db, connect_to_db, State, User,
                   Organization, Transaction, UserOrg)


from server import app


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

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # # Import different types of data
    load_states()

