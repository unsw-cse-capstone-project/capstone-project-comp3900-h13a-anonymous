from api.search_v2 import Api
import json
import sqlite3
import pandas as pd
import requests
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from django.db import connection

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
    with connection.cursor() as cursor:
        stock_count = cursor.execute("SELECT COUNT(*) FROM STOCK WHERE CODE= %s", [code]).fetchone()[0]
        print(stock_count)
        if(stock_count != 1):
            cursor.execute("INSERT INTO STOCK (CODE, NAME) \
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
        return errors

def list_watchlist(user_id):
    api = Api()
    errors = {}

    # connect to the database
    with connection.cursor() as cursor:
    # delete the stock from watchlist
        result = cursor.execute("SELECT * FROM WATCHLIST JOIN STOCK ON WATCHLIST.CODE = STOCK.CODE \
            WHERE WATCHLIST.ID = %s ORDER BY WATCHLIST.DATEADD", [user_id])

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
     now =  datetime.now().timestamp()
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

     fig.write_html("sample_historical_data.html", full_html = False)


if __name__ == "__main__":
    add("IC MARKETS:1", 1)
    remove("IC MARKETS:1", 1)
