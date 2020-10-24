from api.search_v2 import Api
import json
import sqlite3
from datetime import datetime
from django.db.models import Sum
from simulator.models import *
import decimal
import purchases


def buy(code, units, email):
    api = Api()
    errors = {}
    tgt = api.search(code)
    user = User.objects.get(email=email)
    stocks = Stock.objects.filter(code=code)
    if(stocks.count() != 1):
        Stock.objects.create(name=tgt["name"], code=code, price=0.00)
    st = Stock.objects.get(code=code)


    price = tgt['c']
    print(price)
    price = decimal.Decimal(float(price))


    money = price * units

    now = datetime.now().timestamp()
    balance = User.objects.get(email=email).balance
    if balance >= money:
        newBalance = balance - money
        User.objects.filter(email=email).update(balance=newBalance)
        Purchase.objects.create(
            user_id=user, stock=st, price=price, dateBought=now, orignialUnitBought=units, unitSold=0)
        Transaction.objects.create(
            user_id=user, stock = st, units = units, price = price, action = "buy")
    else:
        errors['insufficient_fund'] = "Insufficient fund for buying Stock {}".format(
            code)
    return errors


def sell(code, units, email):
    api = Api()
    errors = {}
    tgt = api.search(code)
    user = User.objects.get(email=email)
    stocks = Stock.objects.filter(code=code)
    if(stocks.count() != 1):
        Stock.objects.create(name=tgt["name"], code=code, price=0.00)
    st = Stock.objects.get(code=code)

    price = tgt['c']
    print(price)
    money = price * units

    current_units = purchases.get_total_owned_units(email,code)
    #currentUnit = Purchase.objects.get(user_id=email, code=code).all().aggregate(Sum(orignialUnitBought - UnitSold))
    balance = User.objects.get(email=email).balance
    remaining_sell_units = units
    if current_units >= units:
        ps = purchases.get_unsold_purhases(email,code)
        for p in ps:
            print('Units bought in this purchase' + str(p.orignialUnitBought))
            if(remaining_sell_units == 0):
                print('breaking')
                break
            unsold_purchased_units = p.orignialUnitBought - p.unitSold
            print('unsold_purchased_units: ' + str(unsold_purchased_units))
            if(unsold_purchased_units <= remaining_sell_units):
                print('first')
                remaining_sell_units = remaining_sell_units - unsold_purchased_units
                p.unitSold=p.orignialUnitBought
                p.save()
            else:
                print('second')
                p.unitSold=p.unitSold + remaining_sell_units
                p.save()
                remaining_sell_units = 0

        newBalance = balance + decimal.Decimal(float(money))
        User.objects.filter(email=email).update(balance=newBalance)
        Transaction.objects.create(
            user_id=user, stock = st, units = units, price = price, action = "sell")
    else:
        errors['insufficient_share'] = "Insufficient share for selling Stock {}".format(code)
        return errors



if __name__ == "__main__":
    buy("BINANCE:BTCUSDT", 1, 1)
