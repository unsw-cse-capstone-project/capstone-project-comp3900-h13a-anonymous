from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.response import Response
from api import historical2
import api
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CustomUserCreationForm, BuyForm, SellForm, SetWatchPriceForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Stock, WatchListItem, WatchListAlert
from api.search_v2 import Api
import watchlist
import prediction
from django.views.generic import (
    ListView
)
import buy_sell
from watchprice_2 import Watchprice
import transactions
import purchases
import pandas as pd
from datetime import datetime
import requests
import plotly.graph_objects as go
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


User = get_user_model()

# Create your views here.


@login_required
def stock_list(request):
    stocks = Stock.objects.all()
    return render(request, 'simulator/sidebar.html', {'stocks': stocks})


@login_required
def stock_detail(request, code):
    # stock = get_object_or_404(Stock, code=code)
    stock = Stock.objects.get(code=code)
    return render(request, 'simulator/stock_detail.html', {'stock': stock})


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            # messages.success(request, 'Account created successfully')
            login(request, new_user)
            return redirect('/')
    else:
        form = CustomUserCreationForm()

    return render(request, 'simulator/signup.html', {'form': form})

@login_required
def search_view(request):

    if("code" in request.GET):
        errors = {}
        api = Api()
        code = request.GET.get('code')
        result = api.search(code)
        print(result)
        if(result == "The stock code you searched was invalid"):
            errors['invalid stock code'] = result
            search_info = {'errors': errors}
        else:
            search_info = result
        return render(request, 'simulator/search.html', search_info)

    return render(request, 'simulator/search.html')


@login_required
def add_to_watchlist(request, code):
    errors = watchlist.add(code, request.user)
    return HttpResponseRedirect('../../my_watchlist/display=false/')


@login_required

def my_watchlist_view(request, errors={}, display='false'):
    wlist, errors_2 = watchlist.list_watchlist(request.user, errors)
    context = {'wlist': wlist, 'errors': errors_2, 'display': display}
    return render(request, 'simulator/my_watchlist.html', context)


@login_required
def remove_watchlist(request, code):
    errors = watchlist.remove(code, request.user)
    return HttpResponseRedirect('../../my_watchlist/display=false/')


@login_required
def buy_stock(request, code):
    if request.method == 'POST':
        form = BuyForm(request.POST)
        if form.is_valid():
            amount = form.save()
            errors = buy_sell.buy(code, amount, request.user)
            return my_watchlist_view(request, errors)
            # return redirect('watchlist', errors=errors)
    else:
        form = BuyForm()
    return render(request, 'simulator/buy_form.html', {'form': form})


@login_required
def sell_stock(request, code):
    if request.method == 'POST':
        form = SellForm(request.POST)
        if form.is_valid():
            amount = form.save()
            errors = buy_sell.sell(code, amount, request.user)
            return my_watchlist_view(request, errors)
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
    purchase_summary = purchases.get_purchases_info(request.user, False)
    codes = purchases.get_unique_purchases_codes(request.user, False)
    context = {'purchases':purchase_summary, 'codes':codes, "defaultCode":defaultCode}
    return render(request, 'simulator/purchases.html', context)

@login_required
def purchasesIncludeSold_view(request, defaultCode=""):
    purchase_summary = purchases.get_purchases_info(request.user, True)
    codes = purchases.get_unique_purchases_codes(request.user, True)
    context = {'purchases':purchase_summary, 'includeSold':True, 'codes':codes, "defaultCode":defaultCode}
    return render(request, 'simulator/purchases.html', context)

@login_required
def portfolio_view(request):
    portfolio_summary, total_portfolio_profit = purchases.get_portfolio_info(request.user)
    context = {'portfolio':portfolio_summary, 'total_portfolio_profit':total_portfolio_profit}
    return render(request, 'simulator/my_portfolio.html', context)

@login_required
def gen_graph(request, code, date):
    historical2.get_historical(code, date)
    return HttpResponseRedirect('../../my_watchlist/display=true/')


@login_required
def show_graph(request):
    return render(request, 'simulator/graph.html')


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
            errors = w.set(code, price, request.user, action)
            return my_watchlist_view(request, errors)
    else:
        form = SetWatchPriceForm()
    return render(request, 'simulator/set_watchprice.html', {'form': form})

@login_required
def remove_watchprice(request, id):
    w = Watchprice()
    errors = w.remove(request.user, id)
    return my_watchlist_view(request, errors)

# class WatchListView(ListView):
#     template_name = "simulator/my_watchlist.html"
#     queryset = WatchListItem.objects.all()
#     context_object_name = 'wlist'


class ChartView(View):
    def get(self, request, code):
        return render(request, 'charts.html', {"code": code})


def get_data(request, code):
    qs_count = User.objects.all().count()
    labels = []
    default_items = []
    predictData = prediction.predict(code, 30)
    for i in predictData:
        labels.append(i[0].strftime("%B %d"));
        default_items.append(i[1]);

    data = {
        "labels": labels,
        "default": default_items,
    }
    return JsonResponse(data)  # http response

