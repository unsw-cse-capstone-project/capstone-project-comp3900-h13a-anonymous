from api.search import Api
import threading
from simulator.models import *
import time
import pandas as pd
from datetime import datetime


'''
Class used to help monitor watch prices that are set by the user
'''
class Watchprice:
    def __init__(self):
        self.api = Api()

    '''
    Method used to check if a given watch price alert has been trigged.

    parameters
        alertId : WatchListAlert model ID field
    '''
    def check(self, alertId):
        while True:
            time.sleep(10)
            alert = WatchListAlert.objects.get(id=alertId)
            if alert.triggered:
                return
            code = alert.stock.code
            action = alert.action
            try:
                current_price = self.api.search(code)['c']
                if action == "sell":
                    # current price is greater than or equal to watchprice
                    if current_price >= alert.watchprice:
                        # frontend - add new notification
                        alert.dateTriggered = datetime.now().isoformat(' ', 'seconds')
                        # db - set flag to true
                        alert.triggered = True
                        alert.save()
                        return
                elif action == "buy":
                    # current price is less than or equal to watchprice
                    if current_price <= alert.watchprice:
                        # frontend - add new notification
                        alert.dateTriggered = datetime.now().isoformat(' ', 'seconds')
                        # db - set flag to true
                        alert.triggered = True
                        alert.save()
                        return
            except:
                pass


    '''
    Method used to set a watchprice of a given stock. Watchprices with a "buy" action are triggered 
    when the current price is below the watch price (buy low), whereas watchprices with a "sell" action 
    are triggered when the current price is above the watch price (sell high).

    parameters
        code : string
        price : float
        user : User model
        action : string ("buy" or "sell")
    returns
        messages : {string : string}
    '''
    def set(self, code, price, user, action):
        stock = Stock.objects.get(code=code)
        alert = WatchListAlert.objects.create(user_id=user, stock=stock, watchprice=price, action=action)
        messages = {}
        messages['watchprice_set'] = f"Successfully set trigger to {action} stock {code} at watch price {price}"

        alertId = alert.pk

        th = threading.Thread(target=self.check, args=(alertId,))
        th.start()

        print("Returning messages")

        return messages


    '''
    Starts the threads which will monitor the watchprices by with the check method
    '''
    def start_up(self):
        alerts = WatchListAlert.objects.filter(triggered = False)
        for alert in alerts:
            th = threading.Thread(target=self.check, args=(alert.id,))
            th.start()


    '''
    Removes a given watch price

    parameters
        user : User model
        alert : WatchListAlert model
    returns
        messages : {string : string}
    '''
    def remove(self, user, alert):
        alert_obj = WatchListAlert.objects.get(user_id=user, id=alert)

        code = alert_obj.stock.code
        price = alert_obj.watchprice
        messages = {}
        messages['removed_wp'] = "Watchprice {} of stock {} has been removed from your watchlist".format(price, code)
        alert_obj.delete()

        return messages

        