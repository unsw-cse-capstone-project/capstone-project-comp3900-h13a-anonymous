from django.shortcuts import render, get_object_or_404
from .models import Stock
from api.search_v2 import Api
import watchlist

# Create your views here.
def stock_list(request):
    stocks = Stock.objects.all()
    frontend_stocks = {'stocks': stocks}
    return render(request, 'simulator/sidebar.html', frontend_stocks)

def stock_detail(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    frontend_stock = {'stock': stock}
    return render(request, 'simulator/stock_detail.html', frontend_stock)

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

def add_to_watchlist(request, code):
    errors = watchlist.add(code, 1)
    return my_watchlist_view(request, errors)


def my_watchlist_view(request, errors={}):
    wlist = watchlist.list_watchlist(1)
    context = {'wlist':wlist, 'errors':errors}
    return render(request, 'simulator/my_watchlist.html', context)