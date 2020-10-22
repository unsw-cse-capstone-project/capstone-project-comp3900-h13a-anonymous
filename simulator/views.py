from django.shortcuts import render, get_object_or_404, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from api.search_v2 import Api
import watchlist

# Create your views here.
@login_required
def stock_list(request):
    stocks = Stock.objects.all()
    frontend_stocks = {'stocks': stocks}
    return render(request, 'simulator/sidebar.html', frontend_stocks)

@login_required
def stock_detail(request, pk):
    # stock = get_object_or_404(Stock, pk=pk)
    # frontend_stock = {'stock': stock}

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
    

    frontend_stock = {'name': pk}
    return render(request, 'simulator/stock_detail.html')

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

def add_to_watchlist(request, code):
    errors = watchlist.add(code, 1)
    return my_watchlist_view(request, errors)

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
    return render(request, 'simulator/my_watchlist.html', context)

