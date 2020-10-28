from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from . import views
from .views import (
    WatchListView
)

from .views import HomeView, get_data, ChartData


urlpatterns = [
    # 127.0.0.1:8000/
    path('', views.stock_list, name='stock_list'),

    # 127.0.0.1:8000/stock/1
    path('stock/<str:code>/', views.stock_detail, name='stock_detail'),

    # 127.0.0.1:8000/signup
    path('signup/', views.signup, name='signup'),

    # Search
    path('search/', views.search_view, name='search'),
    path('search/<str:code>/', views.search_view, name='search_code'),

    # Watchlist
    path('add_watchlist/<str:code>/', views.add_to_watchlist, name='add'),
    path('my_watchlist/', views.my_watchlist_view, name='watchlist'),
    # path('my_watchlist/', WatchListView.as_view(), name='add'),
    path('remove_watchlist/<str:code>/', views.remove_watchlist, name='remove'),

    path('api/data/', views.get_data, name ='api-data'),
    path('api/chart/data', views.ChartData.as_view()),

    # Buy / sell
    path('buy/<str:code>/', views.buy_stock, name='buy'),
    path('sell/<str:code>/', views.sell_stock, name='sell'),
]