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
from .forms import CustomUserCreationForm, BuyForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Stock, WatchListItem
from api.search_v2 import Api
import watchlist
from django.views.generic import (
    ListView
)
import buy_sell
import pandas as pd
import requests
from datetime import datetime
import plotly.graph_objects as go
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


User = get_user_model()

# Create your views here.


@login_required
def stock_list(request):
    stocks = Stock.objects.all()
    frontend_stocks = {'stocks': stocks}
    return render(request, 'simulator/sidebar.html', frontend_stocks)


@login_required
def stock_detail(request, code):
    # stock = get_object_or_404(Stock, code=code)
    stock = Stock.objects.get(code=code)
    frontend_stock = {'stock': stock}
    return render(request, 'simulator/stock_detail.html', frontend_stock)


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

# @login_required
# @transaction.atomic
# def update_profile(request):
#     if request.method == 'POST':
#         user_form = UserForm(request.POST, instance=request.user)
#         profile_form = ProfileForm(request.POST, instance=request.user.profile)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, _('Your profile was successfully updated!'))
#             return redirect('settings:profile')
#         else:
#             messages.error(request, _('Please correct the error below.'))
#     else:
#         user_form = UserForm(instance=request.user)
#         profile_form = ProfileForm(instance=request.user.profile)
#     return render(request, 'profiles/profile.html', {
#         'user_form': user_form,
#         'profile_form': profile_form
#     })


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
    wlist = watchlist.list_watchlist(request.user)
    context = {'wlist': wlist, 'errors': errors, 'display': display}
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
    else:
        form = BuyForm()

    return render(request, 'simulator/buy_form.html', {'form': form})


@login_required
def sell_stock(request, code):
    errors = buy_sell.sell(code, 3, request.user)
    return my_watchlist_view(request, errors)


@login_required
def gen_graph(request, code, date):
    historical2.get_historical(code, date)
    return HttpResponseRedirect('../../my_watchlist/display=true/')


@login_required
def show_graph(request):
    return render(request, 'simulator/graph.html')
    


class WatchListView(ListView):
    template_name = "simulator/my_watchlist.html"
    queryset = WatchListItem.objects.all()
    context_object_name = 'wlist'


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'charts.html', {"customers": 10})


def get_data(request, *args, **kwargs):
    #qs_count = User.objects.all().count()
    labels = ["Users", "Blue", "Yellow", "Green", "Purple", "Orange"]
    #default_items = [qs_count, 23, 2, 3, 12, 2]
    time = 1601577795
    code = "AAPL"
    now =  datetime.now().timestamp()
    df = pd.read_csv(f'https://finnhub.io/api/v1/stock/candle?symbol={code}&resolution=1&from={time}&to={now}&token=btkkvsv48v6r1ugbcp70&format=csv')

    high = df['h'].tolist()
    low = df['l'].tolist()
    closePrice = df['c'].tolist()
    openPrice = df['o'].tolist()

    date = []
    for d in df['t'].tolist():
        date.append(datetime.fromtimestamp(d))
    '''
    default_items=[go.Candlestick(x=date,
                open=df['o'], high=df['h'],
                low=df['l'], close=df['c'])
                        ]'''
    data = {
            "labels": date,
            "default": high,
    }
    return JsonResponse(data) # http response


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        qs_count = User.objects.all().count()
        labels = ["Users", "Blue", "Yellow", "Green", "Purple", "Orange"]
        default_items = [qs_count, 23, 2, 3, 12, 2]
        data = {
                "labels": labels,
                "default": default_items,
        }
        return Response(data)

