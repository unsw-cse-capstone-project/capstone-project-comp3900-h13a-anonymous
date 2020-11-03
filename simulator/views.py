from django.shortcuts import render, get_object_or_404, redirect
from .forms import CustomUserCreationForm, BuyForm, SellForm, SetWatchPriceForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Stock, WatchListItem, WatchListAlert
from api.search_v2 import Api
import watchlist
from django.views.generic import (
    ListView
)
import buy_sell
from watchprice_2 import Watchprice

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
            search_info = {'errors':errors}
        else:
            search_info = result
        return render(request, 'simulator/search.html', search_info)

    return render(request, 'simulator/search.html')

@login_required
def add_to_watchlist(request, code):
    errors = watchlist.add(code, request.user)
    return my_watchlist_view(request, errors)

@login_required
def my_watchlist_view(request, errors={}):
    wlist, errors_2 = watchlist.list_watchlist(request.user, errors)
    context = {'wlist':wlist, 'errors':errors_2}
    return render(request, 'simulator/my_watchlist.html', context)

@login_required
def remove_watchlist(request, code):
    errors = watchlist.remove(code, request.user)
    return my_watchlist_view(request, errors)

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

