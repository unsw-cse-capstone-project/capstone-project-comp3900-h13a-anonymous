from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from . import views
from .views import (
    WatchListView
)
from .views import ChartView, get_data


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
    path('my_watchlist/display=<str:display>/', views.my_watchlist_view, name='watchlist'),


    # path('my_watchlist/', WatchListView.as_view(), name='add'),
    path('remove_watchlist/<str:code>/', views.remove_watchlist, name='remove'),

    # Display Chart
    path('charts/<str:code>/', views.ChartView.as_view(), name = 'charts'),

    # Fetch prediction data
    path('api/data/<str:code>/', views.get_data, name ='api-data'),

    # Buy / sell
    path('buy/<str:code>/', views.buy_stock, name='buy'),
    path('sell/<str:code>/', views.sell_stock, name='sell'),

    # Generate graph
    path('my_watchlist/<str:code>/<str:date>', views.gen_graph, name='gen_graph'),

    # Show graph
    path('my_watchlist/graph.html/', views.show_graph, name='plot')
]