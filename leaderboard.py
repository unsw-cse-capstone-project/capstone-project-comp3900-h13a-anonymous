from simulator.models import *
from api.search import Api
from django.db.models import F


def get_leaderboard_info():
    profiles = Profile.objects.all()
    cprice_cache = {}
    leaderboard = []
    for p in profiles:
        if p.user.is_superuser:
            continue
        user_entry = {}
        user_entry['name'] = p.user.username
        user_entry['balance'] = float(p.balance)
        user_entry['portfolio_worth'], cprice_cache = get_user_profit(p.user, cprice_cache)
        user_entry['total_worth'] = round(user_entry['balance'] + user_entry['portfolio_worth'],2)
        leaderboard.append(user_entry)

    sorted_leaderboard = sorted(leaderboard, key = lambda l: l['total_worth'], reverse=True)
    i = 1
    for l in sorted_leaderboard:
        l['rank'] = i
        i = i + 1

    return sorted_leaderboard

    

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