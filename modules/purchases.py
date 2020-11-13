from simulator.models import *
from django.db.models import F
import decimal
from api.search import Api
import pandas as pd
import time

'''
Gets the total number of units owned of a given stock in a user's portfolio

parameters
    code : string
    user_id : User model
returns
    total_units : int
'''
def get_total_owned_units(user_id, code):
    code = code.upper()
    purchases = Purchase.objects.filter(user_id=user_id, stock=code)
    total_units = 0
    for purchase in purchases:
        total_units = total_units + purchase.orignialUnitBought - purchase.unitSold
    return total_units


'''
Gets a Django QuerySet corrosponding to the Purchases of a given stock in a user's portfolio

parameters
    code : string
    user_id : User model
returns
    purchases : Django QuerySet of Purchase model
'''
def get_unsold_purhases(user_id, code):
    code = code.upper()
    purchases = Purchase.objects.filter(user_id=user_id, stock=code, unitSold__lt=F('orignialUnitBought')).order_by('dateBought')
    return purchases


'''
Gets a set of the unique codes that a given user has purchased. When the 'include_sold' arguement
is True, the list will contain the codes of stocks that were previously in the portfolio,
but have since been sold.

parameters
    user_id : User model
    include_sold : Bool
returns
    codes : [ string ]
'''
def get_unique_purchases_codes(user_id, include_sold):
    if include_sold:
        purchases = Purchase.objects.filter(user_id=user_id).order_by('dateBought')
    else:
        purchases = Purchase.objects.filter(user_id=user_id, unitSold__lt=F('orignialUnitBought')).order_by('dateBought')
    codes = set()
    for purchase in purchases:
        codes.add(purchase.stock.code)
    
    return codes


'''
Gets a list of dictionaries containing information about all the purchases that a given
user has made. When the 'include_sold' arguement is True, the list will contain purchases that
have has all their units previously sold

parameters
    user_id : User model
    include_sold : Bool
returns
    purchase_summary : [ { string : any} ]
    messages : {string : string}
'''
def get_purchases_info(user_id, include_sold):
    api = Api()
    if include_sold:
        purchases = Purchase.objects.filter(user_id=user_id).order_by('dateBought')
    else:
        purchases = Purchase.objects.filter(user_id=user_id, unitSold__lt=F('orignialUnitBought')).order_by('dateBought')
    cprice_cache = {}
    purchase_summary = []
    messages = {}
    for purchase in purchases:
        summary_entry = {}
        summary_entry['code'] = purchase.stock.code
        summary_entry['dateBought'] = purchase.dateBought
        summary_entry['price'] = purchase.price
        summary_entry['orignialUnitBought'] = purchase.orignialUnitBought
        summary_entry['unitsSold'] = purchase.unitSold
        summary_entry['unitsOwned'] = purchase.orignialUnitBought - purchase.unitSold
        summary_entry['paid'] = summary_entry['unitsOwned'] * summary_entry['price']
        if purchase.stock.code not in cprice_cache.keys():
            print("caching")
            try:
                stockinfo = api.search(purchase.stock.code)
            except Exception as e:
                messages['error'] = str(e)
                return [], messages
            # Add api result to cache
            cprice_cache[purchase.stock.code] = stockinfo['c']
        summary_entry['c'] = cprice_cache[purchase.stock.code]
        summary_entry['worth'] = summary_entry['unitsOwned'] * summary_entry['c']
        summary_entry['profit'] = round(float(summary_entry['worth']) - float(summary_entry['paid']),2)
        summary_entry['timestamp'] = purchase.dateBought
        purchase_summary.append(summary_entry)
    
    return purchase_summary, messages


'''
Gets a list of dictionaries containing information about all stocks in a given user's portfolio
(i.e. an aggragtion of individual purchases by stock code). The function also retruns the total
profit that the user would make by selling all the stock units they currently own, by taking the 
the difference between the current price and the purchase price.

parameters
    user_id : User model
    include_sold : Bool
returns
    portfolio_summary : [ { string : any} ]
    total_portfolio_profit : float
    messages : {string : string}
'''
def get_portfolio_info(user_id):
    purchase_summary, messages = get_purchases_info(user_id, False)
    total_portfolio_profit = 0
    portfolio_classes = {}
    for purchase_entry in purchase_summary:
        if purchase_entry['code'] not in portfolio_classes.keys():
            portfolioEntry = PortfolioEntry(purchase_entry)
            portfolio_classes[purchase_entry['code']] = portfolioEntry
        else:
            portfolioEntry = portfolio_classes[purchase_entry['code']]
            portfolioEntry.add_purchase(purchase_entry)
        total_portfolio_profit = total_portfolio_profit + purchase_entry['profit']
    
    portfolio_summary = []
    for key, value in portfolio_classes.items():
        portfolio_summary.append(value.to_json())

    return portfolio_summary, total_portfolio_profit, messages



'''
Instantiations of this class are used by the get_portfolio_info function
to cache portfolio entry information. Each time a new purchase of a stock
is found, the add_purchase() method is called on the onbject. Once all
purchases are processed, the to_json() method is used to create the
portfolio entry summary
'''
class PortfolioEntry():
    def __init__(self, purchase_entry):
        self.code = purchase_entry['code']
        self.noPurchases = 1
        self.totalUnits = purchase_entry['unitsOwned']
        self.totalPaid = purchase_entry['paid']
        self.currentPrice = purchase_entry['c']
        self.totalWorth = purchase_entry['worth']
        self.totalProfit = purchase_entry['profit']
        self.timestamp = purchase_entry['timestamp']

    def add_purchase(self, purchase_entry):
        self.noPurchases = self.noPurchases + 1
        self.totalUnits = self.totalUnits + purchase_entry['unitsOwned']
        self.totalPaid = self.totalPaid + purchase_entry['paid']
        self.totalWorth = self.totalWorth + purchase_entry['worth']
        self.totalProfit = self.totalProfit + purchase_entry['profit']
        self.timestamp = time.time()

    def to_json(self):
        purchase_entry = {
            'code': self.code,
            'noPurchases': self.noPurchases,
            'totalUnits': self.totalUnits,
            'totalPaid': round(self.totalPaid,2),
            'currentPrice': self.currentPrice,
            'totalWorth': round(self.totalWorth,2),
            'totalProfit': round(self.totalProfit,2),
            'timestamp': self.timestamp
        }
        return purchase_entry
    