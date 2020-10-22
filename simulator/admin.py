from django.contrib import admin
from .models import Stock, User, WatchList, Purchase


# Register your models here.
admin.site.register(Stock)
admin.site.register(User)
admin.site.register(WatchList)
admin.site.register(Purchase)