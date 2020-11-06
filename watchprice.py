from api.search_v2 import Api
import threading
from simulator.models import *
import time


class watchprice:
    def __init__(self):
        self.api = Api()

    def check(self, uid, code, original, price, action):
        while True:
            # db - retrive flag value from watchlist table
            # if flag is true:
            #   break
            time.sleep(5)
            item = WatchListItem.objects.get(user_id=uid, stock=code)
            if item.triggered:
                break

            try:
                p = self.api.search(code)['c']
                if action == "sell":
                    if p <= price and p >= original:
                        # frontend - add new notification
                        # db - create new entry of watchlistalerts
                        WatchListAlert.objects.create(
                            user_id=uid, stock=code, watchprice=price)
                        # db - set flag to true
                        item.triggered = True
                        item.save()
                        return
                elif action == "buy":
                    if p >= price and p <= original:
                        # frontend - add new notification
                        # db - create new entry of watchlistalerts
                        WatchListAlert.objects.create(
                            user_id=uid, stock=code, watchprice=price)

                        # db - set flag to true
                        item.triggered = True
                        item.save()
                        return
            except:
                pass

    # frontend will use this method to set a watchprice
    # action is either "buy" or "sell"
    def set(self, uid, code, price, action):
        p = self.api.search(code)['c']
        # db - add new watch price entry to database
        # db - get the wid from the insert
        WatchListItem.objects.create(
            user_id=uid, stock=code, original=p, watchprice=price, action=action)

        th = threading.Thread(target=self.check, args=(
            uid, code, p, price, action))
        th.start()

    # frontend will use this method to remove a watchprice
    def remove(self, uid, code):
        # TODO:
        # db - find the entry in watchlist table given by the wid(watchid)
        # db - set the flag in the entry to be true
        item = WatchListItem.objects.get(user_id=uid, stock=code)
        item.triggered = True
        item.save()
        pass


if __name__ == "__main__":
    w = watchprice()
    w.set(1, "aapl", 2, "buy")
    time.sleep(5)
    w.remove(1, "aapl")


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
