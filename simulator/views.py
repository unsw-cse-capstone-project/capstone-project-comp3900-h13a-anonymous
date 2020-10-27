from django.shortcuts import render, get_object_or_404, redirect
from .forms import CustomUserCreationForm
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
import transactions
import pandas as pd
from datetime import datetime


# Create your views here.
@login_required
def stock_list(request):
    stocks = Stock.objects.all()
    frontend_stocks = {'stocks': stocks}
    return render(request, 'simulator/sidebar.html', frontend_stocks)

@login_required
def stock_detail(request, code):
    stock = get_object_or_404(Stock, code=code)
    frontend_stock = {'stock': stock}

    # if("code" in request.GET):
    #     errors = {}
    #     api = Api()
    #     code = request.GET.get('code')
    #     result = api.search(code)
    #     print(result)
    #     if(result == "The stock code you searched was invalid"):
    #         errors['invalid stock code'] = result
    #         frontend_stock = {'errors':errors}
    #     else:
    #         frontend_stock = result
    #     return render(request, 'simulator/stock_detail.html', frontend_stock)
    

    # frontend_stock = {'name': pk}
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
    wlist = watchlist.list_watchlist(request.user)
    context = {'wlist':wlist, 'errors':errors}
    return render(request, 'simulator/my_watchlist.html', context)

@login_required
def buy_stock(request, code):
    errors = buy_sell.buy(code, 3, request.user)
    return my_watchlist_view(request, errors)

@login_required
def sell_stock(request, code):
    errors = buy_sell.sell(code, 3, request.user)
    return my_watchlist_view(request, errors)

@login_required
def transactions_view(request):
    trans = transactions.get_user_transactions(request.user)
    date = pd.to_datetime(datetime.now().timestamp(), unit='s')
    context = {'transactions':trans, 'datetime': date}
    return render(request, 'simulator/transactions.html', context)


class WatchListView(ListView):
    template_name = "simulator/my_watchlist.html"
    queryset = WatchListItem.objects.all()
    context_object_name = 'wlist'

