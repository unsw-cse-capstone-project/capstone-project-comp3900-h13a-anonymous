from simulator.models import *
from django.db.models import F 
import pandas as pd

'''
Get's a list of dictionaries containing information about a given user's
entire transaction history. The list is ordered from most recent transaction
to least

parameters
    user : User model
    transactions_list : [ {string : any} ]
'''
def get_user_transactions(user_id):
    transactions = Transaction.objects.filter(user_id=user_id).order_by(F('date').desc())
    transactions_list = []
    for t in transactions:
        transactions_entry = {
            "code":t.stock.code,
            "action":t.action,
            "price":t.price,
            "units":t.units,
            "price":round(t.price,2),
            "datetime": t.date,
            "change": t.price * t.units
        }
        transactions_list.append(transactions_entry)

    return transactions_list