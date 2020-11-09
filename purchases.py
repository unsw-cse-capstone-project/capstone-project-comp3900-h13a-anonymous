from simulator.models import *
from django.db.models import F
import decimal
from api.search import Api
import pandas as pd
import time


def get_total_owned_units(user_id, code):
    purchases = Purchase.objects.filter(user_id=user_id, stock=code)
    total_units = 0
    for purchase in purchases:
        total_units = total_units + purchase.orignialUnitBought - purchase.unitSold
    return total_units

def get_unsold_purhases(user_id, code):
    purchases = Purchase.objects.filter(user_id=user_id, stock=code, unitSold__lt=F('orignialUnitBought')).order_by('dateBought')
    return purchases

def get_unique_purchases_codes(user_id, include_sold):
    if include_sold:
        purchases = Purchase.objects.filter(user_id=user_id).order_by('dateBought')
    else:
        purchases = Purchase.objects.filter(user_id=user_id, unitSold__lt=F('orignialUnitBought')).order_by('dateBought')
    codes = set()
    for purchase in purchases:
        codes.add(purchase.stock.code)
    
    return codes

def get_purchases_info(user_id, include_sold):
    api = Api()
    if include_sold:
        purchases = Purchase.objects.filter(user_id=user_id).order_by('dateBought')
    else:
        purchases = Purchase.objects.filter(user_id=user_id, unitSold__lt=F('orignialUnitBought')).order_by('dateBought')
    cprice_cache = {}
    purchase_summary = []
    for purchase in purchases:
        summary_entry = {}
        summary_entry['code'] = purchase.stock.code
        summary_entry['dateBought'] = pd.to_datetime(purchase.dateBought, unit='s')
        summary_entry['price'] = purchase.price
        summary_entry['orignialUnitBought'] = purchase.orignialUnitBought
        summary_entry['unitsSold'] = purchase.unitSold
        summary_entry['unitsOwned'] = purchase.orignialUnitBought - purchase.unitSold
        summary_entry['paid'] = summary_entry['unitsOwned'] * summary_entry['price']
        if purchase.stock.code not in cprice_cache.keys():
            stockinfo = api.search(purchase.stock.code)
            cprice_cache[purchase.stock.code] = stockinfo['c']
            #cprice_cache[purchase.stock.code] = 100.00
        summary_entry['c'] = cprice_cache[purchase.stock.code]
        summary_entry['worth'] = summary_entry['unitsOwned'] * summary_entry['c']
        summary_entry['profit'] = round(float(summary_entry['worth']) - float(summary_entry['paid']),2)
        summary_entry['timestamp'] = round(float(purchase.dateBought))
        print(purchase.dateBought)
        purchase_summary.append(summary_entry)
    
    return purchase_summary

def get_portfolio_info(user_id):
    purchase_summary = get_purchases_info(user_id, False)
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

    return portfolio_summary, total_portfolio_profit


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
            'totalPaid': self.totalPaid,
            'currentPrice': self.currentPrice,
            'totalWorth': self.totalWorth,
            'totalProfit': self.totalProfit,
            'timestamp': self.timestamp
        }
        return purchase_entry
    