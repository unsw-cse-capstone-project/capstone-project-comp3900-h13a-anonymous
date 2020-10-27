from simulator.models import *
from django.db.models import F 

def get_user_transactions(user_id):
    transactions = Transaction.objects.filter(user_id=user_id).order_by(F('date').desc())
    return transactions