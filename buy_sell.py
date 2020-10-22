from search import search
import json
import sqlite3

def buy(name, amount, id):
    tgt = search(name)
    stockinfo = json.loads(tgt)

    price = stockinfo["data"][0]['p']
    print(price)
    money = price * amount

    conn = sqlite3.connect('hermes.db')
    #interact with database to subtract money
    conn.execute("UPDATE USER set BALANCE = BALANCE - ? where ID = ?", (money,id))
    conn.commit()
    print ("Total number of rows updated :", conn.total_changes)
    #interact with database to add stock to user's account

def sell(name, amount, id):
    
    if check(name, amount, id): 
        tgt = search(name)
        stockinfo = json.loads(tgt)
        price = stockinfo["data"][0]['p']
        money = price * amount
        conn = sqlite3.connect('hermes.db')
        conn.execute(
            "UPDATE USER set BALANCE = BALANCE + ? where ID = ?", (money, id))
        conn.commit()
        print("Total number of rows updated :", conn.total_changes)

def check(name, amount, id):
    conn = sqlite3.connect('hermes.db')
    conn.execute('')


if __name__ == "__main__":
    buy("IC MARKETS:1", 1, 1)
