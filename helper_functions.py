"""HELPER FUNCTIONS"""

from flask import Flask, redirect, request, session, jsonify
from sqlalchemy import func

from model import (User, Organization, Transaction,
                   UserOrg, State, Referral,
                   connect_to_db, db)



def get_current_transaction(user_obj):
    """get most recent transaction in database so it can be updated throughout payment process"""

    current_transaction = (Transaction.query
                                      .filter(Transaction.user_id == user_obj.user_id)
                                      .order_by(Transaction.transaction_id)
                                      .all()[-1])

    return current_transaction

#function that deletes all records of dory for testing purposes
def make_dory_forget(dory):
    if dory.transactions:
        for item in dory.transactions:
            db.session.delete(item)
            db.session.commit()
    db.session.delete(dory)
    db.session.commit()    
    return User.query.filter(User.fname == "Dory").first()










