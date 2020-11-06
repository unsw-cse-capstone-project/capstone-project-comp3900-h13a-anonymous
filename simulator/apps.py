from django.apps import AppConfig
from django.db.models.signals import pre_save


        
class SimulatorConfig(AppConfig):
    name = 'simulator'
    def ready(self):
        from watchprice_2 import Watchprice
        Watchprice = Watchprice()
        Watchprice.start_up()
