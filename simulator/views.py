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
        #print(result)
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

<<<<<<< HEAD
def my_watchlist_view(request, code=None, errors={}):
    context = {}
    if(code != None):
        st = Stock.objects.get(code=code)
        #should use currently logged in user
        user= User.objects.get(email=1) 
        entry = WatchList.objects.get(user_id=user, code=st)
        context['entry'] = entry
        #graph = entry.plot_watchlist()
        graph = watchlist.plot_watchlist(code, entry.date, None)
        #entry.plot_watchlist()
        context['graph'] = graph

    wlist = watchlist.list_watchlist(1)
    context['wlist'] = wlist
    context['errors'] = errors
=======
@login_required
def my_watchlist_view(request, errors={}):
    wlist = watchlist.list_watchlist(request.user)
    context = {'wlist':wlist, 'errors':errors}
>>>>>>> master
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
    else:
        form = BuyForm()
    
    return render(request, 'simulator/buy_form.html', {'form': form})

@login_required
def sell_stock(request, code):
    errors = buy_sell.sell(code, 3, request.user)
    return my_watchlist_view(request, errors)


class WatchListView(ListView):
    template_name = "simulator/my_watchlist.html"
    queryset = WatchListItem.objects.all()
    context_object_name = 'wlist'

