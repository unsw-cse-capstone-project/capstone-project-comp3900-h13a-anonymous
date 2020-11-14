from api.search import Api
from datetime import datetime
from simulator.models import *
import decimal
import modules.purchases as purchases

'''
Purchases a given number of units of a stock, provided the given user has 
suffiecent funds in their account balance.

parameters
    code : string
    units : int
    user : User model
returns
    messages : {string : string}
'''
def buy(code, units, user):
    code = code.upper()
    api = Api()
    messages = {}
    try:
        tgt = api.search(code)
    except Exception as e:
        messages['error'] = str(e)
        return messages
    stocks = Stock.objects.filter(code=code)
    if(stocks.count() != 1):
        Stock.objects.create(name=tgt["name"], code=code)
    st = Stock.objects.get(code=code)
    price = tgt['c']
    price = decimal.Decimal(float(price))
    money = price * units

    balance = user.profile.balance
    if balance >= money:
        newBalance = balance - money
        user.profile.balance = newBalance
        user.save()
        Purchase.objects.create(
            user_id=user, stock=st, price=price, orignialUnitBought=units, unitSold=0)
        Transaction.objects.create(
            user_id=user, stock = st, units = units, price = price, action = "buy")
        messages['success'] = "Successfully bought {} shares of Stock {} costing {}".format(units, 
            code, round(money, 2))
    else:
        messages['error'] = "Insufficient funds in balance for buying {} units of Stock {} for ${}".format(
            units, code, round(money,2))
    return messages

'''
Sells a given number of units of a stock, provided the given user has 
suffiecent units of the stock in their portfolio.

parameters
    code : string
    units : int
    user : User model
returns
    messages : {string : string}
'''
def sell(code, units, user):
    code = code.upper()
    api = Api()
    messages = {}
    try:
        tgt = api.search(code)
    except Exception as e:
        messages['error'] = str(e)
        return messages
    stocks = Stock.objects.filter(code=code)
    if(stocks.count() != 1):
        Stock.objects.create(name=tgt["name"], code=code)
    st = Stock.objects.get(code=code)

    price = tgt['c']
    money = price * units

    current_units = purchases.get_total_owned_units(user,code)
    balance = user.profile.balance
    remaining_sell_units = units
    if current_units >= units:
        ps = purchases.get_unsold_purhases(user,code)
        for p in ps:
            if(remaining_sell_units == 0):
                break
            unsold_purchased_units = p.orignialUnitBought - p.unitSold
            if(unsold_purchased_units <= remaining_sell_units):
                remaining_sell_units = remaining_sell_units - unsold_purchased_units
                p.unitSold=p.orignialUnitBought
                p.save()
            else:
                p.unitSold=p.unitSold + remaining_sell_units
                p.save()
                remaining_sell_units = 0

        newBalance = balance + decimal.Decimal(float(money))
        user.profile.balance=newBalance
        user.save()
        messages['success'] = "Successfully sold {} shares of Stock {} costing {}".format(units, 
            code, round(money, 2))
        Transaction.objects.create(
            user_id=user, stock = st, units = units, price = price, action = "sell")
    else:
        messages['error'] = "Insufficient number of shares in Stock {} to sell {} units".format(code, units)
    return messages



if __name__ == "__main__":
    buy("IC MARKETS:1", 1, 1)
