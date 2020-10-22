from search_v2 import Api
import threading


class watchprice:
    def __init__(self):
        self.api = Api()


    ## may need to add an argument user id to make notification
    def check(self, uid, code, original, price, action):
        while True:
            try:
                p = self.api.search(code)['c']
                if action == "sell":
                    if p <= price and p >= original:
                        # add new notification
                        return
                elif action == "buy":
                    if p >= price and p <= original:
                        # add new notification
                        return
            except:
                pass

    def set(self, uid, code, price, action):
        p = self.api.search(code)['c']
        th = threading.Thread(target=self.check, args=(uid, code, p, price, action))
        th.start()
        ## add new watch price entry to database



if __name__ == "__main__":
    watch = {"AAPL": 200, "AMZN": 3000}
    action = "sell"

    watchprice = watchprice()
    for stock in watch.keys():
        watchprice.set(1, stock, watch[stock], "sell")
