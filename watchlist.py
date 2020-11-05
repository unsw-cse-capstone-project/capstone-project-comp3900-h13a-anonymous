from api.search_v2 import Api
import json
import sqlite3
import pandas as pd
import requests
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from django.db import connection
from django.contrib.auth.models import User
from simulator.models import *
from datetime import datetime

'''
def add(code, user_id):
    # get current stock info from Finnhub API
    api = Api()
    errors = {}
    stockinfo = api.search(code)
    price = stockinfo['c']
    print("price is " + str(price))
    timestamp = stockinfo['t']
    print("time is " + str(timestamp))
    # connect to the database
    conn = sqlite3.connect('hermes.db')
    stock_count = conn.execute("SELECT COUNT(*) FROM STOCK WHERE CODE=?", (code,)).fetchone()[0]
    print(stock_count)
    if(stock_count != 1):
        conn.execute("INSERT INTO STOCK (CODE, NAME) \
            VALUES (?, ?)", (code, stockinfo["name"]))
    watchlist_count = conn.execute("SELECT COUNT(*) FROM WATCHLIST WHERE CODE=? AND ID=?", (code,user_id,)).fetchone()[0]
    if(watchlist_count != 0):
        errors['already_added'] = "Stock {} is already in your watchlist".format(code)
        return errors
    # add stock to the watchlist
    conn.execute("INSERT INTO WATCHLIST (ID, CODE, DATEADD) \
      VALUES (?, ?, ?)", (user_id, code, timestamp))
    conn.commit()
    print("Total number of rows updated :", conn.total_changes)
    return errors
'''

def add(code, user):
    # get current stock info from Finnhub API
    code = code.upper()

    api = Api()
    errors = {}
    stockinfo = api.search(code)

    price = stockinfo['c']
    #print("price is " + str(price))
    timestamp = stockinfo['t']
    #print("time is " + str(timestamp))

    # connect to the database
    stocks = Stock.objects.filter(code=code)
    if(stocks.count() != 1):
        Stock.objects.create(name=stockinfo["name"], code=code)
    
    stock_to_add_in_wl = Stock.objects.get(code=code)
    wl = WatchListItem.objects.filter(user_id=user, stock=stock_to_add_in_wl)
    if(wl.count() != 0):
        errors['already_added'] = "Stock {} is already in your watchlist".format(code)
        return errors
    
    WatchListItem.objects.create(user_id=user, stock=stock_to_add_in_wl, timestamp=datetime.utcnow().timestamp())
    '''
    with connection.cursor() as cursor:
        stock_count = cursor.execute("SELECT COUNT(*) FROM Stock WHERE CODE= %s", [code]).fetchone()[0]
        print(stock_count)
        if(stock_count != 1):
            cursor.execute("INSERT INTO Stock (CODE, NAME) \
                VALUES (?, ?)", (code, stockinfo["name"]))
        watchlist_count = cursor.execute("SELECT COUNT(*) FROM WATCHLIST WHERE CODE=%s AND ID=%s", [code, user_id]).fetchone()[0]
        if(watchlist_count != 0):
            errors['already_added'] = "Stock {} is already in your watchlist".format(code)
            return errors
        # add stock to the watchlist
        cursor.execute("INSERT INTO WATCHLIST (ID, CODE, DATEADD) \
        VALUES (%s, %s, %s)", [user_id, code, timestamp])
        cursor.commit()
        print("Total number of rows updated :", cursor.total_changes)
        '''
    return errors

def list_watchlist(user, errors):
    api = Api()
    # errors = {}
    '''
    # connect to the database
    with connection.cursor() as cursor:
    # delete the stock from watchlist
        result = cursor.execute("SELECT * FROM WATCHLIST JOIN STOCK ON WATCHLIST.CODE = STOCK.CODE \
            WHERE WATCHLIST.ID = %s ORDER BY WATCHLIST.DATEADD", [user_id])
    '''
    result = WatchListItem.objects.filter(user_id=user)

    wlist = []
    
    for row in result:
        #print(row)
        wlist_entry = {}
        code = row.stock.code
        wlist_entry['code'] = code
        wlist_entry['name'] = row.stock.name
        wlist_entry['date'] = row.date
        wlist_entry['timestamp'] = row.timestamp

        stockinfo = api.search(code)

        wlist_entry['current'] = stockinfo['c']
        wlist_entry['change'] = stockinfo['change']
        wlist.append(wlist_entry)

        # Get all alerts related to stock
        stock = Stock.objects.get(code=code)
        alerts_to_show = WatchListAlert.objects.filter(user_id=user, stock=stock,triggered=False)
        for alert in alerts_to_show:
            # If sell, current price should be >= watchprice
            if alert.action == "sell" and wlist_entry['current'] >= alert.watchprice:
                alert.dateTriggered = pd.to_datetime(stockinfo['t'], unit='s')
                errors[f'{alert.action} alert at {alert.dateTriggered} for {alert.stock.code}'] = f"Stock {alert.stock.name} hit {alert.watchprice} at {alert.dateTriggered}"
                alert.triggered=True
                alert.save()
            # If buy, current price should be <= watchprice 
            elif alert.action == "buy" and wlist_entry['current'] <= alert.watchprice:
                # print('alert to show in watchlist' + alert.stock)
                alert.dateTriggered = pd.to_datetime(stockinfo['t'], unit='s')
                errors[f'{alert.action} alert at {alert.dateTriggered} for {alert.stock.code}'] = f"Stock {alert.stock.name} hit {alert.watchprice} at {alert.dateTriggered}"
                alert.triggered=True
                alert.save()
        
        # Column for watch prices not triggered yet
        alerts_not_triggered_yet = WatchListAlert.objects.filter(user_id=user, stock=stock, triggered=False)
        wlist_entry['alerts'] = []
        for alert in alerts_not_triggered_yet:
            wlist_entry['alerts'].append(alert)
    
    return wlist, errors


def remove(code,  user):
    code = code.upper()
    errors = {}

    stock_to_remove_from_wl = Stock.objects.get(code=code)
    wl = WatchListItem.objects.get(user_id=user, stock=stock_to_remove_from_wl)
    # if(wl.count() == 0):
    #     errors['not_in_wl'] = "Stock {} is not in your watchlist".format(code)
    #     return errors

    untriggered_alerts = WatchListAlert.objects.filter(user_id=user, stock=stock_to_remove_from_wl, triggered=False)
    for alert in untriggered_alerts:
        alert.delete()

    wl.delete()

    errors['removed_from_wl'] = "Stock {} and untriggered alerts have been removed from your watchlist".format(code)
    return errors

'''
def remove(code, user_id):
    api = Api()
    errors = {}

    # connect to the database
    with connection.cursor() as cursor:
        # check if the stock exists on the watchlist
        watchlist_count = cursor.execute("SELECT COUNT(*) FROM WATCHLIST WHERE CODE=%s AND ID=%s", [code, user_id]).fetchone()[0]
        if(watchlist_count == 0):
            errors['not_exist'] = "Stock {} is not exist in your watchlist".format(code)
            return errors

        # delete the stock from watchlist
        cursor.execute("DELETE from WATCHLIST where CODE = %s", [code])
        cursor.commit()
        print("Total number of rows deleted :", cursor.total_changes)
'''

'''
def remove(code, id):
    # connect to the database
    conn = sqlite3.connect('hermes.db')
    # delete the stock from watchlist
    conn.execute("DELETE from WATCHLIST where CODE = ?", (code,))
    conn.commit()
    print("Total number of rows deleted :", conn.total_changes)
def list_watchlist(user_id):
    api = Api()
    errors = {}
    # connect to the database
    conn = sqlite3.connect('hermes.db')
    # delete the stock from watchlist
    result = conn.execute("SELECT * FROM WATCHLIST JOIN STOCK ON WATCHLIST.CODE = STOCK.CODE \
                WHERE WATCHLIST.ID=? ORDER BY WATCHLIST.DATEADD", (user_id,))
    wlist = []
    for row in result:
        print(row)
        wlist_entry = {}
        code = row[1]
        stockinfo = api.search(code)
        wlist_entry['code'] = row[1]
        wlist_entry['name'] = row[4]
        wlist_entry['date'] = pd.to_datetime(row[2], unit='s')
        wlist_entry['current'] = stockinfo['c']
        wlist_entry['change'] = stockinfo['change']
        wlist.append(wlist_entry)
    return wlist
'''

def plot_watchlist(code, time, path):
    time = 1601577795
    now =  datetime.now().timestamp()
    #r = requests.get('https://finnhub.io/api/v1/stock/candle?symbol=AAPL&resolution=1&from=1572651390&to=1572910590&token=btkkvsv48v6r1ugbcp70')
    #print(r)
    #df = pd.read_json(r.json())
    df = pd.read_csv(f'https://finnhub.io/api/v1/stock/candle?symbol={code}&resolution=1&from={time}&to={now}&token=btkkvsv48v6r1ugbcp70&format=csv')

    print(df)

    date = []
    for d in df['t']:
        date.append(datetime.fromtimestamp(d))
    fig = go.Figure(data=[go.Candlestick(x=date,
                open=df['o'], high=df['h'],
                low=df['l'], close=df['c'])
                        ])

    fig.update_layout(xaxis_rangeslider_visible=False)

    return fig.write_image(file="./simulator/templates/simulator/sample_historical_data.jpg", format = "jpg")


if __name__ == "__main__":
    # add("IC MARKETS:1", 1)
    # remove("IC MARKETS:1", 1)
    print("Hello world")