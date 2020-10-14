from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # 127.0.0.1:8000
    path('', views.stock_list, name='stock_list'),

    # 127.0.0.1:8000/stock/1
    path('stock/<int:pk>/', views.stock_detail, name='stock_detail'),

    # 127.0.0.1:8000/accounts/login
    path('accounts/login/', auth_views.LoginView.as_view(), name='login')
]