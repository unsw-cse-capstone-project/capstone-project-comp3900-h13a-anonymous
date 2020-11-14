from api.search import Api
from simulator.models import *
from datetime import datetime


'''
Adds the stock corrosponding to a given code to a user's watchlist,
provided the stock code is valid.

parameters
    code : string
    user : User model
returns
    messages : {string : string}
'''
def add(code, user):
    # Get current stock info from Finnhub API
    code = code.upper()
    api = Api()
    messages = {}
    try:
        stockinfo = api.search(code)
    except Exception as e:
        messages['error'] = str(e)
        return messages

    price = stockinfo['c']
    timestamp = stockinfo['t']

    # cache stock info if this is the first time app has encountered stock
    stocks = Stock.objects.filter(code=code)
    if(stocks.count() != 1):
        Stock.objects.create(name=stockinfo["name"], code=code)
    
    stock_to_add_in_wl = Stock.objects.get(code=code)
    wl = WatchListItem.objects.filter(user_id=user, stock=stock_to_add_in_wl)
    if(wl.count() != 0):
        messages['error'] = "Stock {} is already in your watchlist".format(code)
        return messages
    
    WatchListItem.objects.create(user_id=user, stock=stock_to_add_in_wl, timestamp=datetime.utcnow().timestamp())
    messages['success'] = "Stock {} added to your watchlist".format(code)

    return messages


'''
Returns a list of dictionaries containing information about all stocks in a given
user's watchlist.

parameters
    user : User model
    messages : {string : string}
returns
    wlist : [ {string : any} ]
    messages : {string : string}
'''
def list_watchlist(user, messages):
    api = Api()
    result = WatchListItem.objects.filter(user_id=user)

    wlist = []
    
    for row in result:
        wlist_entry = {}
        code = row.stock.code
        wlist_entry['code'] = code
        wlist_entry['name'] = row.stock.name
        wlist_entry['date'] = row.date
        wlist_entry['timestamp'] = row.timestamp
        
        # Get current stock info from Finnhub API
        try:
            stockinfo = api.search(code)
            wlist_entry['current'] = stockinfo['c']
            wlist_entry['change'] = stockinfo['change']
        except Exception as e:
            wlist_entry['current'] = "N/A"
            wlist_entry['change'] = "N/A"
            messages['error'] = str(e)

        
        wlist.append(wlist_entry)

        # Get all alerts related to stock
        stock = Stock.objects.get(code=code)
        alerts_to_show = WatchListAlert.objects.filter(user_id=user, stock=stock, triggered=True, shown=False)
        print(len(alerts_to_show))
        for alert in alerts_to_show:
            messages[f'alert at {alert.dateTriggered} for {alert.stock.code}'] = f"Stock {alert.stock.name} hit {alert.watchprice} at {alert.dateTriggered}"
            alert.shown=True
            alert.save()
        
        # Column for watch prices not triggered yet
        alerts_not_triggered_yet = WatchListAlert.objects.filter(user_id=user, stock=stock, triggered=False)
        wlist_entry['alerts'] = []
        for alert in alerts_not_triggered_yet:
            wlist_entry['alerts'].append(alert)
    
    return wlist, messages


'''
Removes the watchlist entry of a given stock code from a users watchlist, 
as well as all untriggered alerts for that watchlist entry.

parameters
    code : string
    user : User model
returns
    messages : {string : string}
'''
def remove(code,  user):
    code = code.upper()
    messages = {}

    stock_to_remove_from_wl = Stock.objects.get(code=code)
    wl = WatchListItem.objects.get(user_id=user, stock=stock_to_remove_from_wl)

    untriggered_alerts = WatchListAlert.objects.filter(user_id=user, stock=stock_to_remove_from_wl, triggered=False)
    for alert in untriggered_alerts:
        alert.delete()

    wl.delete()

    messages['removed_from_wl'] = "Stock {} and untriggered alerts have been removed from your watchlist".format(code)
    return messages
