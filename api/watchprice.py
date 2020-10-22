from search_v2 import Api
import threading


class watchprice:
    def __init__(self):
        self.api = Api()

    def set(self, code, price, action):
        th = threading.Thread(target=check, args=(code, price, action))
        th.start()

    def check(self, code, price, action):
        while True:
            try:
                p = self.api.search(code)['c']
                if action == "sell":
                    if p <= price:
                        # add new notification
                        return
                elif action == "buy":
                    if p >= price:
                        # add new notification
                        return
            except:
                pass

if __name__ == "__main__":
    watch = {"AAPL": 200, "AMZN": 3000}
    action = "sell"

    watchprice = watchprice()
    for stock in watch.keys():
        watchprice.set(stock, watch[stock], "sell")
