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

# def sell(name, amount):
    
#     if check(name, amount): 
#         tgt = search(name)
#         stockinfo = json.loads(tgt)
#         price = stockinfo["data"][0]['p']
#         money = price * amount
if __name__ == "__main__":
    buy("BINANCE:BTCUSDT", 1, 1)
