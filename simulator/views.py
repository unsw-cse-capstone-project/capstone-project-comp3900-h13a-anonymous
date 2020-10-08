from django.shortcuts import render, get_object_or_404
from .models import Stock 

# Create your views here.
def stock_list(request):
    stocks = Stock.objects.all()
    frontend_stocks = {'stocks': stocks}
    return render(request, 'simulator/stock_list.html', frontend_stocks)

def stock_detail(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    frontend_stock = {'stock': stock}
    return render(request, 'simulator/stock_detail.html', frontend_stock)