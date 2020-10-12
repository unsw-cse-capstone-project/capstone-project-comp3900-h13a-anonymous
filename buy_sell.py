from search import search
import json
def buy(name, amount):
    tgt = search(name)
    stockinfo = json.loads(tgt)

    price = stockinfo["data"][0]['p']
    print(price)
    money = price * amount
    #interact with database to subtract money
    #interact with database to add stock to user's account

# def sell(name, amount):
    
#     if check(name, amount): 
#         tgt = search(name)
#         stockinfo = json.loads(tgt)
#         price = stockinfo["data"][0]['p']
#         money = price * amount
if __name__ == "__main__":
    buy("BINANCE:BTCUSDT", 1)
