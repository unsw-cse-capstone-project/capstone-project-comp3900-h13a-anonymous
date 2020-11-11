from simulator.models import *
from api.search import Api
from django.db.models import F

'''
Returns a list of dictionaries containing leaderboard information for
all users of the application. The list is sorted from user with highest
worth to user with lowest worth.

returns
    sorted_leaderboard : [ {string : any} ]
    messages : {string : string}
'''
def get_leaderboard_info():
    profiles = Profile.objects.all()
    cprice_cache = {}
    leaderboard = []
    messages = {}
    for p in profiles:
        if p.user.is_superuser:
            continue
        user_entry = {}
        user_entry['name'] = p.user.username
        user_entry['balance'] = float(p.balance)
        try:
            user_entry['portfolio_worth'], cprice_cache = get_user_profit(p.user, cprice_cache)
        except Exception as e:
            messages['error'] = str(e)
            return [], messages
        user_entry['portfolio_worth'], cprice_cache = get_user_profit(p.user, cprice_cache)
        user_entry['total_worth'] = round(user_entry['balance'] + user_entry['portfolio_worth'],2)
        leaderboard.append(user_entry)

    sorted_leaderboard = sorted(leaderboard, key = lambda l: l['total_worth'], reverse=True)
    i = 1
    for l in sorted_leaderboard:
        l['rank'] = i
        i = i + 1

    return sorted_leaderboard, messages

    
'''
Gets the total worth of all stock units in a given users portfolio. Also adds any api
call results to a given cache.

parameters
    code : string
    cprice_cache : { string : {} }
returns
    total worth of user portfolio : float
    cprice_cache : { string : {} }
'''
def get_user_profit(user_id, cprice_cache):
    api = Api()
    purchases = Purchase.objects.filter(user_id=user_id, unitSold__lt=F('orignialUnitBought'))
    total_worth = 0
    for purchase in purchases:
        orignialUnitBought = purchase.orignialUnitBought
        unitSold = purchase.unitSold
        unitsOwned = orignialUnitBought - unitSold
        if purchase.stock.code not in cprice_cache.keys():
            stockinfo = api.search(purchase.stock.code)
            cprice_cache[purchase.stock.code] = stockinfo['c']
        current_price = cprice_cache[purchase.stock.code]
        purchase_worth = round(unitsOwned * current_price, 2)
        total_worth = total_worth + purchase_worth
    
    return round(total_worth,2), cprice_cache