from api.search_v2 import Api
import json
import sqlite3
import pandas as pd
from stock.models import Stock
from user.models import User
from watchlist.models import Watchlist


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
    new_watchlist = Watchlist(id = user_id, code = code, date = timestamp)
    new_watchlist.save()'''


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
        

    


if __name__ == "__main__":
    add("IC MARKETS:1", 1, 1)
    remove("IC MARKETS:1", 1)
