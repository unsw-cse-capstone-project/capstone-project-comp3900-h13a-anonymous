from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CustomUserCreationForm, BuyForm, SellForm, SetWatchPriceForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Stock, WatchListItem, WatchListAlert
from django.views.generic import (
    ListView
)
import pandas as pd
from datetime import datetime
import requests
import plotly.graph_objects as go
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
User = get_user_model()


# Hermes Modules
import api
from api import historical
from api.search import Api
import modules.buy_sell as buy_sell
import modules.transactions as transactions
import modules.purchases as purchases
import modules.leaderboard as leaderboard
import modules.watchlist as watchlist
import modules.prediction as prediction
from modules.watchprice import Watchprice


'''
This file contains the views which are used to render the html
pages for the Hermes Web Application.
'''

@login_required
def stock_list(request):
    return render(request, 'simulator/home.html')


@login_required
def stock_detail(request, code):
    stockObj = Stock.objects.get(code=code)
    api = Api()
    stockinfo = api.search(code)
    stock = {}
    stock['code'] = stockObj.code
    stock['name'] = stockObj.name
    stock['current'] = stockinfo['c']
    stock['change'] = stockinfo['change']
    stock['alerts'] = []
    alerts_not_triggered_yet = WatchListAlert.objects.filter(user_id=request.user, stock=stockObj, triggered=False)
    if alerts_not_triggered_yet.count() == 0:
        stock['alert'] = "No alerts to display"
    else:
        stock['alert'] = ""
        for alert in alerts_not_triggered_yet:
            stock['alerts'].append(alert)

    return render(request, 'simulator/stock_detail.html', {'stock': stock})


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('/')
    else:
        form = CustomUserCreationForm()

    return render(request, 'simulator/signup.html', {'form': form})

@login_required
def search_view(request):

    if("code" in request.GET):
        messages = {}
        api = Api()
        code = request.GET.get('code')

        try:
            result = api.search(code)
        except Exception as e:
            messages['error'] = str(e)
            search_info = {'messages': messages}
        else:
            search_info = result
        finally:
            return render(request, 'simulator/search.html', search_info)

    return render(request, 'simulator/search.html')


@login_required
def add_to_watchlist(request, code):
    messages = watchlist.add(code, request.user)
    return HttpResponseRedirect('../../my_watchlist/display=false/')


@login_required
def my_watchlist_view(request, messages={}, display='false'):
    messages_2 = {}
    wlist, messages_2 = watchlist.list_watchlist(request.user, messages_2)
    messages.update(messages_2)
    context = {'wlist': wlist, 'messages': messages_2, 'display': display}
    return render(request, 'simulator/my_watchlist.html', context)


@login_required
def remove_watchlist(request, code):
    messages = watchlist.remove(code, request.user)
    return HttpResponseRedirect('../../my_watchlist/display=false/')


@login_required
def buy_stock(request, code):
    if request.method == 'POST':
        form = BuyForm(request.POST)
        if form.is_valid():
            amount = form.save()
            messages = buy_sell.buy(code, amount, request.user)
            #return purchases_view(request, messages=messages)
            # return redirect('watchlist', messages=messages)
            request.session['messages'] = messages
            return HttpResponseRedirect('../../purchases/')
    else:
        form = BuyForm()
    return render(request, 'simulator/buy_form.html', {'form': form})


@login_required
def sell_stock(request, code):
    if request.method == 'POST':
        form = SellForm(request.POST)
        if form.is_valid():
            amount = form.save()
            messages = buy_sell.sell(code, amount, request.user)
            #return portfolio_view(request, messages=messages)
            request.session['messages'] = messages
            return HttpResponseRedirect('../../my_portfolio/display=false/')
    else:
        form = SellForm()
    return render(request, 'simulator/sell_form.html', {'form': form})

@login_required
def transactions_view(request):
    trans = transactions.get_user_transactions(request.user)
    date = pd.to_datetime(datetime.now().timestamp(), unit='s')
    context = {'transactions':trans, 'datetime': date}
    return render(request, 'simulator/transactions.html', context)

@login_required
def purchases_view(request, defaultCode=""):
    messages={}
    if 'messages' in request.session.keys():
        messages.update(request.session['messages'])
        del request.session['messages']
        request.session.modified = True
    purchase_summary, messages2 = purchases.get_purchases_info(request.user, False)
    messages.update(messages2)
    codes = purchases.get_unique_purchases_codes(request.user, False)
    context = {'purchases':purchase_summary, 'codes':codes, "defaultCode":defaultCode, 'messages': messages}
    return render(request, 'simulator/purchases.html', context)

@login_required
def purchasesIncludeSold_view(request, defaultCode=""):
    purchase_summary, messages = purchases.get_purchases_info(request.user, True)
    codes = purchases.get_unique_purchases_codes(request.user, True)
    context = {'purchases':purchase_summary, 'includeSold':True, 'codes':codes, "defaultCode":defaultCode, 'messages': messages}
    return render(request, 'simulator/purchases.html', context)

@login_required
def portfolio_view(request, display='false'):
    messages={}
    if 'messages' in request.session.keys():
        messages.update(request.session['messages'])
        del request.session['messages']
        request.session.modified = True
    portfolio_summary, total_portfolio_profit, messages2 = purchases.get_portfolio_info(request.user)
    messages.update(messages2)
    context = {'portfolio':portfolio_summary, 'total_portfolio_profit':total_portfolio_profit, 'display': display, 'messages': messages}
    return render(request, 'simulator/my_portfolio.html', context)

@login_required
def leaderboard_view(request):
    lboard, messages = leaderboard.get_leaderboard_info()
    username = request.user.get_username()
    context = {'leaderboard':lboard, 'username':username, 'messages': messages}
    return render(request, 'simulator/leaderboard.html', context)

@login_required
def gen_graph(request, code, date):
    historical.get_historical(code, date)
    return HttpResponseRedirect('../../my_watchlist/display=true/')


@login_required
def show_graph(request):
    return render(request, 'simulator/graph.html')

@login_required
def gen_graph_port(request, code, date):
    historical.get_historical(code, date)
    return HttpResponseRedirect('../../my_portfolio/display=true/')

@login_required
def alerts(request):
    alerts = WatchListAlert.objects.filter(user_id=request.user).reverse()
    return render(request, 'simulator/alerts.html', {'alerts': alerts})

@login_required
def set_watchprice(request, code):
    if request.method == 'POST':
        form = SetWatchPriceForm(request.POST)
        if form.is_valid():
            price, action = form.save()
            w = Watchprice()
            messages = w.set(code, price, request.user, action)
            return my_watchlist_view(request, messages)
    else:
        form = SetWatchPriceForm()
    return render(request, 'simulator/set_watchprice.html', {'form': form})

@login_required
def remove_watchprice(request, id):
    w = Watchprice()
    messages = w.remove(request.user, id)
    return my_watchlist_view(request, messages)


class ChartView(View):
    def get(self, request, code):
        return render(request, 'charts.html', {"code": code})


def get_data(request, code):
    qs_count = User.objects.all().count()
    labels = []
    default_items = []
    predictData = prediction.predict(code, 30)
    for i in predictData:
        labels.append(i[0].strftime("%B %d"))
        default_items.append(i[1])

    data = {
        "labels": labels,
        "default": default_items,
    }
    return JsonResponse(data)  # http response

