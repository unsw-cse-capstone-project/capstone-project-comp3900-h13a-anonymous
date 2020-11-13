from django.apps import AppConfig
from django.db.models.signals import pre_save


        
class SimulatorConfig(AppConfig):
    name = 'simulator'
    def ready(self):
        try:
            from modules.watchprice import Watchprice
            Watchprice = Watchprice()
            Watchprice.start_up()
        except:
            pass
