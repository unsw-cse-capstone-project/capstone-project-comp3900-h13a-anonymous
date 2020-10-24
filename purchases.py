from simulator.models import *
from django.db.models import F 

def get_total_owned_units(user_id, code):
    purchases = Purchase.objects.filter(user_id=user_id, stock=code)
    total_units = 0
    for purchase in purchases:
        total_units = total_units + purchase.orignialUnitBought - purchase.unitSold
    return total_units

def get_unsold_purhases(user_id, code):
    purchases = Purchase.objects.filter(user_id=user_id, stock=code, unitSold__lt=F('orignialUnitBought')).order_by('dateBought')
    return purchases