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


