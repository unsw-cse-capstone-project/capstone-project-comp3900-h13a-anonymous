from search import search
import json
import sqlite3


def add(stock, amount, id):
    # get current stock info from Finnhub API
    tgt = search(stock)
    stockinfo = json.loads(tgt)

    price = stockinfo["data"][0]['p']
    print("price is " + str(price))
    timestamp = stockinfo["data"][0]['t']
    print("time is " + str(timestamp))
    code = stockinfo["data"][0]['s']
    print("code is " + str(code))
    print(price)
    money = price * amount

    # connect to the database
    conn = sqlite3.connect('hermes.db')
    # add stock to the watchlist
    conn.execute("INSERT INTO WATCHLIST (ID, CODE, DATEADD) \
      VALUES (?, ?, ?)", (id, code, timestamp))
    conn.commit()
    print("Total number of rows updated :", conn.total_changes)


def remove(code, id):
    # connect to the database
    conn = sqlite3.connect('hermes.db')
    # delete the stock from watchlist
    conn.execute("DELETE from WATCHLIST where CODE = ?", (code,))
    conn.commit()
    print("Total number of rows deleted :", conn.total_changes)


if __name__ == "__main__":
    add("IC MARKETS:1", 1, 1)
    remove("IC MARKETS:1", 1)
