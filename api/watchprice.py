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

    ## frontend will use this method to set a watchprice
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
    