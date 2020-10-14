from django.urls import path
from . import views

urlpatterns = [
    # 127.0.0.1:8000
    path('', views.stock_list, name='stock_list'),

    # 127.0.0.1:8000/stock/1
    path('stock/<int:pk>/', views.stock_detail, name='stock_detail'),
]