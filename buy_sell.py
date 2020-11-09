from api.search import Api
import json
import sqlite3
from datetime import datetime
from django.db.models import Sum
from simulator.models import *
import decimal
import purchases

# {id: , 'email: , sddd}
# {'profile': {}}

def buy(code, units, user):
    api = Api()
    errors = {}
    tgt = api.search(code)
    stocks = Stock.objects.filter(code=code)
    if(stocks.count() != 1):
        Stock.objects.create(name=tgt["name"], code=code)
    st = Stock.objects.get(code=code)


    price = tgt['c']
    print(price)
    price = decimal.Decimal(float(price))


    money = price * units

    now = datetime.now().timestamp()
    balance = user.profile.balance
    if balance >= money:
        newBalance = balance - money
        user.profile.balance = newBalance
        user.save()
        Purchase.objects.create(
            user_id=user, stock=st, price=price, dateBought=now, orignialUnitBought=units, unitSold=0)
        Transaction.objects.create(
            user_id=user, stock = st, units = units, price = price, action = "buy", date=now)
        errors['purchase_complete'] = "Successfully bought {} shares of Stock {} costing {}".format(units, 
            code, round(money, 2))
    else:
        errors['insufficient_fund'] = "Insufficient funds for buying Stock {}".format(
            code)
    return errors


def sell(code, units, user):
    api = Api()
    errors = {}
    tgt = api.search(code)
    stocks = Stock.objects.filter(code=code)
    if(stocks.count() != 1):
        Stock.objects.create(name=tgt["name"], code=code)
    st = Stock.objects.get(code=code)

    price = tgt['c']
    print(price)
    money = price * units

    current_units = purchases.get_total_owned_units(user,code)
    #currentUnit = Purchase.objects.get(user_id=email, code=code).all().aggregate(Sum(orignialUnitBought - UnitSold))
    balance = user.profile.balance
    remaining_sell_units = units
    if current_units >= units:
        ps = purchases.get_unsold_purhases(user,code)
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
        user.profile.balance=newBalance
        user.save()
        now = datetime.now().timestamp()
        Transaction.objects.create(
            user_id=user, stock = st, units = units, price = price, action = "sell", date=now)
    else:
        errors['insufficient_share'] = "Insufficient share for selling Stock {}".format(code)
        return errors



if __name__ == "__main__":
    buy("IC MARKETS:1", 1, 1)
