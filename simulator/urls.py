from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from . import views
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
    path('my_portfolio/display=<str:display>/', views.portfolio_view, name='graph'),

    # path('my_watchlist/', WatchListView.as_view(), name='add'),
    path('remove_watchlist/<str:code>/', views.remove_watchlist, name='remove'),
    # Set Watch price 
    path('set_watchprice/<str:code>/', views.set_watchprice, name='set_watchprice'),
    path('remove_watchprice/<str:id>/', views.remove_watchprice, name='remove_watchprice'),
    
    # Alerts
    path('alerts/', views.alerts, name='alerts'),

    # Display Chart
    path('charts/<str:code>/', views.ChartView.as_view(), name = 'charts'),

    # Fetch prediction data
    path('api/data/<str:code>/', views.get_data, name ='api-data'),

    # Buy / sell
    path('buy/<str:code>/', views.buy_stock, name='buy'),
    path('sell/<str:code>/', views.sell_stock, name='sell'),

    # Transactions
    path('transactions/', views.transactions_view, name='transactions'),

    # Purchases
    path('purchases/', views.purchases_view, name='purchases'),
    path('purchasesIncludeSold/', views.purchasesIncludeSold_view, name='purchasesIncludeSold'),
    path('purchases/<str:defaultCode>/', views.purchases_view, name='purchasesCode'),
    path('purchasesIncludeSold/<str:defaultCode>/', views.purchasesIncludeSold_view, name='purchasesIncludeSoldCode'),

    # Portfolio
    path('portfolio/', views.portfolio_view, name='portfolio'),

    # Leaderboard
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),

    # Generate graph
    path('my_watchlist/<str:code>/<str:date>', views.gen_graph, name='gen_graph'),

    # Show graph
    path('my_watchlist/graph.html/', views.show_graph, name='plot'),

    # Generate graph
    path('my_portfolio/<str:code>/<str:date>', views.gen_graph, name='portfolio_graph'),

    # Show graph
    path('my_portfolio/graph.html/', views.show_graph, name='portfolio_plot')
]