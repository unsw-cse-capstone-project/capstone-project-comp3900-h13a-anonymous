from api.search_v2 import Api
import threading
from simulator.models import *
import time
import pandas as pd

class Watchprice:
    def __init__(self):
        self.api = Api()

    def check(self, user, code, price, action):
        while True:
            # db - retrive flag value from watchlist table
            # if flag is true:
            #   break
            # stock = Stock.objects.get(code=code)
            # # Get all alerts related to stock
            # stock = Stock.objects.get(code=code)
            
            # Goes through untriggered alerts
            alerts = WatchListAlert.objects.filter(user_id=user, triggered=False)
            for alert in alerts:
                code = alert.stock.code
                try:
                    current_price = self.api.search(code)['c']
                    if action == "sell":
                        # current price is greater than or equal to watchprice
                        if current_price >= alert.watchprice:
                            # frontend - add new notification
                            alert.dateTriggered = pd.to_datetime(self.api.search(code)['t'], unit='s')
                            # db - set flag to true
                            alert.triggered = True
                            alert.save()
                            return
                    elif action == "buy":
                        # current price is less than or equal to watchprice
                        if current_price <= alert.watchprice:
                            # frontend - add new notification
                            alert.dateTriggered = pd.to_datetime(self.api.search(code)['t'], unit='s')
                            # db - set flag to true
                            alert.triggered = True
                            alert.save()
                            return
                except:
                    pass

    # frontend will use this method to set a watchprice
    # action is either "buy" or "sell"
    def set(self, code, price, user, action):
        # db - add new watch price entry to database
        # db - get the wid from the insert

        stock = Stock.objects.get(code=code)
        WatchListAlert.objects.create(user_id=user, stock=stock, watchprice=price, action=action)
        errors = {}
        errors['watchprice_set'] = f"Successfully set trigger to {action} stock {code} at watch price {price}"

        th = threading.Thread(target=self.check, args=(user, code, price, action))
        th.start()

        print("Returning errors")

        return errors

    def remove(self, user, alert):
        alert_obj = WatchListAlert.objects.get(user_id=user, id=alert)

        code = alert_obj.stock.code
        price = alert_obj.watchprice
        errors = {}
        errors['removed_wp'] = "Watchprice {} of stock {} has been removed from your watchlist".format(price, code)
        alert_obj.delete()

        return errors

        
    '''
    # frontend will use this method to remove a watchprice
    def remove(self, uid, code):
        # db - find the entry in watchlist table given by the wid(watchid)
        # db - set the flag in the entry to be true
        item = WatchListItem.objects.get(user_id=uid, stock=code)
        item.triggered = True
        item.save()
        pass
    '''


# if __name__ == "__main__":
#     w = watchprice()
#     w.set(1, "aapl", 2, "buy")
#     time.sleep(5)
#     w.remove(1, "aapl")


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
