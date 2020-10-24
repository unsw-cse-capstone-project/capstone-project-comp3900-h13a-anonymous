from django.contrib import admin
from .models import Stock, Profile, WatchListItem, Purchase, Transaction


# Register your models here.
admin.site.register(Stock)
admin.site.register(Profile)
admin.site.register(WatchListItem)
admin.site.register(Purchase)
admin.site.register(Transaction)
