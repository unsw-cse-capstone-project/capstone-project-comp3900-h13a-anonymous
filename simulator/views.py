from django.shortcuts import render, get_object_or_404
from .models import Stock 

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
    if request.method == "POST":
        # Get stock data from API
        code = request.POST.get('code')
        search_result = {'code': code, 'price': '$10.00', 'change': '0.1%'}

    print(request.GET)
    if("code" in request.GET) :
        # Get stock data from API
        print("here")
        search_result = {'code': request.GET.get('code'), 'price': '$10.00', 'change': '0.1%'}
        return render(request, 'simulator/search.html', search_result)

    return render(request, 'simulator/search.html')
    