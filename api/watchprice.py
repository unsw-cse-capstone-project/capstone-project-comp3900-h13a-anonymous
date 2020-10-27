from search_v2 import Api
import threading


class watchprice:
    def __init__(self):
        self.api = Api()


    def check(self, uid, code, original, price, action, wid):
        while True:
            # db - retrive flag value from watchlist table
            # if flag is false:
            #   break
            try:
                p = self.api.search(code)['c']
                if action == "sell":
                    if p <= price and p >= original:
                        # frontend - add new notification
                        # db - set flag to false
                        return
                elif action == "buy":
                    if p >= price and p <= original:
                        # frontend - add new notification
                        # db - set flag to false
                        return
            except:
                pass

    ## frontend will use this method to set a watchprice
    def set(self, uid, code, price, action):
        p = self.api.search(code)['c']
        ## db - add new watch price entry to database
        # db - get the wid from the insert
        th = threading.Thread(target=self.check, args=(uid, code, p, price, action, wid))
        th.start()

    ## frontend will use this method to remove a watchprice
    def remove(self, wid):
        # TODO:
        # db - find the entry in watchlist table given by the wid(watchid)
        # db - set the flag in the entry to be false
        pass



if __name__ == "__main__":
    watch = {"AAPL": 200, "AMZN": 3000}
    action = "sell"

    watchprice = watchprice()
    for stock in watch.keys():
        watchprice.set(1, stock, watch[stock], "sell")


# ##########################################################
# ## template of killing multi threads

# import threading
# import time

# class w:
#     def __init__(self):
#         self.data = {}

#     def check(self, n):
#         self.data[n] = False
#         while True:
#             print(n)
#             time.sleep(0.5)
#             if self.data[n]:
#                 break

#     def set(self, n):
#         th = threading.Thread(target=self.check, args=(n))
#         th.start()


#     def kill(self, n):
#         self.data[n] = True

# if __name__ == "__main__":
#     w = w()
#     w.set("1")
#     time.sleep(3)
#     w.set("2")
#     time.sleep(10)
#     w.kill("1")
#     time.sleep(5)
#     w.kill("2")
    