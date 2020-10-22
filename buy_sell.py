from api.search_v2 import Api
import json
import sqlite3
import datetime
from django.db.models import Sum
from simulator.models import *

def buy(code, units, email):
    api = Api()
    errors = {}
    tgt = api.search(code)

    price = tgt['c']
    print(price)
    money = price * units

    now = datetime.now().timestamp()
    balance = User.objects.get(email=email).balance
    if balance >= money:
        newBalance = balance - money
        User.objects.filter(email=email).update(balance=newBalance)
        Purchase.objects.create(
            user_id=email, code=code, price=price, dateBuy=now, orignialUnitBought=units, unitSold=0)
        Transaction.objects.create(
            user_id = email, code = code, units = units, price = price, action = "buy")
    else:
        errors['insufficient_fund'] = "Insufficient fund for buying Stock {}".format(
            code)
    return errors


def sell(code, amount, email):
    api = Api()
    errors = {}
    tgt = api.search(code)

    price = tgt['c']
    print(price)
    money = price * amount
    '''
    conn = sqlite3.connect('hermes.db')
    conn.execute(
        "UPDATE USER set BALANCE = BALANCE + ? where ID = ?", (money, id))
    conn.commit()
    print("Total number of rows updated :", conn.total_changes)
    '''

    currentUnit = Purchase.objects.get(user_id=email, code=code).all().aggregate(Sum(orignialUnitBought - UnitSold))
    balance = User.objects.get(email=email).balance
    if currentUnit >= amount:
        newUnit = currentUnit - amount
        newBalance = balance + money
        User.objects.filter(email=email).update(balance=newBalance)
        # update unitsold from oldest 
        Purchase.objects.filter(email=email)
    else:
        errors['insufficient_share'] = "Insufficient share for selling Stock {}".format(code)
        return errors



if __name__ == "__main__":
    buy("BINANCE:BTCUSDT", 1, 1)
