from django.shortcuts import render, get_object_or_404, redirect
from .models import Stock 
from .forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required



# Create your views here.
@login_required
def stock_list(request):
    stocks = Stock.objects.all()
    frontend_stocks = {'stocks': stocks}
    return render(request, 'simulator/stock_list.html', frontend_stocks)

@login_required
def stock_detail(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    frontend_stock = {'stock': stock}
    return render(request, 'simulator/stock_detail.html', frontend_stock)

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return redirect('/')
    else:
        form = UserForm()
    return render(request, 'simulator/signup.html', {'form': form})