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

def stacked_bar_data():

    group_param = cast(Transaction.timestamp, DATE) #
    transactions = (db.session.query(func.sum(Transaction.amount),
                                     group_param,
                                     Transaction.org_id,
                                     func.count(Transaction.transaction_id))
                              .group_by(group_param,
                                        Transaction.org_id)
                              .order_by(group_param,
                                        Transaction.org_id)
                              .all())

    # org_ids = [org.org_id for org in Organization.query.all()]
    orgs = Organization.query.all()

    #make list of dictionaries with dates;
    #FIXME it works, but there's an extra key that's a blank dict
    data_by_date = []
    dup_check = set()
    for item in transactions:
        date = {}
        if item[1] not in dup_check:
            date[item[1]] = {}
            data_by_date.append(date)
            dup_check.add(item[1])

    ###################################UP UNTIL THIS POINT, it builds list of
    #dictionaries with date: {} pairs

    for i in range(len(data_by_date)):
        for org in orgs:
            data_by_date[i][org.name]


    for date_dict in data_by_date:
        for org in orgs:
            data_by_date[key][org.name] = {"total_donated": None,
                                           "num_donations": None,
                                           "display_name": org.short_name}

    #populate the dictionary with info specific to each org
    for org in orgs:
        transactions = Transaction.get_transactions_by_org_date(org.org_id)

        for transaction in transactions:
            total_donated, num_donations, date  = transaction
            data_by_date[date][org.name]['total_donated'] = total_donated
            data_by_date[date][org.name]['num_donations'] = num_donations


#####BUILD THIS OUT
    data_by_date = []
    dup_check = set()
    for item in transactions:
        total_donated, date, org_id, num_donations = item
        data_by_date = {}
        if date not in dup_check:
            date[item[1]] = {}
            data_by_date.append(date)
            dup_check.add(item[1])














